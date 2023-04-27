import json
from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
import os
from tkinter import messagebox
import json
import shutil
from tkinter import Toplevel, Listbox, Scrollbar, END
import datetime
class Notes:
    file_name = None
    def __init__(self, text_widget, root):
        self.file_name = None
        self.text = text_widget
        self.root = root
    def new_file(self):
        global file_name
        file_name = "Без названия"
        self.text.delete('1.0', END)

    def save_as(self):
        out = asksaveasfile(mode='w', defaultextension='.json')
        if out is None:
            return
        data = self.text.get('1.0', END)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_data = {'created_at': now, 'content': data}
        try:
            json.dump(note_data, out)
            config = {'saved_files_dir': os.path.dirname(out.name)}
            with open('config.json', 'w') as f:
                json.dump(config, f)
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

    def read_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def open_all_notes(self):
        config = self.read_config()
        saved_files_dir = config.get('saved_files_dir', '')
        if not saved_files_dir:
            messagebox.showerror("Ошибка", "Путь к папке с заметками не задан в конфигурационном файле")
            return

        try:
            if not os.path.isdir(saved_files_dir):
                messagebox.showerror("Ошибка", f"Директория {saved_files_dir} не существует")
                return
            files = [f for f in os.listdir(saved_files_dir) if f.endswith('.json')]
            if not files:
                messagebox.showinfo("Информация", "Папка с заметками пуста")
                return

            # Создаем новое окно
            notes_window = Toplevel(self.root)
            notes_window.title("Список заметок")

            # Создаем Listbox и Scrollbar для него
            scrollbar = Scrollbar(notes_window, orient=VERTICAL)
            listbox = Listbox(notes_window, yscrollcommand=scrollbar.set)

            # Добавляем имена файлов в Listbox
            for file in files:
                full_path = os.path.join(saved_files_dir, file)
                try:
                    with open(full_path, 'r') as f:
                        data = json.load(f)
                        listbox.insert(END, file)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не могу прочитать файл {file}: {str(e)}")
                    return

            scrollbar.config(command=listbox.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            listbox.pack(side=LEFT, fill=BOTH, expand=True)

            # Добавляем обработчик события двойного щелчка на элементе списка
            def on_double_click(event):
                selection = listbox.curselection()
                if not selection:
                    return
                file_name = listbox.get(selection[0])
                full_path = os.path.join(saved_files_dir, file_name)
                try:
                    with open(full_path, 'r') as f:
                        note_data = json.load(f)
                        notes_window.destroy()
                        edit_window = Toplevel(self.root)
                        edit_window.title(file_name)
                        text_widget = Text(edit_window)
                        text_widget.pack(expand=True, fill=BOTH)
                        text_widget.insert('1.0', note_data['content'])
                        Notes(text_widget, self.root).file_name = full_path
                        # Добавляем информацию о дате и времени создания заметки
                        creation_time = note_data.get('created_at')
                        if creation_time:
                            text_widget.insert(END, f'\n\nДата и время создания: {creation_time}')
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не могу прочитать файл {file_name}: {str(e)}")

            def on_delete():
                selection = listbox.curselection()
                if not selection:
                    return
                file_name = listbox.get(selection[0])
                full_path = os.path.join(saved_files_dir, file_name)
                try:
                    os.remove(full_path)
                    listbox.delete(selection[0])
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не могу удалить файл {file_name}: {str(e)}")

            delete_button = Button(notes_window, text="Удалить", command=on_delete)
            delete_button.pack()

            listbox.bind('<Double-1>', on_double_click)
        except OSError:
            messagebox.showerror("Ошибка", f"Не могу прочитать файлы в директории {saved_files_dir}")
            return



