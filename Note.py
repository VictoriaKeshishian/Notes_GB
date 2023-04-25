import json
from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile

class Notes:
    file_name = None
    def __init__(self, text_widget):
        self.file_name = None
        self.text = text_widget
    def new_file(self):
        global file_name
        file_name = "Без названия"
        self.text.delete('1.0', END)
    def save_as(self):
        out = asksaveasfile(mode='w', defaultextension='.json')
        if out is None:
            return
        data = self.text.get('1.0', END)
        try:
            json.dump(data, out)
        except Exception:
            messagebox.showerror("Не могу сохранить!")
    def open_file(self):
        global file_name
        inp = askopenfile(mode='r')
        if inp is None:
            return
        file_name = inp.name
        data = inp.read()
        if data:
            try:
                data = json.loads(data)
                self.text.delete('1.0', END)
                self.text.insert('1.0', data)
            except Exception:
                messagebox.showerror("Ошибка при загрузке файла!", "Не удалось загрузить данные из файла.")
