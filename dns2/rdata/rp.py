from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream

class Rp(Rdata):
    """
    Responsible person RR

    RP has the following format:

    <owner> <ttl> <class> RP <mbox-dname> <txt-dname>

    Both RDATA fields are required in all RP RRs.

    https://tools.ietf.org/html/rfc1183#section-2.2
    """

    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.mbox_dname = datatypes.BitData(datatypes.DomainName,
                                                datatypes.decode_domain_from_binsting(datastream), str)
            self.txt_dname = datatypes.BitData(datatypes.DomainName,
                                                datatypes.decode_domain_from_binsting(datastream), str)
        elif isinstance(data, dict):
            self.mbox_dname = datatypes.BitData(datatypes.DomainName,
                                                data.get('mbox_dname'), str)
            self.txt_dname = datatypes.BitData(datatypes.DomainName,
                                               data.get('txt_dname'), str)


