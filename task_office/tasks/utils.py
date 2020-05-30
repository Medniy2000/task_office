from task_office.core.models.db_models import Task
from task_office.database import Model
from task_office.extensions import db


def reset_tasks_ordering(
    instance: Model, column_uuid: str, new_value: int, old_value: int = None
) -> bool:
    if new_value != old_value:
        if old_value is None:
            # if column already created
            qs = Task.query.filter(
                Task.id != instance.id,
                Task.column_uuid == column_uuid,
                Task.position >= new_value,
            )
            qs.update(dict(position=Task.position + 1))
        elif new_value > old_value:
            qs = Task.query.filter(
                Task.id != instance.id,
                Task.column_uuid == column_uuid,
                Task.position > old_value,
                Task.position <= new_value,
            )
            qs.update(dict(position=Task.position - 1))
        else:
            Task.query.filter(
                Task.id != instance.id,
                Task.column_uuid == column_uuid,
                Task.position < old_value,
                Task.position >= new_value,
            ).update(dict(position=Task.position + 1))

        db.session.commit()

        return True

    return False
