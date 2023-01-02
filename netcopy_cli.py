import sys
from socket import socket, AF_INET, SOCK_STREAM
import hashlib


def messageProcesser(toDecode):
    message = []
    tmp = ""
    for letter in toDecode:
        if letter == '|':
            message.append(tmp)
            tmp = ""
        else:
            tmp += letter
    message.append(tmp)
    return message


bufferSize = 1024

server_addr = (sys.argv[1], int(sys.argv[2]))
checksum_addr = (sys.argv[3], int(sys.argv[4]))

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)
    file = open(sys.argv[6], 'rb')
    client.sendfile(file)
    file.close()
    client.close()
    #  print("Sent to server: \n" + toCheckSum + "\n~~~~~~~~~")

with socket(AF_INET, SOCK_STREAM) as client_checks:
    client_checks.connect(checksum_addr)
    reader = open(sys.argv[6], 'rb')
    toCheckSum = reader.read().decode().encode('utf-8')
    # print("~~~~~~~~\n" + str(toCheckSum) + "\n~~~~~~~~")
    m = hashlib.md5()
    m.update(toCheckSum)
    # print(m.hexdigest() + '\n~~~~~~~~~')
    client_checks.sendall(("BE|" + sys.argv[5] + "|60|" + str(str(m.hexdigest()).__sizeof__()) + "|"
                           + str(m.hexdigest())).encode())
    client_checks.close()
