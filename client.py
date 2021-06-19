import socket

TCP_IP = "192.168.1.3"
TCP_PORT = 5005
BUFFER_SIZE = 1024

def clientka(game):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    while True:
        MESSAGE = input()
        s.sendall(str.encode(MESSAGE))
        data = s.recv(BUFFER_SIZE)
        print(bytes.decode(data))
        if MESSAGE == "vege": break
        
    s.close()

if __name__ in "__main__":
    clientka("ads")
