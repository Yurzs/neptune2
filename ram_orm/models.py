import datetime
import re
from functools import partial


class Node:
    def __init__(self, **kwargs):
        self.__fields__ = {}
        for attr, item in self.__class__.__dict__.items():
            if not re.match('__[A-z]+__', attr) and issubclass(item.__class__, Field):
                self.__fields__[attr] = item
                if isinstance(item, ForeignKey):
                    setattr(self, attr, item.set(kwargs.get(attr), attr))
                    setattr(self, attr + '__id', kwargs.get(attr))
                else:
                    setattr(self, attr, item.set(kwargs.get(attr), attr))


class email(str):

    def validate(self):
        from email.utils import parseaddr
        if parseaddr(self)[1] == self:
            return self
        else:
            raise ValueError('Email is not valid')


class obj_link(int):
    pass

    def validate(self):
        return self


class Field:
    pass


class IntegerField(Field):
    def __init__(self, unique=False, default=None, null=False, blank=False, primary_key=False):
        self.unique = unique
        self.default = default
        self.null = null
        self.blank = blank
        self.primary_key = primary_key

    type = int

    def set(self, value, field_name):
        if self.default and not value:
            return self.type(self.default)
        elif not self.null and value is None:
            raise ValueError(f'{field_name} = {self.__class__.__name__}(null={self.null}) but value is None')
        elif not self.blank and value == '':
            raise ValueError(f'{field_name} = {self.__class__.__name__}(blank={self.blank}) but value is ""')
        elif self.null and not value:
            return None
        elif self.blank and not value:
            return ''
        elif value:
            return self.type(value)

    def __str__(self):
        if getattr(self, 'value', None):
            return self.value
        else:
            return str(self.__class__.__name__)


class TextField(Field):
    def __init__(self, unique=False, default=None, null=False, blank=False):
        self.unique = unique
        self.default = default
        self.null = null
        self.blank = blank

    type = str

    def validate(self, value):
        pass

    def set(self, value, field_name):
        if self.default and not value:
            return self.type(self.default)
        elif not self.null and value is None:
            raise ValueError(f'{field_name} = {self.__class__.__name__}(null={self.null}) but value is None')
        elif not self.blank and value == '':
            raise ValueError(f'{field_name} = {self.__class__.__name__}(blank={self.blank}) but value is ""')
        elif self.null and not value:
            return None
        elif self.blank and not value:
            return ''
        elif value:
            return self.type(value)

    def __str__(self):
        if getattr(self, 'value', None):
            return self.value
        else:
            return str(self.__class__.__name__)


class BoolField(Field):
    def __init__(self, unique=False, default=False, null=False, blank=False):
        self.unique = unique
        self.default = default
        self.null = null
        self.blank = blank

    type = bool

    def validate(self, value):
        pass

    def set(self, value, field_name):
        if value is None and hasattr(self, 'default'):
            return self.type(self.default)
        elif not self.null and value is None:
            raise ValueError(f'{field_name} = {self.__class__.__name__}(null={self.null}) but value is None')
        elif not self.blank and value == '':
            raise ValueError(f'{field_name} = {self.__class__.__name__}(blank={self.blank}) but value is ""')
        elif self.null and not value:
            return None
        elif self.blank and not value:
            return ''
        elif value:
            return self.type(value)

    def __str__(self):
        return self
        # else:
        #     return str(self.__class__.__name__)


class EmailField(Field):
    def __init__(self, unique=False, default=False, null=False, blank=False):
        self.unique = unique
        self.default = default
        self.null = null
        self.blank = blank

    type = email

    def set(self, value, field_name):
        if not self.null and value is None:
            raise ValueError(f'{field_name} = {self.__class__.__name__}(null={self.null}) but value is None')
        elif not self.blank and value == '':
            raise ValueError(f'{field_name} = {self.__class__.__name__}(blank={self.blank}) but value is ""')
        elif self.null and not value:
            return None
        elif self.blank and not value:
            return ''
        elif self.default and not value:
            return self.type(self.default)
        elif value:
            return self.type(value).validate()

    def __str__(self):
        if getattr(self, 'value', None):
            return self.value
        else:
            return str(self.__class__.__name__)


