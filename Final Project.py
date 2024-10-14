import tkinter as tk
from tkinter import messagebox
import json

class Task:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.title} [{self.category}] - {status}\nDescription: {self.description}"

def save_tasks(tasks):
    """Save tasks to a JSON file."""
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

def load_tasks():
    """Load tasks from a JSON file."""
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.config(bg='black')  # Set the background to black

        # Center the grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Load tasks
        self.tasks = load_tasks()

        # Title Entry (Bold and larger texts)
        self.title_label = tk.Label(root, text="Task Title:", bg='black', fg='white', font=('Arial', 14, 'bold'))
        self.title_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30, font=('Arial', 14))  # Larger text
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)

        # Description Entry (Bold and larger texts)
        self.desc_label = tk.Label(root, text="Task Description:", bg='black', fg='white', font=('Arial', 14, 'bold'))
        self.desc_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.desc_entry = tk.Entry(root, width=30, font=('Arial', 14))  # Larger text
        self.desc_entry.grid(row=2, column=1, padx=10, pady=5)

        # Category Entry (Bold and larger texts)
        self.cat_label = tk.Label(root, text="Category:", bg='black', fg='white', font=('Arial', 14, 'bold'))
        self.cat_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.cat_entry = tk.Entry(root, width=30, font=('Arial', 14))  # Larger text
        self.cat_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons with increased padding and larger text
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg='#4CAF50', fg='white', font=('Arial', 14, 'bold'), width=15, padx=10, pady=10)
        self.add_button.grid(row=4, column=0, padx=15, pady=10)

        self.view_button = tk.Button(root, text="View Tasks", command=self.view_tasks, bg='#2196F3', fg='white', font=('Arial', 14, 'bold'), width=15, padx=10, pady=10)
        self.view_button.grid(row=4, column=1, padx=15, pady=10)

        self.mark_button = tk.Button(root, text="Mark Task Completed", command=self.mark_task_completed, bg='#009688', fg='white', font=('Arial', 14, 'bold'), width=15, padx=10, pady=10)
        self.mark_button.grid(row=5, column=0, padx=15, pady=10)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, bg='#F44336', fg='white', font=('Arial', 14, 'bold'), width=15, padx=10, pady=10)
        self.delete_button.grid(row=5, column=1, padx=15, pady=10)

        # Save and Quit Buttons with increased padding
        self.save_button = tk.Button(root, text="Save", command=self.save_tasks, bg='#673AB7', fg='white', font=('Arial', 14, 'bold'), width=15, padx=10, pady=10)
        self.save_button.grid(row=6, column=0, padx=15, pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=self.quit_app, bg='#9E9E9E', fg='white', font=('Arial', 14, 'bold'), width=15, padx=10, pady=10)
        self.quit_button.grid(row=6, column=1, padx=15, pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, width=50, height=10, font=('Arial', 12), bg='black', fg='white')
        self.task_listbox.grid(row=7, column=0, columnspan=2, padx=15, pady=15)  # Increased spacing

        # Refresh task list
        self.refresh_task_list()

    def add_task(self):
        """Add a new task to the task list."""
        title = self.title_entry.get()
        description = self.desc_entry.get()
        category = self.cat_entry.get()

        if title and description and category:
            new_task = Task(title, description, category)
            self.tasks.append(new_task)
            self.refresh_task_list()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def view_tasks(self):
        """Display all tasks."""
        self.refresh_task_list()

    def mark_task_completed(self):
        """Mark a specific task as completed."""
        selected_task = self.get_selected_task()
        if selected_task:
            selected_task.mark_completed()
            self.refresh_task_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a task.")

    def delete_task(self):
        """Delete a specific task from the task list."""
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.refresh_task_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def refresh_task_list(self):
        """Refresh the listbox to show the updated task list."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, repr(task))

    def get_selected_task(self):
        """Get the task that is currently selected in the listbox."""
        selected_index = self.task_listbox.curselection()
        if selected_index:
            return self.tasks[selected_index[0]]
        return None

    def clear_entries(self):
        """Clear the entry fields after a task is added."""
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.cat_entry.delete(0, tk.END)

    def save_tasks(self):
        """Save tasks to a file and show a message."""
        save_tasks(self.tasks)
        messagebox.showinfo("Save Successful", "Tasks have been saved successfully!")

    def quit_app(self):
        """Save tasks and quit the application."""
        save_tasks(self.tasks)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

