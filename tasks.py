import tkinter as tk
from tkinter import messagebox, filedialog
import json

class Task:
    def __init__(self, task_id, description, due_date, priority):
        self.task_id = task_id
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False

    def complete_task(self):
        self.completed = True

    def edit_task(self, new_description, new_due_date, new_priority):
        self.description = new_description
        self.due_date = new_due_date
        self.priority = new_priority

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["task_id"], data["description"], data["due_date"], data["priority"])
        task.completed = data["completed"]
        return task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def edit_task(self, task_id, new_description, new_due_date, new_priority):
        for task in self.tasks:
            if task.task_id == task_id:
                task.edit_task(new_description, new_due_date, new_priority)

    def filter_tasks(self, keyword):
        return [task for task in self.tasks if keyword.lower() in task.description.lower()]

    def view_tasks(self):
        for task in self.tasks:
            print(f"Task ID: {task.task_id}")
            print(f"Description: {task.description}")
            print(f"Due Date: {task.due_date}")
            print(f"Priority: {task.priority}")
            print(f"Completed: {task.completed}")
            print("---------------")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            tasks_data = [task.to_dict() for task in self.tasks]
            json.dump(tasks_data, file, indent=2)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            tasks_data = json.load(file)
            self.tasks = [Task.from_dict(data) for data in tasks_data]

# Tkinter GUI
class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        # Ustawienia kolorystyczne dla trybu jasnego i ciemnego
        self.light_mode_bg = "white"
        self.light_mode_fg = "black"
        self.dark_mode_bg = "black"
        self.dark_mode_fg = "white"

        # Domyślnie ustaw tryb jasny
        self.bg_color = self.light_mode_bg
        self.fg_color = self.light_mode_fg

        self.task_manager = TaskManager()

        self.create_widgets()

    def create_widgets(self):
        # Przycisk zmiany trybu
        self.toggle_mode_button = tk.Button(self.master, text="Toggle Dark Mode", command=self.toggle_dark_mode, bg=self.bg_color, fg=self.fg_color)
        self.toggle_mode_button.pack(pady=10)

        # Lista zadań
        self.task_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, height=10, width=50, bg=self.bg_color, fg=self.fg_color)
        self.task_listbox.pack(pady=10)

        # Przyciski
        self.edit_button = tk.Button(self.master, text="Edit Task", command=self.edit_task, bg=self.bg_color, fg=self.fg_color)
        self.edit_button.pack(pady=5)

        self.remove_button = tk.Button(self.master, text="Remove Task", command=self.remove_task, bg=self.bg_color, fg=self.fg_color)
        self.remove_button.pack(pady=5)

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task, bg=self.bg_color, fg=self.fg_color)
        self.add_button.pack(pady=5)

        self.save_button = tk.Button(self.master, text="Save to File", command=self.save_to_file, bg=self.bg_color, fg=self.fg_color)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(self.master, text="Load from File", command=self.load_from_file, bg=self.bg_color, fg=self.fg_color)
        self.load_button.pack(pady=5)

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.task_id}: {task.description} (Priority: {task.priority})")

    def add_task(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Add Task")

        tk.Label(add_task_window, text="Description:", bg=self.bg_color, fg=self.fg_color).pack()
        description_entry = tk.Entry(add_task_window, bg=self.bg_color, fg=self.fg_color)
        description_entry.pack()

        tk.Label(add_task_window, text="Due Date:", bg=self.bg_color, fg=self.fg_color).pack()
        due_date_entry = tk.Entry(add_task_window, bg=self.bg_color, fg=self.fg_color)
        due_date_entry.pack()

        tk.Label(add_task_window, text="Priority (High/Medium/Low):", bg=self.bg_color, fg=self.fg_color).pack()
        priority_entry = tk.Entry(add_task_window, bg=self.bg_color, fg=self.fg_color)
        priority_entry.pack()

        def save_task():
            description = description_entry.get()
            due_date = due_date_entry.get()
            priority = priority_entry.get()
            if description and due_date and priority:
                task_id = len(self.task_manager.tasks) + 1
                new_task = Task(task_id, description, due_date, priority)
                self.task_manager.add_task(new_task)
                self.refresh_task_list()
                add_task_window.destroy()
            else:
                messagebox.showerror("Error", "Description, due date, and priority are required.")

        tk.Button(add_task_window, text="Save Task", command=save_task, bg=self.bg_color, fg=self.fg_color).pack()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            task = self.task_manager.tasks[task_index]

            edit_task_window = tk.Toplevel(self.master)
            edit_task_window.title("Edit Task")

            tk.Label(edit_task_window, text="New Description:", bg=self.bg_color, fg=self.fg_color).pack()
            new_description_entry = tk.Entry(edit_task_window, bg=self.bg_color, fg=self.fg_color)
            new_description_entry.insert(0, task.description)
            new_description_entry.pack()

            tk.Label(edit_task_window, text="New Due Date:", bg=self.bg_color, fg=self.fg_color).pack()
            new_due_date_entry = tk.Entry(edit_task_window, bg=self.bg_color, fg=self.fg_color)
            new_due_date_entry.insert(0, task.due_date)
            new_due_date_entry.pack()

            tk.Label(edit_task_window, text="New Priority (High/Medium/Low):", bg=self.bg_color, fg=self.fg_color).pack()
            new_priority_entry = tk.Entry(edit_task_window, bg=self.bg_color, fg=self.fg_color)
            new_priority_entry.insert(0, task.priority)
            new_priority_entry.pack()

            def save_edited_task():
                new_description = new_description_entry.get()
                new_due_date = new_due_date_entry.get()
                new_priority = new_priority_entry.get()
                task.edit_task(new_description, new_due_date, new_priority)
                self.refresh_task_list()
                edit_task_window.destroy()

            tk.Button(edit_task_window, text="Save Changes", command=save_edited_task, bg=self.bg_color, fg=self.fg_color).pack()
        else:
            messagebox.showinfo("Info", "Please select a task to edit.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            task_id = self.task_manager.tasks[task_index].task_id
            self.task_manager.remove_task(task_id)
            self.refresh_task_list()
        else:
            messagebox.showinfo("Info", "Please select a task to remove.")

    def save_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            self.task_manager.save_to_file(filename)
            messagebox.showinfo("Info", f"Tasks saved to {filename}")

    def load_from_file(self):
        filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            self.task_manager.load_from_file(filename)
            self.refresh_task_list()
            messagebox.showinfo("Info", f"Tasks loaded from {filename}")

    def toggle_dark_mode(self):
        # Przełączanie trybu jasnego/ciemnego
        if self.bg_color == self.light_mode_bg:
            self.bg_color = self.dark_mode_bg
            self.fg_color = self.dark_mode_fg
        else:
            self.bg_color = self.light_mode_bg
            self.fg_color = self.light_mode_fg

        # Aktualizacja kolorów dla wszystkich elementów
        self.master.configure(bg=self.bg_color)
        self.task_listbox.configure(bg=self.bg_color, fg=self.fg_color)
        self.toggle_mode_button.configure(bg=self.bg_color, fg=self.fg_color)
        self.edit_button.configure(bg=self.bg_color, fg=self.fg_color)
        self.remove_button.configure(bg=self.bg_color, fg=self.fg_color)
        self.add_button.configure(bg=self.bg_color, fg=self.fg_color)
        self.save_button.configure(bg=self.bg_color, fg=self.fg_color)
        self.load_button.configure(bg=self.bg_color, fg=self.fg_color)

# Użycie
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
