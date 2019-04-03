import hashlib
# import pyopenssl
import base64
import dns
from dns import datatypes
import math
import Crypto
import bitstring

def rsa2dnskey(key):
    octets = b''
    explen = int(math.ceil(math.log(key.e, 2) / 8))
    if explen > 255:
        octets = b"\x00"
    octets += Crypto.Util.number.long_to_bytes(explen) + \
              Crypto.Util.number.long_to_bytes(key.e) + \
              Crypto.Util.number.long_to_bytes(key.n)
    return octets


class RSAMD5:
    def __init__(self, data):
        pass

class DH:
    pass

class DSA:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def new(cls, keysize):
        from Crypto.PublicKey import DSA
        key = DSA.generate(bits=keysize)
        return cls(public_key=key.publickey(), private_key=key)

class ECC:
    pass


class RSASHA1:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def new(cls, keysize):
        from Crypto.PublicKey import RSA
        return cls(key=RSA.generate(keysize))

    @classmethod
    def key_import(cls, key, **kwargs):
        from Crypto.PublicKey import RSA
        return cls(key=RSA.importKey(key))

    @property
    def rdata_public_key(self):
        key = getattr(self, 'key')
        exponent_length = len(format(key.e, 'b'))
        if 255 >= key.e > 1:
            exponent_length = format(exponent_length, 'b').zfill(8)
        else:
            exponent_length = format(0, 'b').zfill(8) + format(exponent_length, 'b').zfill(16)
        exponent = format(key.e, 'b').zfill(8 * math.ceil(len(format(key.e, 'b'))/8))
        modulus = format(key.n, 'b').zfill(8 * math.ceil(len(format(key.n, 'b'))/8))
        return base64.b64encode(bitstring.BitArray(bin=exponent_length + exponent + modulus).bytes).decode('ascii')



class DSA_NSEC3_SHA1:
    pass

class RSASHA1_NSEC3_SHA1:
    pass

class RSASHA256:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def new(cls, keysize):
        from Crypto.PublicKey import RSA
        return cls(key=RSA.generate(keysize))

    @classmethod
    def key_import(cls, key):
        from Crypto.PublicKey import RSA
        return cls(key=RSA.importKey(key))

    @property
    def rdata_public_key(self):
        key = getattr(self, 'key')
        exponent_length = len(format(key.e, 'b'))
        if 255 >= key.e > 1:
            exponent_length = format(exponent_length, 'b').zfill(8)
        else:
            exponent_length = format(0, 'b').zfill(8) + format(exponent_length, 'b').zfill(16)
        exponent = format(key.e, 'b').zfill(8 * math.ceil(len(format(key.e, 'b')) / 8))
        modulus = format(key.n, 'b').zfill(8 * math.ceil(len(format(key.n, 'b')) / 8))
        return base64.b64encode(bitstring.BitArray(bin=exponent_length + exponent + modulus).bytes).decode('ascii')

    def sign(self, rrsig_rdata_without_signature, rrset):
        from Crypto.Hash import SHA256
        from Crypto.Signature import PKCS1_v1_5
        from Crypto.PublicKey import RSA
        key = RSA.import_key(self.key)
        for item in rrset:
            rrsig_rdata_without_signature += item.encode()
        h = SHA256.new(rrsig_rdata_without_signature)
        signature = PKCS1_v1_5.new(key).sign(h)
        return base64.b64encode(signature).decode('ascii')




