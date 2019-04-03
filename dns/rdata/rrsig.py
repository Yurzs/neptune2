from dns import datatypes
from .rdata import RDATA

name_datatype = {
    # TODO HELP
    'type_covered': datatypes.int16,
    'algorithm': datatypes.int8,
    'labels': datatypes.int8,
    'original_ttl': datatypes.int32,
    'signature_expiration': datatypes.int32,
    'signature_inception': datatypes.int32,
    'key_tag': datatypes.int16,
    'signers_name': datatypes.UrlAddress,
    'signature': datatypes.local_str_without_prefix
}

name_length = {
    'type_covered': 16,
    'algorithm': 8,
    'labels': 8,
    'original_ttl': 32,
    'signature_expiration': 32,
    'signature_inception': 32,
    'key_tag': 16,
    'signers_name': 'DYNAMIC',
    'signature': 'REST'
}


class RRSIG(RDATA):
    name_length = name_length
    name_datatype = name_datatype