# dns_records/dns.py

def read_dns_file(file_path):
    records = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore comments and empty lines
                parts = line.split()
                record = {
                    "name": parts[0],
                    "type": parts[2],
                    "ttl": parts[1],
                }
                # Handle different record types
                if parts[2] in ["A", "AAAA"]:
                    ip_port = parts[3].split(':')
                    record["data"] = {
                        "ip": ip_port[0],
                        "port": int(ip_port[1]) if len(ip_port) > 1 else None
                    }
                elif parts[2] == "CNAME":
                    target_port = parts[3].split(':')
                    record["data"] = {
                        "target": target_port[0],
                        "port": int(target_port[1]) if len(target_port) > 1 else None
                    }
                elif parts[2] == "MX":
                    mx_parts = parts[3].split(':')
                    record["data"] = {
                        "priority": int(parts[1]),
                        "exchange": mx_parts[0],
                        "port": int(mx_parts[1]) if len(mx_parts) > 1 else None
                    }
                elif parts[2] == "SRV":
                    record["data"] = {
                        "priority": int(parts[3]),
                        "weight": int(parts[4]),
                        "port": int(parts[5].split(':')[0]),
                        "target": parts[6].split(':')[0]
                    }
                elif parts[2] == "NAME":
                    name_parts = parts[3].split(':')
                    record["data"] = {
                        "value": name_parts[0],
                        "port": int(name_parts[1]) if len(name_parts) > 1 else None
                    }
                records.append(record)
    return records

def write_dns_file(file_path, records):
    with open(file_path, 'w') as file:
        for record in records:
            if record['type'] in ['A', 'AAAA']:
                ip = record['data']['ip']
                port = record['data'].get('port')
                line = f"{record['name']} {record['ttl']} IN {record['type']} {ip}"
                if port is not None:
                    line += f":{port}"
                line += "\n"
            elif record['type'] == 'CNAME':
                target = record['data']['target']
                port = record['data'].get('port')
                line = f"{record['name']} {record['ttl']} IN {record['type']} {target}"
                if port is not None:
                    line += f":{port}"
                line += "\n"
            elif record['type'] == 'MX':
                exchange = record['data']['exchange']
                port = record['data'].get('port')
                line = f"{record['name']} {record['data']['priority']} IN {record['type']} {exchange}"
                if port is not None:
                    line += f":{port}"
                line += "\n"
            elif record['type'] == 'SRV':
                line = f"{record['name']} {record['data']['priority']} {record['data']['weight']} {record['data']['port']} {record['data']['target']}\n"
            elif record['type'] == 'NAME':
                value = record['data']['value']
                port = record['data'].get('port')
                line = f"{record['name']} {record['ttl']} IN {record['type']} {value}"
                if port is not None:
                    line += f":{port}"
                line += "\n"
            file.write(line)
