from dns import datatypes


class GenericDnsException(Exception):
    def __init__(self, *args, **kwargs):
        for item in kwargs:
            setattr(self, item, kwargs[item])


class DnsFormatError(GenericDnsException):
    message = 'NXDOMAIN'
    rcode = datatypes.int4(1)


class DnsServerFailure(GenericDnsException):
    message = 'Some ERROR occurred'
    rcode = datatypes.int4(2)


class DnsNameError(GenericDnsException):
    message = 'Domain not found locally'
    rcode = datatypes.int4(3)


class DnsNotImplemented(GenericDnsException):
    message = 'This type is not yet implemented'
    rcode = datatypes.int4(4)


class DnsRefused(GenericDnsException):
    message = 'Request Refused'
    rcode = datatypes.int4(5)
