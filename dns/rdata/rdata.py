import bitstring

name_datatype = {}

name_length = {}


class RDATA:
    name_length = name_length
    name_datatype = name_datatype

    def __init__(self, *args, **kwargs):
        self.domain_links = kwargs.get('domain_links')
        self.byte_counter = kwargs.get('byte_counter')
        if kwargs.get('dictionary'):
            self.from_dictionary(kwargs.get('dictionary'))
        elif kwargs.get('byte_data'):
            self.from_bytes(kwargs.get('byte_data'))

    @classmethod
    def decode(cls, byte_counter, domain_links, dictionary: dict = (),
               byte_data: bitstring.BitArray = bitstring.BitArray('')):
        result = cls(byte_counter=byte_counter,
                     domain_links=domain_links,
                     dictionary=dictionary,
                     byte_data=byte_data)
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

    def encode(self):
        BINARY = ''
        for item in self.name_datatype:
            BINARY += getattr(self, item).binary
        if len(BINARY) % 8 != 0:
            print(f'{self.__class__}')
            for item in self.name_datatype:
                print(f'{item} length is {len(getattr(self, item).binary)}')
        return bitstring.BitArray(bin=BINARY)

    def from_bytes(self, byte_data):
        self.data = byte_data
        for item in self.name_datatype:
            if self.name_length[item] == 'REST':
                obj, self.data, self.byte_counter, self.domain_links = self.name_datatype[item].decode(
                    byte_data=self.data,
                    byte_counter=self.byte_counter,
                    domain_links=self.domain_links
                )
                setattr(self, item, obj)
                break
            elif isinstance(self.name_length[item], list):
                setattr(self, item, self.name_datatype[item](self.data[:getattr(self, self.name_length[item][0])]))
                self.data = self.data[getattr(self, self.name_datatype[item][0]):]
            elif self.name_length[item] == 'DYNAMIC':
                print(self.__dict__)
                print(self.__class__, item)
                obj, self.data, self.byte_counter, self.domain_links = self.name_datatype[item].decode(
                    byte_data=self.data,
                    byte_counter=self.byte_counter,
                    domain_links=self.domain_links
                )
                setattr(self, item, obj)
            else:
                try:
                    obj, self.data, self.byte_counter, self.domain_links = self.name_datatype[item].decode(
                        byte_data=self.data,
                        byte_counter=self.byte_counter,
                        domain_links=self.domain_links
                    )
                    setattr(self, item, obj)
                except AttributeError:
                    if issubclass(self.name_datatype[item], int):
                        setattr(self, item, self.name_datatype[item](self.data.bin[:self.name_length[item]], base=2))
                        self.data = self.data[int(self.name_length[item]/8):]
                    else:
                        setattr(self, item, self.name_datatype[item](self.data[:self.name_length[item]]))
                        self.data = self.data[self.name_length[item]:]


    def from_dictionary(self, data):
        for item in self.name_datatype:
            if isinstance(self.name_datatype[item], dict):
                setattr(self, item, self.name_datatype[item][data[item]])
            else:
                setattr(self, item, self.name_datatype[item](data[item]))
