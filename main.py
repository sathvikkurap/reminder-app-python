import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import threading
import platform
import os

import winsound


class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder App")

        self.reminders = {}
        self.queued_reminders = []

        self.reminder_listbox = tk.Listbox(root)
        self.reminder_listbox.pack(padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Reminder", command=self.add_reminder)
        self.add_button.pack(pady=5)

        self.add_checklist_item_button = tk.Button(root, text="Add Checklist Item", command=self.add_checklist_item)
        self.add_checklist_item_button.pack(pady=5)

        self.show_reminders_button = tk.Button(root, text="Show Reminders", command=self.show_reminders)
        self.show_reminders_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=5)

        self.reminder_thread = threading.Thread(target=self.check_reminders)
        self.reminder_thread.start()

    def add_reminder(self):
        reminder_name = tk.simpledialog.askstring("Add Reminder", "Enter reminder name:")
        time_str = tk.simpledialog.askstring("Add Reminder", "Enter reminder time (HH:MM AM/PM):")
        checklist = []

        time_format = "%I:%M %p"  # 12-hour time format
        reminder_time = time.strptime(time_str, time_format)

        self.reminders[reminder_name] = {
            'time': reminder_time,
            'checklist': checklist
        }
        self.reminder_listbox.insert(tk.END, reminder_name)

    def add_checklist_item(self):
        selected_index = self.reminder_listbox.curselection()
        if selected_index:
            selected_name = self.reminder_listbox.get(selected_index)
            item = tk.simpledialog.askstring("Add Checklist Item", f"Add checklist item for '{selected_name}':")
            self.reminders[selected_name]['checklist'].append(item)

    def show_reminders(self):
        for name, data in self.reminders.items():
            checklist_status = "Done" if all(data['checklist']) else "Pending"
            messagebox.showinfo(
                "Reminder Info",
                f"Name: {name}\nTime: {time.strftime('%I:%M %p', data['time'])}\nChecklist: {checklist_status}"
            )

    def check_reminders(self):
        while True:
            current_time = time.localtime()
            for name, data in self.reminders.items():
                if data['time'].tm_hour == current_time.tm_hour and data['time'].tm_min == current_time.tm_min:
                    if self.is_computer_unlocked():
                        self.notify(name)
                    else:
                        self.queue_reminder(name)
            time.sleep(10)  # Check every 10 seconds

    def is_computer_unlocked(self):
        if platform.system() == "Windows":
            return os.system("quser") == 0
        elif platform.system() == "Darwin":
            return os.system("ioreg -n IODisplayWrangler | grep -i IOPowerManagement").find("CurrentPowerState = 4") != -1
        elif platform.system() == "Linux":
            return os.system("xscreensaver-command -time").find("is locked") == -1
        # Add more cases for other platforms

    def queue_reminder(self, reminder_name):
        self.queued_reminders.append(reminder_name)

    def notify(self, reminder_name):
        winsound.Beep(500, 1000)  # Beep sound notification
        messagebox.showinfo("Reminder", f"It's time for '{reminder_name}'!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
