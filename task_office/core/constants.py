LOOKUP_MAP = {
    "gt": lambda q, k, v: q.filter(k > v),
    "gte": lambda q, k, v: q.filter(k >= v),
    "lt": lambda q, k, v: q.filter(k < v),
    "lte": lambda q, k, v: q.filter(k <= v),
    "e": lambda q, k, v: q.filter(k == v),
    "ne": lambda q, k, v: q.filter(k != v),
}
