#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Jerry Wang<wangjianjun@gmail.com>"
import asyncio
from .utils import (
    pack_outgoing_message_to_nest,
    receive_all_messages,
    unpack_incoming_response_from_nest,
)


class MsTcpClient:
    """Tcp client for nestjs microservice"""

    def __init__(self, host, port):
        self.host = host
        if isinstance(port, str):
            self.port = int(port)
        else:
            self.port = port

    async def send(self, pattern, data):
        """send pattern data to microservice"""
        reader, writer = await asyncio.open_connection(self.host, self.port)

        json_data = pack_outgoing_message_to_nest(pattern, data)

        writer.write(json_data)
        await writer.drain()

        message = await receive_all_messages(reader)

        writer.close()
        await writer.wait_closed()

        return unpack_incoming_response_from_nest(message)