class ForeignKey(Field):
    def __init__(self, to_model, on_delete, null=False, blank=False):
        self.to_model = to_model
        self.on_delete = on_delete
        self.null = null
        self.blank = blank

    type = obj_link

    def validate(self, value):
        pass

    def set(self, value, field_name):
        if not self.null and value is None:
            raise ValueError(f'{field_name} = {self.__class__.__name__}(null={self.null}) but value is None')
        elif not self.blank and value == '':
            raise ValueError(f'{field_name} = {self.__class__.__name__}(blank={self.blank}) but value is ""')
        elif self.null and not value:
            return None
        elif self.blank and not value:
            return ''
        elif value:
            return partial(ORM().get, eval(self.to_model), id=value)

    def __str__(self):
        if getattr(self, 'value', None):
            return self.value
        else:
            return str(self.__class__.__name__)


class CASCADE:
    pass


class SET_NULL:
    pass


def get_item(dataset, obj_cls, **kwargs):
    copy = dataset.copy()
    for n, item in enumerate(copy):
        if isinstance(item, obj_cls):
            for_trigger = len(kwargs)
            counter = 0
            for attr, value in kwargs.items():
                if getattr(item, attr, None) == value:
                    counter += 1
            if for_trigger == counter:
                return item
    return None


def filter_item(dataset, obj_cls, **kwargs):
    found = []
    copy = dataset.copy()
    for n, item in enumerate(copy):
        if isinstance(item, obj_cls):
            for_trigger = len(kwargs)
            counter = 0
            for attr, value in kwargs.items():
                if getattr(item, attr, None) == value:
                    counter += 1
            if for_trigger == counter:
                found.append(item)
    return found


class ORM:
    __storage__ = []

    def set(self, obj):
        for field_name, field in obj.__fields__.items():
            if isinstance(field, ForeignKey) and not getattr(obj, field_name, None):
                setattr(obj, field_name, partial(lambda: None))
            if getattr(obj.__class__, 'Meta', None):
                meta = getattr(obj.__class__, 'Meta')
                unique_together = getattr(meta, 'unique_together', None)
                if unique_together:
                    if self.filter(obj.__class__, **{key: getattr(obj, key, None) for key in unique_together}):
                        raise ValueError(f'Duplicate {field_name}: {getattr(obj, field_name)}')
                    continue
            if getattr(field, 'unique', None):
                print(field)
                if self.filter(obj.__class__, **{field_name: getattr(obj, field_name)}):
                    raise ValueError(f'Duplicate {field_name}: {getattr(obj, field_name)}')
        self.__storage__.append(obj)

    def remove(self, obj_cls, **kwargs):
        storage_copy = self.__storage__.copy()
        for n, record in enumerate(storage_copy):
            if isinstance(record, obj_cls):
                for_trigger = len(kwargs)
                counter = 0
                for attr, value in kwargs.items():
                    if getattr(record, attr, None) == value:
                        counter += 1
                if counter == for_trigger:
                    self.__storage__.pop(n)
        return True if storage_copy != self.__storage__ else False

    def get(self, obj_cls, **kwargs):
        return get_item(self.__storage__, obj_cls, **kwargs)

    def filter(self, obj_cls, **kwargs):
        result = []

        for kwarg, value in kwargs.copy().items():
            if re.match('[A-z]+__[A-z]+', kwarg):
                if kwarg.split('__')[1] == 'contains':
                    kwargs.pop(kwarg)
                    for item in filter_item(self.__storage__, obj_cls, **kwargs):
                        if value in getattr(item, kwarg.split('__')[0]):
                            result.append(item)
        if not result:
            for item in filter_item(self.__storage__, obj_cls, **kwargs):
                result.append(item)
        return result


