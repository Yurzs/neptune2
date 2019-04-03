import asyncio
import platform

import bitstring

import dns
import funcs
from dns import exceptions
from ram_orm import models as nodes
from psql import models


async def load():
    for domain in await models.Domain.query.order_by(models.Domain.id).gino.all():
        funcs.ram_db.set(nodes.Domain(id=domain.id,
                                      label=domain.label,
                                      parent=domain.parent_id,
                                      is_zone=domain.is_zone,
                                      primary_nameserver=domain.primary_nameserver_id,
                                      responsible_user_email=domain.responsible_user_email,
                                      responsible_user_id=domain.responsible_user_id))
    for atype, rrtype in funcs.type_rr.items():
        if atype == 255:
            continue
        try:
            for rr in await rrtype.query.order_by(rrtype.id).gino.all():
                dmn = rr.domain_id
                print({key: value for key, value in rr.__dict__['__values__'].items() if key != 'domain_id'})
                funcs.ram_db.set(getattr(nodes, str(rr.__class__.__name__).upper())(domain=dmn,
                                                                                    **{key: value for
                                                                                       key, value in
                                                                                       rr.__dict__[
                                                                                           '__values__'].items()
                                                                                       if
                                                                                       key != 'domain_id'}))
        except AttributeError:
            continue
    print('init done')


# %%
class UdpProtocol(asyncio.DatagramProtocol):

    def connection_made(self, transport):
        self.transport = transport

    # @funcs.timer
    def datagram_received(self, data, addr):
        kwargs = {}
        kwargs['skip_functions'] = []
        data = bitstring.BitArray(data)
        kwargs['raw_data'] = data
        message = dns.Message(byte_data=data)
        kwargs['message'] = message
        # print(message.header.id, message.question[0].__dict__)
        kwargs['conn_socket'] = self.transport
        kwargs['client_address'] = addr
        kwargs['skip_functions'] = []
        kwargs['skip_flow_step'] = []
        asyncio.Task(new_router(**kwargs))


async def new_router(**kwargs):
    message = kwargs.get('message')
    try:
        kwargs = await funcs.find_in_ram_orm(**kwargs)
        if kwargs['import_dict']:
            # await funcs.store_in_cache(**kwargs)
            # if getattr(kwargs.get('message').edns, 'dnssec_ok', False):
            #     kwargs = await funcs.sign_import_dict(**kwargs)
            # else:
            kwargs = await funcs.add_to_message(**kwargs)
            await funcs.send_message(**kwargs)
    except exceptions.GenericDnsException as e:
        message.error_caught(e.rcode)
        kwargs['message'] = message
        # await funcs.store_in_cache(**kwargs)
        await funcs.send_message(**kwargs)


async def main():
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpProtocol(),
        local_addr=('0.0.0.0', 53))
    try:
        await asyncio.sleep(999999999999999999999999)
    finally:
        transport.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    listen = loop.create_datagram_endpoint(
        UdpProtocol, local_addr=('0.0.0.0', 53))
    transport, protocol = loop.run_until_complete(listen)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    transport.close()
    loop.close()
