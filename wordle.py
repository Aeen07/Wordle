import customtkinter as ctk
import tkinter as tk
import threading
from PIL import Image
from collections import defaultdict
import random
import time
import os
import sys

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='white')
        self.title('Wordle')
        self.geometry(f'1550x800+{-10}+{0}')
        ctk.set_appearance_mode('white')

        self.columnconfigure((0,1,2), weight=1, uniform='x')
        self.rowconfigure(0, weight=1, uniform='x')

        screen_frame = ctk.CTkFrame(self, fg_color= 'transparent')
        screen_frame.grid(row = 0, column = 1, sticky = 'nesw')

        screen_frame.rowconfigure(0, weight=25, uniform='a')
        screen_frame.rowconfigure(1, weight=10, uniform='a')
        screen_frame.columnconfigure(0, weight=1, uniform='a')

        random_word, all_words = self.random_choose()
        print(random_word)
      
        popup_gg = ctk.CTkLabel(self, text = 'Great', fg_color='#121212', text_color='white', font = ('Helvetica', 14), height=45, width = 80, corner_radius=4, anchor='center')
        popup_notinwords = ctk.CTkLabel(self, text = 'Not in words list', fg_color='#121212', text_color='white', font = ('Helvetica', 14), height=45, width = 120, corner_radius=4)

        self.answers = Answers(screen_frame)
        self.keyboard = Keyboard(screen_frame, self.answers, random_word, all_words, popup_gg, popup_notinwords)
        self.title = Title(self)

        self.bind("<KeyRelease>", self.keyboard_to_char)
    
    def random_choose(self):
        with open('wordle/wordle_words.txt') as f:
            words = f.read().splitlines()
            return random.choice(words), words
        
    def keyboard_to_char(self, e):
        if e.keycode == 8:
            self.keyboard.delete_word()
        elif e.char == '\r':
            self.keyboard.enter()
        elif e.char.isalpha:
            self.keyboard.keyboard_func(e.char.upper())


    
