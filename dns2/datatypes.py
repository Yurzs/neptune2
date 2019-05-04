import re
import typing

import bitstring
from bitstring import BitArray
from functools import reduce
import dns2


class BitStorage:
    _bitstorage = []
    _itemstorage = []

    def __init__(self, msg):
        self._storage = []
        self._message = msg
        self._bitstorage = []

    def push(self, item: typing.Union['Header', 'Question', 'Answer', 'EDNS'] = None):
        if isinstance(item, dns2.Header) \
            or isinstance(item, dns2.Question) \
            or isinstance(item, dns2.Answer) \
            or isinstance(item, dns2.EDNS) and not item in self._itemstorage:
                self._itemstorage.append(item)

    def bitpush(self, bitdata: 'BitData'):
        self._bitstorage.append(bitdata)

    def cut(self, pos_start: int, pos_end: int):
        pass

    def replace(self, pos_start: int, pos_end: int, new_bits: 'BitData'):
        pass

    def to_bytes(self) -> BitArray:
        for item in self._itemstorage:
            if not item._injected:
                item.push_binstorage()
        binstring = ''
        for x in self._bitstorage:
            if isinstance(x, dns2.EDNS.OptionStorage):
                binstring += x.binary
            # RDATA shouldn't be compressed!
            # elif issubclass(x.value.__class__, dns2.Rdata):
            #     for item in x.value.binary_instructions:
            #         if isinstance(item.value, DomainName):
            #             binstring += dns2.Domain(self._message._domains, item.value, len(binstring),
            #                                      shortening_allowed=getattr(item, 'shortening_allowed', True)).binary
            #         else:
            #             binstring += item.binary
            elif isinstance(x.value, DomainName):
                binstring += dns2.Domain(self._message._domains, x.value, len(binstring),
                                         shortening_allowed=getattr(x, 'shortening_allowed', True)).binary
            else:
                binstring += x.binary
        # print(self._message._domains.storage)
        return BitArray(bin=binstring)


class BitData:

    def __init__(self, datatype, value, repr_type, to_bin_func=lambda x: x.value.binary, **kwargs):
        self._to_bin_func = to_bin_func
        self._raw_value = value
        self._datatype = datatype
        if issubclass(datatype, CustomInt):
            self.value = datatype(value)
        elif issubclass(datatype, CustomStr):
            self.value = datatype(value=value, **kwargs)
        elif issubclass(datatype, dns2.Rdata):
            self.value = datatype(value)
        else:
            self.value = datatype(value)
        self._repr_type = repr_type
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return str(self._repr_type(self.value))

    def __len__(self):
        return len(str(self._raw_value))

    def __int__(self):
        if issubclass(self._datatype, CustomInt):
            return self.value
        else:
            raise TypeError

    @property
    def binary(self):
        # print(self._to_bin_func(self))
        return self._to_bin_func(self)

    # def __int__(self):
    #     return int(self.value)


def bin_cutter2(data: bitstring.BitArray, octets=2):
    data = bitstring.BitArray(bin=data.bin[octets * 8:])
    return data


def bin_cutter(data: bitstring.BitArray, counter, octets=2):
    """
    Cuts part of binary string
    :param data: binary string BitArray
    :param octets: number of bytes (8bit) to cut from beginning of string
    :return: BitArray without cut part
    """
    return bitstring.BitArray(bin=data.bin[octets * 8:]), counter + octets


def decode_domain_from_binsting(binstring: bitstring.ConstBitStream) -> str:
    domain = ''
    length_octet = binstring.read('uint:8')
    while length_octet > 0:
        for x in range(length_octet):
            domain += chr(binstring.read('uint:8'))
        length_octet = binstring.peek('uint:8')
        if length_octet:
            domain += '.'
    return domain

def decode_domain(message: 'Message') -> list:
    """
    Decodes domain name from message data flow
    :param message:
    :return: list of Domain
    """
    domain = []
    if message._data.peek('bin:8')[0:2] == '11':
        found_in_storage = message._domainstorage.search(message._data.read('bin:16')[2:])
        if found_in_storage:
            return found_in_storage
    else:
        while message._data.peek('int:8'):
            subdomain = ''
            position = message._data.pos
            for c in range(message._data.read('int:8')):
                subdomain += chr(message._data.read('int:8'))
            domain.append((subdomain, position))
            if message._data.peek('bin:8')[0:2] == '11':
                found_in_storage = message._domainstorage.search(message._data.read('bin:16')[2:])
                if found_in_storage:
                    domain.append((found_in_storage.label, message._data.pos - 16))
                break
            if not message._data.peek('uint:8'):
                break
    domains = []
    message._data.read('bin:8')  # last 00000000 of length octet
    for n, (label, pos) in enumerate(domain):
        domains.append(dns2.Domain(message._domains,
                                   '.'.join([x for m, (x, y) in enumerate(domain) if m >= n]), pos))
    return domains
    # for n, domain in enumerate(urls_for_count):
    #     if '.'.join(url[n + 1:]) not in domain_links.values():
    #         if not [item for item in domain_links if item == '.'.join(url[n + 1:])]:
    #             domain_links[domain_start_byte + len(domain) + 1] = '.'.join(url[n + 1:])
    #     domain_start_byte = domain_start_byte + len(domain) + 1
    # return UrlAddress('.'.join(url)), raw_bin_data, domain_links, bytes_counter


