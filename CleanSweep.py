import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class CleanSweep:
    def __init__(self, root):
        self.root = root
        self.root.title("CleanSweep - Executable Uninstaller")
        self.root.geometry("400x200")

        # Label
        self.label = tk.Label(root, text="Select an executable to uninstall:", font=("Arial", 12))
        self.label.pack(pady=10)

        # File selection button
        self.file_button = tk.Button(root, text="Browse Executable", command=self.browse_file, width=20)
        self.file_button.pack(pady=5)

        # Uninstall button
        self.uninstall_button = tk.Button(root, text="Uninstall", command=self.uninstall, width=20, state=tk.DISABLED)
        self.uninstall_button.pack(pady=5)

        # Status Label
        self.status_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=10)

        self.selected_file = None

    def browse_file(self):
        filetypes = [("Executable files", "*.exe"), ("All files", "*.*")]
        self.selected_file = filedialog.askopenfilename(title="Select Executable", filetypes=filetypes)
        if self.selected_file:
            self.status_label.config(text=f"Selected: {self.selected_file}")
            self.uninstall_button.config(state=tk.NORMAL)

    def uninstall(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No executable selected!")
            return

        try:
            exe_dir = os.path.dirname(self.selected_file)
            exe_name = os.path.basename(self.selected_file)

            # Confirm before deletion
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to uninstall '{exe_name}'?")
            if not confirm:
                return

            # Remove the executable
            if os.path.exists(self.selected_file):
                os.remove(self.selected_file)

            # Look for additional related files
            related_files = [f for f in os.listdir(exe_dir) if exe_name.split('.')[0] in f]
            for file in related_files:
                file_path = os.path.join(exe_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            self.status_label.config(text=f"Uninstalled: {exe_name}")
            messagebox.showinfo("Success", f"'{exe_name}' has been uninstalled.")
            self.uninstall_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CleanSweep(root)
    root.mainloop()
