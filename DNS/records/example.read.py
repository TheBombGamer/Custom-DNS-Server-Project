from dns_records import read_dns_file, write_dns_file

# Example usage
dns_records = [
    {"name": "example.com.", "ttl": "3600", "type": "A", "data": {"ip": "192.0.2.1", "port": 8080}},
    {"name": "example.com.", "ttl": "3600", "type": "AAAA", "data": {"ip": "2001:db8::1", "port": 8080}},
    {"name": "example.com.", "ttl": "3600", "type": "CNAME", "data": {"target": "www.example.com", "port": 8080}},
    {"name": "example.com.", "ttl": "3600", "type": "MX", "data": {"priority": 10, "exchange": "mail.example.com", "port": 8080}},
    {"name": "mail.example.com.", "ttl": "3600", "type": "A", "data": {"ip": "192.0.2.2", "port": 8080}},
    {"name": "service.example.com.", "ttl": "3600", "type": "SRV", "data": {"priority": 10, "weight": 60, "port": 8080, "target": "service.example.com"}},
    {"name": "name.example.com.", "ttl": "3600", "type": "NAME", "data": {"value": "Some Name", "port": 8080}}
]

# Write records to a .dns file
write_dns_file('example.dns', dns_records)

# Read records from the .dns file
read_records = read_dns_file('example.dns')
print(read_records)
