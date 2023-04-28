from PIL import Image
from mcap.records import Message, Schema
from mcap_ros2.decoder import Decoder
from pyzstd import decompress


def decompress_message(message: Message) -> Message:
    message.data = decompress(message.data)
    return message


def image_to_torch(message: Message, schema: Schema, decompressed: bool = True) -> int:
    decoder = Decoder()
    if decompressed:
        ros_msg = decoder.decode(schema, decompress_message(message))
    else:
        ros_msg = decoder.decode(schema, message)
    return 0
