from socket import *
from select import *

sock_list = [] # 데이터 수신 또는 연결 소켓 목록
sock = socket() # 옵션이 없으면 TCP 소켓 사용
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock_list.append(sock)
sock.connect(('localhost', 2500))

while 1:
    r_sock, w_sock, e_sock = select(sock_list, [], [], 0) # 비블록킹 모드로 동작
    if r_sock: # 데이터 수신한 소켓 조사
        for s in r_sock:
            if s == sock: # 수신 소켓이 자기자신
                msg = sock.recv(1024).decode()
                print("Received: ", msg)
    smsg = input("msg to send: ") # 메세지 송신
    sock.send(smsg.encode())