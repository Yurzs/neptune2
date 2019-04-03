import datetime

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy import Text, UniqueConstraint, text
# from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy import and_
import config
import asyncio

db = config.db
loop = config.loop
redisconnection = config.redisconnection


class A(db.Model):
    __tablename__ = 'database_a'
    __table_args__ = (
        UniqueConstraint('domain_id', 'address'),
    )
    type = 1
    id = db.Column(db.Integer(), primary_key=True, server_default=db.text("nextval('database_a_id_seq'::regclass)"))
    address = db.Column(INET, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    # @property
    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'address': self.address}
        }


class Aaaa(db.Model):
    __tablename__ = 'database_aaaa'
    __table_args__ = (
        UniqueConstraint('domain_id', 'address'),
    )
    type = 28
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_aaaa_id_seq'::regclass)"))
    address = db.Column(INET, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'address': self.address}
        }


class Caa(db.Model):
    __tablename__ = 'database_caa'
    __table_args__ = (
        UniqueConstraint('domain_id', 'value'),
    )
    type = 257
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_caa_id_seq'::regclass)"))
    flag = db.Column(db.Integer(), nullable=False)
    tag = db.Column(Text, nullable=False)
    value = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        import dns
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'flag': self.flag,
                      'tag_length': int(len(dns.rdata.CAA.name_datatype['tag'](self.tag).binary) / 8),
                      'tag': self.tag,
                      'value': self.value}
        }


class Cname(db.Model):
    __tablename__ = 'database_cname'
    __table_args__ = (
        UniqueConstraint('domain_id', 'cname'),
    )
    type = 5
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_cname_id_seq'::regclass)"))
    cname = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'cname': self.cname.replace('http://', '')}
        }


