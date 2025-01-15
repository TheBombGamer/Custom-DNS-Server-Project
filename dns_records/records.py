# records.py

dns_records = {}

def load_records_from_file(file_path):
    """Load DNS records from a .dns file."""
    global dns_records
    dns_records = {}  # Reset existing records
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore comments and empty lines
                parts = line.split()
                if len(parts) >= 4 and parts[2] == "A":  # Assuming A records
                    domain = parts[0]
                    ip_port = parts[3].split(':')
                    ip = ip_port[0]
                    port = int(ip_port[1]) if len(ip_port) > 1 else None
                    dns_records[domain] = (ip, port)

def add_record(domain, ip, port):
    """Add a new DNS record."""
    dns_records[domain] = (ip, port)

def get_record(domain):
    """Get the DNS record for a domain."""
    return dns_records.get(domain)
