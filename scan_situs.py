import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import re
import sys
import socket
import time
from urllib.parse import urlparse
from tqdm import tqdm
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

# === Konfigurasi Telegram ===
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

KEYWORDS_JUDI = [
    "judi", "casino", "bet", "poker", "slot", "togel", "sportsbook", "bandar", "taruhan",
    "sabung ayam", "domino", "dadu", "qq", "aduq", "adu ayam", "bola tangkas", "capsa",
    "bandarq", "qq online", "rolet", "blackjack", "baccarat", "agen bola"
]

KEYWORDS_PORNO = [
    "porn", "sex", "adult", "xxx", "nude", "pornography", "hentai", "erotic", "nsfw",
    "cam girl", "sex video", "adult video", "mature content"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SiteScanner/1.0)"
}

ICON_MAP = {
    'judi': '🎲 situs judi',
    'porno': '🔞 situs porno',
    'bukan': '✅ situs bukan'
}

def is_port_open(ip, port, timeout=3):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

def fetch_url(ip):
    urls = [f"http://{ip}", f"https://{ip}"]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=5, verify=False, allow_redirects=True)
            parsed = urlparse(r.url)
            path = parsed.path if parsed.path else "/"
            return r.text, parsed.scheme, path, True
        except:
            continue
    return "", "-", "-", False

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=' ', strip=True)

def detect_category(text):
    text = text.lower()
    for keyword in KEYWORDS_JUDI:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
            return "judi"
    for keyword in KEYWORDS_PORNO:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
            return "porno"
    return "bukan"

def get_ip_location(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        data = r.json()
        city = data.get('city', '')
        region = data.get('region', '')
        country = data.get('country', '')

        if city and region and city.lower() == region.lower():
            loc = f"{city}, {country}"
        else:
            loc = f"{city}, {region}, {country}"
        return f"{loc.strip(', ')} 🌍"
    except:
        return "Unknown 🌍"

def send_telegram_message(message):
    if TELEGRAM_TOKEN.startswith("YOUR") or TELEGRAM_CHAT_ID.startswith("YOUR"):
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass

def colorize_kategori(kategori):
    if kategori == 'judi':
        return Fore.YELLOW + ICON_MAP[kategori] + Style.RESET_ALL
    elif kategori == 'porno':
        return Fore.MAGENTA + ICON_MAP[kategori] + Style.RESET_ALL
    else:
        return Fore.GREEN + ICON_MAP[kategori] + Style.RESET_ALL

def scan_ip(ip):
    html, protokol, path, success = fetch_url(ip)
    lokasi = get_ip_location(ip)  # Tetap dapatkan lokasi meskipun situs tidak dapat diakses
    
    if not success:
        return (ip, 'bukan', lokasi, '-', '-', '❌ Situs tidak tersedia', '-', '-')
    
    text = extract_text(html)
    kategori = detect_category(text)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return (ip, kategori, lokasi, protokol, path, '✅ Akses berhasil', timestamp, html)

def main(file_path):
    try:
        with open(file_path, "r") as f:
            ips = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan!")
        return

    print("\nMulai proses scanning:\n")
    hasil = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scan_ip, ip): ip for ip in ips}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Progres", unit="ip", ncols=70, colour="cyan"):
            ip = futures[future]
            try:
                ip, kategori, lokasi, protokol, path, status, timestamp, html = future.result()

                colored_kategori = colorize_kategori(kategori)
                hasil.append(f"{ip: <18} | {lokasi: <25} | {colored_kategori: <15} | {protokol: <6} | {path: <12} | {Fore.GREEN + status + Style.RESET_ALL: <20}")
            except Exception as e:
                hasil.append(f"{ip: <18} | {'-': <25} | {'-': <15} | {'-': <6} | {'-': <12} | {Fore.RED + '❌ Error' + Style.RESET_ALL: <20}")

    # Output hasil ke terminal
    header = f"{'IP': <18} | {'Lokasi': <25} | {'Kategori': <15} | {'Prot.': <6} | {'Path': <12} | Status\n"
    print("\n" + header, end="")
    print("-" * 85)
    for line in hasil:
        print(line)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python3 scan_situs.py <file_daftar_ip>")
    else:
        main(sys.argv[1])
