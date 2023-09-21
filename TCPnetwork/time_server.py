# time_server.py
import socket
import time

# TCP 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('', 5000) #'': 임의주소, 포트번호 = 5000
s.bind(address) #소켓과 주소 결합
s.listen(5) #연결 대기 , 5개까지 동시 수용

while True:
    client, addr = s.accept() # 연결 허용
    print("Conneciton requested form ", addr)
    client.send(time.ctime(time.time()).encode()) # 현재 시간을 전송
    client.close() #소켓종료