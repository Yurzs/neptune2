from bitstring import ConstBitStream
import dns2


class Question:
    def __init__(self, message):
        self._injected = False
        self._message = message
        if isinstance(message._data, dict):
            self.parse_dict()
        elif isinstance(message._data, ConstBitStream):
            self.parse_bytes()

    def parse_bytes(self):
        domains = dns2.datatypes.decode_domain(self._message)
        if isinstance(domains, dns2.Domain):
            self._qname = dns2.datatypes.BitData(dns2.DomainName, domains.label, str)
            dns2.Domain(self._message._domains,domains.label, self._message._data.pos)
        else:
            self._qname = dns2.datatypes.BitData(dns2.DomainName, domains[0].label, str)
            for domain in domains:
                dns2.Domain(self._message._domains, domain.label, self._message._data.pos)
        self._qtype = dns2.datatypes.BitData(dns2.datatypes.int16, self._message._data.read('uint:16'), int)
        self._qclass = dns2.datatypes.BitData(dns2.datatypes.int16, self._message._data.read('uint:16'), int)

    def parse_dict(self, **kwargs):
        self._qname = dns2.datatypes.BitData(dns2.DomainName, kwargs.get('label'), str)
        self._qtype = dns2.datatypes.BitData(dns2.datatypes.int16, kwargs.get('qtype'), int)
        self._qclass = dns2.datatypes.BitData(dns2.datatypes.int16, kwargs.get('qclass'), int)


    def push_to_storage(self):
        self._message._bitstorage.push(self)

    def push_binstorage(self):
        self._injected = True
        self._message._bitstorage.bitpush(self._qname)
        self._message._bitstorage.bitpush(self._qclass)
        self._message._bitstorage.bitpush(self._qtype)




    @property
    def qname(self):
        return

    @qname.setter
    def qname(self, value):
        self._qname.value = value

    @property
    def qtype(self):
        return

    @qtype.setter
    def qtype(self, value):
        self._qtype.value = value

    @property
    def qclass(self):
        return

    @qclass.setter
    def qclass(self, value):
        self._qclass.value = value
