import logging

def setup_logging():
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers, if any
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a stream handler for terminal output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)

    # Optionally, create a file handler to also log to a file
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Add handlers to the root logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
