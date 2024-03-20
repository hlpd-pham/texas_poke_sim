def to_string(value):
    if isinstance(value, dict):
        return {str(key): to_string(val) for key, val in value.items()}
    elif isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set):
        return [to_string(item) for item in value]
    else:
        return str(value)
