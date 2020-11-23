from typing import Any


def make_params(
    wstoken: str, wsfunction: str, moodlewsrestformat: str = "json"
) -> dict:
    return {
        "wstoken": wstoken,
        "wsfunction": wsfunction,
        "moodlewsrestformat": moodlewsrestformat,
    }


def to_dict(args: Any) -> Any:
    if not args:
        return args

    if isinstance(args, dict):
        data = {key: value for key, value in args.items()}

        return data

    if isinstance(args, list):
        pass

    if isinstance(args, tuple):
        pass

    return args
