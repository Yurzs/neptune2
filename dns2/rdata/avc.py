from . import Rdata
from dns2 import datatypes
import typing


class Avc(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.option_value = datatypes.BitData(datatypes.CustomStr, data, str, length_prefix=True)
        elif isinstance(data, dict):
            self.option_value = datatypes.BitData(datatypes.CustomStr, data.get('option_value'), str, length_prefix=True)
