expected_output = {
    "interfaces": {
        "Port-channel1": {
            "name": "Port-channel1",
            "protocol": "lacp",
            "members": {
                "GigabitEthernet2": {
                    "interface": "GigabitEthernet2",
                    "oper_key": 1,
                    "admin_key": 1,
                    "port_num": 1,
                    "lacp_port_priority": 32768,
                    "flags": "SA",
                    "activity": "auto",
                    "state": "bndl",
                    "bundled": True,
                    "port_state": 61,
                },
                "GigabitEthernet3": {
                    "interface": "GigabitEthernet3",
                    "oper_key": 1,
                    "admin_key": 1,
                    "port_num": 1,
                    "lacp_port_priority": 32768,
                    "flags": "SA",
                    "activity": "auto",
                    "state": "bndl",
                    "bundled": True,
                    "port_state": 61,
                },
            },
        },
        "Port-channel2": {
            "name": "Port-channel2",
            "protocol": "lacp",
            "members": {
                "GigabitEthernet4": {
                    "interface": "GigabitEthernet4",
                    "oper_key": 2,
                    "admin_key": 2,
                    "port_num": 1,
                    "lacp_port_priority": 32768,
                    "flags": "SA",
                    "state": "bndl",
                    "activity": "auto",
                    "bundled": True,
                    "port_state": 61,
                },
                "GigabitEthernet5": {
                    "interface": "GigabitEthernet5",
                    "oper_key": 2,
                    "admin_key": 2,
                    "port_num": 1,
                    "lacp_port_priority": 32768,
                    "flags": "SA",
                    "activity": "auto",
                    "state": "bndl",
                    "bundled": True,
                    "port_state": 61,
                },
                "GigabitEthernet6": {
                    "interface": "GigabitEthernet6",
                    "oper_key": 2,
                    "admin_key": 2,
                    "port_num": 1,
                    "lacp_port_priority": 32768,
                    "flags": "SA",
                    "activity": "auto",
                    "state": "bndl",
                    "bundled": True,
                    "port_state": 61,
                },
            },
        },
    }
}
