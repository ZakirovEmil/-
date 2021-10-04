from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR

from cache import Cache

RECORDS = [1, 2, 12, 28]
DESTINATION = "192.168.1.2"
GOOGLE_DNS = "8.8.8.8"
DNS_PORT = 53


class Server:
    def __init__(self, cache):
        self.cache = cache

    def run(self):
        sniff(filter=f'udp port {DNS_PORT}', prn=self.handle_dns_udp_packet)

    def request(self, pkt):
        ip = IP(dst=GOOGLE_DNS)
        udp = UDP(dport=DNS_PORT)
        dns = DNS(rd=1, qd=DNSQR(qname=pkt[DNSQR].qname.decode('cp1251'), qtype=pkt[DNSQR].qtype))
        response = sr1(ip / udp / dns)
        if response[DNS].ancount == 0:
            return
        for i in range(response[DNS].ancount + response[DNS].nscount + response[DNS].arcount):
            self.parse_field(response, i)
        self.cache.update()

    def parse_field(self, response, i):
        rtype = response[DNSRR][i].type
        if rtype in RECORDS:
            data = response[DNSRR][i].rdata
            if type(data) == bytes:
                rdata = data.decode('cp1251')
            else:
                rdata = data
            ttl = int(response[DNSRR][i].ttl)
            self.cache.add_record(response[DNSRR][i].rrname.decode(), rtype, [rdata, ttl, time.time() + ttl])

    def response(self, pkt):
        qname = pkt[DNSQR].qname.decode('cp1251')
        qtype = pkt[DNSQR].qtype
        cache_data = self.cache.data[qname][qtype]
        ip = IP(dst=pkt[IP].src)
        udp = UDP(dport=53)
        rdata = cache_data[0]
        ttl = int(cache_data[1])
        dns_rr = DNSRR(rrname=qname, type=qtype, rdata=rdata, ttl=ttl)
        dns = DNS(id=pkt[DNS].id, qr=1, rd=1, ra=1, qd=pkt[DNS].qd, an=dns_rr)
        send(ip / udp / dns, verbose=False)

    def is_in_cache(self, pkt):
        qname = pkt[DNSQR].qname.decode('cp1251')
        print(f'\nFor: {qname}\n')
        return qname in self.cache.data.keys() and pkt[DNSQR].qtype in self.cache.data[qname] \
               and self.is_not_expired(qname, pkt)

    def is_not_expired(self, qname, pkt):
        return float(self.cache.data[qname][pkt[DNSQR].qtype][2]) >= time.time()

    def handle_dns_udp_packet(self, pkt):
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0 and pkt[IP].dst == DESTINATION:
            if not self.is_in_cache(pkt):
                self.request(pkt)
            self.response(pkt)


def main():
    cache = Cache("cache.txt")
    cache.init()
    try:
        Server(cache).run()
        print('Server started')
    finally:
        cache.update()


if __name__ == '__main__':
    main()
