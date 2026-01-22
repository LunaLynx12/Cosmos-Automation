import json
from datetime import datetime

def to_json(obj) -> str:
    def default(o):
        if isinstance(o, datetime):
            return o.isoformat()
        return str(o)

    return json.dumps(obj, default=default)


def pretty(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True)