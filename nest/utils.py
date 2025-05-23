#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Jerry Wang<wangjianjun@gmail.com>"

from asyncio import StreamReader
import uuid
import json


def pack_outgoing_message_to_nest(pattern, data):
    """put pattern and data in correct format

    message format, refer to
    https://stackoverflow.com/questions/55628093/use-socket-client-with-nestjs-microservice
    used to send request to other nest microservice
    """
    _id = uuid.uuid4()
    dict_merged = {"pattern": pattern, "data": data, "id": str(_id)}
    s_json = json.dumps(obj=dict_merged)
    return f"{len(s_json)}#{s_json}".encode()


def unpack_incoming_response_from_nest(message):
    """to unpack message from other nest microservice"""
    _s = message.split(b"#")
    final_length = int(_s[0])
    message = json.loads(message[len(str(final_length)) + 1 :].decode())

    return message.get("err"), message.get("response")


def pack_outgoing_message_to_client(response, message_id, err=None):
    """send the message to the client as microservice server"""
    dict_merged = {
        "err": err,
        "response": response,
        "isDisposed": True,
        "id": message_id,
    }
    s_json = json.dumps(obj=dict_merged)
    return f"{len(s_json)}#{s_json}".encode()


def unpack_incoming_message_from_client(message):
    """unpack the incoming message from client as microservice server"""
    _s = message.split(b"#")
    final_length = int(_s[0])
    message = json.loads(message[len(str(final_length)) + 1 :].decode())
    return message["pattern"], message["data"], message["id"]


def get_response_message(message, data, final_length):
    """get the response message

    message -- previous received message
    data - new received messages
    """
    if message == b"":
        _s = data.split(b"#")
        final_length = int(_s[0].decode())

    message += data
    try:
        if len(message.decode()) == final_length + len(str(final_length)) + 1:
            return message, final_length, True
    except UnicodeDecodeError:
        pass
    return message, final_length, False


async def receive_all_messages(reader: StreamReader):
    """get all messages from the sock"""
    message = b""
    final_length = 0
    while True:
        _d = await reader.read(1024)
        if _d:
            message, final_length, done = get_response_message(
                message, _d, final_length
            )
            if done:
                break
        else:
            break
    return message
