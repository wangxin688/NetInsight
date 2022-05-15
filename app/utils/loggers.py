import logging.config

import yaml

from app.core.config import PROJECT_DIR

with open(f"{PROJECT_DIR}/logging.yml", "r", encoding="utf-8") as f:
    logging_config = yaml.save_load(f)
    logging_configuration = logging_config.copy()
    logging_configuration["handlers"]["file"]["filename"] = (
        str(PROJECT_DIR) + "/log/app.log"
    )

logging.config.dictConfig(logging_configuration)
app_logger = logging.getLogger("app")
