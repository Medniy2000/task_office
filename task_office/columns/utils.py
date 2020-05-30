"""Columns utils."""
from task_office.core.models.db_models import BoardColumn
from task_office.database import Model
from task_office.extensions.db import db


def reset_columns_ordering(
    instance: Model, board_uuid: str, new_value: int, old_value: int = None
) -> bool:
    if new_value != old_value:
        if old_value is None:
            # if column already created
            qs = BoardColumn.query.filter(
                BoardColumn.id != instance.id,
                BoardColumn.board_uuid == board_uuid,
                BoardColumn.position >= new_value,
            )
            qs.update(dict(position=BoardColumn.position + 1))
        elif new_value > old_value:
            qs = BoardColumn.query.filter(
                BoardColumn.id != instance.id,
                BoardColumn.board_uuid == board_uuid,
                BoardColumn.position > old_value,
                BoardColumn.position <= new_value,
            )
            qs.update(dict(position=BoardColumn.position - 1))
        else:
            BoardColumn.query.filter(
                BoardColumn.id != instance.id,
                BoardColumn.board_uuid == board_uuid,
                BoardColumn.position < old_value,
                BoardColumn.position >= new_value,
            ).update(dict(position=BoardColumn.position + 1))

        db.session.commit()

        return True

    return False
