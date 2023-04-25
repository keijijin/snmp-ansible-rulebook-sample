import json
import struct


def decode_oid(binary_data):
    oid_list = []
    first_byte = binary_data[0]
    oid_list.append(str(first_byte // 40))
    oid_list.append(str(first_byte % 40))

    value = 0
    for byte in binary_data[1:]:
        value = (value << 7) | (byte & 0x7F)
        if not (byte & 0x80):
            oid_list.append(str(value))
            value = 0

    return ".".join(oid_list)

def parse_snmptrap_v1(binary_data):
    data = list(binary_data)
    idx = 4
    # SNMP version
    version = struct.unpack('!B', binary_data[idx:idx + 1])[0]
    idx += 2

    # Community string length
    community_length = struct.unpack('!B', binary_data[idx:idx + 1])[0]
    idx += 1

    # Extract community string
    community = binary_data[idx:idx + community_length].decode('utf-8')
    idx += community_length

    pdu_type = struct.unpack('!B', binary_data[idx:idx + 1])[0]
    idx += 3

    # Extract enterprise OID
    enterprise_length = struct.unpack('!B', binary_data[idx:idx + 1])[0]
    idx += 1
    enterprise = decode_oid(binary_data[idx:idx+enterprise_length])
    idx += enterprise_length + 2

    # Extract agent address
    agent_address = '.'.join([str(x) for x in binary_data[idx:idx + 4]])
    idx += 6

    # Extract generic trap
    generic_trap = struct.unpack('!B', binary_data[idx:idx + 1])[0]
    idx += 2

    # Extract specific trap
    specific_trap_length = int.from_bytes(binary_data[idx:idx + 1], byteorder='big')
    idx += 1
    specific_trap = int.from_bytes(binary_data[idx:idx + specific_trap_length], byteorder='big')
    idx += specific_trap_length

    # Extract uptime
    # if binary_data[idx] == b'\x43':
    idx += 1
    uptime = struct.unpack('!I', binary_data[idx:idx + 4])[0]
    idx += 4 + 3

    # Extract varBinds
    var_binds = []

    while idx < len(binary_data):
        idx += 3
        oid_length = struct.unpack('!B', binary_data[idx:idx + 1])[0]
        idx += 1
        oid = decode_oid(binary_data[idx:idx + oid_length])
        idx += oid_length
        vtype = binary_data[idx:idx+1]
        idx += 1
        value_length = struct.unpack('!B', binary_data[idx:idx + 1])[0]
        idx += 1
        if vtype == b'\x04':
            # print("OCTET_STRING")
            value = binary_data[idx:idx + value_length].decode('utf-8')
        elif vtype == b'\x02':
            # print("INTEGER")
            value = int.from_bytes(binary_data[idx:idx + value_length], byteorder='big')
        elif vtype == b'\x05':
            value = None
        idx += value_length
        var_binds.append({'oid': oid, 'value': value})

    return {
        'version': version,
        'community': community,
        'enterprise': enterprise,
        'agentAddress': agent_address,
        'genericTrap': generic_trap,
        'specificTrap': specific_trap,
        'uptime': uptime,
        'varBinds': var_binds
    }

if __name__ == '__main__':
    # binary_data = b'0g\x02\x01\x00\x04\x04test\xa4\\\x06\x0c+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#@\x04\x7f\x00\x00\x01\x02\x01\x00\x02\x01!C\x04\x06V9K0:0\x18\x06\x0f+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00!\x01\x04\x05123450\x1e\x06\x0f+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00!\x02\x04\x0bHello World'
    # binary_data = b'0j\x02\x01\x00\x04\x04test\xa4_\x06\x0c+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#@\x04\x7f\x00\x00\x01\x02\x01\x00\x02\x02\x03\xe7C\x04\x06_@B0<0\x19\x06\x10+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00\x87g\x01\x04\x05123450\x1f\x06\x10+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00\x87g\x02\x04\x0bHello World'
    binary_data = b'0l\x02\x01\x00\x04\x06public\xa4_\x06\x0c+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#@\x04\x7f\x00\x00\x01\x02\x01\x00\x02\x02\x03\xe7C\x04\x06a\xcb\x8f0<0\x19\x06\x10+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00\x87g\x01\x04\x05123450\x1f\x06\x10+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00\x87g\x02\x04\x0bHello World'

    trap_v1_parameters = parse_snmptrap_v1(binary_data)
    print(json.dumps(trap_v1_parameters, indent=2))

