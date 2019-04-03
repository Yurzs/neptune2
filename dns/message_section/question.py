from dns import datatypes
from .message_sections import MessageSection

name_datatype = {
    'labels': datatypes.UrlAddress,
    'qtype': datatypes.int16,
    'qclass': datatypes.int16,
}

name_length = {
    'labels': 'DYNAMIC',
    'qtype': 16,
    'qclass': 16,
}


class Question(MessageSection):
    name_datatype = name_datatype
    name_length = name_length

