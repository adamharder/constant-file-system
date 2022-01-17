

# from util_content_hash import content_hash
import copy
from datetime import datetime
import hashlib
import io
import json
import struct
import binascii
from cfs.cfs_base import CFS_Base

# this is an interface for the constant file system. it can be backed by a file on the filesystem, or a blobstore that supports http get range queries.

class CFS_Bytestream(CFS_Base):
    def __init__(self, file_buffer:bytes):
        self._file_buffer = file_buffer
        magic_word=file_buffer[:3]
        assert b'CFS' == magic_word
        assert(file_buffer[3+20+4+4]==ord('{'))
        self._manifest=json.loads(file_buffer[31:31+self.manifest_size].decode())

    @property
    def sha1(self):
        return binascii.hexlify(self._file_buffer[3:23])

    @property
    def manifest_size(self)->int:
        return struct.unpack("I", self._file_buffer[27:31])[0]  #  cfs_full_content.write(struct.pack("I", int(timestamp.timestamp()))))

    @property
    def timestamp(self)->datetime:
        raw_ts = struct.unpack("I", self._file_buffer[23:27])[0]
        return datetime.fromtimestamp(raw_ts)
        # return arrow.Arrow.fromtimestamp( struct.unpack("I", self._file_buffer[23:27])[0] ) #  cfs_full_content.write(struct.pack("I", int(timestamp.timestamp()))))

    @property
    def content_offset(self):
        return 3+20+4+4+self.manifest_size

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
    def blobs(self):
        return self._manifest['blobs']

    def get_blob_mimetype(self, blob_path):
        return self.blobs[blob_path]['mimetype']

    def get_blob_metadata(self, blob_path):
        return self.blobs[blob_path]['metadata']

    def get_file(self, file_path, confirm=True):
        file_obj=self.blobs[file_path]
        sha1=file_obj['sha1']
        file_start_offset=self.content_offset + file_obj['offset']
        length=file_obj['size']
        file_bytes = self._file_buffer[file_start_offset:file_start_offset+length]
        if confirm:
            c_sha1 = hashlib.sha1()
            c_sha1.update(file_bytes)
            assert c_sha1.hexdigest()==sha1
        return file_bytes
