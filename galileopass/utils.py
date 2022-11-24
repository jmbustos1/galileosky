"""
This file have the utils for check and parser data frame of ruptela
"""
import logging
import struct
from collections import namedtuple
from typing import Dict, List
from .data_description_dictionary import data_description

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

def parser_header_payload_crc(data: bytes) -> dict:
    """
    This function parser header, payload and crc.

    The data type it handler is bytes.

    Parameters:
        :data (bytes):
    Returns:
        :result (dict): Dictionary with packet_length, imei, command_id,
                        payload, crc
    """

    header = data
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
    print("here2")

    (command_id2,packet_length, payload ,crc) = struct.unpack(
        header_data_format_payload_crc, data
    )

    packet_length = flip_bytes(packet_length)
    print("here3")

    command_id = header[0]
    result = dict(
        command_id=command_id,
        packetlenght1=data[3:5],
        header_crc = data[-2:],
        command_id2=command_id2,
        crc = crc,
        packet_length=packet_length,
        payload=payload
    )
    print("here3")

    return result

def flip_bytes(data: bytes) -> int:
    data = struct.pack(
        '<H', data
    )
    data = int.from_bytes(data, "big")
    return data