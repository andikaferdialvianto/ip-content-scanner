#!/bin/bash

# Spinner animasi
spinner() {
    local pid=$!
    local delay=0.1
    local spinstr='|/-\\'
    while ps -p $pid &>/dev/null; do
        for i in $(seq 0 3); do
            printf "\r[%c] Sedang memproses..." "${spinstr:$i:1}"
            sleep $delay
        done
    done
    printf "\r    \r"
}

# Cek akses root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "\e[31m✖ Harap jalankan script ini dengan sudo atau sebagai root.\e[0m"
    exit 1
fi

echo -e "\e[34m🔍 Mendeteksi jenis OS...\e[0m"

# Deteksi distro
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo -e "\e[31m✖ Tidak dapat mendeteksi OS. /etc/os-release tidak ditemukan.\e[0m"
    exit 1
fi

# Fungsi instalasi universal
install_common() {
    echo -e "\e[32m⚙️  Menginstal Python3 dan pip3...\e[0m"
    if command -v apt &>/dev/null; then
        (apt update && apt install -y python3 python3-pip) & spinner
    elif command -v dnf &>/dev/null; then
        (dnf install -y python3 python3-pip) & spinner
    elif command -v yum &>/dev/null; then
        (yum install -y python3 python3-pip) & spinner
    else
        echo -e "\e[31m✖ Tidak ditemukan manajer paket yang didukung.\e[0m"
        exit 1
    fi

    if ! command -v pip3 &>/dev/null; then
        echo -e "\e[33m⚠️  pip3 tidak ditemukan. Menginstal pip3...\e[0m"
        (python3 -m ensurepip --upgrade) & spinner
    fi
}

# Jalankan instalasi
install_common

# Membuat file requirements.txt
echo -e "\e[36m📝 Membuat file requirements.txt...\e[0m"
cat <<EOL > requirements.txt
requests
beautifulsoup4
selenium
python-whois
tabulate
tqdm
colorama
EOL

# Install dependencies Python
echo -e "\e[32m📦 Menginstal dependencies Python...\e[0m"
(pip3 install -r requirements.txt) & spinner

# Verifikasi instalasi
echo -e "\e[36m🔍 Memverifikasi instalasi...\e[0m"
python3 --version
pip3 list | grep -E 'requests|beautifulsoup4|selenium|tabulate|tqdm|colorama|whois'

# Bersih-bersih
rm -f requirements.txt
echo -e "\e[32m✅ Instalasi selesai dengan sukses!\e[0m"
