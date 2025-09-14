from logging import getLogger, INFO

logger = getLogger(__name__)
logger.setLevel(INFO)

logger.debug("This LOG is DEBUG level")
logger.info("This LOG is INFO level")
logger.warning("This LOG is WARNING level")
logger.error("This LOG is ERROR level")
logger.critical("This LOG is CRITICAL level")
