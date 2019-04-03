from dns import datatypes
from .rdata import RDATA

name_datatype = {
    # TODO HELP
    'type_covered': datatypes.int16,
    'algorithm': datatypes.int8,
    'labels': datatypes.int8,
    'original_ttl': datatypes.int32,
    'signature_expiration': datatypes.int32,
    'key_tag': 16,
    'signers_name': 'DYNAMIC',
    'signature': 'REST'
}

name_length = {
    'type_covered': 16,
    'algorithm': 8,
    'labels': 8,
    'original_ttl': 32,
    'signature_expiration': 32,
    'key_tag': 16,
    'signers_name': 'DYNAMIC',
    'signature': 'REST'
}


class SIG(RDATA):
    name_length = name_length
    name_datatype = name_datatype
