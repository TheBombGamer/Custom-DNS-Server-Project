# dns_server.py

from flask import Flask, request, jsonify
import socket
from dnslib import DNSRecord, DNSHeader, RR, A, QTYPE
from records import load_records_from_file, get_record

app = Flask(__name__)

class DNSServer:
    def __init__(self, host='0.0.0.0', port=53, records_file='example.dns'):
        self.host = host
        self.port = port
        self.records_file = records_file
        load_records_from_file(self.records_file)  # Load records from the .dns file

    def start(self):
        """Start the DNS server."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        print(f"DNS Server running on {self.host}:{self.port}")

        while True:
            data, addr = sock.recvfrom(512)  # DNS messages are typically small
            self.handle_request(data, addr, sock)

    def handle_request(self, data, addr, sock):
        """Handle incoming DNS requests."""
        request = DNSRecord.parse(data)
        response = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1))

        for question in request.questions:
            domain = str(question.qname)
            record = get_record(domain)

            if record:
                ip, port = record
                # Create an A record response
                response.add_answer(RR(question.qname, QTYPE.A, rdata=A(ip), ttl=60))
                print(f"Resolved {domain} to {ip}:{port}")
            else:
                # If the domain is not found, return an empty response
                print(f"Domain {domain} not found.")
                response.header.rcode = 3  # NXDOMAIN

        sock.sendto(response.pack(), addr)

@app.route('/resolve', methods=['GET'])
def resolve():
    """HTTP endpoint to resolve a domain."""
    domain = request.args.get('domain')
    record = get_record(domain)

    if record:
        ip, port = record
        return jsonify({"domain": domain, "ip": ip, "port": port}), 200
    else:
        return jsonify({"error": "Domain not found"}), 404

if __name__ == "__main__":
    server = DNSServer(records_file='example.dns')  # Specify your .dns file here
    server.start()
