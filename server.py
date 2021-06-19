import socket


def Serverke(game):
    TCP_IP = socket.gethostbyname(socket.gethostname())
    print(TCP_IP)
    TCP_PORT = 5005
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print ('Connection address:', addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        if bytes.decode(data) == "vege": break
        print( "received data:", bytes.decode(data))
        conn.send(data)  # echo
    conn.close()

if __name__ in "__main__":
    Serverke("ads")