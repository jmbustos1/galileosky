import asyncio
import logging
import os
import struct
import time
from datetime import datetime, timedelta
from .utils import (
    check_header,
    parser_header_payload_crc,
)


async def create_server(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
):
    """
    Creates a ruptela object when each client connects to the server.
    """

    ruptela = GalileoServer(reader, writer)

    print("cs> create_server:%d", id(ruptela))
    await ruptela()
    print("cs< create_server:%d", id(ruptela))


class GalileoServer:  # pylint: disable=too-many-instance-attributes
    """
    Handles the data sent by the client.

    USAGE:
        ruptela = RuptelaServer(reader, writer)
        await ruptela ()
    """

    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        print("rs>__init__:%d", id(self))

        self.reader = reader
        self.writer = writer
        self.consumer = None
        self.buffer = b""
        self.counter_check_data = 0
        self.connection_state = "disconnected"
        self.result = dict()
        self.peername = tuple()
        self.tasks_list = list()
        self.timeout = 120

        # variables to upload cfg
        self._index_cfg_packets_list = 0
        self._cfg_packets_list = list()
        self._status_cfg = "finish"
        self._cfg_timeout_start = 0
        self._task_check_cfg_timeout = None

        # varables to upload firmware
        self._index_firmware_packets_list = 0
        self._firmware_packets_list = list()
        self._status_firmware = "finish"
        self._firmware_timeout_start = 0
        self._task_check_firmware_timeout = None

        # consumer
        #self.consumer = RuptelaConsumer(self)

        print("rs<__init__:%d", id(self))
    async def __call__(self):
        """
        call
        """
        self.peername = self.writer.get_extra_info("peername")
        print("rs>__call__:%s:%d", self.peername, id(self))

        self._connection_made()

        #consumer_task = asyncio.create_task(self.consumer())
        received_task = asyncio.create_task(self.data_received())

        await asyncio.gather(received_task)

        for task in self.tasks_list:
            await task

        print("rs<__call__:%s:%d", self.peername, id(self))



    def _connection_made(self):
        """
        This method log the connection made from client.
        """
        self.peername = self.writer.get_extra_info("peername")
        print("rs>_connection_made:%s:%d", self.peername, id(self))

        self.connection_state = "connected"
        print(
            "Connection from %s with %d", self.peername, id(self.consumer)
        )

        print("rs<_connection_made:%s:%d", self.peername, id(self))



    async def data_received(self):
        """
        This method receives and parser the data sent by clients
        """
        self.peername = self.writer.get_extra_info("peername")
        print("rs>data_received:%s:%d", self.peername, id(self))

        imei = None
        imei_group_datetime = datetime.utcnow() - timedelta(minutes=15)
        try:
            while self.connection_state == "connected":
                print("rs>...0...data_received:%d", id(self))
                data = b""
                try:
                    data_with_timeout = await asyncio.wait_for(
                        self.reader.read(1024), timeout=self.timeout
                    )
                    print(datetime.utcnow())
                except asyncio.TimeoutError:
                    print("timeout error")
                    pass
                else:
                    data += data_with_timeout
                print("rs>...1...data_received:%d", id(self))

                self.buffer += data
                check_data = await self._check_data()

                if data and check_data:
                    await asyncio.create_task(
                        self._response_ack(self.result["command_id"], self.result["header_crc"])
                    )
                    #self.buffer = b""

        except:
            pass
    
    async def _check_data(self) -> bool:
        """
        This method check the data sent by clients.

        Close the connection when CRC is False and when
        counter_check_data is 3.

        Check Header -> Check Packet Length -> Check CRC.
        """
        self.peername = self.writer.get_extra_info("peername")
        print("rs>_check_data:%s:%d", self.peername, id(self))

        result_check_header = check_header(self.buffer)
        if result_check_header:
            result = parser_header_payload_crc(self.buffer)
            self.result = result
            print(self.result["command_id"])
            print(self.result["header_crc"])
            print(self.result["command_id2"])
            print(self.result["crc"])
            print(self.result["packet_length"])
            print(self.result["packetlenght1"])
            print(self.result)
            self.buffer = b""
            return True

        print("rs<_check_data:%s:%d", self.peername, id(self))
        return False


    async def _response_ack(self, command_id: int, header_crc: bytes) -> None:
        """8
        This method responds to the client with an acknowledge command.
        """
        self.peername = self.writer.get_extra_info("peername")
        print("rs>_response_ack:%s:%d", self.peername, id(self))
        if command_id == 1:
            print("executing confirmation package")
            print("confirmation_pack 1 ")

            pack_checksum = header_crc
            print(header_crc)
            print("W1")
            confirmation_header = b'\x02'
            print("W1")
            confirmation_pack = confirmation_header + pack_checksum
            print("W3")
            print("confirmation_pack")
            print(confirmation_pack)

            self.writer.write(confirmation_pack)
            await self.writer.drain()

