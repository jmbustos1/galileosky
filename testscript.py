"""
This file have the utils for check and parser data frame of ruptela
"""
import logging
import struct
from collections import namedtuple
from typing import Dict, List
#from .data_description_dictionary import data_description

#import crcmod

#from .data_description_dictionary import data_description

HEADER_DATA_FORMAT = ">b"  # Format: ID, packet_length | packet_length, imei, command_id
PACKET_LENGTH_DATA_FORMAT = "H"  # Format: packet length | packet legth
CRC_DATA_FORMAT = "H"  # Format: CRC
HEADER_FORMAT_IN_BYTES = ">11s"  # Format header in bytes
FORMAT_TO_CHECK_CRC = ">QB"  # Format to pack data and check crc
# Format for the "record header" for extended protocol
RECORD_HEADER_FORMAT = ">L3Bll2HBHBH"
LEN_HEADER = 3

head_byte = b'\x01'



#data = b'\x01\x17\x80\x01\x9b\x02 \x03354762115484021\x042\x00\x85\x9e'

data = b'\x01a\x00\x03354762115484021\x042\x00\x10\x9d\x10 \xa4\xb0~c0 \x05\x18\x02\xfe\xd5\xd3\xca\xfb3\x00\x00\x00\x004\x00\x005\xff@\x00*A\xed]B\xed\x0eC)G\x00\x00\x00\x00\xc4\x00\xd4\x19\x00\x00\x00\xdb\x00\x00\x00\x00\xfe\x13\x00\x81\x00\xafd\x82\x00!N\x83\x00\xda\x02\x84\x00\x02\x00\x85\x00\xaf\xe8\xd9'
print(len(data))
head_byte = b'\x01'
header = data
print(header)
print(bytes(header[0]))

print(header[0])
print(int.from_bytes(head_byte, "big"))
result = False


header_data_format_size = struct.calcsize(HEADER_DATA_FORMAT)
packet_length_data_format_size = struct.calcsize(PACKET_LENGTH_DATA_FORMAT)
# Calculate size of crc
crc_size = struct.calcsize(CRC_DATA_FORMAT)
print("here1")

header_data_format_payload_crc = (
    f"{HEADER_DATA_FORMAT}"
    f"{PACKET_LENGTH_DATA_FORMAT}"
    f"{len(data)-header_data_format_size-packet_length_data_format_size-crc_size}s"
    f"{CRC_DATA_FORMAT}"
)


print(header_data_format_payload_crc
    )
print("here2")
try:
    (command_id2,packet_length, payload ,crc) = struct.unpack(
        header_data_format_payload_crc, data
    )
except Exception as e:
    print(e)
print("here3")

print("pack", packet_length )
packet_length = struct.pack(
        '<H', packet_length
    )
print("pack2", packet_length )

print("pack3", int.from_bytes(packet_length, "big") )
command_id = header[0]
result = dict(
    command_id=command_id,
    pack= data[1:3],
    pack_correct= data[2] + data[1],
    header_crc = data[-2:],
    command_id2=command_id2,
    crc = crc,
    packet_length=packet_length,
    payload =payload
)
print("here3")
print (result)
print(result["pack"])
print(int.from_bytes(result["pack"], "big"))
if header[0] == int.from_bytes(head_byte, "big"):
    print("hello World")

    # Check header
    result = True
print (result)







def parser_payload_header(command_id: int, payload: bytes) -> tuple or None:
    """
    This function parser the header of the payload and depending on the id of
    the command, it returns the header and the records.

    Parameters:
        :command_id (int):
        :payload (bytes):
    Returns:
        :header_payload (tuple or None): (header_payload, records)
    """

    if command_id in (1, 2):
        # for command_id 68 or 1 the header payload is:
        # record_left, number_records.

        # Struct format for header_payload an rest data
        format_header_payload_rest = calc_format_data_rest(">2B", payload)

        # unpak header of payload an the rest data (records)
        header_payload = struct.unpack(format_header_payload_rest, payload)
    else:
        header_payload = None

    return header_payload

def calc_format_data_rest(head_format: str, data: bytes) -> str:
    """
    This function returns the format indicated in 'head_format' argument with
    the format of the rest of the data.

    Parameters:
        :head_format (str): struct format of head of data.
        :data (bytes): data in bytes.
    Returns:
        :(string):
    """

    return f"{head_format}{len(data)-struct.calcsize(head_format)}s"