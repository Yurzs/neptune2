from dns2 import datatypes


class EDNS:
    class OptionStorage:
        def __init__(self):
            self.storage = []

        def push(self, option: 'Option'):
            self.storage.append(option)

        @property
        def binary(self):
            binstring = ''
            for item in self.storage:
                binstring += item.binary
            return binstring

    class Option:
        def __init__(self, stream):
            self.code = datatypes.BitData(datatypes.int16, stream.read('uint:16'), int)
            self.length = datatypes.BitData(datatypes.int16, stream.read('uint:16'), int)
            self.data = datatypes.BitData(datatypes.int16, stream.read(f'bin:{self.length.value}'), int)

        @property
        def binary(self):
            binstring = ''
            for item in self.__dict__:
                binstring += item.binary
            return binstring

    def __init__(self, name, atype, message: 'Message'):
        self._injected = False
        self._name = name
        self._type = atype
        self._message = message
        self._requestor_udp_payload_size = datatypes.BitData(datatypes.int16,
                                                             self._message._data.read('uint:16'),
                                                             int)
        self._extended_rcode = datatypes.BitData(datatypes.int8,
                                                 self._message._data.read('uint:8'),
                                                 int)
        self._version = datatypes.BitData(datatypes.int8,
                                          self._message._data.read('uint:8'), int)
        self._DNSSEC_OK = datatypes.BitData(datatypes.int2,
                                            self._message._data.read('uint:2'), bool)
        self._z = datatypes.BitData(datatypes.int14,
                                    self._message._data.read('uint:14'), int)
        self._rdlen = datatypes.BitData(datatypes.int16,
                                        self._message._data.read('uint:16'), int)
        left_len = self._rdlen.value
        self._rdata = self.OptionStorage()
        while left_len > 0:
            cur_pos = self._message._data.pos
            self._rdata.push(self.Option(self._message._data))
            left_len -= self._message._data.pos - cur_pos
        message._edns = self

    def push_to_storage(self):
        self._message._bitstorage.push(self)

    def push_binstorage(self):
        self._injected = True
        self._message._bitstorage.bitpush(self._name)
        self._message._bitstorage.bitpush(self._type)
        self._message._bitstorage.bitpush(self._requestor_udp_payload_size)
        self._message._bitstorage.bitpush(self._extended_rcode)
        self._message._bitstorage.bitpush(self._version)
        self._message._bitstorage.bitpush(self._DNSSEC_OK)
        self._message._bitstorage.bitpush(self._z)
        self._message._bitstorage.bitpush(self._rdlen)
        self._message._bitstorage.bitpush(self._rdata)

