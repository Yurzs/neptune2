from . import Rdata
from dns2 import datatypes
import typing


class Txt(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.txt_data = datatypes.BitData(datatypes.CustomStr, data, str, length_prefix=True)
        elif isinstance(data, dict):
            self.txt_data = datatypes.BitData(datatypes.CustomStr, data.get('txt_data'), str, length_prefix=True)

