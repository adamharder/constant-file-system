"""
    Constant File System base class. All readable CFS implementations should inherit from this.
"""

from datetime import datetime
from abc import ABC, abstractmethod

class CFS_Base(ABC):
    def __init__(self):
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    @abstractmethod
    def sha1(self)->str:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    @abstractmethod
    def manifest_size(self)->int:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    @abstractmethod
    def timestamp(self)->datetime:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    @abstractmethod
    def content_offset(self)->int:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    @abstractmethod
    def metadata(self)->dict:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    @abstractmethod
    def file_list(self)->list:
        return self.blob_paths

    # throws an exception if blob not found
    def get_blob_info(self, blob_name)->dict:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    #@abstractmethod
    def blob_paths(self)->list:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    def manifest(self)->dict:
        return dict(metadata=self.metadata, blob_manifest=self.blob_manifest())

    @property
    def blob_manifest(self)->dict:
        assert False, "NOT IMPLEMENTED"
        pass

    @property
    def blobs(self)->dict:
        assert False, "NOT IMPLEMENTED"
        pass

    def get_mimetype(self, blob_path:str)->str:
        return self.blobs[blob_path]['mimetype']

    def get_blob_metadata(self, blob_path:str)->dict:
        return self.blobs[blob_path]['metadata']

    def get_blob(self, blob_path:str, confirm:bool=True)->bytes:
        assert False, "NOT IMPLEMENTED"
        pass

