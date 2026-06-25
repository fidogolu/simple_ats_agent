# utils/logger.py
import logging
import os
import sys
import structlog


def get_logger() -> logging.Logger:
    logger = logging.getLogger("app")

    if logger.handlers:
        return logger

    logger.propagate = False

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(console_handler)

    # File Handler
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Silencer les loggers tiers bruyants
    for noisy_logger in [
        "llm_guard",
        "presidio_analyzer",
        "presidio_anonymizer",
        "transformers",
        "transformers.tokenization_utils_base",
    ]:
        logging.getLogger(noisy_logger).setLevel(logging.ERROR)

    # Silencer structlog utilisé par llm_guard
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.ERROR),
    )

    return logger


LOGGER = get_logger()
