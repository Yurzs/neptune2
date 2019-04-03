import re

import bitstring


def bin_cutter(data: bitstring.BitArray, counter, octets=2):
    """
    Cuts part of binary string
    :param data: binary string BitArray
    :param octets: number of bytes (8bit) to cut from beginning of string
    :return: BitArray without cut part
    """
    return bitstring.BitArray(bin=data.bin[octets * 8:]), counter + octets


def decode_url(raw_bin_data: bitstring.BitArray, domain_links: dict, bytes_counter: int):
    """
    Decodes url from binary string
    :param raw_bin_data:
    :return:
    """
    url = []
    length_octet = raw_bin_data.bin[0:8]
    if length_octet[0:2] == '11':
        url.append(domain_links[int(raw_bin_data.bin[2:16], base=2)])
        raw_bin_data, bytes_counter = bin_cutter(raw_bin_data, bytes_counter, 2)
        return UrlAddress('.'.join(url)), raw_bin_data, domain_links, bytes_counter
    else:
        raw_bin_data, bytes_counter = bin_cutter(raw_bin_data, bytes_counter, 1)
        domain_start_byte = bytes_counter - 1
    while int(length_octet, base=2):
        suburl = ''.join([chr(int(raw_bin_data.bin[i:i + 8], base=2)) for i in
                          range(0, len(raw_bin_data.bin[0:8 * int(length_octet, base=2)]), 8)])
        url.append(suburl)
        raw_bin_data, bytes_counter = bin_cutter(raw_bin_data, bytes_counter, octets=int(length_octet, base=2))
        length_octet = raw_bin_data.bin[0:8]
        if length_octet[0:2] == '11':
            url.append(domain_links[int(raw_bin_data.bin[2:16], base=2)])
            raw_bin_data, bytes_counter = bin_cutter(raw_bin_data, bytes_counter, 2)
            break
        if not length_octet:
            break
        else:
            raw_bin_data, bytes_counter = bin_cutter(raw_bin_data, bytes_counter, 1)
    urls_for_count = url.copy()
    domain_links[domain_start_byte] = '.'.join(url)
    for n, domain in enumerate(urls_for_count):
        if '.'.join(url[n + 1:]) not in domain_links.values():
            if not [item for item in domain_links if item == '.'.join(url[n + 1:])]:
                domain_links[domain_start_byte + len(domain) + 1] = '.'.join(url[n + 1:])
        domain_start_byte = domain_start_byte + len(domain) + 1
    return UrlAddress('.'.join(url)), raw_bin_data, domain_links, bytes_counter


class int1(int):
    """
    Subclass of int with binary length of 1 bit
    """
    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(1)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:1], byteorder='big'), byte_data[1:], byte_counter + 1, domain_links

    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(1)


class int2(int):
    """
    Subclass of int with binary length of 2 bits
    """
    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(2)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:2], byteorder='big'), byte_data[2:], byte_counter + 2, domain_links


class int3(int):
    """
    Subclass of int with binary length of 3 bits
    """
    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(3)

    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(3)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:3], byteorder='big'), byte_data[3:], byte_counter + 3, domain_links

class int4(int):
    """
    Subclass of int with binary length of 4 bits
    """
    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(4)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:4], byteorder='big'), byte_data[4:], byte_counter + 4, domain_links

    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(4)


class int8(int):
    """
    Subclass of int with binary length of 8 bits
    """
    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(8)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:8], byteorder='big'), byte_data[8:], byte_counter + 32, domain_links

    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(8)

class int14(int):
    """
    Subclass of int with binary length of 14 bits
    """
    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(14)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:14], byteorder='big'), byte_data[14:], byte_counter + 14, domain_links

    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(14)

class int16(int):
    """
    Subclass of int with binary length of 16 bits
    """
    @property
    def binary(self):
        return str(bin(self)[2:]).zfill(16)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     print(f'int16 {cls(byte_data.bin[:16], base=2)}')
    #     return cls(byte_data.bin[:16], base=2), byte_data[16:], byte_counter + 16, domain_links
    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(16)


