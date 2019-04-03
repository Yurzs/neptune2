import bitstring

name_datatype = {}

name_length = {}


class MessageSection:
    name_datatype = name_datatype
    name_length = name_length

    def __init__(self, *args, **kwargs):
        self.domain_links = kwargs.get('domain_links', {})
        self.byte_counter = kwargs.get('byte_counter')
        if kwargs.get('dictionary'):
            for item in self.name_datatype:
                setattr(self, item, self.name_datatype[item](kwargs.get('dictionary')[item]))
        elif kwargs.get('byte_data'):
            self.data = kwargs.get('byte_data')
            self.from_bytes()

    def from_bytes(self):
        bin_counter = 0
        for item in self.name_datatype:
            if self.name_length[item] == 'REST':
                setattr(self, item, self.name_datatype[item](self.data))
                self.byte_counter += int(len(self.data) / 8)
                break
            elif isinstance(self.name_length[item], list):
                setattr(self, item,
                        self.name_datatype[item](self.data[:getattr(self, self.name_datatype[item][0])]))
                self.data = self.data[getattr(self, self.name_datatype[item][0]):]
                self.byte_counter += int(self.data[:getattr(self, self.name_datatype[item][0])] / 8)
            elif self.name_length[item] == 'DYNAMIC':
                obj, self.data, self.byte_counter, self.domain_links = self.name_datatype[item].decode(
                    byte_data=self.data,
                    byte_counter=self.byte_counter,
                    domain_links=self.domain_links)
                setattr(self, item, obj)
            elif issubclass(self.name_datatype[item], int) and isinstance(self.data, bitstring.BitArray):
                    setattr(self, item, self.name_datatype[item](self.data.bin[:self.name_length[item]], base=2))
                    self.data = bitstring.BitArray(bin=self.data.bin[self.name_length[item]:])
                    if self.name_length[item] >= 8:
                        self.byte_counter += int(self.name_length[item] / 8)
                    else:
                        bin_counter += self.name_length[item]
            else:
                setattr(self, item, self.name_datatype[item](self.data[:self.name_length[item]]))
                self.data = self.data[self.name_length[item]:]
                if self.name_length[item] >= 8:
                    self.byte_counter += int(self.name_length[item] / 8)
                else:
                    bin_counter += self.name_length[item]
            if bin_counter >= 8:
                self.byte_counter += bin_counter // 8
                bin_counter = bin_counter % 8

    @classmethod
    def decode(cls, byte_counter, domain_links, dictionary: dict = (),
               byte_data: bitstring.BitArray = bitstring.BitArray('')):
        kwargs = {}
        kwargs['byte_counter'] = byte_counter
        kwargs['domain_links'] = domain_links
        kwargs['dictionary'] = dictionary
        kwargs['byte_data'] = byte_data
        result = cls(**kwargs)
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
        return bitstring.BitArray(bin=BINARY)

    def __setitem__(self, key, value):
        if self.name_datatype.get(key):
            setattr(self, key, self.name_datatype[key](value))
        else:
            raise ValueError('Wrong key')