class Dnskey(db.Model):
    __tablename__ = 'database_dnskey'
    type = 48
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_dnskey_id_seq'::regclass)"))
    sep = db.Column(db.Boolean(), nullable=False)
    protocol = db.Column(db.Integer(), nullable=False)
    algorithm = db.Column(db.Integer(), nullable=False)
    size = db.Column(db.Integer(), nullable=False)
    private_key = db.Column(Text, nullable=True)
    generate_new = db.Column(db.Boolean(), nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False)
    dns_class = db.Column(db.Integer(), nullable=False)
    revoke = db.Column(db.Boolean(), nullable=False)
    zone = db.Column(db.Boolean(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dnssec import algorithms
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'flags': int(
                str('').zfill(7) + str(int(self.zone)) + str(int(self.revoke)) + str('').zfill(6) + str(int(self.sep)),
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


class Rrsig():
    type = 46
    dns_class = 1

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @classmethod
    async def set_rrset(cls, rrset, dnskey):
        result = cls()
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
            result += datatypes.int8(len(self.rrset[0].domain.label.split('.'))).binary
        result += datatypes.int32(110).binary
        result += datatypes.int32((datetime.datetime.now() + datetime.timedelta(seconds=100)).timestamp()).binary
        result += datatypes.int32((datetime.datetime.now() - datetime.timedelta(seconds=5)).timestamp()).binary
        result += datatypes.int16(self.dnskey.key_tag).binary
        if isinstance(self.rrset[0], Domain):
            result += datatypes.UrlAddress(self.rrset[0].full_name).binary
        else:
            result += datatypes.UrlAddress(self.rrset[0].domain.full_name).binary
        return result

    @property
    def dictionary(self):
        from dnssec import algorithms
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {
                'type_covered': self.rrset[0].type if not isinstance(self.rrset[0], Domain) else 6,
                'algorithm': self.dnskey.algorithm,
                'labels': len(self.domain.full_name.split('.')),
                'original_ttl': 110,
                'signature_expiration': (datetime.datetime.now() + datetime.timedelta(seconds=100)).timestamp(),
                'signature_inception': (datetime.datetime.now() - datetime.timedelta(seconds=100)).timestamp(),
                'key_tag': self.dnskey.key_tag,
                'signers_name': self.domain.full_name,
                'signature': algorithms.dnssec_algorithm_type[self.dnskey.algorithm].key_import(
                    key=self.dnskey.private_key).sign(
                    rrset=self.rrset, rrsig_rdata_without_signature=self.rdata_without_signature()
                )
            }
        }


class Domain(db.Model):
    __tablename__ = 'database_domain'
    __table_args__ = (
        UniqueConstraint('parent_id', 'label'),
    )
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_domain_id_seq'::regclass)"))
    is_zone = db.Column(db.Boolean(), nullable=False)
    label = db.Column(db.String(32), nullable=False)
    parent_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), index=True)
    primary_nameserver_id = db.Column(db.ForeignKey('database_ns.id', deferrable=True, initially='DEFERRED'),
                                      index=True)
    responsible_user_email = db.Column(db.String(254), nullable=False)
    responsible_user_id = db.Column(db.Integer(), nullable=False)

    async def async_get_parent(self, redis: 'RedisPickle' = None):
        if redis:
            result = redis.get(f'domain_id={self.parent_id}')
            if result:
                await result.build()
                return result
        else:
            result = await Domain.query.where(Domain.id == self.parent_id).gino.first()
            if result:
                await result.build()
                return result
        return result

    async def async_get_child(self, label, redis: 'RedisPickle' = None):
        if redis:
            return redis.get(f'domain_id={self.id}&children')
        return await Domain.query.where(and_(Domain.parent_id == self.id, Domain.label == label)).gino.first()

    async def async_get_zone(self, redis: 'RedisPickle' = None):
        if self.is_zone:
            return self
        if self.parent:
            parent = self.parent
            for n in range(len(self.full_name.split('.'))):
                if parent.is_zone:
                    return parent
                else:
                    await self.parent.build()
                    try:
                        parent = self.parent.parent
                        await parent.build()
                    except:
                        return None
        return None

    async def async_get_primary_nameserver(self, redis: 'RedisPickle' = None):
        if redis:
            return redis.get(f'domain_id={self.id}&type=2&rr_id={self.primary_nameserver_id}')
        return await Ns.query.where(Ns.id == self.primary_nameserver_id).gino.first()

    async def async_get_full_parent_name(self):
        if getattr(self, 'parent', None):
            path = self.parent.label
            if self.parent.parent_id:
                item = await self.parent.async_get_parent()
                path += f'.{item.label}'
                while True:
                    if item.parent_id:
                        item = await item.async_get_parent()
                        path += f'.{item.label}'
                    else:
                        break
            return path
        elif getattr(self, 'parent_id', None):
            setattr(self, 'parent', await self.async_get_parent())
            path = self.parent.label
            if self.parent.parent_id:
                item = await self.parent.async_get_parent()
                path += f'.{item.label}'
                while True:
                    if item.parent_id:
                        item = await item.async_get_parent()
                        path += f'.{item.label}'
                    else:
                        break
        else:
            return ''

    async def build(self, redis: 'RedisPickle' = None):
        setattr(self, 'parent', await self.async_get_parent(redis=redis))
        setattr(self, 'full_name', await self.async_get_full_name(redis=redis))
        setattr(self, 'nsdname', await self.async_get_nsdname(redis=redis))
        setattr(self, 'zone', await self.async_get_zone(redis=redis))
        if self.zone:
            setattr(self.zone, 'full_name', await self.zone.async_get_full_name())

    async def async_get_nsdname(self, redis: 'RedisPickle' = None):
        self.primary_nameserver = await self.async_get_primary_nameserver()

    async def async_get_full_name(self, redis: 'RedisPickle' = None):
        return str(self.label) + '.' + await self.async_get_full_parent_name() if self.parent else '.' + str(self.label)

    @property
    def rdata(self):
        rdata = {
            'mname': self.primary_nameserver.nsdname,
            'rname': self.responsible_user_email.replace('@', '.'),
            'serial': datetime.datetime.now().strftime('%Y%m%d%H'),
            'refresh': 1200,
            'retry': 120,
            'expire': 1209600,
            'minimum': 100
        }
        return rdata

    @property
    def dictionary(self):
        from dns import datatypes
        return {'name': datatypes.UrlAddress(self.full_name),
                'atype': datatypes.int16(6),
                'aclass': datatypes.int16(1),
                'ttl': datatypes.int32((1 * 60 + 0) * 60 + 10),
                'rdlength': datatypes.int16(99),
                'rdata': self.rdata}

    def __repr__(self):
        if getattr(self, 'full_name', None):
            return self.full_name
        else:
            return ''


class Soa():

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @classmethod
    async def set_rrset(cls, rrset, dnskey):
        result = cls()
        result.rrset = rrset
        result.dnskey = dnskey
        return result

    @property
    def dictionary(self):
        return self.domain.dictionary


class Domainrr(db.Model):
    __tablename__ = 'database_domainrr'
    __table_args__ = (
        UniqueConstraint('parent_zone_id', 'target', 'dns_class', 'type'),
    )

    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_domainrr_id_seq'::regclass)"))
    type = db.Column(db.Integer(), nullable=False)
    dns_class = db.Column(db.Integer(), nullable=False)
    target = db.Column(Text, nullable=False)
    parent_zone_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'),
                               nullable=False,
                               index=True)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()


class Ds(db.Model):
    __tablename__ = 'database_ds'

    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_ds_id_seq'::regclass)"))


class Dsfordnskey(db.Model):
    __tablename__ = 'database_dsfordnskey'

    id = db.Column(db.Integer(), primary_key=True,
                   server_default=text("nextval('database_dsfordnskey_id_seq'::regclass)"))
    digest_type = db.Column(db.Integer(), nullable=False)
    dnskey_id = db.Column(db.ForeignKey('database_dnskey.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)

    @property
    def dnskey(self):
        query = Dnskey.query.where(Dnskey.id == self.dnskey_id).gino.first()
        result = yield from config.loop.create_task(query)
        return asyncio.ensure_future(query, loop=config.loop)


class Hinfo(db.Model):
    __tablename__ = 'database_hinfo'
    __table_args__ = (
        UniqueConstraint('domain_id', 'cpu', 'os'),
    )
    type = 13
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_hinfo_id_seq'::regclass)"))
    cpu = db.Column(Text, nullable=False)
    os = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'cpu': self.cpu, 'os': self.os}
        }


