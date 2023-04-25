from tkinter import *

root = Tk()
root.title('Заметки')
root.geometry('600x700')

menu_bar = Menu(root)
file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Файл", menu=file_menu)

text = Text(root, width=600, height=700)
text.pack()

root.config(menu=menu_bar)
root.mainloop()
