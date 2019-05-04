from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream

class Px(Rdata):
    pass
    # TODO map822 domain
    # TODO mapx400 domain
    # def __init__(self, data: typing.Union[str, dict]):
    #     if isinstance(data, str):
    #         datastream = ConstBitStream(bin=data)
    #         self.preference = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
    #         self.map822 =
    #         self.mapx400
    #         self.txt_data = datatypes.BitData(datatypes.CustomStr, data, str, length_prefix=True)
    #     elif isinstance(data, dict):
    #         self.txt_data = datatypes.BitData(datatypes.CustomStr, data.get('txt_data'), str, length_prefix=True)
