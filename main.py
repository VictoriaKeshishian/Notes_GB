from tkinter import *
from Note import *

root = Tk()
root.title('Заметки')
root.geometry('600x700')

menu_bar = Menu(root)
file_menu = Menu(menu_bar)

def new_file():
    notes.new_file()
def save_as():
    notes.save_as()
def open_file():
    notes.open_file()

file_menu.add_command(label="Новая заметка", command=new_file)
file_menu.add_command(label="Сохранить как", command=save_as)
file_menu.add_command(label="Открыть", command=open_file)

menu_bar.add_cascade(label="Файл", menu=file_menu)


text = Text(root, width=600, height=700)
text.pack()

notes = Notes(text)

root.config(menu=menu_bar)
root.mainloop()
