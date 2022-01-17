# Constant File System

The constant file system is a micro-filesystem for storing a collection of files and metadata in a single flat file where any file in the collection can be fetched in constant time. Inspired by the Constant Database (CDB).

It is designed such that it can be stored on a blobstore that supports http get range queries. 
You can think of it as a flat, read-only filesystem without folders, file permissions
or timestamps.

The format is as follows:
magic word (3 bytes):  0x434653 -> "CFS"
sha1 (20 bytes): a 20 byte SHA 1 hash of the remaining bytres in the file
timestamp (4 bytes): a 32 bit integer UTC unix timestamp representing when the CFS was created
manifest_length (4 bytes): 32 bit number representing length of the manifest in bytes offset for the start of the file content
    manifsest length = content_start - 3
manifest: the manifest as a json document
the file contents
thus the first 32 bytes of a maptiles file should be :
0x0x434653  ######################################## ######## ######## 7B ->  "CFS####{"



timestamp:
arrow.Arrow.fromtimestamp(int(arrow.utcnow().timestamp()))

to unix timestamp int: int(arrow.utcnow().timestamp())
from unix timestamp: arrow.Arrow.fromtimestamp(int_val)

header:
CFS[4-byte timestamp][sha256 - 20 bytes][length of manifest][manifest string][file1][file2][file3]...

sha1 encoding:
hashlib.sha1().digest()    -> b'\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t'
hashlib.sha1().hexdigest() -> 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
