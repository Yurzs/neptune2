from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'txt_data': datatypes.local_str
}

name_length = {
    'hash_alg': 8,
    'flags': 8,
    'iterations': 16,
    'salt_length': 8,
    'salt': ['salt_length', ],
    'hash_length': 8,
    'next_hashed_owner_name': ['hash_length', ],
    'type_bit_maps': 'REST'
}


class NSEC3(RDATA):
    """
    https://www.rfc-archive.org/getrfc.php?rfc=5155
    """
    name_length = name_length
    name_datatype = name_datatype
