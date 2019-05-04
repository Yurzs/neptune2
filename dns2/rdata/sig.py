from . import Rdata
from dns2 import datatypes
from bitstring import ConstBitStream
import typing


class Sig(Rdata):

    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.type_covered = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.algorithm = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.labels = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.original_ttl = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.signature_expiration = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.signature_inception = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.key_tag = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.signers_name = datatypes.BitData(datatypes.DomainName,
                                             datatypes.decode_domain_from_binsting(datastream), str)
            self.signature = datatypes.BitData(datatypes.CustomStr, data[datastream.pos:], str)
        elif isinstance(data, dict):
            self.type_covered = datatypes.BitData(datatypes.int16, data.get('type_covered'), int)
            self.algorithm = datatypes.BitData(datatypes.int8, data.get('algorithm'), int)
            self.labels = datatypes.BitData(datatypes.int8, data.get('labels'), int)
            self.original_ttl = datatypes.BitData(datatypes.int32, data.get('original_ttl'), int)
            self.signature_expiration = datatypes.BitData(datatypes.int32, data.get('signature_expiration'), int)
            self.signature_inception = datatypes.BitData(datatypes.int32, data.get('signature_inception'), int)
            self.key_tag = datatypes.BitData(datatypes.int16, data.get('key_tag'), int)
            self.signers_name = datatypes.BitData(datatypes.DomainName, data.get('signers_name'), str)
            self.signature = datatypes.BitData(datatypes.CustomStr, data.get('signature'), str)