class Domain(Node):
    id = IntegerField(unique=True, primary_key=True)
    is_zone = BoolField(default=False)
    parent = ForeignKey('Domain', on_delete=CASCADE, null=True)
    label = TextField()
    responsible_user_id = IntegerField()
    responsible_user_email = EmailField()
    primary_nameserver = ForeignKey('NS', on_delete=CASCADE, null=True)
    __children__ = []
    __rr__ = {}

    class Meta:
        unique_together = ('label', 'parent')

    async def add_child(self, domain_node):
        self.__children__.append(domain_node)

    async def del_child(self, **kwargs):
        pass

    @property
    def children(self):
        return self.__children__

    def add_rr(self, rr):
        if self.__rr__.get(rr.__class__.__name__, None):
            self.__rr__[rr.__class__.__name__].append(rr)
        else:
            self.__rr__[rr.__class__.__name__] = [rr]

    def del_rr(self, **kwargs):
        pass

    @property
    def rdata(self):
        if isinstance(self.primary_nameserver, partial):
            if self.primary_nameserver():
                print(self.primary_nameserver())
                mname = getattr(self.primary_nameserver(), 'nsdname')
            else:
                mname = None
        else:
            mname = None
        rdata = {
            'mname': mname,
            'rname': self.responsible_user_email.replace('@', '.'),
            'serial': datetime.datetime.now().strftime('%Y%m%d%H'),
            'refresh': 1200,
            'retry': 120,
            'expire': 1209600,
            'minimum': 100
        }
        return rdata

    def get_full_parent_name(self):
        if isinstance(self.parent, partial):
            if self.parent():
                path = self.parent().label
                item = self.parent()
                while True:
                    if getattr(item, 'parent', None):
                        if item.parent():
                            path += '.'
                            path += item.parent().label
                            item = getattr(item, 'parent')
                        else:
                            break
                    else:
                        break
                return path
        return ''

    @property
    def full_name(self):
        return str(self.label) + '.' + self.get_full_parent_name() if self.parent else '.' + str(self.label)

    @property
    def from_zone(self):
        domain = self
        if domain.is_zone:
            return domain
        while True:
            if isinstance(domain.parent, partial):
                if domain.parent():
                    domain = domain.parent()
                    if domain.is_zone:
                        return domain
                    else:
                        continue
                else:
                    break
            else:
                break
        return None

    @property
    def dictionary(self):
        from dns import datatypes
        return {'name': datatypes.UrlAddress(self.full_name),
                'atype': datatypes.int16(6),
                'aclass': datatypes.int16(1),
                'ttl': datatypes.int32((1 * 60 + 0) * 60 + 10),
                'rdlength': datatypes.int16(99),
                'rdata': self.rdata}


class RR(Node):
    pass


class A(RR):
    id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    address = TextField()
    type = 1

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'address': self.address}
        }


class AAAA(RR):
    id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    address = TextField()
    type = 28

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'address': self.address}
        }


class NS(RR):
    id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    nsdname = TextField()
    type = 2

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'nsdname': self.nsdname.replace('http://', '')}
        }


class CAA(RR):
    id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    type = 257
    flag = IntegerField()
    tag = TextField()
    value = TextField()

    @property
    def dictionary(self):
        import dns
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'flag': self.flag,
                      'tag_length': int(len(dns.rdata.CAA.name_datatype['tag'](self.tag).binary) / 8),
                      'tag': self.tag,
                      'value': self.value}
        }


class CNAME(RR):
    id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    cname = TextField()
    type = 5

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'cname': self.cname.replace('http://', '')}
        }