class CustomInt(int):

    @classmethod
    def from_bits(cls, bits):
        return cls(bits, base=2)

    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(int(re.search('\d+', self.__class__.__name__).group(0)))


class int1(CustomInt):
    pass

class int2(CustomInt):
    pass

class int3(CustomInt):
    pass

class int4(CustomInt):
    pass

class int8(CustomInt):
    pass

class int14(CustomInt):
    pass

class int16(CustomInt):
    pass

class int32(CustomInt):
    pass

class int48(CustomInt):
    pass

class int128(CustomInt):
    pass


class CustomStr:
    type = str

    def __init__(self, value: str, length_prefix: bool = True):
        value = str(value)
        self.prefix = length_prefix
        self.value = ''
        if value == '':
            pass
        elif min(value) == '0' and max(value) == '1':
            if self.prefix:
                prf_length = int(value[:8], 2)
                value = value[8:]
                for x in range(0, prf_length - 1):
                    self.value += chr(int(value[x*8:(x+1)*8], 2))
            elif self.prefix is False:
                self.value = ''.join([value[n:n+8] for n in range(0, len(value), 8)])
        elif isinstance(value, str):
            self.value = value

    @property
    def binary(self):
        if self.prefix is True:
            string = ''.join(map(lambda x: bin(ord(x))[2:].zfill(8), self.value))
            return bin(int(len(string) / 8))[2:].zfill(8) + string
        elif self.prefix is False:
            return ''.join(map(lambda x: bin(ord(x))[2:].zfill(8), self.value))

    @classmethod
    def read_prefixed(cls, binstring: bitstring.ConstBitStream):
        string = ''
        for cint in range(binstring.read('uint:8')):
            string += chr(cint)
        return cls(string)
            

class X121:
    pass


class ReversePointer:
    def __init__(self, value):
        self.value = value

    @property
    def IpAddress(self):
        from ipaddress import IPv4Address, IPv6Address
        if len(self.value.split('.')) > 6:
            return IPv6Address('.'.join(reversed(self.value.split('.')[:-2])))
        else:
            return IPv4Address('.'.join(reversed(self.value.split('.')[:-2])))

class Map822:
    # TODO
    pass

class MapX400:
    # TODO
    pass

class BitMap:
    def __init__(self, value):
        self.value = value

    @property
    def binary(self):
        return self.value

    # @property
    # def binary(self):
    #     binstring = ''
    #     for
# class local_str_without_prefix(str):
#     """
#     ASCII string without leading length prefix
#     """
#
#     @property
#     def binary(self):
#         return ''.join([str(bin(ord(char))[2:]).zfill(8) for char in self])
#
#     @classmethod
#     def decode(cls, byte_data, *args, **kwargs):
#         result_str = ''
#         for byte in byte_data.bytes:
#             result_str += chr(byte)
#         return cls(result_str), bitstring.BitArray(), kwargs.get('byte_counter', 0) + len(byte_data), kwargs.get(
#             'domain_links', {})


# class local_str(str):
#     """
#     ASCII string WITH leading length prefix
#     """
#
#     # def __init__(self):
#     #     if isinstance(self, bitstring.BitArray):
#     #         result = self[self[0:8]]
#     #         super(local_str).__init__(result)
#     #     else:
#     #         super().__init__()
#
#     @property
#     def binary(self):
#         return str(bin(len([str(bin(ord(char))[2:]).zfill(8) for char in self]))[2:]).zfill(8) + \
#                ''.join([str(bin(ord(char))[2:]).zfill(8) for char in self])
#
#     @classmethod
#     def decode(cls, byte_data, *args, **kwargs):
#         length = int.from_bytes(byte_data[0:8], byteorder='big')
#         result_str = ''
#         for char in byte_data[8:length]:
#             result_str += chr(char)
#         return cls(result_str), byte_data[8 + length:], kwargs.get('byte_counter', 0) + length, kwargs.get(
#             'domain_links', {})


