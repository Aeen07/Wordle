import customtkinter as ctk
import tkinter as tk
import threading
from PIL import Image
from collections import defaultdict
import random
import time
import os
import sys

root = ctk.CTk(fg_color='white')
root.title('Wordle')
x = int(root.winfo_screenwidth()/2 - 500/2)
y =int(root.winfo_screenheight()/2 - 680/2)
root.geometry(f'1550x800+{-10}+{0}')
all_answers = []

ctk.set_appearance_mode('white')
ctk.set_default_color_theme("dark-blue")

global letter_pos, current_line, answer_text, is_deleted, is_enter
letter_pos = 1
current_line = 1
answer_text = []
is_deleted = False
is_enter = False

def keyboard_func(text):
    global letter_pos,current_line, answer_text, is_enter, is_deleted
    if is_enter == False:
        if letter_pos <= 5 or is_deleted:
            buttons_dict[current_line][letter_pos].config(text = text, highlightbackground = '#878a8c')
            answer_text.append(text.lower())
            letter_pos += 1
            is_deleted = False
        else:
            print('not enough letters!')
    else:
        answer_text = []
        buttons_dict[current_line][letter_pos].config(text = text, highlightbackground = '#878a8c')
        answer_text.append(text.lower())
        letter_pos += 1
        is_enter = False

def enter():
    global letter_pos, current_line, is_enter
    if letter_pos < 5:
        print('not eligible')
    else: 
        print(answer_text)
        letters_correctly = ''
        if (''.join(answer_text).lower() in all_words):
            for i, letter in enumerate(answer_text):
                if letter == random_word[i]:
                    buttons_dict[current_line][i + 1].config(bg = '#6aaa64', fg = 'white', highlightthickness = 0)
                    globals()[f"btn{letter.upper()}"].configure(fg_color = '#6aaa64', text_color = 'white', hover_color = '#6aaa64')
                    letters_correctly += random_word[i]
                elif letter in random_word and letter not in letters_correctly:
                    buttons_dict[current_line][i + 1].config(bg = '#c9b458', fg = 'white', highlightthickness = 0)
                    globals()[f"btn{letter.upper()}"].configure(fg_color = '#c9b458', text_color = 'white', hover_color = '#c9b458')
                else:
                    buttons_dict[current_line][i + 1].config(bg = '#787c7e', fg = 'white', highlightthickness = 0)
                    globals()[f"btn{letter.upper()}"].configure(fg_color = '#787c7e', text_color = 'white', hover_color = '#787c7e')
            if ''.join(answer_text) == random_word :
                popup_gg.place(x = 728, y = 125)
                t1 = threading.Thread(target=delay_close, args=(popup_gg,))
                t1.start()

            is_enter = True
            
            letter_pos = 1
            current_line += 1
            
        else:
            popup_notinwords.place(x = 710, y = 125)
            t1 = threading.Thread(target=delay_close, args=(popup_notinwords,))
            t1.start()

def delay_close(item):
    time.sleep(2)
    item.place_forget()
    os.execl(sys.executable, sys.executable, * sys.argv)
    return

def random_choose():
    with open('wordle/wordle_words.txt') as f:
        words = f.read().splitlines()
        return random.choice(words), words
    
random_word, all_words = random_choose()
print(random_word)

def delete_word():
    global is_deleted, letter_pos, current_line
    if letter_pos > 1:
        answer_text.pop()
        letter_pos -= 1
        is_deleted = True
        buttons_dict[current_line][letter_pos].config(text = '', highlightbackground = '#d3d6da')
        print(letter_pos)

root.columnconfigure((0,1,2), weight=1, uniform ='x')
root.rowconfigure(0, weight=1, uniform='x')
screen_frame = ctk.CTkFrame(root, fg_color= 'transparent')
screen_frame.grid(row = 0, column = 1, sticky = 'nesw')

#base grid
screen_frame.rowconfigure(0, weight=25, uniform='a')
screen_frame.rowconfigure(1, weight=10, uniform='a')
screen_frame.columnconfigure(0, weight=1, uniform='a')

#keyboard frame
keyboard_frame = ctk.CTkFrame(screen_frame, fg_color='transparent')
keyboard_frame.grid(row = 1, column = 0, sticky = 'nesw')

#keyboard lines
frame1 = ctk.CTkFrame(keyboard_frame, fg_color='transparent')
frame2 = ctk.CTkFrame(keyboard_frame, fg_color='transparent')
frame3 = ctk.CTkFrame(keyboard_frame, fg_color='transparent')
frame1.pack(fill = 'both', expand = True)
frame2.pack(fill = 'both', expand = True, padx = 33)
frame3.pack(fill = 'both', expand = True)

#frame1
frame1.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight= 1, uniform='b')
frame1.rowconfigure(0, weight=1, uniform='b')
btnQ = ctk.CTkButton(frame1, text='Q', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('Q'))
btnW = ctk.CTkButton(frame1, text='W', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('W'))
btnE = ctk.CTkButton(frame1, text='E', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('E'))
btnR = ctk.CTkButton(frame1, text='R', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('R'))
btnT = ctk.CTkButton(frame1, text='T', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('T'))
btnY = ctk.CTkButton(frame1, text='Y', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('Y'))
btnU = ctk.CTkButton(frame1, text='U', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('U'))
btnI = ctk.CTkButton(frame1, text='I', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('I'))
btnO = ctk.CTkButton(frame1, text='O', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('O'))
btnP = ctk.CTkButton(frame1, text='P', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('P'))
btnQ.grid(row = 0, column = 0)
btnW.grid(row = 0, column = 1)
btnE.grid(row = 0, column = 2)
btnR.grid(row = 0, column = 3)
btnT.grid(row = 0, column = 4)
btnY.grid(row = 0, column = 5)
btnU.grid(row = 0, column = 6)
btnI.grid(row = 0, column = 7)
btnO.grid(row = 0, column = 8)
btnP.grid(row = 0, column = 9)

