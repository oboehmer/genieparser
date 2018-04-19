''' show_mrib.py

IOSXR parsers for the following show commands:
    * 'show mrib vrf <WORD> <WORD> route'
'''

# Python
import re

# Metaparser
from metaparser import MetaParser
from metaparser.util.schemaengine import Schema, Any, Optional, Or, And,\
                                         Default, Use

# ==============================================
# Parser for 'show mrib vrf <WORD> <WORD> route'
# ==============================================

class ShowMribVrfRouteSchema(MetaParser):
    
    """Schema for show mrib vrf <vrf> <address-family> route"""

    schema = {
        'vrf': 
            {Any(): 
                {'address_family': 
                    {Any(): 
                        {'multicast_group': 
                            {Any(): 
                                {'source_address': 
                                    {Any(): 
                                        {'uptime': str,
                                        Optional('flags'): str,
                                        Optional('rpf_nbr'): str,
                                        Optional('mvpn_tid'): str,
                                        Optional('mvpn_remote_tid'): str,
                                        Optional('mvpn_payload'): str,
                                        Optional('mdt_ifh'): str,
                                        Optional('mt_slot'): str,
                                        Optional('incoming_interface_list'): 
                                            {Any(): 
                                                {'uptime': str,
                                                'flags': str,
                                                Optional('rpf_nbr'): str,
                                                },
                                            },
                                        Optional('outgoing_interface_list'): 
                                            {Any(): 
                                                {'uptime': str,
                                                'flags': str,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }

class ShowMribVrfRoute(ShowMribVrfRouteSchema):
    
    """Parser for show mrib vrf <vrf> <address-family> route"""

    def cli(self, vrf='default', af='ipv4'):
        out = self.device.execute('show mrib vrf {vrf} {af} route'.\
                                  format(vrf=vrf, af=af))
        
        # Init vars
        parsed_dict = {}
        rpf_nbr = ''

        for line in out.splitlines():
            line = line.rstrip()

            # (192.168.0.12,227.1.1.1) RPF nbr: 192.168.0.12 Flags: RPF ME MH
            # (*,ff00::/8)
            # (1::1:1:1:2,ff15::1:1)
            p1 = re.compile(r'^\s*\((?P<source_address>(\S+))\,'
                             '(?P<multicast_group>(\S+))\)'
                             '(?: *RPF +nbr: +(?P<rpf_nbr>(\S+)))?'
                             '(?: *Flags: +(?P<flags>[a-zA-Z\s]+))?$')
            m = p1.match(line)
            if m:
                # Get values
                source_address = m.groupdict()['source_address']
                multicast_group = m.groupdict()['multicast_group']
                rpf_nbr = m.groupdict()['rpf_nbr']
                flags = m.groupdict()['flags']
                # Init dict
                if 'vrf' not in parsed_dict:
                    parsed_dict['vrf'] = {}
                if vrf not in parsed_dict['vrf']:
                    parsed_dict['vrf'][vrf] = {}
                if 'address_family' not in parsed_dict['vrf'][vrf]:
                    parsed_dict['vrf'][vrf]['address_family'] = {}
                if af not in parsed_dict['vrf'][vrf]['address_family']:
                    parsed_dict['vrf'][vrf]['address_family'][af] = {}
                if 'multicast_group' not in parsed_dict['vrf'][vrf]\
                        ['address_family'][af]:
                    parsed_dict['vrf'][vrf]['address_family'][af]\
                        ['multicast_group'] = {}
                if multicast_group not in parsed_dict['vrf'][vrf]\
                        ['address_family'][af]['multicast_group']:
                    parsed_dict['vrf'][vrf]['address_family'][af]\
                        ['multicast_group'][multicast_group] = {}
                if 'source_address' not in parsed_dict['vrf'][vrf]\
                        ['address_family'][af]['multicast_group']\
                        [multicast_group]:
                    parsed_dict['vrf'][vrf]['address_family'][af]\
                        ['multicast_group'][multicast_group]\
                        ['source_address'] = {}
                if source_address not in parsed_dict['vrf'][vrf]\
                        ['address_family'][af]['multicast_group']\
                        [multicast_group]['source_address']:
                    parsed_dict['vrf'][vrf]['address_family'][af]\
                        ['multicast_group'][multicast_group]\
                        ['source_address'][source_address] = {}
                sub_dict = parsed_dict['vrf'][vrf]['address_family'][af]\
                    ['multicast_group'][multicast_group]\
                    ['source_address'][source_address]
                # Set values
                if rpf_nbr:
                    sub_dict['rpf_nbr'] = rpf_nbr
                if flags:
                    sub_dict['flags'] = flags
                continue

            # RPF nbr: 150::150:150:150:150 Flags: L C RPF P
            p2 = re.compile(r'^\s*RPF +nbr: +(?P<rpf_nbr>(\S+))'
                             ' +Flags: (?P<flags>[a-zA-Z\s]+)$')
            m = p2.match(line)
            if m:
                rpf_nbr = m.groupdict()['rpf_nbr']
                sub_dict['rpf_nbr'] = rpf_nbr
                sub_dict['flags'] = m.groupdict()['flags']
                continue

            # Flags: D P
            p3 = re.compile(r'^\s*Flags: (?P<flags>[a-zA-Z\s]+)$')
            m = p3.match(line)
            if m:
                sub_dict['flags'] = m.groupdict()['flags']
                continue

            # Up: 00:00:54
            p4 = re.compile(r'^\s*Up: +(?P<uptime>(\S+))$')
            m = p4.match(line)
            if m:
                sub_dict['uptime'] = m.groupdict()['uptime']
                continue

            # MT Slot: 0/2/CPU0
            p5 = re.compile(r'^\s*MT +Slot: +(?P<mt_slot>(\S+))$')
            m = p5.match(line)
            if m:
                sub_dict['mt_slot'] = m.groupdict()['mt_slot']
                continue

            # MVPN TID: 0xe000001f
            p6 = re.compile(r'^\s*MVPN +TID: +(?P<mvpn_tid>(\S+))$')
            m = p6.match(line)
            if m:
                sub_dict['mvpn_tid'] = m.groupdict()['mvpn_tid']
                continue

            # MVPN Remote TID: 0x0
            p7 = re.compile(r'^\s*MVPN +Remote +TID:'
                             ' +(?P<mvpn_remote_tid>(\S+))$')
            m = p7.match(line)
            if m:
                sub_dict['mvpn_remote_tid'] = m.groupdict()['mvpn_remote_tid']
                continue

            # MVPN Payload: IPv4
            p8 = re.compile(r'^\s*MVPN +Payload: +(?P<mvpn_payload>(\S+))$')
            m = p8.match(line)
            if m:
                sub_dict['mvpn_payload'] = \
                    str(m.groupdict()['mvpn_payload']).lower()
                continue

            # MDT IFH: 0x803380
            p9 = re.compile(r'^\s*MDT +IFH: +(?P<mdt_ifh>(\S+))$')
            m = p9.match(line)
            if m:
                sub_dict['mdt_ifh'] = m.groupdict()['mdt_ifh']
                continue

            # Incoming Interface List
            p10 = re.compile(r'^\s*Incoming Interface List$')
            m = p10.match(line)
            if m:
                intf_list_type = 'incoming_interface_list'
                if intf_list_type not in sub_dict:
                    sub_dict[intf_list_type] = {}
                    continue

            # Outgoing Interface List
            p11 = re.compile(r'^\s*Outgoing Interface List$')
            m = p11.match(line)
            if m:
                intf_list_type = 'outgoing_interface_list'
                if intf_list_type not in sub_dict:
                    sub_dict[intf_list_type] = {}
                    continue

            # Loopback0 Flags: F A, Up: 00:00:54
            # GigabitEthernet0/1/0/1 Flags: NS, Up: 00:00:01
            # Decaps6tunnel0 Flags: NS DI, Up: 00:04:40
            # mdtvpn1 Flags: F NS MI MT MA, Up: 00:02:53
            p12 = re.compile(r'^\s*(?P<interface>(\S+)) +Flags:'
                              ' +(?P<flags>[a-zA-Z\s]+), +Up:'
                              ' +(?P<uptime>(\S+))$')
            m = p12.match(line)
            if m:
                # Get values
                interface = m.groupdict()['interface']
                flags = m.groupdict()['flags']
                uptime = m.groupdict()['uptime']
                if interface not in sub_dict[intf_list_type]:
                    sub_dict[intf_list_type][interface] = {}
                if flags:
                    sub_dict[intf_list_type][interface]['flags'] = flags
                if uptime:
                    sub_dict[intf_list_type][interface]['uptime'] = uptime
                if intf_list_type == 'incoming_interface_list' and rpf_nbr:
                    sub_dict[intf_list_type][interface]['rpf_nbr'] = rpf_nbr
                    continue

        return parsed_dict