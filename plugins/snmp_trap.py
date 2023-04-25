import asyncio
import socket
from typing import Any, Dict

import sys
from utility.decode_snmptrapv1 import parse_snmptrap_v1
sys.path.append('/Users/kjin/Ansible/eda/sample1')

from utility.snmpToJson import convert_snmptrap_to_json

async def listen_for_snmp_traps(queue: asyncio.Queue, host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print("Listening for SNMP traps on {}:{}".format(host, port))

    while True:
        data, addr = await asyncio.to_thread(sock.recvfrom, 1024)
        print("Received SNMP trap from {}:{}".format(addr[0], addr[1]))
        # print("Raw data:", data)
        event_data = parse_snmptrap_v1(data)
        print("EvntData:", event_data)
        await queue.put(dict(snmp_trap=event_data))

async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    host = args.get("host", "0.0.0.0")
    port = args.get("port", 162)

    await asyncio.create_task(listen_for_snmp_traps(queue, host, port))

if __name__ == "__main__":
    class MockQueue:
        def put(self, event):
            print(event)

    mock_arguments = dict(host="0.0.0.0", port=162)
    asyncio.run(main(MockQueue(), mock_arguments))
