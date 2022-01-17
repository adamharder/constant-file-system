

# from util_content_hash import content_hash
from datetime import datetime
import hashlib
import json
import struct
import binascii
from pathlib import Path
from cfs.cfs_base import CFS_Base

#from schemas.schema_aligned_cfs import metadata
# this is an interface for the constant file system. it can be backed by a file on the filesystem, or a blobstore that supports http get range queries.

class CFS_File(CFS_Base):
    def __init__(self, file_path:Path):
        assert file_path.is_file()
        self._file_path = file_path
        with open(file_path, "rb") as file_buffer:

            magic_word=file_buffer.read(3)
            print(magic_word)
            assert b'CFS' == magic_word

            self._sha1 = binascii.hexlify(file_buffer.read(20))
            self._timestamp = arrow.Arrow.fromtimestamp( struct.unpack("I", file_buffer.read(4))[0])
            self._manifest_size =  struct.unpack("I", file_buffer.read(4))[0]
            manifest_bytes=file_buffer.read(self.manifest_size)
            assert(manifest_bytes[0]==ord('{'))
            self._manifest=json.loads(manifest_bytes.decode())


    @property
    def sha1(self):
        return self._sha1

    @property
    def manifest_size(self)->int:
        return self._manifest_size

    @property
    def timestamp(self)->datetime:
        return self._timestamp

    @property
    def content_offset(self):
        return 31+self.manifest_size

    @property
    def metadata(self):
        return self._manifest["metadata"]

    @property
    def file_list(self):
        return list(self._manifest.keys())

    # throws an exception if blob not found
    def get_blob_info(self, blob_name):
        return self.blobs[blob_name]

    @property
    def blob_paths(self):
        return list(self.blobs.keys())

    @property
    def manifest(self):
        return dict(metadata=self.metadata, blob_manifest=self.blob_manifest())

    @property
    def blob_manifest(self):
        # r={}

        # for i in self.blobs:
        #     blob=self.blobs[i]
        #     print(blob.keys())
        #     r[i]=dict(name=i, sha1=blob['sha1'], mimetype=blob['mimetype'], size=blob['size'], offset=)
        # return r
        return self.blobs


    @property
    def blobs(self):
        return self._manifest['blobs']

    def get_mimetype(self, blob_path):
        return self.blobs[blob_path]['mimetype']

    def get_file_metadata(self, file_path):
        return self.blobs[file_path]['metadata']

    def get_file(self, file_path, confirm=True):
        file_obj=self.blobs[file_path]
        sha1=file_obj['sha1']
        file_start_offset=self.content_offset + file_obj['offset']
        length=file_obj['size']

        with open(self._file_path, "rb") as file_buffer:
            file_buffer.seek(file_start_offset)
            file_bytes = file_buffer.read(length)

        if confirm:
            c_sha1 = hashlib.sha1()
            c_sha1.update(file_bytes)
            assert c_sha1.hexdigest()==sha1
        return file_bytes


