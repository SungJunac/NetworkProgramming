import socket
port = int(input("Port No: "))
address = ("localhost", port) # 주소는 항상 (ip, port) 튜플
BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address) #서버 연결 요청

while True:
    msg = input("Message to send: ")
    s.send(msg.encode())  # send a message to server
    # data = s.recv(BUFSIZE) #recive message from server
    # print("Recieved message: %s" %data.decode()) #바이트형을 문자열로 변환