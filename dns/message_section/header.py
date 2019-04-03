from dns import datatypes
from .message_sections import MessageSection

name_datatype = {
    'id': datatypes.int16,
    'qr': datatypes.int1,
    'opcode': datatypes.int4,
    'aa': datatypes.int1,
    'tc': datatypes.int1,
    'rd': datatypes.int1,
    'ra': datatypes.int1,
    'z': datatypes.int3,
    'rcode': datatypes.int4,
    'qdcount': datatypes.int16,
    'ancount': datatypes.int16,
    'nscount': datatypes.int16,
    'arcount': datatypes.int16
}

name_length = {
    'id': 16,
    'qr': 1,
    'opcode': 4,
    'aa': 1,
    'tc': 1,
    'rd': 1,
    'ra': 1,
    'z': 3,
    'rcode': 4,
    'qdcount': 16,
    'ancount': 16,
    'nscount': 16,
    'arcount': 16
}


class Header(MessageSection):
    name_datatype = name_datatype
    name_length = name_length
    # http://www.eric-a-hall.com/specs/draft-hall-status-opcode-00-1.txt

