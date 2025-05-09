#!/usr/bin/env python3
import subprocess
import re, platform, socket
import threading

def main():
    if not platform.system() == "Linux":
        print("Sadece Linux Sistemlerde çalışır.")
    else:
        liste = net_check()
        print(liste)
        secim = input("Bu bilgisayarın adresini seçin: 0/1/2 : ")
        if secim.isdigit() and int(secim) <= len(liste)-1:
            print("Seçilen Adres: ",liste[int(secim)],
                  "\nSeçilen adres için 1..255 arası tarama yapılacak onaylıyor musunuz?")
            tarama(liste[int(secim)])
        else:
            print("Seçim yapılmadı...")


def tarama(ip_addr):
    ipadres= str(ip_addr).split(".")
    a = ipadres[0]
    b = ipadres[1]
    c = ipadres[2]
    for i in range(1, 256): # 255 olması için
        hedef = str(a+"."+b+"."+c+"."+str(i))
        for x in MOST_PORTS:
            t1 = threading.Thread(target=kontrol, args=(hedef,x))
            t1. start()
    while 1:
        if len(SONUCLAR) == 255:
            break
    for s in SONUCLAR:
        print(s)


def kontrol(ip, port):
    print("Taranıyor...", ip, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((str(ip),int(port)))
        sock.close()
        SONUCLAR.append(ip + ":" + str(port) + " Açık")
    except:
        SONUCLAR.append(ip + ":" + str(port) + " Kapalı")


def net_check():
    liste = []
    adresler = []
    bash_out = subprocess.check_output("ip addr", stderr=subprocess.STDOUT, shell=True)
    satirlar = bash_out.splitlines()
    for i in satirlar:
        liste.append(re.sub(r'(\s+)', ' ', str(i)))
    regex = r"\d+.\d+.\d+.\d+\/"
    for x in liste:
        aranan = re.findall(regex, x)
        if len(aranan):
            adresler.append((str(aranan[0]).replace("/", "")))
    return adresler


MOST_PORTS = [80]
SONUCLAR  = []

if __name__ == "__main__":
    main()
