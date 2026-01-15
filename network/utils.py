def to_camel(string: str) -> str:
    """
    Converts a snake_case string to camelCase.
    """
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])