class int32(int):
    """
    Subclass of int with binary length of 32 bits
    """

    @property
    def binary(self) -> str:
        return str(bin(self)[2:]).zfill(32)

    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(32)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:32], byteorder='big'), byte_data[32:], byte_counter + 32, domain_links

class int128(int):
    """
    Subclass of int with binary length of 128 bit
    """
    @property
    def binary(self) -> str:
        return str(bin(self)[2:]).zfill(128)

    # @classmethod
    # def decode(cls, byte_data, byte_counter, domain_links):
    #     return cls.from_bytes(byte_data[:128], byteorder='big'), byte_data[128:], byte_counter + 128, domain_links

    # def __str__(self):
    #     return str(bin(self)[2:]).zfill(128)


class local_str_without_prefix(str):
    """
    ASCII string without leading length prefix
    """
    @property
    def binary(self):
        return ''.join([str(bin(ord(char))[2:]).zfill(8) for char in self])

    @classmethod
    def decode(cls, byte_data, *args, **kwargs):
        result_str = ''
        for byte in byte_data.bytes:
            result_str += chr(byte)
        return cls(result_str), bitstring.BitArray(), kwargs.get('byte_counter', 0) + len(byte_data), kwargs.get('domain_links', {})



class local_str(str):
    """
    ASCII string WITH leading length prefix
    """
    # def __init__(self):
    #     if isinstance(self, bitstring.BitArray):
    #         result = self[self[0:8]]
    #         super(local_str).__init__(result)
    #     else:
    #         super().__init__()

    @property
    def binary(self):
        return str(bin(len([str(bin(ord(char))[2:]).zfill(8) for char in self]))[2:]).zfill(8) + \
               ''.join([str(bin(ord(char))[2:]).zfill(8) for char in self])

    @classmethod
    def decode(cls, byte_data, *args, **kwargs):
        length = int.from_bytes(byte_data[0:8], byteorder='big')
        result_str = ''
        for char in byte_data[8:length]:
            result_str += chr(char)
        return cls(result_str), byte_data[8 + length:], kwargs.get('byte_counter', 0) + length, kwargs.get('domain_links', {})


class IpAddress(str):
    """
    ASCII string of IPv4 address without separation
    """
    @property
    def binary(self):
        return ''.join([str(bin(int(item))[2:]).zfill(8) for item in self.split('.')])

    @classmethod
    def decode(cls, byte_data, *args, **kwargs):
        bin_ip = byte_data.bin[0:32]
        result = '.'.join([str(int(bin_ip[i:i + 8], base=2)) for i in range(0, len(bin_ip), 8)])
        return cls(result), byte_data[4:], kwargs.get('byte_counter', 0) + 4, kwargs.get('domain_links', {})


class Ip6Address(str):
    """
    ASCII string of IPv6 address without separation
    """
    @property
    def binary(self):
        result = ''
        if re.findall('::', self):
            length = len(self.split(':')) - 1
            self = self.replace('::', ':0' * (8 - length) + ':')
        for i in self.split(':'):
            if len(i) == 0:
                result += int16('0').binary
            else:
                result += int16(i, base=16).binary
        return result

    @classmethod
    def decode(cls, byte_data, *args, **kwargs):
        import ipaddress
        return cls(ipaddress.IPv6Address(int(byte_data[0:128].bin, base=2))), byte_data[16:], kwargs.get('byte_counter',
                                                                                                         0) + 16, kwargs.get(
            'domain_links', {})


class UrlAddress(str):
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

    @classmethod
    def decode(cls, byte_data, domain_links, byte_counter):
        url, raw_bin_data, domain_links, byte_counter = decode_url(raw_bin_data=byte_data,
                                                                   domain_links=domain_links,
                                                                   bytes_counter=byte_counter)
        return cls(url), raw_bin_data, byte_counter, domain_links


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
