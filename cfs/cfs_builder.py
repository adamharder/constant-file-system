# from util_content_hash import content_hash
#from python.common.util_mimetype import get_mimetype, mimetypes,  validate_mimetype
#from schemas.schema_aligned_cfs import metadata
#from schemas.schema_floorplan_master_cfs import metadata_schema

# from . import cfs_schema
import copy
import hashlib
import io
import json
import struct
# import arrow
from typing import List
import datetime
import mimetypes

from cfs.cfs_base import CFS_Base

#x=mimetypes.



    


class CFS_Blob(object):
    blob:bytes
    def __init__(self, *, name:str, content:bytes, mimetype:str, metadata:dict=None):
        assert isinstance(name, str)
        assert isinstance(content, bytes)
        if mimetype is not None:
            assert isinstance(mimetype, str)
        if metadata is not None:
            assert isinstance(metadata, dict)
        self._content=copy.copy(content)
        self._name=name
        self._sha1=hashlib.sha1()
        self._sha1.update(content)
        self._sha1=self._sha1.hexdigest()
        if mimetype is not None:
            self._mimetype=mimetype
        else:
            self._mimetype= "application/octet-stream"

        self._metadata={}

        if metadata is not None:
            self._metadata=metadata

    @property
    def size(self):
        return len(self._content)

    @property
    def name(self):
        return self._name

    @property
    def sha1(self):
        return self._sha1

    @property
    def mimetype(self):
        return self._mimetype

    @property
    def metadata(self):
        return self._metadata

    @property
    def content(self):
        return self._content

    @property
    def blob_manifest_entry(self):
        return dict(
            metadata=self.metadata,
            mimetype=self.mimetype,
            sha1=self.sha1,
            name=self.name,
            size=self.size,
        )
        

class CFS_Builder(object):
    def __init__(self, metadata={}):
        self._blobs=dict()
        self._content_bytes=b''
        self._cfs_metadata={}
        if metadata is not None:
            assert isinstance(metadata, dict)
            self._cfs_metadata=metadata
        

    @staticmethod
    def wrap(cfs:CFS_Base):
        assert False, "NOT IMPLEMENTED"
    @property
    def cfs_metadata(self)->dict:
        return self._cfs_metadata

    @property
    def blob_paths(self)->List[str]:
        return list(self._blobs.keys())

    def get_bytes(self, name)->bytes:
        return copy.copy(self._blobs[name].content) #raises an exception

    
    def build(self)->bytes:
        
        timestamp= datetime.datetime.now() #.isoformat() #  arrow.utcnow()
        timestamp_str=timestamp.isoformat()
        self._cfs_metadata["timestamp"]=timestamp_str
        content_block=io.BytesIO()
        blob_offsets={}
        file_list={}
        manifest={}

        for name in self._blobs:
            blob=self._blobs[name]

            if blob._sha1 not in blob_offsets:
                offset=content_block.tell()
                content_block.write(blob.content)
                blob_offsets[blob._sha1]=dict(offset=offset, size=blob.size)

            file_list[name]=dict(
                sha1=blob._sha1, 
                offset=blob_offsets[blob._sha1]['offset'], 
                metadata=blob.metadata, 
                mimetype=blob.mimetype, 
                size=blob_offsets[blob._sha1]['size'])

        content_sha1=hashlib.sha1()
        content_sha1.update(content_block.getvalue())
        content_sha1=content_sha1.hexdigest()
        manifest=dict()
        manifest=dict(timestamp=timestamp_str,metadata=self.cfs_metadata, sha1=content_sha1, blobs=file_list, size=len(content_block.getvalue()))
        # cfs_schema.validate(manifest)
        manifest_bytes=json.dumps(manifest).encode()
        manifest_length=len(manifest_bytes)

        cfs_full_content = io.BytesIO()
        cfs_full_content.write(struct.pack("I", int(timestamp.timestamp())))
        cfs_full_content.write(struct.pack("I", manifest_length))
        cfs_full_content.write(manifest_bytes)
        cfs_full_content.write(content_block.getvalue())

        outer_sha1=hashlib.sha1()
        outer_sha1.update(cfs_full_content.getvalue())

        output_str = io.BytesIO()
        output_str.write(b"CFS")
        output_str.write(outer_sha1.digest())
        output_str.write(cfs_full_content.getvalue())
        return output_str.getvalue()

    def add(self, *, blob:CFS_Blob):
        self._content_bytes=b''  # blow away any file structure if it exists
        self._blobs[blob.name]=blob

    def add_blob(self, name:str, val:bytes, metadata:dict={}, mimetype:str=None):
        assert isinstance(val, bytes)
        assert isinstance(name, str)
        assert isinstance(metadata, dict)
        if mimetype is None:
            mimetype="/octet-stream"

        #validate_mimetype(mimetype)  # raises a ValueError Exception
        self._content_bytes=b''  # blow away any file structure if it exists
        self._blobs[name]=CFS_Blob(name=name, content=val, mimetype=mimetype, metadata=metadata)
        return self

    def merge(self, rhs:'CFS_Builder')->'CFS_Builder':
        # merging consists of merging over all of the blobs in the rhs file system.
        # exisiting blobs with the same name will be overwritten
        # file system metadata from the rhs file will not be copied over
        for blob_path in rhs._blobs:
            rhs_blob=rhs._blobs[blob_path]
            assert isinstance(rhs_blob, CFS_Blob)
            self._blobs[rhs_blob]=rhs_blob

    @property
    def blob_manifest(self):
        r={}
        for blob in self._blobs.values():
            r[blob.name]=blob.blob_manifest_entry
        return r

    @property
    def manifest(self):
        return dict(metadata=self._cfs_metadata, blob_manifest=self.blob_manifest)