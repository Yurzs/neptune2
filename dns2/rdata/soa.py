from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream, BitArray


class Soa(Rdata):

    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.mname = datatypes.BitData(datatypes.DomainName,
                                           datatypes.decode_domain_from_binsting(datastream), str)
            self.rname = datatypes.BitData(datatypes.DomainName,
                                           datatypes.decode_domain_from_binsting(datastream), str)
            self.serial = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.refresh = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.retry = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.expire = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.minimum = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
        elif isinstance(data, dict):
            self.mname = datatypes.BitData(datatypes.DomainName,
                                           data.get('mname'), str)
            self.rname = datatypes.BitData(datatypes.DomainName,
                                           data.get('rname'), str)
            self.serial = datatypes.BitData(datatypes.int32, data.get('serial'), int)
            self.refresh = datatypes.BitData(datatypes.int32, data.get('refresh'), int)
            self.retry = datatypes.BitData(datatypes.int32, data.get('retry'), int)
            self.expire = datatypes.BitData(datatypes.int32, data.get('expire'), int)
            self.minimum = datatypes.BitData(datatypes.int32, data.get('minimum'), int)