#frame2
frame2.columnconfigure((0,1,2,3,4,5,6,7,8), weight= 1, uniform='c')
frame2.rowconfigure(0, weight=1, uniform='c')
btnA = ctk.CTkButton(frame2, text='A', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('A'))
btnS = ctk.CTkButton(frame2, text='S', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('S'))
btnD = ctk.CTkButton(frame2, text='D', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('D'))
btnF = ctk.CTkButton(frame2, text='F', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('F'))
btnG = ctk.CTkButton(frame2, text='G', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('G'))
btnH = ctk.CTkButton(frame2, text='H', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('H'))
btnJ = ctk.CTkButton(frame2, text='J', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('J'))
btnK = ctk.CTkButton(frame2, text='K', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('K'))
btnL = ctk.CTkButton(frame2, text='L', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('L'))
btnA.grid(row = 0, column = 0)
btnS.grid(row = 0, column = 1)
btnD.grid(row = 0, column = 2)
btnF.grid(row = 0, column = 3)
btnG.grid(row = 0, column = 4)
btnH.grid(row = 0, column = 5)
btnJ.grid(row = 0, column = 6)
btnK.grid(row = 0, column = 7)
btnL.grid(row = 0, column = 8)

#frame3
img_backspace = ctk.CTkImage(Image.open('Image Editor/backspace2.png'))
frame3.columnconfigure((0,1,2,3,4,5,6,7,8), weight= 1)
frame3.rowconfigure(0, weight=1, uniform='c')
btnENTER = ctk.CTkButton(frame3, text='ENTER', height= 58, width = 75, text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', font = ('Helvetica', 12 , 'bold'), command=enter)
btnZ = ctk.CTkButton(frame3, text='Z', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('Z'))
btnX = ctk.CTkButton(frame3, text='X', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('X'))
btnC = ctk.CTkButton(frame3, text='C', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('C'))
btnV = ctk.CTkButton(frame3, text='V', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('V'))
btnB = ctk.CTkButton(frame3, text='B', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('B'))
btnN = ctk.CTkButton(frame3, text='N', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('N'))
btnM = ctk.CTkButton(frame3, text='M', height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = lambda : keyboard_func('M'))
btnBACK = ctk.CTkButton(frame3, image=img_backspace,text = '', height= 58, width = 75, text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command=delete_word)
btnENTER.grid(row = 0, column = 0)
btnZ.grid(row = 0, column = 1)
btnX.grid(row = 0, column = 2)
btnC.grid(row = 0, column = 3)
btnV.grid(row = 0, column = 4)
btnB.grid(row = 0, column = 5)
btnN.grid(row = 0, column = 6)
btnM.grid(row = 0, column = 7)
btnBACK.grid(row = 0, column = 8)

#answer frame
base_frame = ctk.CTkFrame(screen_frame, fg_color='transparent')
base_frame.grid(row = 0, column = 0, sticky = 'nesw', pady = (0, 10))

base_frame.rowconfigure((1,2,3,4,5,6), weight= 1, uniform='d')
base_frame.rowconfigure(0, weight= 2, uniform='d')
base_frame.columnconfigure((1,2,3,4,5), weight=4, uniform='d')
base_frame.columnconfigure((0,6), weight=5, uniform='d')

buttons_dict = defaultdict(dict)
num_questions = 6
answers_per_question = 5

for q in range(1, num_questions+1):
    for a in range(1, answers_per_question+1):
        curr_button = tk.Label(base_frame, text='', fg='black', bg='white', highlightbackground='#d3d6da', highlightthickness=2, font = ('Helvetica', 32, 'bold'))
        curr_button.grid(row = q, column = a, sticky = 'nesw', padx = 2.5, pady = 2.5)
        buttons_dict[q][a]=curr_button


def keyboard_to_char(e):
    if e.keycode == 8:
        delete_word()
    elif e.char == '\r':
        enter()
    elif e.char.lower() in 'qwertyuioplkjhgfdsazxcvbnm':
        keyboard_func(e.char.upper())

root.bind("<KeyRelease>", keyboard_to_char)



#title frame
title_frame = ctk.CTkFrame(root, fg_color='white', border_color='#d3d6da', border_width=1, corner_radius=0, width= 1550, height = 75)
title_frame.place(x=0, y=0)

title_label = ctk.CTkLabel(title_frame, text = 'Wordle', font = ('karnakpro-condensedblack', 40 ), width= 1550)
title_label.pack(pady = 10)

popup_gg = ctk.CTkLabel(root, text = 'Great', fg_color='#121212', text_color='white', font = ('Helvetica', 14), height=45, width = 80, corner_radius=4, anchor='center')
popup_notinwords = ctk.CTkLabel(root, text = 'Not in words list', fg_color='#121212', text_color='white', font = ('Helvetica', 14), height=45, width = 120, corner_radius=4)

root.mainloop()