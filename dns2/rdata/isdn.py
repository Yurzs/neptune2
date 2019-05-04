from . import Rdata
from dns2 import datatypes
import typing


class Isdn(Rdata):
    # TODO https://tools.ietf.org/html/rfc1183#section-3.2
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.isdn_address = datatypes.BitData(

            )
            self.sa = datatypes.BitData()
        elif isinstance(data, dict):
            self.isdn_address = datatypes.BitData(

            )
            self.sa = datatypes.BitData()