class DNSKEY(RR):
    id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    sep = BoolField(default=False)
    protocol = IntegerField()
    algorithm = IntegerField()
    size = IntegerField()
    private_key = TextField()
    generate_new = BoolField(default=False)
    revoke = BoolField(default=False)
    zone = BoolField(default=False)
    type = 48

    @property
    def dictionary(self):
        from dnssec import algorithms
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'flags': int(
                str('').zfill(7) + str(int(bool(self.zone))) + str(int(bool(self.revoke))) + str('').zfill(6) + str(
                    int(bool(self.sep))),
                base=2),
                'protocol': self.protocol,
                'algorithm': self.algorithm,
                'public_key':
                    algorithms.dnssec_algorithm_type[self.algorithm].key_import(self.private_key).rdata_public_key}
        }

    @property
    def key_tag(self):
        import dns
        key, lol, byte_counter, domain_links = dns.rdata.KEY.decode(byte_counter=0, domain_links={},
                                                                    dictionary=self.dictionary['rdata'])
        key = key.encode().bytes
        ac = 0
        for i, byte in enumerate(key):
            ac += byte if (i & 1) else byte << 8
        ac += ac >> 16 & 0xFFFF
        return ac & 0xFFFF


class RRSIG(RR):
    # id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    type = 46

    @classmethod
    def set_rrset(cls, rrset, dnskey, **kwargs):
        result = cls(**kwargs)
        result.rrset = rrset
        result.dnskey = dnskey
        return result

    def rdata_without_signature(self):
        from dns import datatypes
        result = ''
        if isinstance(self.rrset[0], Domain):
            result += datatypes.int16(6).binary
        else:
            result += datatypes.int16(self.rrset[0].type).binary
        result += datatypes.int8(self.dnskey.algorithm).binary
        if isinstance(self.rrset[0], Domain):
            result += datatypes.int8(len(self.rrset[0].full_name.split('.'))).binary
        else:
            result += datatypes.int8(len(self.rrset[0].domain().label.split('.'))).binary
        result += datatypes.int32(110).binary
        result += datatypes.int32((datetime.datetime.now() + datetime.timedelta(seconds=100)).timestamp()).binary
        result += datatypes.int32((datetime.datetime.now() - datetime.timedelta(seconds=5)).timestamp()).binary
        result += datatypes.int16(self.dnskey.key_tag).binary
        if isinstance(self.rrset[0], Domain):
            result += datatypes.UrlAddress(self.rrset[0].full_name).binary
        else:
            result += datatypes.UrlAddress(self.rrset[0].domain().full_name).binary
        return result

    @property
    def dictionary(self):
        from dnssec import algorithms
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {
                'type_covered': self.rrset[0].type if not isinstance(self.rrset[0], Domain) else 6,
                'algorithm': self.dnskey.algorithm,
                'labels': len(self.domain().full_name.split('.')),
                'original_ttl': 110,
                'signature_expiration': (datetime.datetime.now() + datetime.timedelta(seconds=100)).timestamp(),
                'signature_inception': (datetime.datetime.now() - datetime.timedelta(seconds=100)).timestamp(),
                'key_tag': self.dnskey.key_tag,
                'signers_name': self.domain().full_name,
                'signature': algorithms.dnssec_algorithm_type[self.dnskey.algorithm].key_import(
                    key=self.dnskey.private_key).sign(
                    rrset=self.rrset, rrsig_rdata_without_signature=self.rdata_without_signature()
                )
            }
        }


class SOA:
    type = 6

    @classmethod
    async def set_rrset(cls, rrset, dnskey):
        result = cls()
        result.rrset = rrset
        result.dnskey = dnskey
        return result

    @property
    def dictionary(self):
        return self.domain.dictionary


class TXT(RR):
    id = IntegerField(unique=True, primary_key=True)
    domain = ForeignKey('Domain', on_delete=CASCADE)
    dns_class = IntegerField(default=1)
    txt_data = TextField()
    type = 16

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain().full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'txt_data': self.txt_data}
        }


class HINFO:
    pass


class MX:
    pass


class MB:
    pass


class MR:
    pass


class PTR:
    pass
