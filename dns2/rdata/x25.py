from . import Rdata
from dns2 import datatypes
import typing


class X25(Rdata):
    # TODO FIX X.121
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.psdn_name = datatypes.BitData(datatypes.CustomStr, data, str, length_prefix=False)
        elif isinstance(data, dict):
            self.psdn_name = datatypes.BitData(datatypes.CustomStr, data.get('psdn_name'), str, length_prefix=False)


