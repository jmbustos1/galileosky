import asyncio
import logging
import os
import struct
import time
from datetime import datetime, timedelta


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
        self.timeout = ""

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



