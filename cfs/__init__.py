import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

from cfs.cfs_base import CFS_Base
from cfs.cfs_builder import CFS_Builder
from cfs.cfs_bytestream import CFS_Bytestream
from cfs.cfs_file import CFS_File
from cfs.exceptions import CFS_Error

try:
    __version__ = metadata.version("cfs")
except metadata.PackageNotFoundError:
    __version__ = "99.99.99"



def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


VERSION = tuple(map(int_or_str, __version__.split(".")))


__all__ = [
    "CFS_Base",
    "CFS_Builder",
    "CFS_Bytestream",
    "CFS_Error",
    "CFS_File",
]