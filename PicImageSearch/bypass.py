import requests
import socket

old_getaddrinfo = socket.getaddrinfo
dns_cache = {}
def new_getaddrinfo(*args):
    try:
        return dns_cache[args[:2]]
    except:
        return old_getaddrinfo(*args)
socket.getaddrinfo = new_getaddrinfo

def add_dns_cache(hostname,ip):
    global dns_cache
    key = (hostname.encode('ascii'),443)
    if dns_cache.get(key) == None:
        dns_cache[key] = []
    if ip.find(':') != -1:
        dns_cache[key].append((socket.AddressFamily.AF_INET6, socket.SocketKind.SOCK_STREAM, 0, '', (ip, 443, 0, 0)))
    else:
        dns_cache[key].append((socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM, 0, '', (ip, 443)))

def BypassHostname(hostname:str):
    """
    bypass DNS cache pollution
    """
    headers = {"Accept": "application/dns-json"}
    v4_params = {
        "name": hostname,
        "type": "A",
        "do": "false",
        "cd": "false",
    }

    v6_params = {
        "name": hostname,
        "type": "AAAA",
        "do": "false",
        "cd": "false",
    }
    DOH_URLS = (
        "https://dns.alidns.com/resolve",
        "https://1.0.0.1/dns-query",
        "https://1.1.1.1/dns-query",
        "https://cloudflare-dns.com/dns-query",
        "https://doh.dns.sb/dns-query",
    )

    for url in DOH_URLS:
        try:
            for params in [v4_params,v6_params]:
                response = requests.get(
                    url, headers=headers, params=params, timeout=5
                )
                for answer in response.json()["Answer"]:
                    add_dns_cache(hostname,str(answer["data"]))
            return
        except Exception:
            pass
    raise Exception("DNS query error")