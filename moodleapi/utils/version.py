"""
Version module contains functions to return stable and lastest version
"""


def get_version(version=None):
    """Return only stable version for production. The lastest version can be
    returned with get_last_version."""

    if not version:
        return "Invalid call from version."

    else:
        return f"{version[0]}.{version[1]}.{version[2]}"
