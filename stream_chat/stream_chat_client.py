import tkinter as tk
import cv2
from PIL import Image, ImageTk
import socket
import threading


# 웹캠 갱신 함수
def update():
    try:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            label.config(image=photo)
            label.image = photo
    except cv2.error as e:
        print("Error: can't grab frame -", str(e))

    client_window.after(10, update)  # 수정: client_window로 변경


# 메시지 보내기 함수
def send_message():
    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)
    # 메시지를 서버로 전송
    try:
        client_socket.send(message.encode('utf-8'))
    except socket.error as e:
        print("Error: can't send message -", str(e))


# 서버로부터 메시지 받기 함수
def receive_message():
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, "상대방: " + data + "\n")
            chat_text.config(state=tk.DISABLED)
        except ConnectionResetError:
            break


# 클라이언트 GUI 초기화
client_window = tk.Tk()
client_window.title("Stream_client")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

# 라벨 위젯을 사용하여 영상 표시 (80%)
label = tk.Label(client_window)
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(client_window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 입력 필드 (20%)
entry = tk.Entry(client_window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 보내기 버튼 (20%)
send_button = tk.Button(client_window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# 행 및 열 가중치 설정
client_window.grid_rowconfigure(0, weight=1)
client_window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
client_window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

# 갱신 함수 호출
update()

# TCP 클라이언트 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(('localhost', 12345))
except socket.error as e:
    print("Error: can't connect to the server -", str(e))
    client_window.destroy()

# 채팅 수신 스레드 시작
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# GUI 시작
client_window.mainloop()

# 스레드 종료 및 웹캠 해제
receive_thread.join()
cap.release()