from models import Database, Task
from views import MainView, TaskForm
import tkinter as tk
from tkinter import messagebox

class AppController:
    def __init__(self):
        self.db = Database()
        self.view = MainView()
        
        # Bind view buttons to controller actions
        self.view.tasks_tab.add_btn.config(command=self.show_add_task)
        self.view.tasks_tab.edit_btn.config(command=self.show_edit_task)
        self.view.tasks_tab.delete_btn.config(command=self.delete_task)
        self.view.tasks_tab.complete_btn.config(command=self.complete_task)
        self.view.tasks_tab.filter_btn.config(command=self.refresh_task_list)
        
        # Bind Notebook tab change event to refresh UI
        self.view.notebook.bind("<<NotebookTabChanged>>", lambda e: self.refresh_task_list())

        # Initial data load
        self.refresh_task_list()
        
    def start(self):
        # Ensure database is closed cleanly
        self.view.protocol("WM_DELETE_WINDOW", self.on_close)
        self.view.mainloop()

    def on_close(self):
        self.db.close()
        self.view.destroy()

    def refresh_task_list(self):
        # 1. Fetch filtered tasks
        status_f = self.view.tasks_tab.status_var.get()
        priority_f = self.view.tasks_tab.priority_var.get()
        
        tasks_for_list = self.db.get_all_tasks(filter_status=status_f, filter_priority=priority_f)
        
        # 2. Update list view
        try:
            self.view.tasks_tab.populate_list(tasks_for_list)
        except AttributeError:
            pass # Form not fully loaded
        
        # 3. Update dashboard stats (always uses unfiltered data for overall stats)
        self.update_dashboard()

        # 4. Update calendar view
        all_tasks = self.db.get_all_tasks()
        try:
            self.view.calendar_tab.set_tasks(all_tasks)
        except AttributeError:
            pass

    def update_dashboard(self):
        all_tasks = self.db.get_all_tasks()
        total = len(all_tasks)
        completed = sum(1 for t in all_tasks if t.status == "Completed")
        
        pending_tasks = [t for t in all_tasks if t.status == "Pending"]
        if pending_tasks:
            # Tasks are already sorted by deadline ASC from the DB query
            next_d = pending_tasks[0]
            next_deadline_info = f"'{next_d.title}' due {next_d.deadline}"
        else:
            next_deadline_info = "No pending tasks 🎉"
            
        self.view.dashboard_tab.update_metrics(total, completed, next_deadline_info)

    def show_add_task(self):
        form = TaskForm(self.view)
        self.view.wait_window(form)
        if form.result:
            new_task = Task(None, form.result["title"], form.result["description"], form.result["deadline"], form.result["priority"], form.result["status"])
            self.db.add_task(new_task)
            self.refresh_task_list()

    def show_edit_task(self):
        task_id = self.view.tasks_tab.get_selected_task_id()
        if not task_id: return
        
        all_tasks = self.db.get_all_tasks()
        task_to_edit = next((t for t in all_tasks if t.id == task_id), None)
        if not task_to_edit: return
        
        form = TaskForm(self.view, task=task_to_edit)
        self.view.wait_window(form)
        if form.result:
            task_to_edit.title = form.result["title"]
            task_to_edit.description = form.result["description"]
            task_to_edit.deadline = form.result["deadline"]
            task_to_edit.priority = form.result["priority"]
            task_to_edit.status = form.result["status"]
            self.db.update_task(task_to_edit)
            self.refresh_task_list()
            
    def delete_task(self):
        task_id = self.view.tasks_tab.get_selected_task_id()
        if not task_id: return
        
        if messagebox.askyesno("Confirm Delete", "Are you absolutely sure you want to delete this task?"):
            self.db.delete_task(task_id)
            self.refresh_task_list()

    def complete_task(self):
        task_id = self.view.tasks_tab.get_selected_task_id()
        if not task_id: return
        
        all_tasks = self.db.get_all_tasks()
        task_to_edit = next((t for t in all_tasks if t.id == task_id), None)
        if task_to_edit:
            task_to_edit.status = "Completed"
            self.db.update_task(task_to_edit)
            self.refresh_task_list()
