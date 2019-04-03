import bitstring

from dns import datatypes
from .rdata import RDATA

OPTION_CODES = {

}

name_datatype = {
    'option_code': datatypes.int16,
    'option_length': datatypes.int16,
    'option_data': datatypes.local_str
}

name_length = {
    'option_code': 16,
    'option_length': 16,
    'option_data': 'REST'
}


# @do_not_cache
class OPT(RDATA):
    """
    Pseudo-RR
    0 or 1 no more per message
    OPTION-CODE    (Assigned by IANA.)
    OPTION-LENGTH  Size (in octets) of OPTION-DATA.
    OPTION-DATA    Varies per OPTION-CODE.
    """
    name_length = name_length
    name_datatype = name_datatype

    def encode(self):
        BINARY = ''
        for item in self.name_datatype:
            try:
                BINARY += getattr(self, item).binary
            except AttributeError:
                break
        return bitstring.BitArray(bin=BINARY)

    def from_dictionary(self, data):
        for item in self.name_datatype:
            try:
                if isinstance(self.name_datatype[item], dict):
                    setattr(self, item, self.name_datatype[item][data[item]])
                else:
                    setattr(self, item, self.name_datatype[item](data[item]))
            except AttributeError:
                continue
