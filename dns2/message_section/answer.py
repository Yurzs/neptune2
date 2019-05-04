import typing
from bitstring import ConstBitStream
import dns2


class Answer:

    # def __init__(self, message: 'Message'):
    #     self._message = message
    #     if isinstance(message._data, dict):
    #         self.parse_dict()
    #     elif isinstance(message._data, ConstBitStream):
    #         self.parse_bytes()

    @classmethod
    def parse(cls, message: 'Message'):
        answer = cls()
        answer._injected = False
        answer._message = message
        if isinstance(message._data, dict):
            return answer.parse_dict(**message._data)
        elif isinstance(message._data, ConstBitStream):
            return answer.parse_bytes()

    def parse_dict(self, **kwargs):
        self._name = dns2.datatypes.BitData(dns2.DomainName, kwargs.get('name'), str)
        self._type = dns2.datatypes.BitData(dns2.datatypes.int16, kwargs.get('type'), int)
        self._cls = dns2.datatypes.BitData(dns2.datatypes.int16, kwargs.get('cls'), int)
        self._ttl = dns2.datatypes.BitData(dns2.datatypes.int32, kwargs.get('ttl'), int)
        # self._rdlength = dns2.datatypes.BitData(dns2.datatypes.int16, kwargs.get('rdlength'), int)
        self._rdata = dns2.datatypes.BitData(datatype=dns2.rdata_type[self._type.value],
                                             repr_type=dns2.rdata_type[self._type.value],
                                             value=kwargs.get('rdata'))
        return self

    def parse_bytes(self):
        name = dns2.datatypes.decode_domain(self._message)
        if isinstance(name, dns2.Domain):
            self._name = dns2.datatypes.BitData(dns2.DomainName, name.label, str)
        elif name:
            self._name = dns2.datatypes.BitData(dns2.DomainName, name[0].label, str)
        else:
            self._name = dns2.datatypes.BitData(dns2.DomainName, '', str)
        self._type = dns2.datatypes.BitData(dns2.datatypes.int16, self._message._data.read('uint:16'), int)
        if self._type.value == 41:
            dns2.EDNS(self._name, self._type, self._message)
        else:
            self._cls = dns2.datatypes.BitData(dns2.datatypes.int16, self._message._data.read('uint:16'), int)
            self._ttl = dns2.datatypes.BitData(dns2.datatypes.int32, self._message._data.read('uint:32'), int)
            self._rdlength = dns2.datatypes.BitData(dns2.datatypes.int16, self._message._data.read('uint:16'), int)
            self._rdata = dns2.datatypes.BitData(dns2.rdata_type[self._type.value],
                                                 self._message._data.read(f'bin:{self._rdlength.value * 8}'),
                                                 dns2.rdata_type[self._type.value])
        # self._cls
        # self._ttl
        # self._rdlength
        # self._rdata

    def push_to_storage(self):
        self._message._bitstorage.push(self)

    def push_binstorage(self):
        self._injected = True
        self._message._bitstorage.bitpush(self._name)
        self._message._bitstorage.bitpush(self._type)
        self._message._bitstorage.bitpush(self._cls)
        self._message._bitstorage.bitpush(self._ttl)
        self._message._bitstorage.bitpush(self.rdlength)
        self._message._bitstorage.bitpush(self._rdata)


    @property
    def rdlength(self):
        return dns2.datatypes.BitData(dns2.datatypes.int16, int(len(self._rdata.binary) / 8), int)
