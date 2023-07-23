import socket
import threading
import time

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print("Waiting for connection...")
    return s

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        print("accept message is %s" % data.decode('utf-8'))
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

if __name__ == "__main__":
    s = create_socket()
    while True:
        sock,addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

