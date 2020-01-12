from task_office.settings import CONFIG

BOARDS_PREFIX = CONFIG.API_V1_PREFIX + "/boards"
BOARD_RETRIEVE_URL = BOARDS_PREFIX + "/<board_uuid>"
