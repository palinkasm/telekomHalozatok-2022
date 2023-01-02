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

m = hashlib.md5()

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)

    sockets = [server]

    client, client_addr = server.accept()
    sockets.append(client)
    mssg = client.recv(bufferSize).decode()
    # print("ÜZENET: ", mssg)
    client.close()
    server.close()

    Check = mssg.encode('utf-8')
    # print("~~~~~~~~\n" + str(Check) + "\n~~~~~~~~")
    m.update(Check)
    checkSumClient = socket(AF_INET, SOCK_STREAM)
    checkSumClient.connect(checksum_addr)
    checkSumClient.sendall(("KI|" + sys.argv[5]).encode())
    data = checkSumClient.recv(bufferSize).decode()
    gotHASH = messageProcesser(data)
    print(gotHASH)
    print(m.hexdigest())
    checkSumClient.close()

    if str(m.hexdigest()) == str(gotHASH[1]):
        print("CSUM OK")
        f = open("serverFile.txt", "a")
        f.write(mssg)
        f.close()
        server.close()
    else:
        print("CSUM CORRUPTED")

