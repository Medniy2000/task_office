import pytest

from task_office.core.models.db_models import Permission

PERMISSIONS_VALID_DATA = [{"role": role} for role in Permission.Role.get_values()]

PERMISSIONS_INVALID_DATA = []


@pytest.fixture(params=PERMISSIONS_VALID_DATA)
def role_valid_data(request):
    return request.param


@pytest.fixture(params=PERMISSIONS_INVALID_DATA)
def role_invalid_data(request):
    return request.param
