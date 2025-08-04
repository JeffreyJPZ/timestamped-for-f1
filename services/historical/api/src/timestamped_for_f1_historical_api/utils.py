from typing import Any


def get_non_empty_entries(**params) -> dict[str, Any]:
    """
    Returns a dict with only values that are not None.
    """

    non_empty_dict = {}

    for key, value in params.items():
        if value is not None:
            non_empty_dict[key] = value

    return non_empty_dict

