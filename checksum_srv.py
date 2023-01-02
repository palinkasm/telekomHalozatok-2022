from socket import socket, AF_INET, SOCK_STREAM
from select import select
import sys
import time


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


server_addr = (sys.argv[1], int(sys.argv[2]))

bufferSize = 1024

keptData = []
#     {"fileID":,
#      "md5HASH":,
#      "bytes":,
#      "timeOfArrival":,
#      "timeOfValidity":
#     }

with socket(AF_INET, SOCK_STREAM) as checkServer:
    checkServer.bind(server_addr)
    checkServer.listen(1)

    sockets = [checkServer]

    while True:

        toDELETE = []
        for data in keptData:
            if (time.time() - data["timeOfArrival"]) > float(data["timeOfValidity"]):
                print("DELETING DUE TO TIMEOUT: ", data)
                toDELETE.append(data)
        for data in toDELETE:
            keptData.remove(data)

        r, w, e = select(sockets, [], [], 1)
        if not (r or w or e):
            continue

        for s in r:
            if s is checkServer:
                client, client_addr = s.accept()
                sockets.append(client)
                print("CONNECTED: ", client_addr)
            else:
                data = s.recv(bufferSize).decode()
                if not data:
                    sockets.remove(s)
                    s.close()
                else:
                    mssg = messageProcesser(data)
                    if mssg[0] == 'BE':
                        keptData.append({
                            "fileID": mssg[1],
                            "md5HASH": mssg[4],
                            "bytes": mssg[3],
                            "timeOfArrival": time.time(),
                            "timeOfValidity": mssg[2]
                        })
                    elif mssg[0] == 'KI':
                        toDELETE = []
                        for data in keptData:
                            if data["fileID"] == mssg[1]:
                                s.sendall((str(data["bytes"]) + "|" + str(data["md5HASH"])).encode())
                                toDELETE.append(data)
                        for data in toDELETE:
                            keptData.remove(data)
