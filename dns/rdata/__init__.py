from .a import A
from .aaaa import AAAA
from .caa import CAA
from .cname import CNAME
from .hinfo import HINFO
from .mb import MB
from .mg import MG
from .minfo import MINFO
from .mr import MR
from .mx import MX
from .ns import NS
from .opt import OPT
from .ptr import PRT
from .rdata import RDATA
from .soa import SOA
from .txt import TXT
from .wks import WKS
from .dnskey import DNSKEY
from .key import KEY
from .sig import SIG
from .rrsig import RRSIG

TYPES = {
    1: A,
    2: NS,
    5: CNAME,
    6: SOA,
    7: MB,
    8: MG,
    9: MR,
    11: WKS,
    12: PRT,
    13: HINFO,
    14: MINFO,
    15: MX,
    16: TXT,
    25: KEY,
    28: AAAA,
    41: OPT,
    46: RRSIG,
    48: DNSKEY,
    257: CAA,
}
