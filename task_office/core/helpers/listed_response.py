from task_office.core.utils import lookup_filter


class ListedResponseHelper:
    RESPONSE_TEMPLATE = {"count": 0, "results": []}

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
        query = self._get_query_paginated(
            query, query_params.get("limit"), query_params.get("offset")
        )
        count = query.count()
        data = dict(self.RESPONSE_TEMPLATE)
        data["count"] = count
        data["results"] = schema.dump(query)
        return data


listed_response = ListedResponseHelper()
