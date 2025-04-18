#!/usr/bin/python3
import socket
import ssl
import sys
import pprint
import socks

def send_http_request(ssock, hostname):
    try:
        # Send HTTP GET request
        request = b"GET / HTTP/1.1\r\nHost: " + hostname.encode() + b"\r\nConnection: close\r\n\r\n"
        ssock.sendall(request)
        
        # Read response
        response = b''
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            response += data
        
        # Print headers and body
        headers, _, body = response.partition(b'\r\n\r\n')
        print("HTTP Response Headers:")
        print(headers.decode())
        print("\nHTTP Response Body (preview):")
        print(body[:500].decode())  # Preview of the body
    except Exception as e:
        print(f"[!] Error in send_http_request: {e}")

def download_google_icon(ssock, hostname):
    try:
        # Use Google's favicon API to get the standard Google icon
        icon_path = "/s2/favicons?domain=google.com&sz=128"
        
        # Send HTTP GET request for the Google icon
        request = b"GET " + icon_path.encode() + b" HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n"
        ssock.sendall(request)
        
        print(f"Downloading Google icon from: www.google.com{icon_path}")
        
        # Receive response
        response = b''
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            response += data
        
        # Separate headers and image data
        if b'\r\n\r\n' in response:
            headers, _, image_data = response.partition(b'\r\n\r\n')
            
            # Save image
            filename = "google_icon.png"
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f"Image saved as {filename}")
        else:
            print("Failed to download image: Invalid response format")
    except Exception as e:
        print(f"[!] Error in download_google_icon: {e}")

def download_image_https(hostname, proxy_host, proxy_port, context):
    try:
        # Create a new connection to the hostname for the image
        sock = socks.socksocket()
        sock.set_proxy(socks.HTTP, proxy_host, proxy_port)
        sock.connect((hostname, 443))
        ssock = context.wrap_socket(sock, server_hostname=hostname)
        
        # Use Google's favicon API path
        icon_path = "/s2/favicons?domain=google.com&sz=128"
        request = b"GET " + icon_path.encode() + b" HTTP/1.1\r\nHost: " + hostname.encode() + b"\r\nConnection: close\r\n\r\n"
        ssock.sendall(request)
        
        print(f"Downloading image from: {hostname}{icon_path}")
        
        response = b''
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            response += data
        
        if b'\r\n\r\n' in response:
            headers, _, image_data = response.partition(b'\r\n\r\n')
            filename = "downloaded_image.png"
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f"Image saved as {filename}")
        else:
            print("Failed to download image: Invalid response format")
        ssock.close()
    except Exception as e:
        print(f"[!] Error in download_image_https: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: ./script.py hostname")
        sys.exit(1)
        
    hostname = sys.argv[1]
    port = 443
    proxy_host = "proxy62.iitd.ac.in"
    proxy_port = 3128
    cadir = '/etc/ssl/certs'

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
        context.load_verify_locations(cafile='./certs/ca-certificates.crt')
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True

        ssock = context.wrap_socket(sock, server_hostname=hostname, do_handshake_on_connect=False)
        print("[+] Starting TLS handshake...", flush=True)
        ssock.do_handshake()
        print("[+] Cipher used:", ssock.cipher())
        print("[+] TLS handshake completed\n", flush=True)

        # Print cert
        cert = ssock.getpeercert()
        print("[+] Server certificate:")
        pprint.pprint(cert)
        
        while True:
            print("\nMenu:")
            print("1. Send HTTP request")
            print("2. Send HTTP request to download Google icon")
            print("3. Download image using HTTPS request")
            print("4. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                send_http_request(ssock, hostname)
            elif choice == '2':
                # Create a new connection to www.google.com for the icon
                icon_sock = socks.socksocket()
                icon_sock.set_proxy(socks.HTTP, proxy_host, proxy_port)
                icon_sock.connect(("www.google.com", 443))
                icon_ssock = context.wrap_socket(icon_sock, server_hostname="www.google.com")
                download_google_icon(icon_ssock, "www.google.com")
                icon_ssock.close()
            elif choice == '3':
                download_image_https("www.google.com", proxy_host, proxy_port, context)
            elif choice == '4':
                break
            else:
                print("Invalid choice")

        # Close the TLS Connection
        ssock.shutdown(socket.SHUT_RDWR)
        ssock.close()
        print("[+] Connection closed cleanly", flush=True)

    except Exception as e:
        print(f"[!] Error: {e}", flush=True)

if __name__ == "__main__":
    main()

