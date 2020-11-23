from moodleapi.utils import make_params, to_dict


def simple_contents_information(
    r,
    url: str,
    token: str,
    wsfunction: str,
    **kwargs,
) -> tuple:
    params = make_params(token, wsfunction, "json")
    params.update(to_dict(kwargs))

    events = r.get(url, params=params, stream=True).json()

    for modules in events:
        if modules["modules"]:
            return (
                modules["modules"][0]["completiondata"]["state"],
                modules["modules"][0]["completiondata"]["timecompleted"],
            )
