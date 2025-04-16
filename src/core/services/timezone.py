import requests


def get_timezone_by_ip(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    return data.get("timezone")
