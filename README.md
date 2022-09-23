# Constant File System

The constant file system is a micro-filesystem that flattens a collection of files and metadata into a single flat file where any file in the collection can be fetched in constant time. A CFS file can be used with a blobstore that supports range queries. You can collect thousands of files into a single CFS, upload the CFS in a single action, and the files in the CFS can be accessed with two lookups. CFS is inspired by the Constant Database (CDB).

You can think of a CFS as a flat, read-only filesystem without folders, file permissions or timestamps.

In keeping with the blobstore concept, the files exists as blobs of bytes at a named location.

The format is as follows:

1. magic word
   * 3 bytes
   * `0x434653` -> "CFS"
2. sha1
   * 20 bytes
   * SHA 1 hash of the remaining bytes in the file
3. timestamp (4 bytes)
   * a 32 bit integer UTC unix timestamp
   * time the CFS was created
4. manifest_length (4 bytes)
   * 32 bit number
   * length of the manifest in bytes offset for the start of the file content
   * `manifsest length = content_start - 3`
5. Manifest
   * Valriable length JSON document
   * Details below
6. Blob Content
   * Variable length block of bytes.
   * The content of the files as a single block of bytes

   * 6. : the manifest as a json document
   * file blob manifest entry



file blob manifest entry
```
{ 
    metadata={},
    mimetype=''
    sha1=
    name=''
    size=1234
    offset=100
}
```


Example CFS file contents:
`CFS[sha256 - 20 bytes][4-byte timestamp][length of manifest][manifest json string][file1][file2][file3]...`

