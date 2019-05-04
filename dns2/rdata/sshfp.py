from . import Rdata
from dns2 import datatypes
import typing


class Sshfp(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.algorithm = datatypes.BitData(datatypes.int8, data[0:8], int)
            self.fp_type = datatypes.BitData(datatypes.int8, data[8:16], int)
            self.fingerprint = datatypes.BitData(datatypes.CustomStr, data[16:], str, length_prefix=False)
        elif isinstance(data, dict):
            self.algorithm = datatypes.BitData(datatypes.int8, data.get('algorithm'), int)
            self.fp_type = datatypes.BitData(datatypes.int8, data.get('fp_type'), int)
            self.fingerprint = datatypes.BitData(datatypes.CustomStr, data.get('fingerprint'), str, length_prefix=False)


