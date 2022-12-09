"""
This file have the utils for check and parser data frame of ruptela
"""
import logging
import struct
from collections import namedtuple
from typing import Dict, List
from galileopass.data_description_dictionary import data_description
from galileopass.data_description_dictionary_extended import data_description_extended
def bitwise_and_bytes(a, b):
    g = int.from_bytes(a, byteorder="big")
    f = int.from_bytes(b, byteorder="big")
    print(g)
    print(f)
    result_int = g & f
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")
def bitwise_or_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") | int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")
def bitwise_xor_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") ^ int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")
for j in data_description_extended:
    a= 1
    #print(j, data_description_extended[str(j)]["tag"],  data_description_extended[str(j)]["description_name"])


Data = [7, 192, 14, 50, 3, 184, 215, 45, 5]

Data2 = [92, 0, 72, 8]

d = b'\x99'
mask = b'\xf0'

op = bitwise_and_bytes(d, mask)
print(op)


sat = Data[0]&15
correctness = Data[0]&240
latitude = (int.from_bytes(list(map(int, Data[1:5])), byteorder='little', signed=True))/1000000
longitude = (int.from_bytes(list(map(int, Data[5:9])), byteorder='little', signed=True))/1000000

print(Data[5:9])

speed = (int.from_bytes(list(map(int, Data2[0:2])), byteorder='little', signed=False))/10
dir = ((int.from_bytes(Data2[2:4], byteorder='little', signed=False))/10)
print("sat: ", sat )
print("correctness: ", correctness)
print("latitude: ", latitude)
print("longitude: ", longitude)
print("speed: ", speed)
print("dir: ", dir)



print(32900-360*90)
