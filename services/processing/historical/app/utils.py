from typing import Any


def get_non_empty_keys(**params: Any) -> dict[str, Any]:
    """
    Returns a dict of keys with values that are not None.
    """

    non_empty_dict = {}

    for key, value in params.items():
        if value is not None:
            non_empty_dict[key] = value

    return non_empty_dict
