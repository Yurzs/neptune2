import asyncio
import datetime

import bitstring
import jsonpickle
from sqlalchemy import and_
from ram_orm import models as nodes
from psql import models
from dns import datatypes, exceptions

db = models.db
ram_db = nodes.ORM()


redisconnection = models.redisconnection

async def old_domain_composer(rr):
    pass

nodes_rr_type = {
    1: nodes.A,
    2: nodes.NS,
    6: nodes.SOA,
    28: nodes.AAAA,
    257: nodes.CAA,
    5: nodes.CNAME,
    13: nodes.HINFO,
    12: nodes.PTR,
    7: nodes.MB,
    9: nodes.MR,
    15: nodes.MX,
    16: nodes.TXT,
    46: nodes.RRSIG,
    48: nodes.DNSKEY,
    255: nodes.A
}


type_rr = {
    1: models.A,
    2: models.Ns,
    28: models.Aaaa,
    257: models.Caa,
    5: models.Cname,
    13: models.Hinfo,
    12: models.Ptr,
    7: models.Mb,
    9: models.Mr,
    15: models.Mx,
    16: models.Txt,
    46: models.Rrsig,
    48: models.Dnskey,
    255: models.A
    # TODO ANY
}

rrsig_rr_node = {
    1: nodes.A,
    2: nodes.NS,
    28: nodes.AAAA,
    257: nodes.CAA,
    5: nodes.CNAME,
    13: nodes.HINFO,
    12: nodes.PTR,
    7: nodes.MB,
    9: nodes.MR,
    15: nodes.MX,
    16: nodes.TXT,
    48: nodes.DNSKEY,
}

rrsig_rr = {
    1: models.A,
    2: models.Ns,
    6: models.Soa,
    28: models.Aaaa,
    257: models.Caa,
    5: models.Cname,
    13: models.Hinfo,
    7: models.Mb,
    9: models.Mr,
    15: models.Mx,
    16: models.Txt,
    48: models.Dnskey,
}


class PickleRedis:
    def __init__(self, redis_connection):
        self.redis = redis_connection

    async def get(self, string=None, **kwargs):
        result = None
        if not kwargs and string:
            result = await self.redis.get(string)
        elif kwargs and not string:
            result = await self.redis.get('&'.join([f'{key}={str(value).lower()}' for key, value in kwargs.items()]))
        if result:
            return jsonpickle.decode(result)
        else:
            return []

    async def set(self, name, obj):
        return await self.redis.set(name, jsonpickle.encode(obj))


rediscon = PickleRedis(redisconnection)


def bin_cutter(data: bitstring.BitArray, counter, octets=2):
    """
    Cuts part of binary string
    :param data: binary string BitArray
    :param octets: number of bytes (8bit) to cut from beginning of string
    :return: BitArray without cut part
    """
    return bitstring.BitArray(bin=data.bin[octets * 8:]), counter + octets


def skip(**kwargs):
    return kwargs


def timer(func):
    def wrapper(*args, **kwargs):
        time_start = datetime.datetime.now().timestamp()
        result = func(*args, **kwargs)
        print('{func_name} took {time}ms to proceed'.format(func_name=func.__name__,
                                                            time=int((
                                                                                 datetime.datetime.now().timestamp() - time_start) * 1000)))
        return result

    return wrapper


async def sign_rr_set(rrset):
    if rrset:
        if isinstance(rrset[0], nodes.Domain):
            domain = rrset[0]
        else:
            domain = rrset[0].domain()
        dnskey = None
        if domain:
            dnskey = ram_db.get(nodes.DNSKEY, domain__id=domain.id, sep=True)
        if dnskey:
            rrsig = nodes.RRSIG.set_rrset(rrset=rrset, dnskey=dnskey, domain=domain.id)
            if rrsig:
                rrset.append(rrsig)
    return rrset


async def build_rrsigs(label):
    domain = ram_db.get(nodes.Domain, full_name=label)
    main_dnskey = ram_db.get(nodes.DNSKEY, domain__id=domain.id, sep=True)
    if main_dnskey:
        answer = []
        for qtype, model in rrsig_rr_node.items():
            if qtype == 6:
                pass
                # rr = await build_rrset(await search_answers([label, ], [6, ], [1, ]))
            else:
                rr = await ram_db.filter(model, domain__id=domain.id)
            if rr:
                rrsig = await nodes.RRSIG.set_rrset(rrset=rr, dnskey=main_dnskey)
                for item in rrsig:
                    answer.append(item)
        # authority = await search_authority(label)
        return answer, [], []
    else:
        return [], [], []


