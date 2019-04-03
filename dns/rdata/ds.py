from .rdata import RDATA

name_datatype = {
    # TODO HELP
    'key_tag': 16,
    'algorithm': 8,
    'digest_type': 8,
    'digest': 'REST'
}

name_length = {
    'key_tag': 16,
    'algorithm': 8,
    'digest_type': 8,
    'digest': 'REST'
}


class DS(RDATA):
    name_length = name_length
    name_datatype = name_datatype