import ssl
import socket
import time
import csv

hosts = [
    "www.google.com",
    "www.cloudflare.com",
    "www.github.com",
    "www.amazon.com",
    "www.microsoft.com",
    "www.wikipedia.org",
    "www.stackoverflow.com",
    "www.reddit.com",
    "www.nytimes.com",
    "www.bbc.com"
]

results = []

for host in hosts:
    for attempt in range(3):  # 3 attempts per host for averaging
        try:
            ctx = ssl.create_default_context()
            start = time.perf_counter()
            with socket.create_connection((host, 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    elapsed = time.perf_counter() - start
                    version = ssock.version()
                    cipher = ssock.cipher()
                    results.append({
                        'host': host,
                        'attempt': attempt + 1,
                        'tls_version': version,
                        'cipher_suite': cipher[0],
                        'cipher_bits': cipher[2],
                        'handshake_time_sec': round(elapsed, 4)
                    })
                    print(f"{host} | {version} | {cipher[0]} | {elapsed:.4f}s")
        except Exception as e:
            print(f"FAILED {host}: {e}")

# Save to CSV
with open('captures/tls_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nDone! Results saved to captures/tls_results.csv")
