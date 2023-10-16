import tkinter as tk
import cv2
from PIL import Image, ImageTk
import socket
import threading

# 화면 갱신 함수
def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(5, update)

# 메시지 보내기 함수
def send_message():
    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)
    # 여기서 클라이언트에게 메시지를 전송하는 코드를 추가하세요

# 클라이언트와 통신하는 스레드 함수
def client_thread(conn, addr):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, "상대방: " + data + "\n")
            chat_text.config(state=tk.DISABLED)
    except ConnectionResetError:
        pass
    conn.close()

# GUI 초기화
window = tk.Tk()
window.title("Stream_server")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

# 라벨 위젯을 사용하여 영상 표시 (80%)
label = tk.Label(window)
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 입력 필드 (20%)
entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 보내기 버튼 (20%)
send_button = tk.Button(window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# 행 및 열 가중치 설정
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

# 갱신 함수 호출
update()

# TCP 서버 설정
HOST = 'localhost'  # 서버 주소
PORT = 12345  # 포트 번호
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# 클라이언트 연결 받기
conn, addr = server_socket.accept()
print('Connected by', addr)

# 클라이언트와 통신하는 스레드 시작
client_thread = threading.Thread(target=client_thread, args=(conn, addr))
client_thread.start()

# GUI 시작
window.mainloop()

# 스레드 종료 및 웹캠 해제
client_thread.join()
cap.release()