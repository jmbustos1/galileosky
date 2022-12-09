"""
This file have the utils for check and parser data frame of ruptela
"""
import logging
import struct
import time
import datetime
from collections import namedtuple
from typing import Dict, List
from galileopass.data_description_dictionary import data_description
from galileopass.data_description_dictionary_extended import data_description_extended
#import crcmod
st = time.time()

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
     # result = True
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


def parser_payload(command_id: int, payload: bytes) -> List[Dict] or List or None or dict:
    if command_id == 1:
        print("\n")
        print("\n")
        payload_len = len(payload)
        print("payload len: ",payload_len)
        print( f"{len(payload)}s" )
        #print(data_description)
        #print(data_description["3"])
        print("payload: ", payload) 
        
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
        z = ""
        for i in payload:
            z = z + str(i)+ " "
        print("payload str:", z)
        for i in payload:
            if standar_on == True:    
                print("byte processing", i)
                print(actual)
                print("seeking, tag ", seeking_tag)
                #print(i)
                print(sum)
                if seeking_tag == False:
                    
                    if sum < data_description[actual]["len"]:
                        print("actual1:", actual)
                        value.append(str(i))
                        sum += 1
                    if sum >= data_description[actual]["len"]:
                        print("actual2:", actual)
                        print("good: ", "obtained tag ", actual, "and value ", value, "name", data_description[actual]["name"])
                        seeking_tag = True
                        sum = 0
                        data_values[data_description[actual]["name"]] = value
                        print("data values: ", data_values)
                        
                elif seeking_tag == True:
                    if actual:
                        print("obtained tag ", actual, "and value ", value, "name", data_description[actual]["len"])
                    for j in data_description:
                        #print(j)
                        ##print(data_description[str(j)])
                        if str(i) == "254":
                            print("extended id protocol detected")
                            standar_on = False
                            seeking_tag = False
                            ext_header = True
                            value = []
                            break
                        elif str(i) == str(int(data_description[str(j)]["tag"],0)):
                            print("processing", str(i))
                            print("tag: ", data_description[str(j)]["tag"], "name: ", data_description[str(j)]["name"])
                            actual = str(j)
                            print("actual3:", actual)
                            sum = 0
                            value = []
                            seeking_tag = False
                            break
                print(value)
            else:
                
                if ext_header:
                    print("ok")
                    print(extended_count)
                    if extended_count < 2:
                        extended_len.append(i)
                        extended_count += 1
                    else:
                        seeking_tag = True
                        extended_count = 0
                        ext_header = False
                print("byte processing", i, extended_len)
                if seeking_tag == False and ext_header == False:
                    if sum < data_description_extended[actual]["len"]:
                        print("actual1:", actual)
                        value.append(str(i))
                        sum += 1
                    if sum >= data_description_extended[actual]["len"]:
                        print("actual2:", actual)
                        seeking_tag = True
                        data_values[data_description_extended[actual]["name"]] = value
                        sum = 0
                        extended_count = 0
                        extended_buff = []
                elif seeking_tag == True:
                    print("byte processing 2", i, extended_len, extended_buff)
                    if extended_count < 2:
                        extended_buff.append(i)
                        extended_count += 1
                    if extended_count >= 2:
                        print("byte processing 3", i, extended_len)
                        print(extended_len)
                        print(extended_buff)
                        for j in data_description_extended:
                            #print(j)
                            #print(str(extended_buff[1] + extended_buff[0]), str(int(data_description_extended[str(j)]["tag"],0)))
                            if str(extended_buff[1] + extended_buff[0]) == str(int(data_description_extended[str(j)]["tag"],0)):
                                print("tag: ", data_description_extended[str(j)]["tag"], "name: ", data_description_extended[str(j)]["name"])
                                seeking_tag = False
                                actual = str(j)
                                sum = 0
                                value = []              
                                print("found : ", str(extended_buff[1] + extended_buff[0]))
                
                        
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
            
            
            
rest = parser_payload(1,result["payload"])
print(rest)
rest2 = interpreter(rest)
print(rest2)


et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

"""
agregar tags en hexa y agregar todos los descriptores.

"""