# class IpAddress(str):
#     """
#     ASCII string of IPv4 address without separation
#     """
#
#     @property
#     def binary(self):
#         return ''.join([str(bin(int(item))[2:]).zfill(8) for item in self.split('.')])
#
#     @classmethod
#     def decode(cls, byte_data, *args, **kwargs):
#         bin_ip = byte_data.bin[0:32]
#         result = '.'.join([str(int(bin_ip[i:i + 8], base=2)) for i in range(0, len(bin_ip), 8)])
#         return cls(result), byte_data[4:], kwargs.get('byte_counter', 0) + 4, kwargs.get('domain_links', {})


# class Ip6Address(str):
#     """
#     ASCII string of IPv6 address without separation
#     """
#
#     @property
#     def binary(self):
#         result = ''
#         if re.findall('::', self):
#             length = len(self.split(':')) - 1
#             self = self.replace('::', ':0' * (8 - length) + ':')
#         for i in self.split(':'):
#             if len(i) == 0:
#                 result += int16('0').binary
#             else:
#                 result += int16(i, base=16).binary
#         return result
#
#     @classmethod
#     def decode(cls, byte_data, *args, **kwargs):
#         import ipaddress
#         return cls(ipaddress.IPv6Address(int(byte_data[0:128].bin, base=2))), byte_data[16:], kwargs.get('byte_counter',
#                                                                                                          0) + 16, kwargs.get(
#             'domain_links', {})


class DomainName(str):
    """
    ASCII string representing domain name split by length octets
    """

    @property
    def binary(self):
        if self == '':
            return str('').zfill(8)
        binary_string = ''
        parts = self.split('.')
        for urlpart in parts:
            binary_string += str(bin(len(urlpart))[2:]).zfill(8)
            for char in urlpart:
                binary_string += str(bin(ord(char))[2:]).zfill(8)
        binary_string += str(bin(0)[2:]).zfill(8)
        return binary_string

    def binary_with_pos(self, urls_dict, octet_counter):
        """

        :param urls_dict:
        :param octet_counter:
        :return:
        """
        binary_string = ''
        parts = self.split('.')
        prev = ''
        if urls_dict:
            for n in range(len(parts)):
                if '.'.join(parts[n:len(parts)]) in urls_dict:
                    prev = '.'.join(parts[n:len(parts)])
                    break
            if prev == self:
                binary_string += '11' + str(bin(int(urls_dict[prev]))[2:]).zfill(16 - 2)
                octet_counter += 2
                return binary_string, urls_dict, octet_counter
            else:
                parts = self.replace(prev, '')[:-1].split('.')
        for n, urlpart in enumerate(parts):
            if prev:
                if not prev + '.' + '.'.join(parts[n:len(parts)]) in urls_dict:
                    binary_string += str(bin(len(urlpart))[2:]).zfill(8)
                    octet_counter += 1
                    for char in urlpart:
                        binary_string += str(bin(ord(char))[2:]).zfill(8)
                        octet_counter += 1
                    break
            else:
                urls_dict.update({'.'.join(parts[n:len(parts)]): int(octet_counter)})
            binary_string += str(bin(len(urlpart))[2:]).zfill(8)
            octet_counter += 1
            for char in urlpart:
                binary_string += str(bin(ord(char))[2:]).zfill(8)
                octet_counter += 1
        if prev:
            binary_string += '11' + str(bin(int(urls_dict[prev]))[2:]).zfill(16 - 2)
            octet_counter += 2
            return binary_string, urls_dict, octet_counter
        binary_string += str(bin(0)[2:]).zfill(8)
        octet_counter += 1
        return binary_string, urls_dict, octet_counter

    # @classmethod
    # def decode(cls, byte_data, domain_links, byte_counter):
    #     url, raw_bin_data, domain_links, byte_counter = decode_url(raw_bin_data=byte_data,
    #                                                                domain_links=domain_links,
    #                                                                bytes_counter=byte_counter)
    #     return cls(url), raw_bin_data, byte_counter, domain_links

# class bytestring(str):
#
#     @property
#     def binary(self):
#         import bitstring
#         return bitstring.BitArray(bytes=self).bin
#
#
# class DomainName:
#     length_octet = ''
#     label = ''
#
#     @classmethod
#     def decode(self, byte_data, domain_links, byte_counter):
#         pass
#
#
# class PublicKey:
#     def __init__(self, value):
#         self.value = value
#
#     def __str__(self):
#         return self.value
#
#     @classmethod
#     def decode(self, byte_data, domain_links, byte_counter):
#         pass
#
#
# class DnsKeyFlags:
#     def __init__(self, *args, **kwargs):
#         self.key_id = kwargs.get('key_id')
#         self.sep = kwargs.get('sep')
#
#     @classmethod
#     def decode(cls, key_id, sep):
#         return cls(key_id=key_id, sep=sep)
