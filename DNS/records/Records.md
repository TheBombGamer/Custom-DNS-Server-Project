# Example DNS Records
```
example.com.        IN  A     192.0.2.1:8080
example.com.        IN  AAAA 2001:db8::1:8080
example.com.        IN  CNAME www.example.com.:8080
example.com.        IN  MX    10 mail.example.com.:8080
mail.example.com.   IN  A     192.0.2.2:8080
service.example.com. IN  SRV   10 60 8080 service.example.com.:8080
name.example.com.   IN  NAME  "Some Name":8080
```
