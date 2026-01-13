import logging


def setup_logger():
    logger = logging.getLogger("weather_etl")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Console handler
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler.setFormatter(formatter)

        # File handler (pipeline.log)
        file_handler = logging.FileHandler("pipeline.log")
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger
