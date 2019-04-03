import bitstring

from dns import datatypes
from dns.parser import ParserMixin
from dns.rdata import TYPES

preparse_name = {
    'name': datatypes.UrlAddress,
    'atype': datatypes.int16,
}

preparse_length = {
    'name': 'DYNAMIC',
    'atype': 16,
}

name_datatype = {
    'aclass': datatypes.int16,
    'ttl': datatypes.int32,
    'rdlength': datatypes.int16,
    'rdata': TYPES,
}

name_length = {
    'aclass': 16,
    'ttl': 32,
    'rdlength': 16,
    'rdata': ['rdlength', ],
}

opt_name_datatype ={
    'aclass': datatypes.int16,
    'extended_rcode': datatypes.int8,
    'version': datatypes.int8,
    'do': datatypes.int2,
    'z': datatypes.int14,
    'rdlength': datatypes.int16,
    'rdata': TYPES,
}
opt_name_length = {
    'aclass': 16,
    'extended_rcode': 8,
    'version': 8,
    'do': 2,
    'z': 14,
    'rdlength': 16,
    'rdata': ['rdlength', ],
}

special_encode = {
    41: opt_name_datatype
}

class RR(ParserMixin):
    def __init__(self, *args, **kwargs):
        self.domain_links = kwargs.get('domain_links')
        self.byte_counter = kwargs.get('byte_counter')
        if kwargs.get('dictionary'):
            self.from_dictionary(kwargs.get('dictionary'))
            # print(f'from dict {self.__dict__}')
        elif kwargs.get('byte_data'):
            self.from_bytes(kwargs.get('byte_data'))
            # print(f'from bytes {self.__dict__}')

    @classmethod
    def decode(cls, byte_counter, domain_links, dictionary: dict = (),
               byte_data: bitstring.BitArray = bitstring.BitArray('')):
        result = cls(byte_counter=byte_counter, domain_links=domain_links, dictionary=dictionary, byte_data=byte_data)
        domain_links = result.domain_links
        byte_counter = result.byte_counter
        result.__dict__.pop('domain_links')
        result.__dict__.pop('byte_counter')
        try:
            data = result.data
            result.__dict__.pop('data')
            return result, data, byte_counter, domain_links
        except AttributeError:
            return result, '', byte_counter, domain_links

    def encode_specials(self, name_datatype):
        BINARY = ''
        for item in name_datatype:
            if item == 'rdata':
                BINARY += getattr(self, item).encode().bin
            else:
                BINARY += getattr(self, item).binary
        return BINARY

    def encode(self):
        BINARY = ''
        for item in preparse_name:
            BINARY += getattr(self, item).binary
        if self.atype in special_encode:
            BINARY += self.encode_specials(special_encode[self.atype])
        else:
            for item in name_datatype:
                if item == 'rdata':
                    BINARY += getattr(self, item).encode().bin
                else:
                    BINARY += getattr(self, item).binary
        return bitstring.BitArray(bin=BINARY)

    def from_bytes(self, byte_data):
        self.data = byte_data
        self.parse_byte_rr(preparse_name, preparse_length)
        if self.atype == 41:
            self.parse_byte_rr(name_datatype=opt_name_datatype, name_length=opt_name_length)
        else:
            self.parse_byte_rr(name_datatype, name_length)


                # elif not getattr(self, 'atype', None) == 257 and item not in ['extended_rcode', 'version', 'do', 'z']:
                #     # print(item)
                #     if issubclass(name_datatype[item], int) and isinstance(self.data, bitstring.BitArray):
                #         setattr(self, item, name_datatype[item](self.data.bin[:name_length[item]], base=2))
                #         self.data = bitstring.BitArray(bin=self.data.bin[name_length[item]:])
                #         self.byte_counter += int(name_length[item] / 8)
                #     else:
                #         setattr(self, item, name_datatype[item](self.data[:name_length[item]]))
                #         self.data = self.data[name_length[item]:]
                #         self.byte_counter += int(name_length[item] / 8)




    def from_dictionary(self, dict_data):
        self.parse_dict_rr(dict_data, preparse_name)
        if self.atype == 41:
            self.parse_dict_rr(dict_data, opt_name_datatype)
        else:
            self.parse_dict_rr(dict_data, name_datatype)