class Keyboard(ctk.CTkFrame):
    def __init__(self, parent, answers, random_word, all_words, popup_gg, popup_notinwords):
        super().__init__(parent, fg_color='transparent')
        self.letter_pos = 1
        self.current_line = 1
        self.answer_text = ''
        self.is_enter = False
        self.grid(row = 1, column = 0, sticky = 'nesw')
        self.answers = answers
        self.random_word = random_word
        self.all_words = all_words
        self.popup_gg = popup_gg
        self.popup_notinwords = popup_notinwords

        #keyboard lines
        frame1 = ctk.CTkFrame(self, fg_color='transparent')
        frame2 = ctk.CTkFrame(self, fg_color='transparent')
        frame3 = ctk.CTkFrame(self, fg_color='transparent')
        frame1.pack(fill = 'both', expand = True)
        frame2.pack(fill = 'both', expand = True, padx = 33)
        frame3.pack(fill = 'both', expand = True)

        #frame1
        frame1.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight= 1, uniform='b')
        frame1.rowconfigure(0, weight=1, uniform='b')

        self.keyboards_dict = defaultdict(dict)
        ascii_chars = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        for c in range (10):
            callback = lambda n=c: self.keyboard_func(ascii_chars[n])
            curr_btn = ctk.CTkButton(frame1, text= ascii_chars[c], height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = callback)
            curr_btn.grid(row = 0, column = c)
            self.keyboards_dict[ascii_chars[c]] = curr_btn

        #frame2
        frame2.columnconfigure((0,1,2,3,4,5,6,7,8), weight= 1, uniform='c')
        frame2.rowconfigure(0, weight=1, uniform='c')

        for c in range (10, 19):
            callback = lambda n=c: self.keyboard_func(ascii_chars[n])
            curr_btn = ctk.CTkButton(frame2, text= ascii_chars[c], height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = callback)
            curr_btn.grid(row = 0, column = c - 10)
            self.keyboards_dict[ascii_chars[c]] = curr_btn

        #frame3
        img_backspace = ctk.CTkImage(Image.open('Image Editor/backspace2.png'))
        frame3.columnconfigure((0,1,2,3,4,5,6,7,8), weight= 1)
        frame3.rowconfigure(0, weight=1, uniform='c')
        btnENTER = ctk.CTkButton(frame3, text='ENTER', height= 58, width = 75, text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', font = ('Helvetica', 12 , 'bold'), command= self.enter)

        for c in range (19, 26):
            callback = lambda n=c: self.keyboard_func(ascii_chars[n])
            curr_btn = ctk.CTkButton(frame3, text= ascii_chars[c], height= 58, width = 42, font = ('Helvetica', 20 , 'bold'), text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command = callback)
            curr_btn.grid(row = 0, column = c - 18)
            self.keyboards_dict[ascii_chars[c]] = curr_btn

        btnBACK = ctk.CTkButton(frame3, image=img_backspace,text = '', height= 58, width = 75, text_color= 'black', fg_color= '#d3d6da',hover_color='#d3d6da', command=self.delete_word)
        btnENTER.grid(row = 0, column = 0)
        btnBACK.grid(row = 0, column = 8)



    def keyboard_func(self, text):
        if self.is_enter == False:
            if self.letter_pos <= 5:
                self.answers.buttons_dict[self.current_line][self.letter_pos].config(text = text, highlightbackground = '#878a8c')
                self.answer_text += text.lower()
                self.letter_pos += 1
            else:
                print('not enough letters!')
        else:
            answer_text = ''
            self.answers.buttons_dict[self.current_line][self.letter_pos].config(text = text, highlightbackground = '#878a8c')
            answer_text += text.lower()
            self.letter_pos += 1
            self.is_enter = False

    def enter(self):
        if self.letter_pos < 5:
            print('not eligible')
        else: 
            print(self.answer_text)
            letters_correctly = ''
            if self.answer_text in self.all_words:
                for i, letter in enumerate(self.answer_text):
                    if letter == self.random_word[i]:
                        self.answers.buttons_dict[self.current_line][i + 1].config(bg = '#6aaa64', fg = 'white', highlightthickness = 0)
                        self.keyboards_dict[letter.upper()].configure(fg_color = '#6aaa64', text_color = 'white', hover_color = '#6aaa64')
                        letters_correctly += self.random_word[i]
                    elif letter in self.random_word and letter not in letters_correctly:
                        self.answers.buttons_dict[self.current_line][i + 1].config(bg = '#c9b458', fg = 'white', highlightthickness = 0)
                        self.keyboards_dict[letter.upper()].configure(fg_color = '#c9b458', text_color = 'white', hover_color = '#c9b458')
                    else:
                        self.answers.buttons_dict[self.current_line][i + 1].config(bg = '#787c7e', fg = 'white', highlightthickness = 0)
                        self.keyboards_dict[letter.upper()].configure(fg_color = '#787c7e', text_color = 'white', hover_color = '#787c7e')
                if self.answer_text == self.random_word :
                    self.popup_gg.place(x = 728, y = 125)
                    t1 = threading.Thread(target=self.delay_close, args=(self.popup_gg,))
                    t1.start()

                self.is_enter = True
            
                self.letter_pos = 1
                self.current_line += 1
            
            else:
                self.popup_notinwords.place(x = 710, y = 125)
                t1 = threading.Thread(target=self.delay_close, args=(self.popup_notinwords,))
                t1.start()

    def delete_word(self):
        if self.letter_pos > 1:
            self.answer_text = self.answer_text[:-1]
            self.letter_pos -= 1
            self.answers.buttons_dict[self.current_line][self.letter_pos].config(text = '', highlightbackground = '#d3d6da')

    def delay_close(self, item):
        time.sleep(2)
        item.place_forget()
        if item.cget('text') == 'Great' : os.execl(sys.executable, sys.executable, * sys.argv)
        return

class Answers(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='transparent')
        self.grid(row = 0, column = 0, sticky = 'nesw', pady = (0, 10))

        self.rowconfigure((1,2,3,4,5,6), weight= 1, uniform='d')
        self.rowconfigure(0, weight= 2, uniform='d')
        self.columnconfigure((1,2,3,4,5), weight=4, uniform='d')
        self.columnconfigure((0,6), weight=5, uniform='d')

        self.buttons_dict = defaultdict(dict)
        num_questions = 6
        answers_per_question = 5

        for q in range(1, num_questions+1):
            for a in range(1, answers_per_question+1):
                curr_button = tk.Label(self, text='', fg='black', bg='white', highlightbackground='#d3d6da', highlightthickness=2, font = ('Helvetica', 32, 'bold'))
                curr_button.grid(row = q, column = a, sticky = 'nesw', padx = 2.5, pady = 2.5)
                self.buttons_dict[q][a]=curr_button

class Title(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='white', border_color='#d3d6da', border_width=1, corner_radius=0, width= 1550, height = 75)
        self.place(x=0, y=0)

        title_label = ctk.CTkLabel(self, text = 'Wordle', font = ('karnakpro-condensedblack', 40 ), width= 1550)
        title_label.pack(pady = 10)


if __name__ == '__main__' :
    root = App()
    root.mainloop()
