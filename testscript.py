import struct



data = b'\x01\x17\x80\x01\x9b\x02'
head_byte = b'\x01'
header = data
print(header)
print(bytes(header[0]))

print(header[0])
print(int.from_bytes(head_byte, "big"))
result = False
if header[0] == int.from_bytes(head_byte, "big"):
    print("hello World")

    # Check header
    result = True
print (result)