"""
This file have the utils for check and parser data frame of ruptela
"""
import logging
import struct
from collections import namedtuple
from typing import Dict, List

#import crcmod

#from .data_description_dictionary import data_description

HEADER_DATA_FORMAT = ">HQB"  # Format packet_length, imei, command_id
PACKET_LENGTH_DATA_FORMAT = ">H"  # Format pacaket length
CRC_DATA_FORMAT = "H"  # Format CRC
HEADER_FORMAT_IN_BYTES = ">11s"  # Format header in bytes
FORMAT_TO_CHECK_CRC = ">QB"  # Format to pack data and check crc
# Format for the "record header" for extended protocol
RECORD_HEADER_FORMAT = ">L3Bll2HBHBH"
LEN_HEADER = 3

head_byte = b'\x01'

def check_header(data: bytes) -> bool:
    """
    This function check header of data frame, the data type it handler is
    bytes.

    Parameters:
        :data (bytes): data to check header.

    Returns:
        :result (bool):

    :return: Bool
    """

    # Get struct format for the header and the rest data.
    #header_format_and_data = calc_format_data_rest(
    #    HEADER_FORMAT_IN_BYTES, data
    #)

    try:
        # Get the header and the rest of the records in _
        header = data
        print(header)
        print(header[0])
        print("hello world 2")
        if header[0] == int.from_bytes(head_byte, "big"):
            print("hello World")

        # Check header
            result = True
    except struct.error:
        result = False

    return result
