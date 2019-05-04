from .rdata import Rdata
from .a import A
from .aaaa import Aaaa
from .cname import Cname
from .ns import Ns
from .mx import Mx
from .afsdb import Afsdb
from .avc import Avc
from .caa import Caa
from .dname import Dname
from .ds import Ds
from .hinfo import Hinfo
from .isdn import Isdn
from .key import Key
from .kx import Kx
from .loc import Loc
from .mb import Mb
from .mg import Mg
from .minfo import Minfo
from .mr import Mr
from .naptr import Naptr
from .null import Null
from .nsap import Nsap
from .nsec import Nsec, Nsec3, Nsec3Param
from .ptr import Ptr
from .px import Px
from .rp import Rp
from .rrsig import Rrsig
from .rt import Rt
from .sig import Sig
from .srv import Srv
from .sshfp import Sshfp
from .tkey import Tkey
from .tlsa import Tlsa
from .tsig import Tsig
from .txt import Txt
from .wks import Wks
from .x25 import X25
from .soa import Soa
from .dnskey import Dnskey

rdata_type = {
    1: A,
    28: Aaaa,
    5: Cname,
    2: Ns,
    15: Mx,
    18: Afsdb,
    258: Avc,
    257: Caa,
    39: Dname,
    48: Dnskey,
    43: Ds,
    13: Hinfo,
    20: Isdn,
    25: Key,
    36: Kx,
    29: Loc,
    7: Mb,
    8: Mg,
    14: Minfo,
    9: Mr,
    35: Naptr,
    10: Null,
    22: Nsap,
    47: Nsec,
    50: Nsec3,
    51: Nsec3Param,
    12: Ptr,
    26: Px,
    17: Rp,
    46: Rrsig,
    21: Rt,
    24: Sig,
    33: Srv,
    44: Sshfp,
    249: Tkey,
    52: Tlsa,
    250: Tsig,
    16: Txt,
    11: Wks,
    19: X25,
    6: Soa,
}