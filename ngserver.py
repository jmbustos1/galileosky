import socket
import datetime
import asyncio
from galileopass.server import create_server
HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 2424  # Port to listen on (non-privileged ports are > 1023)


"""
    ruptela dev server

    https://docs.python.org/3/library/asyncio-stream.html#asyncio.start_server
"""



async def main():
    """
    TCP server using streams.
    """

    server = await asyncio.start_server(create_server, "0.0.0.0", 2424)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
