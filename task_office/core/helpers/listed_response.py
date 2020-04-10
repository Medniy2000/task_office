from flask import request
from flask_babel import lazy_gettext as _

from task_office.core.utils import lookup_filter
from task_office.exceptions import InvalidUsage
from task_office.settings import app_config


class ListedResponseHelper:
    error_messages = {"max_offset_exceeded": _("Max value {} exceeded")}
    RESPONSE_TEMPLATE = {"count": None, "results": [], "next": None, "prev": None}
    RESPONSE_PAGINATED_QS_TEMPLATE = "?limit={}&offset={}"

    @staticmethod
    def _get_query_ordered(query, order_param):
        if order_param:
            query = query.order_by(order_param.fullname)
        return query

    @staticmethod
    def _get_query_filtered(query, filter_params):
        if filter_params:
            for k, v in filter_params.items():
                query = lookup_filter(query, v["key"], v["value"], v["lookup"])
        return query

    @staticmethod
    def _get_query_paginated(query, limit, offset):
        if offset > 0:
            query = query.offset(offset)
        query = query.limit(limit)
        return query

    def serialize(self, query, query_params, schema):
        query = self._get_query_filtered(query, query_params.get("searching", {}))
        query = self._get_query_ordered(query, query_params.get("ordering", ""))
        count = query.count()

        limit = query_params.get("limit", app_config.DEFAULT_LIMIT_VALUE)
        offset = query_params.get("offset", app_config.DEFAULT_OFFSET_VALUE)
        query = self._get_query_paginated(query, limit, offset)

        data = dict(self.RESPONSE_TEMPLATE)
        if offset >= count:
            raise InvalidUsage(
                messages=[self.error_messages["max_offset_exceeded"].format(count - 1)],
                status_code=422,
                key="offset",
            )
        if (offset + limit) <= count:
            data[
                "next"
            ] = f"{request.base_url}{self.RESPONSE_PAGINATED_QS_TEMPLATE.format(limit, offset + limit)}"
        if (offset - limit) > 0:
            data[
                "prev"
            ] = f"{request.base_url}{self.RESPONSE_PAGINATED_QS_TEMPLATE.format(limit, offset - limit)}"
        data["count"] = count
        data["results"] = schema.dump(query)
        return data


listed_response = ListedResponseHelper()
