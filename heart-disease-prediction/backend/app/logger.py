import logging

from app.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("heart-disease-backend")
