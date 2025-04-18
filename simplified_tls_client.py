#!/usr/bin/python3
import socket
import ssl
import sys
import pprint
import socks  # from PySocks

hostname = sys.argv[1]
port = 443
proxy_host = "proxy62.iitd.ac.in"
proxy_port = 3128
# Uncomment line 13 for default behaviour and comment line 15
# cadir = '/etc/ssl/certs'
# For task 2 - choosing a custom certs dir. 
cadir = './certs'

print(f"[+] Connecting to {hostname}:{port} via proxy {proxy_host}:{proxy_port}", flush=True)

try:
    # Create a proxy-aware socket
    sock = socks.socksocket()
    sock.set_proxy(socks.HTTP, proxy_host, proxy_port)
    sock.settimeout(10)
    sock.connect((hostname, port))
    print("[+] Connected to proxy and target host\n", flush=True)

    input("[*] After TCP connection. Press Enter to continue...\n")

    # Wrap with SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # context.load_verify_locations(capath=cadir)
    context.load_verify_locations(cafile='./certs/ca-certificates.crt')
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    # For Task 1.3 comment the line above (34) and uncomment the line below (37)
    # Otherwise keep check_hostname True (i.e. 34 uncommented)
    # context.check_hostname = False
    print(f"context.check_hostname={context.check_hostname}\n")

    ssock = context.wrap_socket(sock, server_hostname=hostname, do_handshake_on_connect=False)
    print("[+] Starting TLS handshake...", flush=True)
    ssock.do_handshake()
    # print("[+] Cipher used:", ssock.cipher())
    print("[+] TLS handshake completed\n", flush=True)

    # Send HTTP Request
    request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\n\r\n".encode()
    ssock.sendall(request)
    print("[+] HTTP Request Sent\n")

    # Read Response
    response = b""
    while True:
        chunk = ssock.recv(4096)
        if not chunk:
            break
        response += chunk

    # Print headers and partial body
    headers_end = response.find(b"\r\n\r\n")
    if headers_end != -1:
        headers = response[:headers_end].decode()
        body = response[headers_end+4:headers_end+2048]  # First 2KB of body
        print("[+] Response Headers:\n", headers)
        print("\n[+] Partial Body:\n", body.decode('utf-8', errors='ignore'))
    else:
        print("[!] Invalid HTTP Response")


    # Print cert
    cert = ssock.getpeercert()
    # print("[+] Server certificate:")
    # pprint.pprint(cert)
    input("\n[*] After handshake. Press Enter to close...")

    ssock.shutdown(socket.SHUT_RDWR)
    ssock.close()
    print("[+] Connection closed cleanly", flush=True)

except Exception as e:
    print(f"[!] Error: {e}", flush=True)