class RSASHA512:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def new(cls, keysize):
        from Crypto.PublicKey import RSA
        return cls(key=RSA.generate(keysize))

    @classmethod
    def key_import(cls, key):
        from Crypto.PublicKey import RSA
        return cls(key=RSA.importKey(key))

    @property
    def rdata_public_key(self):
        key = getattr(self, 'key')
        exponent_length = len(format(key.e, 'b')) / 8
        if 255 >= key.e > 1:
            exponent_length = format(exponent_length, 'b').zfill(8)
        else:
            exponent_length = format(0, 'b').zfill(8) + format(math.ceil(len(format(key.e, 'b')) / 8), 'b').zfill(16)
        exponent = format(key.e, 'b').zfill(8 * math.ceil(len(format(key.e, 'b')) / 8))
        modulus = format(key.n, 'b').zfill(8 * math.ceil(len(format(key.n, 'b')) / 8))
        # encoded = base64.b64encode(bitstring.BitArray(bin=exponent_length + exponent + modulus).bytes).decode('ascii')
        # decoded = bitstring.BitArray(bytes=base64.b64decode(encoded)).bin
        # if int(decoded[0:8], base=2) == 0:
        #     expl = int(decoded[8:24], base=2)
        #     exp = int(decoded[24:24 + expl*8], base=2)
        #     print(f'{expl}, {exp}, {int(decoded[24 + expl*8:], base=2)}')
        #     pub_key = RSA.construct((int(decoded[24 + expl*8:], base=2), exp))
        # else:
        #     expl = int.from_bytes(decoded[0], byteorder='big')
        #     exp = int.from_bytes(decoded[1:1+int(expl)], byteorder='big')
        #     print(f'{expl}, {exp}, {int.from_bytes(decoded[1+expl:], byteorder="big")}')
        #     pub_key = RSA.construct((int.from_bytes(decoded[1+expl:], byteorder='big'), exp))
        # print(pub_key.size_in_bits())
        return base64.b64encode(bitstring.BitArray(bin=exponent_length + exponent + modulus).bytes).decode('ascii')

    def sign(self, rrsig_rdata_without_signature, rrset):
        from Crypto.Hash import SHA512
        from Crypto.Signature import PKCS1_v1_5
        import models
        result_binstring = rrsig_rdata_without_signature
        for item in rrset:
            if isinstance(item, models.Domain):
                result_item, a, b, c = dns.rdata.TYPES[6].decode(0, {}, dictionary=item.dictionary['rdata'])
            elif isinstance(item, models.Rrsig):
                continue
            else:
                result_item, a, b, c = dns.rdata.TYPES[item.type].decode(0, {}, dictionary=item.dictionary['rdata'])
            result_binstring += result_item.encode().bin
        h = SHA512.new(bitstring.BitArray(bin=result_binstring).bytes)
        signature = PKCS1_v1_5.new(self.key).sign(h)
        return base64.b64encode(signature).decode('ascii')

class DIGEST_SHA1:
    def __init__(self, *args, **kwargs):
        dnskey = kwargs.get('dnskey')
        rdata = dnskey.dictionary['rdata']
        local_rdata = datatypes.UrlAddress(dnskey.domain.full_name).binary
        for key, value in dns.rdata.DNSKEY.name_datatype.items():
            local_rdata += value(rdata[key]).binary
        self.hexdigest = hashlib.sha1(local_rdata.encode('ascii')).hexdigest()

    @classmethod
    def encode(cls, dnskey):
        return cls(dnskey=dnskey)

    def __str__(self):
        return self.hexdigest


class DIGEST_SHA256:
    def __init__(self, *args, **kwargs):
        dnskey = kwargs.get('dnskey')
        rdata = dnskey.dictionary['rdata']
        local_rdata = datatypes.UrlAddress(dnskey.domain.full_name).binary
        key_rdata = dns.rdata.DNSKEY.decode(dictionary=dnskey.dictionary['rdata'], domain_links={}, byte_counter=0)[0]
        result = bitstring.BitArray(bin=datatypes.UrlAddress(dnskey.domain.full_name).binary).bytes + key_rdata.encode().bytes
        self.hexdigest = hashlib.sha256(result).hexdigest()

    @classmethod
    def encode(cls, dnskey):
        return cls(dnskey=dnskey)

    def __str__(self):
        return self.hexdigest


class DIGEST_SHA384:
    def __init__(self, *args, **kwargs):
        dnskey = kwargs.get('dnskey')
        rdata = dnskey.dictionary['rdata']
        local_rdata = datatypes.UrlAddress(dnskey.domain.full_name).binary
        for key, value in dns.rdata.DNSKEY.name_datatype.items():
            local_rdata += value(rdata[key]).binary
        self.hexdigest = hashlib.sha384(local_rdata.encode('ascii')).hexdigest()

    @classmethod
    def encode(cls, dnskey):
        return cls(dnskey=dnskey)

    def __str__(self):
        return self.hexdigest

class ECC_GOST:
    pass

class ECDSAP256SHA256:
    pass

class ECDSAP384SHA384:
    pass

class ED25519:
    pass

class ED448:
    pass

class INDIRECT:
    pass

class PRIVATEDNS:
    pass

class PRIVATEOID:
    pass

size = {
    1024: 1024,
    2048: 2048,
    4096: 4096
}

dnssec_algorithm_type = {
    1: RSAMD5,
    2: DH,
    3: DSA,
    4: ECC,
    5: RSASHA1,
    6: DSA_NSEC3_SHA1,
    7: RSASHA1_NSEC3_SHA1,
    8: RSASHA256,
    10: RSASHA512,
    12: ECC_GOST,
    13: ECDSAP256SHA256,
    14: ECDSAP384SHA384,
    15: ED25519,
    16: ED448,
    252: INDIRECT,
    253: PRIVATEDNS,
    254: PRIVATEOID,
}

dnssec_digest_type = {
    1: DIGEST_SHA1,
    2: DIGEST_SHA256,
    4: DIGEST_SHA384,
}

