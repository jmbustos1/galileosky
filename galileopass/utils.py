"""
This file have the utils for check and parser data frame of ruptela
"""
import logging
import struct
from collections import namedtuple
from typing import Dict, List
from .data_description_dictionary import data_description
from typing import Dict, List
import datetime
from .data_description_dictionary_extended import data_description_extended
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
        packetlenght1=data[2] + data[1],
        header_crc = data[-2:],
        command_id2=command_id2,
        crc = crc,
        packet_length=packet_length,
        payload=payload
    )
    print("here3")

    return result

def parser_payload(command_id: int, payload: bytes) -> List[Dict] or List:
    if command_id == 68:
        list_records = list()


def flip_bytes(data: bytes) -> int:
    data = struct.pack(
        '<H', data
    )
    data = int.from_bytes(data, "big")
    return data


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


def parser_payload(command_id: int, payload: bytes) -> List[Dict] or List or None or dict:
    if command_id == 1:

        payload_len = len(payload)
        print("payload len: ",payload_len)

        standar_on = True
        sum = 0
        seeking_tag = True
        actual = ""
        value = []
        data_values = {}
        extended_len= []
        extended_buff= []
        extended_count = 0
        #print(data_description.values())
        for i in payload:
            if standar_on == True:    
                if seeking_tag == False:
                    
                    if sum < data_description[actual]["len"]:
                        value.append(str(i))
                        sum += 1
                    if sum >= data_description[actual]["len"]:
                        seeking_tag = True
                        sum = 0
                        data_values[data_description[actual]["name"]] = value
                        
                elif seeking_tag == True:
                    if actual:
                        print("obtained tag ", actual, "and value ", value, "name", data_description[actual]["len"])
                    for j in data_description:
                        if str(i) == "254":
                            standar_on = False
                            seeking_tag = False
                            ext_header = True
                            value = []
                            break
                        elif str(i) == str(int(data_description[str(j)]["tag"],0)):
                            actual = str(j)
                            sum = 0
                            value = []
                            seeking_tag = False
                            break
                print(value)
            else:
                
                if ext_header:
                    if extended_count < 2:
                        extended_len.append(i)
                        extended_count += 1
                    else:
                        seeking_tag = True
                        extended_count = 0
                        ext_header = False
                if seeking_tag == False and ext_header == False:
                    if sum < data_description_extended[actual]["len"]:
                        value.append(str(i))
                        sum += 1
                    if sum >= data_description_extended[actual]["len"]:
                        seeking_tag = True
                        data_values[data_description_extended[actual]["name"]] = value
                        sum = 0
                        extended_count = 0
                        extended_buff = []
                elif seeking_tag == True:
                    if extended_count < 2:
                        extended_buff.append(i)
                        extended_count += 1
                    if extended_count >= 2:
                        for j in data_description_extended:
                            if str(extended_buff[1] + extended_buff[0]) == str(int(data_description_extended[str(j)]["tag"],0)):
                                seeking_tag = False
                                actual = str(j)
                                sum = 0
                                value = []              
                
                        
                print("value :", value)

        #print(data_values)
    return data_values


def interpreter(dic: dict) -> List[Dict] or List or None or dict:
    rest = {}
    for i in dic:
        """Standar Dict"""
        if i == data_description["3"]["name"]:
            resul = ""
            for j in dic[i]:
                resul += chr(int(j))
            rest[data_description["3"]["name"]] = resul
        
        if i == data_description["4"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description["4"]["name"]] = resul

        if i == data_description["5"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description["5"]["name"]] = resul
        
        if i == data_description["6"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            ts = datetime.datetime.fromtimestamp(resul).strftime('%Y-%m-%d %H:%M:%S')
            rest[data_description["6"]["name"]] = ts
        
        if i == data_description["7"]["name"]:
            resul = ""
            sat = int(dic[i][0])&15
            correctness = int(dic[i][0])&240
            latitude = (int.from_bytes(list(map(int, dic[i][1:5])), byteorder='little', signed=True))/1000000
            longitude = (int.from_bytes(list(map(int, dic[i][5:9])), byteorder='little', signed=True))/1000000
            rest["sat"] = sat
            rest["correctness"] = correctness
            rest["latitude"] = latitude
            rest["longitude"] = longitude

        if i == data_description["8"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            speed = (int.from_bytes(list(map(int, dic[i][0:2])), byteorder='little', signed=False))/10
            dir = ((int.from_bytes(list(map(int, dic[i][2:4])), byteorder='little', signed=False))/10)
            rest["speed"] = speed
            rest["dir"] = dir
        
        if i == data_description["9"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            height = (int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=True))
            rest[data_description["9"]["name"]] = height

        if i == data_description["10"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = (int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False))
            if correctness == 0 or correctness == 2:
                rest[data_description["10"]["name"]] = resul*10
            else:
                rest[data_description["10"]["name"]] = resul/10


        if i == data_description["11"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = (int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False))
            rest[data_description["11"]["name"]] = resul
        
        if i == data_description["12"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description["12"]["name"]] = resul

        if i == data_description["13"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description["13"]["name"]] = resul

        if i == data_description["14"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=True)
            rest[data_description["14"]["name"]] = resul

        if i == data_description["174"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            acceleration = int.from_bytes(list(map(int, dic[i][0])), byteorder='little', signed=False)
            braking = int.from_bytes(list(map(int, dic[i][1])), byteorder='little', signed=False)
            cornering_acceleration = int.from_bytes(list(map(int, dic[i][2])), byteorder='little', signed=False)
            strike_on_bumps = int.from_bytes(list(map(int, dic[i][3])), byteorder='little', signed=False)
            rest["acceleration"] = acceleration
            rest["braking"] = braking
            rest["cornering_acceleration"] = cornering_acceleration
            rest["strike_on_bumps"] = strike_on_bumps

        if i == data_description["37"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=True)
            rest[data_description["37"]["name"]] = resul
        
        if i == data_description["53"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=True)
            rest[data_description["53"]["name"]] = resul
        
        if i == data_description["60"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=True)
            rest[data_description["60"]["name"]] = resul
        


        """Extended Dict"""
        if i == data_description_extended["130"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description_extended["130"]["name"]] = resul
        
        if i == data_description_extended["131"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description_extended["131"]["name"]] = resul
        
        if i == data_description_extended["132"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description_extended["132"]["name"]] = resul
        
        if i == data_description_extended["133"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description_extended["133"]["name"]] = resul

        if i == data_description_extended["134"]["name"]:
            resul = ""
            print(list(map(int, dic[i])))
            resul = int.from_bytes(list(map(int, dic[i])), byteorder='little', signed=False)
            rest[data_description_extended["134"]["name"]] = resul
        
        print(i)
    return rest
"""
32 0x20     48 0x30     64 0x40
33 0x21     49 0x31     65 0x41
34 0x22     50 0x32     66 0x42
35 0x23     51 0x33     67 0x43
36 0x24     52 0x34     68 0x44
37 0x25     53 0x35     69 0x45
38 0x26     54 0x36     70 0x46
39 0x27     55 0x37     71 0x47
40 0x28     56 0x38     72 0x48
41 0x29     57 0x39     73 0x49
42 0x2a     58 0x3a     74 0x4a
43 0x2b     59 0x3b     75 0x4b
44 0x2c     60 0x3c     76 0x4c
45 0x2d     61 0x3d     77 0x4d
46 0x2e     62 0x3e
47 0x2f     63 0x3f







"""