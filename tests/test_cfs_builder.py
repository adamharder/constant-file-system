"""Test making a CFS object."""
from cfs import CFS_Builder, CFS_Bytestream
import hashlib
import os
import pytest 
from pathlib import Path
import random
import string
import json

res_dir=Path(__file__).parent/"res"
assert res_dir.is_dir()

def _random_blob_path():
    chars=string.ascii_letters + string.digits + "/"
    size=random.randint(10,100)
    return ''.join(random.choice(chars) for _ in range(size))

def _rand_bytes(length=None):
    if length is None:
        length = random.randint(10,10000)
    return os.urandom(length)

def _rand_words(length=None):
    if length is None:
        length = random.randint(10,10000)
    words=(res_dir/"word_list.txt").read_text().split("\n")
    rand_words=random.choices(words, k=length)
    return " ".join(rand_words)


def test_simple():
    # write a single file and read it back out
    wf = CFS_Builder(metadata=None)
    blob_path=_random_blob_path()
    blob_content=_rand_bytes()
    wf.add_blob(blob_path, blob_content) 
    assert wf.get_bytes(blob_path)==blob_content
    print(dir(wf))
    wf_bytes = wf.build()
    sha1=wf_bytes[3:23]
    all_content=wf_bytes[23:]

    sha1_rtt=hashlib.sha1()
    sha1_rtt.update(all_content)

    assert sha1 == sha1_rtt.digest()

    bs = CFS_Bytestream(wf_bytes)
    assert bs.get_file(blob_path, confirm=True) == blob_content

    nonexistant_blob_path=_random_blob_path()

    with pytest.raises(KeyError):
        wf.get_bytes(nonexistant_blob_path)
    with pytest.raises(KeyError):
        bs.get_blob_metadata(nonexistant_blob_path)
    with pytest.raises(KeyError):
        bs.get_blob_mimetype(nonexistant_blob_path)

# def test_wrap():
#     assert False

def test_overwriting():

    wf = CFS_Builder(metadata=None)
    blob_path=_random_blob_path()
    blob_content=_rand_bytes()
    wf.add_blob(blob_path, blob_content) 
    assert wf.get_bytes(blob_path)==blob_content
    updated_blob_content=_rand_bytes()
    wf.add_blob(blob_path, updated_blob_content) 
    assert wf.get_bytes(blob_path)==updated_blob_content
    assert wf.get_bytes(blob_path)!=blob_content

    out=wf.build()
    v2=CFS_Bytestream(file_buffer=out)
    assert v2.get_file(file_path=blob_path) == updated_blob_content
    assert v2.get_file(file_path=blob_path) != blob_content
    
def test_random_data():
    # genreate a random metadata object
    # genreate a CFS, containing a random number of files of random length containing random content
    cfs_metadata=dict()
    for i in range(random.randint(5,25)):
        rand_float=random.random()
        rand_words=_rand_words(random.randint(1,25))
        cfs_metadata[_random_blob_path()]= random.choice([rand_words, rand_float, int(rand_float*10000)])

    wf = CFS_Builder(metadata=cfs_metadata)

    filesample_blobs = {}
    for i in range(random.randint(10,100)):
        file_name=_random_blob_path()
        file_content=_rand_bytes()
        filesample_blobs[file_name]=file_content
        wf.add_blob(file_name, file_content)
    cfs_bytes=wf.build()
    print(len(cfs_bytes))
    """
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
def test_edge_cases():
    # genreate a CFS, containing a random number of files of random length containing random content
    # insert the same file twice with differnt names at random places.
    # write a single file and read it back out
    cfs_metadata=dict()
    for i in range(random.randint(5,25)):
        rand_float=random.random()
        rand_words=_rand_words(random.randint(1,25))
        cfs_metadata[_random_blob_path()]= random.choice([rand_words, rand_float, int(rand_float*10000)])
    print(json.dumps(cfs_metadata, indent=2))
    wf = CFS_Builder(metadata=dict())
    filesample_blobs = {}

    duplicate_file_content = rand_bytes()
    for i in range(random.randint(10,100)):
        file_name=_random_file_path()
        rand_float=random.random()
        rand_words=_rand_words(random.randint(1,25))
        file_content=random.choice(rand_words, rand_float)
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
"""