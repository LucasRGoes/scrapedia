"""The VERSION file is the sole source of the project's current version. This
script was created exclusively to fetch its content for __init__.py usage.
"""

from os.path import dirname, join


def version() -> str:
    """Get package version."""
    with open(join(dirname(__file__), 'VERSION')) as f:
        return f.read().strip()


__version__ = version()
