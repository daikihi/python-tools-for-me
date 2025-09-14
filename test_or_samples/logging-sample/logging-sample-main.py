from logging import getLogger, INFO
import logging 

logger = getLogger(__name__)
logger.setLevel(INFO)

# ログのフォーマットを設定
logging.basicConfig(  
    level=INFO,  # ログレベルを設定
    format='%(asctime)s - %(levelname)s - %(message)s',  # 時間とログレベルを含むフォーマット
    datefmt='%Y-%m-%d %H:%M:%S'  # 日付と時間のフォーマット
)

logger.debug("This LOG is DEBUG level")
logger.info("This LOG is INFO level")
logger.warning("This LOG is WARNING level")
logger.error("This LOG is ERROR level")
logger.critical("This LOG is CRITICAL level")