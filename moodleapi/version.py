"""
Version module contains functions to return stable and lastest version

"""


from datetime import datetime as dt


def get_version(version=None):
    """Return only stable version for production. The lastest version can be
    returned with get_last_version."""

    if not version:
        return 'Invalid call from version.'

    else:
        sufix = 'FINAL' if version[2] == 'f' else 'ALPHA'
        return f'MoodleAPI version {version[0]}.{version[1]}.{version[2]} {sufix} - last time checked: {dt.utcnow()}'
