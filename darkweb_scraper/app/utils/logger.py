import logging
import os
from app.config import SERVICE_NAME, ENVIRONMENT

def get_logger(name: str = SERVICE_NAME) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s [env=%(env)s]",
        datefmt="%Y-%m-%dT%H:%M:%SZ"
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    # inject environment field
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.env = ENVIRONMENT
        return record
    logging.setLogRecordFactory(record_factory)

    # IMPORTANT: Never log scraped PII/content. Only operational metadata.
    logger.propagate = False
    return logger

log = get_logger()

