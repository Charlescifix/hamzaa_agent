import os
import openai
from app.core.config import OPENAI_API_KEY, KNOWLEDGE_BASE_PATH

# Import modules for embeddings, vector store, text splitting, and retrieval chain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

# Import chat modules to support a system prompt
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY


def load_knowledge_base() -> str:
    """
    Loads the knowledge base text from a file using a relative path.
    The relative path is defined in the environment variable KNOWLEDGE_BASE_PATH.
    """
    # Compute the project root by going up three directories
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    kb_file_path = os.path.join(base_dir, KNOWLEDGE_BASE_PATH)

    with open(kb_file_path, "r", encoding="utf-8") as f:
        return f.read()


def build_vector_store(text: str) -> FAISS:
    """
    Splits the knowledge base text into chunks and builds a FAISS vector store.
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,    # Adjust chunk size if needed
        chunk_overlap=100  # Adjust overlap if needed
    )
    texts = text_splitter.split_text(text)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store


def build_retrieval_chain(vector_store: FAISS) -> RetrievalQA:
    """
    Creates a RetrievalQA chain that uses the vector store to retrieve context and
    generate an answer using the Chat-based OpenAI LLM with a custom system prompt.
    """
    # Updated system prompt with fallback instructions
    system_message = (
        "You are a helpful assistant for Hamzaa, an auto repair shop management software. "
        "Your role is to assist users with car troubleshooting, automobile-related questions, "
        "and Hamzaa's features. Use the provided context from the knowledge base to answer questions. "
        "If the retrieved context is insufficient or missing details, supplement your answer with your own internal knowledge. "
        "You must only respond to questions about:\n"
        "- Car troubleshooting (e.g., engine problems, brake issues, battery problems).\n"
        "- Automobile maintenance (e.g., oil changes, tire rotations).\n"
        "- Hamzaa's features (e.g., inventory management, scheduling appointments, invoice generation).\n"
        "If a question is outside these topics, politely decline to answer and guide the user to ask automobile-related questions."
    )

    # Build a chat prompt template that includes the system message and placeholders for retrieved context and the user query.
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_message),
        HumanMessagePromptTemplate.from_template("{context}\n\nQuestion: {question}")
    ])

    # Use ChatOpenAI (chat-optimized LLM) so that the system prompt is applied.
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

    # Create the RetrievalQA chain with the custom prompt template.
    # Pass the prompt template using chain_type_kwargs instead of a direct prompt parameter.
    retrieval_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" simply injects the retrieved context into the prompt.
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt_template}
    )
    return retrieval_chain



# --- Initialization of the knowledge base and retrieval chain ---
knowledge_base_text = load_knowledge_base()
vector_store = build_vector_store(knowledge_base_text)
retrieval_chain = build_retrieval_chain(vector_store)


async def generate_response(query: str) -> str:
    """
    Given a query, this function uses the retrieval chain to fetch relevant context
    from the knowledge base and generate a response using the LLM.
    """
    result = retrieval_chain.run(query)
    return result