class Masterserver(db.Model):
    __tablename__ = 'database_masterserver'

    id = db.Column(db.Integer(), primary_key=True,
                   server_default=text("nextval('database_masterserver_id_seq'::regclass)"))
    address = db.Column(INET, nullable=False)
    private_key = db.Column(Text, nullable=False)
    public_key = db.Column(Text, nullable=False)
    slave_pub_key = db.Column(Text, nullable=False)


class Mb(db.Model):
    __tablename__ = 'database_mb'
    __table_args__ = (
        UniqueConstraint('domain_id', 'madname'),
    )
    type = 7
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_mb_id_seq'::regclass)"))
    madname = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'madname': self.madname.replace('http://', '')}
        }


class Mr(db.Model):
    __tablename__ = 'database_mr'
    __table_args__ = (
        UniqueConstraint('domain_id', 'newname'),
    )
    type = 9
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_mr_id_seq'::regclass)"))
    newname = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'newname': self.newname.replace('http://', '')}
        }


class Mx(db.Model):
    __tablename__ = 'database_mx'
    __table_args__ = (
        UniqueConstraint('domain_id', 'exchange'),
    )
    type = 15
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_mx_id_seq'::regclass)"))
    preference = db.Column(db.Integer(), nullable=False)
    exchange = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'preference': self.preference,
                      'exchange': self.exchange.replace('http://', '')}
        }


class Ns(db.Model):
    __tablename__ = 'database_ns'
    __table_args__ = (
        UniqueConstraint('domain_id', 'nsdname'),
    )
    type = 2
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_ns_id_seq'::regclass)"))
    nsdname = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'nsdname': self.nsdname.replace('http://', '')}
        }


class Ptr(db.Model):
    __tablename__ = 'database_ptr'
    type = 12
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_ptr_id_seq'::regclass)"))
    dns_class = db.Column(db.Integer(), nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          unique=True)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()


class Resolver(db.Model):
    __tablename__ = 'database_resolver'

    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_resolver_id_seq'::regclass)"))
    ip_address = db.Column(INET, nullable=False)


class Slaveserver(db.Model):
    __tablename__ = 'database_slaveserver'

    id = db.Column(db.Integer(), primary_key=True,
                   server_default=text("nextval('database_slaveserver_id_seq'::regclass)"))
    address = db.Column(INET, nullable=False)


class Slavezone(db.Model):
    __tablename__ = 'database_slavezones'

    id = db.Column(db.Integer(), primary_key=True,
                   server_default=text("nextval('database_slavezones_id_seq'::regclass)"))
    slave_id = db.Column(db.ForeignKey('database_slaveserver.id', deferrable=True, initially='DEFERRED'),
                         nullable=False,
                         index=True)
    zone_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                        index=True)

    # slave = relationship('Slaveserver')

    # @property
    # def domain(self):
    #     query = Domain.query.where(Domain.id == self.domain_id).gino.first()
    #     task = asyncio.ensure_future(query, loop=connection_config.loop)
    #     result = yield from task
    #     return result


class Txt(db.Model):
    __tablename__ = 'database_txt'
    __table_args__ = (
        UniqueConstraint('domain_id', 'txt_data'),
    )
    type = 16
    id = db.Column(db.Integer(), primary_key=True, server_default=text("nextval('database_txt_id_seq'::regclass)"))
    txt_data = db.Column(Text, nullable=False)
    domain_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                          index=True)
    dns_class = db.Column(db.Integer(), nullable=False)

    async def async_get_domain(self, domain_id=None):
        if domain_id:
            return await Domain.query.where(Domain.id == domain_id).gino.first()
        else:
            return await Domain.query.where(Domain.id == self.domain_id).gino.first()

    @property
    def dictionary(self):
        from dns import datatypes
        return {
            'name': datatypes.UrlAddress(self.domain.full_name),
            'atype': datatypes.int16(self.type),
            'aclass': datatypes.int16(self.dns_class),
            'ttl': datatypes.int32(110),
            'rdlength': datatypes.int16(4),
            'rdata': {'txt_data': self.txt_data}
        }


class Zonenameserver(db.Model):
    __tablename__ = 'database_zonenameservers'

    id = db.Column(db.Integer(), primary_key=True,
                   server_default=text("nextval('database_zonenameservers_id_seq'::regclass)"))
    resource_record_id = db.Column(db.ForeignKey('database_ns.id', deferrable=True, initially='DEFERRED'),
                                   nullable=False,
                                   unique=True)
    zone_id = db.Column(db.ForeignKey('database_domain.id', deferrable=True, initially='DEFERRED'), nullable=False,
                        index=True)

    # resource_record = relationship('Ns', uselist=False)

    @property
    def zone(self):
        query = Domain.query.where(Domain.id == self.domain_id).gino.first()
        task = asyncio.ensure_future(query, loop=config.loop)
        result = yield from task
        return result
