import socket
import sys

# 포트 번호 설정
port = 2600
BUFSIZE = 1024

# 서버 소켓 생성 및 클라이언트 연결 대기
s_sock = socket.socket()
host = ''
s_sock.bind((host,port))
s_sock.listen(1)

print("Waiting for Connection")

c_sock, addr = s_sock.accept()
print("connection from", addr)
msg = c_sock.recv(1024)
print(msg.decode())
filename = input("파일 이름")

c_sock.send(filename.encode())

with open("./dummy/"+filename, 'rb') as f:
    c_sock.sendfile(f,0)

print('sending complete')
c_sock.close()