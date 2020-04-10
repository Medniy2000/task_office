from task_office.settings import app_config

BOARDS_PREFIX = app_config.API_V1_PREFIX + "boards"
BOARD_RETRIEVE_URL = BOARDS_PREFIX + "/<board_uuid>"
