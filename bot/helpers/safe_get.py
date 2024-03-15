def safe_get(list, index, default_value):
    if list is None:
        return default_value

    return list[index] if index < len(list) else default_value
