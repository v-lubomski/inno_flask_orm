"""Additional functions."""
import jsonschema


def json_validate(json: dict, schema: dict) -> bool:
    """JSON validation."""
    try:
        jsonschema.validate(json, schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False
