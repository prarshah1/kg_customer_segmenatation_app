import json
from datetime import date, datetime


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        # Handle Neo4j's Date type
        if hasattr(obj, 'year') and hasattr(obj, 'month') and hasattr(obj, 'day'):
            return f"{obj.year}-{obj.month:02d}-{obj.day:02d}"
        return str(obj)
