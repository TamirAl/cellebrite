"""
This module implements the decompression of a LG/Qualcomm compression algorithm.
This compression protocol was discovered as part of the LG Qualcomm dload mode
For information about how to decompress please start from reading the
"""
import traceback
DEBUG = False


class DecompressLGQC(object):
    def handle_uncompressed(self, next_byte):

    def read_all_copy_bytes(self):
    def copy_compressed(self, offset, copy_bytes):
    def copy_uncompressed(self, length):
    def handle_compressed_with_same_offset(self, next_byte, offset):

    def handle_compressed(self, next_byte):


    def decompress_data(self, compressed_data):
            try:

    def has_more_data(self) :




    """
+--------------------------------------------------------------------------+
--------------------------------------------------------------------------+
UU:
CC:
0x16 (MARKER_0x8000):
0x06 (MARKER_END_OF_COMPRESSED_DATA):

Uncompressed block:
                            +----------------------------+
--------------------------------------+`         
--------------------------------------+    `    
                                                                                
General form of a compressed block:
-----------------------------------------------------------+                                                                               
-----------------------------------------------------------+

header (spread over 1-3 bytes):
  Types of headers:
  Legend:
  header A (offset 11 bit)
  header B (offset 14 bit)
  header C (offset 16 bit)
  header D (same offset as in the last compressed block, no uncompressed data)
  header E (same offset as in the last compressed block, uncompressed data present)

uncompressed bytes (optional):
copy bytes
                       copy bytes chunk
    """