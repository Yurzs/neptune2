import random

from dns import datatypes
import dns
import bitstring


class EDNS:
    def __init__(self, OPT=None):
        if OPT:
            self.on = True
            self.udp_payload_size = OPT.aclass
            self.extended_rcode = OPT.extended_rcode
            self.version = OPT.version
            self.dnssec_ok = OPT.do
            self.z = OPT.z
            self.OPT = OPT
        else:
            self.on = False

    def to_opt(self):
        opt, a, b, c = dns.message_section.Additional.decode(dictionary={
            'name': '',
            'atype': 41,
            'aclass': self.udp_payload_size,
            'extended_rcode': self.extended_rcode,
            'version': self.version,
            'do': self.dnssec_ok,
            'z': self.z,
            'rdlength': 0,
            'rdata': {},
        }, byte_counter=0, domain_links={})
        return opt

    def inject(self, message):
        if self.on:
            additional = getattr(message, 'additional', {})
            if additional:
                additional[max(additional.keys()) + 1] = message.edns.to_opt()
            else:
                setattr(message, 'additional', {
                    0: message.edns.to_opt()
                })
        return message




class Message:
    def __init__(self, *args, **kwargs):
        """
        ACCEPTED TYPES ONLY:
        DICTIONARY WITHOUT OBJECTS (JSON-like)
        BYTES
        :param args:
        :param kwargs:
        """
        self.byte_counter = 0
        self.domain_links = {}
        if kwargs.get('dictionary'):
            # TODO?
            pass
        elif kwargs.get('byte_data'):
            data = kwargs.get('byte_data')
            self.header, data, self.byte_counter, self.domain_links = dns.message_section.Header.decode(
                byte_data=data, domain_links=self.domain_links, byte_counter=self.byte_counter)
            self.check_message_status()
            # print(f'trying to import {self.header.__dict__}')
            if self.header.qdcount > 1:
                self.header.qdcount = datatypes.int16(0)
            if self.header.arcount > 50:
                self.header.arcount = datatypes.int16(0)
            if self.header.qdcount:
                data = self.parse_to_attr('question', self.header.qdcount, data)
            if self.header.ancount:
                data = self.parse_to_attr('answer', self.header.ancount, data)
            if self.header.nscount:
                data = self.parse_to_attr('authority', self.header.nscount, data)
            if self.header.arcount:
                data = self.parse_to_attr('additional', self.header.arcount, data)
            self.set_edns()


    def set_edns(self):
        self.edns = EDNS()
        for key, additional in getattr(self, 'additional', {}).copy().items():
            # print(additional, additional.__dict__)
            if additional.atype == 41:
                self.edns = EDNS(additional)
                self.additional.pop(key)
                break

    def check_message_status(self):
        if self.header.opcode == 2:
            self.header.qdcount = datatypes.int16(0)
            self.header.ancount = datatypes.int16(0)
            self.header.nscount = datatypes.int16(0)
            self.header.arcount = datatypes.int16(0)

    def parse_to_attr(self, attr, counter, data):
        setattr(self, attr, {})
        for resource_recordN in range(counter):
            getattr(self, attr)[
                resource_recordN], data, self.byte_counter, self.domain_links = getattr(dns.message_section,
                                                                                        attr.title()).decode(
                byte_data=data, domain_links=self.domain_links, byte_counter=self.byte_counter
            )
        return data

    def order_for_bin(self):
        result_dict = {}
        for item in ['header', 'question', 'answer', 'authority', 'additional']:
            for selfitem in self.__dict__:
                if selfitem == item:
                    result_dict[item] = getattr(self, selfitem)
        return result_dict

    def encode(self):
        BINARY = ''
        dict_for_bin = self.order_for_bin()
        for item in dict_for_bin:
            if item in ['question', 'answer', 'authority', 'additional']:
                for subitem in dict_for_bin[item]:
                    BINARY += dict_for_bin[item][subitem].encode().bin
            else:
                BINARY += dict_for_bin[item].encode().bin
        return BINARY

    def add_to_attr(self, attr_type, data):
        attr = getattr(self, attr_type, None)
        if not attr:
            setattr(self, attr_type, {})
            n = -1
        else:
            n = max(attr.keys())
        if not isinstance(data, dict):
            data = data.dictionary
        getattr(self, attr_type)[
            n + 1], data, self.byte_counter, self.domain_links = getattr(dns.message_section,
                                                                         attr_type.title()).decode(
            dictionary=data,
            domain_links=self.domain_links,
            byte_counter=self.byte_counter)

    def add(self, data_dict):
        if data_dict.get('header', None):
            self.header, data, self.byte_counter, self.domain_links = dns.message_section.Header.decode(
                dictionary=data_dict['header'], domain_links={}, byte_counter=0)
        for question in data_dict.get('question', []):
            self.add_to_attr('question', question)
        for answer in data_dict.get('answer', []):
            self.add_to_attr('answer', answer)
        for authority in data_dict.get('authority', []):
            self.add_to_attr('authority', authority)
        for additional in data_dict.get('additional', []):
            self.add_to_attr('additional', additional)
        if getattr(self, 'answer', None):
            self.header.qr = datatypes.int1(1)
        try:
            self.header.qdcount = datatypes.int16(len(self.question.keys()))
        except AttributeError:
            self.header.qdcount = datatypes.int16(0)
        try:
            self.header.ancount = datatypes.int16(len(self.answer.keys()))
        except AttributeError:
            self.header.ancount = datatypes.int16(0)
            self.header.rcode = datatypes.int4(3)
        try:
            self.header.nscount = datatypes.int16(len(self.authority.keys()))
        except AttributeError:
            self.header.nscount = datatypes.int16(0)
        try:
            self.header.arcount = datatypes.int16(len(self.additional.keys()))
        except AttributeError:
            self.header.arcount = datatypes.int16(0)

    def self_check(self):
        self.header.qr = datatypes.int1(1)
        try:
            self.header.qdcount = datatypes.int16(len(self.question.keys()))
        except AttributeError:
            self.header.qdcount = datatypes.int16(0)
        try:
            self.header.ancount = datatypes.int16(len(self.answer.keys()))
        except AttributeError:
            self.header.ancount = datatypes.int16(0)
            self.header.rcode = datatypes.int4(3)
        try:
            self.header.nscount = datatypes.int16(len(self.authority.keys()))
        except AttributeError:
            self.header.nscount = datatypes.int16(0)
        try:
            self.header.arcount = datatypes.int16(len(self.additional.keys()))
        except AttributeError:
            self.header.arcount = datatypes.int16(0)

    @classmethod
    def create_question(cls, label, qtype=1, qclass=1):
        message = cls()
        message.add({
            'header': {
                'id': random.randint(0, 5000),
                'qr': 0,
                'opcode': 0,
                'aa': 0,
                'tc': 0,
                'rd': 1,
                'ra': 0,
                'z': 0,
                'rcode': 0,
                'qdcount': 1,
                'ancount': 0,
                'nscount': 0,
                'arcount': 0
            },
            'question': [{
                'labels': label,
                'qtype': qtype,
                'qclass': qclass,
            }]
        })
        return message

    def error_caught(self, rcode):
        try:
            delattr(self, 'answer')
        except:
            pass
        try:
            delattr(self, 'authority')
        except:
            pass
        try:
            delattr(self, 'additional')
        except:
            pass
        self.header.rcode = rcode

# class AlternativeMessage:
#     octets = {
#         1: {'binary': '10101010',
#             '1-8':{
#                 'type': 'cls.Counter',
#                 'link': '2'
#             }
#             },
#         2: {'binary': '11101010',
#             '1-8':{
#                 'type': 'cls.Counter',
#                 'link': '2'
#             }
#             },,
#         3: ...,
#     }