from pathlib import Path
#from python.common.util_res import project_root
res_dir=Path(__file__).parent/"res"
assert res_dir.is_dir()

# from python.cfs.cfs_file import ConstantFileSystem as ConstantFileSystemFile
# from python.cfs.cfs_bytestream import ConstantFileSystem as ConstantFileSystemBytestream
# run with 
#     pytest  -rP  test/unit/python/cfs
# import cfs_read
from cfs import CFS_Bytestream
from cfs import CFS_File

"""
def test_simple_read():
    cfs_file =  res_dir/"test_image_png.cfs"
    assert cfs_file.is_file()
    cc=ConstantFileSystemBytestream(cfs_file.read_bytes())

    print(cc.timestamp)
    print(cc.content_offset)
    assert isinstance(cc._manifest, dict)

def test_simple_read_file():
    cfs_file =  ConstantFileSystemFile(res_dir/"test_image_png.cfs")
    print(cfs_file.timestamp)
    print(cfs_file.content_offset)
    print(dir(cfs_file))
    print(cfs_file.blob_manifest)
    assert isinstance(cfs_file._manifest, dict)


"""