async def find_in_ram_orm(**kwargs):
    message = kwargs.get('message')
    if getattr(message, 'question', None):
        start = datetime.datetime.now().timestamp()
        labels = [message.question[question].labels for question in message.question]
        qtypes = [message.question[question].qtype for question in message.question]
        qclass = [message.question[question].qclass for question in message.question]
        answer = []
        authority = []
        additional = []
        domain = ram_db.get(nodes.Domain, full_name=labels[0])
        if domain:
            message.header.aa = datatypes.int1(1)
            if qtypes[0] == 6:
                soa = nodes.SOA()
                if domain.from_zone:
                    soa.domain = domain.from_zone
                    answer.append(soa)
            else:
                for rr in ram_db.filter(nodes_rr_type[qtypes[0]], domain__id=domain.id):
                    answer.append(rr)
            if domain.from_zone:
                for ns in ram_db.filter(nodes.NS, domain__id=domain.from_zone.id):
                    authority.append(ns)
                    audomain = ram_db.get(nodes.Domain, full_name=ns.nsdname)
                    for an in ram_db.filter(nodes.A, domain__id=audomain.id):
                        additional.append(an)
                    for an in ram_db.filter(nodes.AAAA, domain__id=audomain):
                        additional.append(an)
            if qtypes[0] == 2:
                for an in ram_db.filter(nodes.A, domain__id=domain.id):
                    additional.append(an)
                for an in ram_db.filter(nodes.AAAA, domain__id=domain.id):
                    additional.append(an)
        kwargs['import_dict'] = {
            'answer': answer,
            'authority': authority,
            'additional': additional}
        return kwargs
    kwargs['import_dict'] = {
        'answer': [],
        'authority': [],
        'additional': []}
    return kwargs


async def sign_import_dict(**kwargs):
    message = kwargs.get('message')
    import_dict = kwargs.get('import_dict')
    if getattr(message.edns, 'dnssec_ok', False):
        for rrset_type, rr in import_dict.items():
            if rrset_type in ['answer', 'authority', 'additional']:
                import_dict[rrset_type] = await sign_rr_set(rr)
    try:
        delattr(message, 'answer')
    except AttributeError:
        pass
    try:
        delattr(message, 'authority')
    except AttributeError:
        pass
    try:
        delattr(message, 'additional')
    except AttributeError:
        pass
    kwargs['import_dict'] = import_dict
    kwargs['message'] = message
    return await add_to_message(**kwargs)


# async def store_in_cache(**kwargs):
#     reader, writer = await asyncio.open_connection('cache', 12345, loop=models.loop)
#     message = kwargs.get('message')
#     import_dict = kwargs.get('import_dict')
#     transfer_dict = {
#         'action': 'set',
#         'expire': '30',
#         'label': str(message.question[0].labels),
#         'qtype': str(message.question[0].qtype),
#         'qclass': str(message.question[0].qclass),
#         'import_dict': import_dict
#     }
#     try:
#         writer.write(jsonpickle.encode(transfer_dict).encode())
#         data = await reader.read(100)
#         if data.decode() == 'ok':
#             return True
#         else:
#             return False
#     except ValueError:
#         return False


async def add_to_message(**kwargs):
    kwargs['message'].add(kwargs.get('import_dict'))
    return kwargs


# @timer
async def send_message(*args, **kwargs):

    conn_socket = kwargs.get('conn_socket')
    message = kwargs.get('message')
    message = message.edns.inject(message)
    message.self_check()
    # print(message.header.__dict__)
    # print(f'encoded message {message.encode()}')
    client_address = kwargs.get('client_address')
    if kwargs.get('resolved_message', None):
        conn_socket.sendto(kwargs.get('resolved_message'), client_address)
    elif kwargs.get('encoded_message', None):
        conn_socket.sendto(bitstring.BitArray(bin=kwargs.get('encoded_message')).bytes, client_address)
    else:
        try:
            conn_socket.sendto(bitstring.BitArray(bin=message.encode()).bytes, client_address)
        except bitstring.InterpretError:
            print(f'bad message {message.encode()}')

    return True


async def secure_resolve(**kwargs):
    """
    TBD
    :param args:
    :param kwargs:
    :return:
    """
    return kwargs
