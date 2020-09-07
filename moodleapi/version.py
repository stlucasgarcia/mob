"""
Version module contain functions to return stable and lastest version
"""


from datetime import datetime


def get_version(version=None):
    """Return only stable version for production. The lastest version can be
    returned with get_last_version."""

    if not version:
        return 'Invalid call from version.'

    else:
        sufix = 'FINAL' if version[2] == 'f' else 'ALPHA'
        return f'Core version {version[0]}.{version[1]} {sufix} - last time checked: {datetime.utcnow()}'
