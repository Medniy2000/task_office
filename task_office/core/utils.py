from uuid import UUID


def is_uuid(uuid):
    try:
        UUID(uuid).version
        return True
    except ValueError:
        return False
