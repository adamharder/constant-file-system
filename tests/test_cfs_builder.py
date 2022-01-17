import os
from cfs import cfs_builder
from cfs import cfs_
# from python.common.util_mimetype import mimetypes
# from python.cfs import cfs_bytestream
# from python.cfs import cfs_write
from cfs import cfs_bytestream
import hashlib
import random
import string
import struct
import os


def _random_blob_path():
    chars=string.ascii_letters + string.digits + "/"
    size=random.randint(10,100)
    return ''.join(random.choice(chars) for _ in range(size))

def _rand_bytes():
    return os.urandom(random.randint(10,10000))

def test_simple():
    # write a single file and read it back out
    wf = cfs_builder.CFS_Builder(metadata=None)
    
    wf.add_blob("xxx", b"bbb") 
    assert wf.get_bytes("xxx")==b'bbb'
    wf_bytes = wf.as_bytes
    sha1=wf_bytes[3:23]
    all_content=wf_bytes[23:]

    
    sha1_rtt=hashlib.sha1()
    sha1_rtt.update(all_content)

    assert sha1 == sha1_rtt.digest()

    bs = cfs_bytestream.ConstantFileSystem(wf_bytes)
    assert bs.get_file("xxx", confirm=True) == b'bbb'


    # assert wf.get_bytes("xxx") # should raise an exception
    try:
        wf.get_mimetype("yyy")
        assert False
    except: 
        pass

    # assert wf.get_bytes("xxx") # should raise an exception
    try:
        wf.get_bytes("yyy")
        assert False
    except: 
        pass

def test_wrap():

    assert False

def test_complex():
    # genreate a CFS, containing a random number of files of random length containing random content
    # insert the same file twice with differnt names at random places.
    # write a single file and read it back out
    wf = cfs_write.WriteableConstantFileSystem(metadata=None)
    file_paths = []
    def _random_file_path():
        chars=string.ascii_uppercase + string.digits
        size=random.randint(10,100)
        return ''.join(random.choice(chars) for _ in range(size))
    def rand_bytes():
        return open("/dev/urandom","rb").read(random.randint(10,10000))
    duplicate_file_content = rand_bytes()
    for i in range(random.randint(10,100)):
        file_name=_random_file_path()
        file_content=rand_bytes()
        wf.add_blob(file_name, file_content)
    wf.add_blob("file_1", duplicate_file_content)
    for i in range(random.randint(10,100)):
        file_name=_random_file_path()
        file_content=rand_bytes()
        wf.add_blob(file_name, file_content)
    wf.add_blob("file_2", duplicate_file_content)
    for i in range(random.randint(10,100)):
        file_name=_random_file_path()
        file_content=rand_bytes()
        wf.add_blob(file_name, file_content)
    
    bs = cfs_bytestream.ConstantFileSystem(wf.as_bytes)
    assert bs.get_file("file_1", confirm=True) == duplicate_file_content
    assert bs.get_file("file_2", confirm=True) == duplicate_file_content
