from socket import *
from select import *
from tkinter import *
import time

root = Tk() # 기본 윈도우 생성
btn_color = 'yellow' #버튼 색상
btn_text = 'ON' # 버튼 텍스트

# button click callback
def button_command():
    global sock, btn_text, btn_color # 매개변수를 전달하지 못하므로 전역 변수 사용
    if btn_text == 'ON': # 토글 모드
        btn_text = 'OFF'
        btn_color = 'blue'
    else:
        btn_text = 'ON'
        btn_color = 'red'
    LED_button.configure(text=btn_text, bg=btn_color)
    sock.send(btn_text.encode())

def handle():
    global root, sock, switch_state_label, sock_list
    #root.mainloop()
    r_sock, w_sock, e_sock = select([sock], [], [], 0)
    if r_sock:
        msg = sock.recv(1024).decode()
        print(msg)
        if msg.upper() == 'OFF':
            switch_state_label.configure(text='Switch is OFF')
        else:
            switch_state_label.configure(text='Switch is ON')
    root.after(200, handle)

LED_label = Label(text="LED") #LED 라벨
switch_label = Label(text="SWITCH") #SWITCH 라벨
switch_state_label = Label(text="Switch is OFF", fg='white') #switch 상태 라벨
LED_button = Button(text=btn_text, fg='black', bg=btn_color, \
                    command=button_command)  # button 위젯

#위젯 배치
LED_label.grid(row=0, column=0)
LED_button.grid(row=0, column=1)
switch_label.grid(row=1, column=0)
switch_state_label.grid(row=1, column=1, sticky=E)

#소켓을 생성하고 서버로 연결
sock = socket()
sock.connect(('localhost', 2500))

handle()
mainloop()

