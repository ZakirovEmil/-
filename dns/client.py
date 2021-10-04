import socket
from server import DNS_PORT, DESTINATION

requests = {'ulearn': b"\xcd\xbe\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x61\x70\x69"
                      b"\x06\x75\x6c\x65\x61\x72\x6e\x02\x6d\x65\x00\x00\x01\x00\x01"}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
sock.sendto(requests['ulearn'], (DESTINATION, DNS_PORT))
print('Sent')
