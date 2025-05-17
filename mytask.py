import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 My Task")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.tasks = []  


        self.task_entry = tk.Entry(root, font=("Arial", 14))
        self.task_entry.pack(pady=10, padx=10, fill=tk.X)

        self.date_var = tk.StringVar()
        self.date_options = self.generate_date_options()
        self.date_var.set(self.date_options[0])  

        self.date_menu = tk.OptionMenu(root, self.date_var, *self.date_options)
        self.date_menu.config(font=("Arial", 12))
        self.date_menu.pack(pady=5)

        add_btn = tk.Button(root, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white")
        add_btn.pack(pady=5)

        self.task_listbox = tk.Listbox(root, font=("Arial", 12), selectmode=tk.SINGLE, activestyle='none')
        self.task_listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        delete_btn = tk.Button(root, text="Delete Selected Task", command=self.delete_task, bg="#f44336", fg="white")
        delete_btn.pack(pady=5)

        save_btn = tk.Button(root, text="Save Tasks", command=self.save_tasks)
        save_btn.pack(side=tk.LEFT, padx=10, pady=5)

        load_btn = tk.Button(root, text="Load Tasks", command=self.load_tasks)
        load_btn.pack(side=tk.RIGHT, padx=10, pady=5)

    def generate_date_options(self):
        today = datetime.today()
        return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 30)]

    def add_task(self):
        task = self.task_entry.get().strip()
        date = self.date_var.get()
        if task:
            self.tasks.append((date, task))
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for date, task in self.tasks:
            self.task_listbox.insert(tk.END, f"{date} - {task}")

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for date, task in self.tasks:
                    file.write(f"{date}|{task}\n")

    def load_tasks(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path and os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.tasks = []
                for line in file:
                    if '|' in line:
                        date, task = line.strip().split("|", 1)
                        self.tasks.append((date, task))
            self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
