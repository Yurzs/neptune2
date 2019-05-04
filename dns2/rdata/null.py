from . import Rdata
from dns2 import datatypes
import typing


class Null(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.anything = datatypes.BitData(datatypes.CustomStr, data, str, length_prefix=False)
        elif isinstance(data, dict):
            self.anything = datatypes.BitData(datatypes.CustomStr, data.get('anything'), str, length_prefix=False)
