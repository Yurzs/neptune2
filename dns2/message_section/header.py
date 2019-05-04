from dns2 import datatypes
from bitstring import BitArray, ConstBitStream
import typing
import re


class Header:

    def __init__(self, message):
        self._injected = False
        self._message = message
        if isinstance(message._data, ConstBitStream):
            self.parse_bytes()
        elif isinstance(message._data, dict):
            self.parse_dict()

    def parse_dict(self, **kwargs):
        self._id = datatypes.BitData(datatypes.int16, kwargs.get('id'), int)
        self._qr = datatypes.BitData(datatypes.int1, kwargs.get('qr'), bool)
        self._opcode = datatypes.BitData(datatypes.int4, kwargs.get('opcode'), int)
        self._aa = datatypes.BitData(datatypes.int1, kwargs.get('aa'), bool)
        self._tc = datatypes.BitData(datatypes.int1, kwargs.get('tc'), bool)
        self._rd = datatypes.BitData(datatypes.int1, kwargs.get('rd'), bool)
        self._ra = datatypes.BitData(datatypes.int1, kwargs.get('ra'), bool)
        self._z = datatypes.BitData(datatypes.int3, kwargs.get('z'), int)
        self._rcode = datatypes.BitData(datatypes.int4, kwargs.get('rcode'), int)
        self._qdcount = datatypes.BitData(datatypes.int16, kwargs.get('qdcount', 0), int)
        self._ancount = datatypes.BitData(datatypes.int16, kwargs.get('ancount', 0), int)
        self._nscount = datatypes.BitData(datatypes.int16, kwargs.get('nscount', 0), int)
        self._arcount = datatypes.BitData(datatypes.int16, kwargs.get('arcount', 0), int)


    def parse_bytes(self):
        self._id = datatypes.BitData(datatypes.int16, self._message._data.read('uint:16'), int)
        self._qr = datatypes.BitData(datatypes.int1, self._message._data.read('uint:1'), bool)
        self._opcode = datatypes.BitData(datatypes.int4, self._message._data.read('uint:4'), int)
        self._aa = datatypes.BitData(datatypes.int1, self._message._data.read('uint:1'), bool)
        self._tc = datatypes.BitData(datatypes.int1, self._message._data.read('uint:1'), bool)
        self._rd = datatypes.BitData(datatypes.int1, self._message._data.read('uint:1'), bool)
        self._ra = datatypes.BitData(datatypes.int1, self._message._data.read('uint:1'), bool)
        self._z = datatypes.BitData(datatypes.int3, self._message._data.read('uint:3'), int)
        self._rcode = datatypes.BitData(datatypes.int4,self._message._data.read('uint:4'), int)
        self._qdcount = datatypes.BitData(datatypes.int16, self._message._data.read('uint:16'), int)
        self._ancount = datatypes.BitData(datatypes.int16, self._message._data.read('uint:16'), int)
        self._nscount = datatypes.BitData(datatypes.int16, self._message._data.read('uint:16'), int)
        self._arcount = datatypes.BitData(datatypes.int16, self._message._data.read('uint:16'), int)

    def push_to_storage(self):
        self._message._bitstorage.push(self)

    def push_binstorage(self):
        self._injected = True
        self._message._bitstorage.bitpush(self.id)
        self._message._bitstorage.bitpush(self.qr)
        self._message._bitstorage.bitpush(self.opcode)
        self._message._bitstorage.bitpush(self.aa)
        self._message._bitstorage.bitpush(self.tc)
        self._message._bitstorage.bitpush(self.rd)
        self._message._bitstorage.bitpush(self.ra)
        self._message._bitstorage.bitpush(self.z)
        self._message._bitstorage.bitpush(self.rcode)
        self._message._bitstorage.bitpush(self.qdcount)
        self._message._bitstorage.bitpush(self.ancount)
        self._message._bitstorage.bitpush(self.nscount)
        self._message._bitstorage.bitpush(self.arcount)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id.value = self._id._datatype(value)

    @property
    def qr(self):
        return self._qr

    @qr.setter
    def qr(self, value):
        self._qr.value = self._qr._datatype(value)

    @property
    def opcode(self):
        return self._opcode

    @opcode.setter
    def opcode(self, value):
        self._opcode.value = self._opcode._datatype(value)

    @property
    def aa(self):
        return self._aa

    @aa.setter
    def aa(self, value):
        self._aa.value = self._aa._datatype(value)

    @property
    def tc(self):
        return self._tc

    @tc.setter
    def tc(self, value):
        self._tc.value = self._tc._datatype(value)

    @property
    def rd(self):
        return self._rd

    @rd.setter
    def rd(self, value):
        self._rd.value = self._rd._datatype(value)

    @property
    def ra(self):
        return self._ra

    @ra.setter
    def ra(self, value):
        self._ra.value = self._ra._datatype(value)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z.value = self._z._datatype(value)

    @property
    def rcode(self):
        return self._rcode

    @rcode.setter
    def rcode(self, value):
        self._rcode.value = self._rcode._datatype(value)

    @property
    def qdcount(self):
        return datatypes.BitData(datatypes.int16, 1 if hasattr(self._message, 'question') else 0, int)

    @qdcount.setter
    def qdcount(self, value):
        self._qdcount.value = self._qdcount._datatype(value)

    @property
    def ancount(self):
        return datatypes.BitData(datatypes.int16, len(self._message.answers['answer']), int)

    @ancount.setter
    def ancount(self, value):
        self._ancount.value = self._ancount._datatype(value)

    @property
    def nscount(self):
        return datatypes.BitData(datatypes.int16, len(self._message.answers['authority']), int)

    @nscount.setter
    def nscount(self, value):
        self._nscount.value = self._nscount._datatype(value)


    @property
    def arcount(self):
        return datatypes.BitData(datatypes.int16,
                                 len(self._message.answers['additional']) + 1 if self._message._edns else len(self._message.answers['additional']),
                                 int)


    @arcount.setter
    def arcount(self, value):
        self._arcount.value = self._arcount._datatype(value)





    # @property
    # def id(self):
    #     return self.__id
    #
    # @id.setter
    # def id(self, value):
    #     self.__id = value


