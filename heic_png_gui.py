import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def install_and_setup_pywin32():
    try:
        # First try to import win32event
        import win32event
    except ImportError:
        print("Setting up pywin32...")
        # Install pywin32
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        
        # Get Python Scripts directory
        scripts_dir = os.path.join(os.path.dirname(sys.executable), 'Scripts')
        postinstall_script = os.path.join(scripts_dir, 'pywin32_postinstall.py')
        
        # Run post-install script
        if os.path.exists(postinstall_script):
            subprocess.check_call([sys.executable, postinstall_script, '-install'])
        
        # Verify installation
        try:
            import win32event
        except ImportError:
            messagebox.showerror("Error", "Failed to setup pywin32. Please run as administrator.")
            sys.exit(1)

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
required_packages = ['Pillow', 'pillow-heif']
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        install_package(package)

# Setup pywin32
install_and_setup_pywin32()

# Now import all required packages
import win32event
import win32api
import winerror
from PIL import Image
from pillow_heif import register_heif_opener

# Create mutex at startup
mutex_name = "HeicConverterMutex"
try:
    mutex = win32event.CreateMutex(None, 1, mutex_name)
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        messagebox.showerror("Error", "Application is already running!")
        sys.exit(0)
except Exception as e:
    messagebox.showerror("Error", f"Failed to create mutex: {str(e)}")
    sys.exit(1)

class HeicConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to PNG Converter")
        self.root.geometry("600x400")
        self.conversion_running = False
        
        # Set up proper window closure
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Folder selection
        self.folder_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Select Folder:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2)
        
        # Delete original files checkbox
        self.delete_originals = tk.BooleanVar()
        ttk.Checkbutton(self.main_frame, text="Delete original HEIC files after conversion", 
                       variable=self.delete_originals).grid(row=1, column=0, columnspan=3, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, length=400, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        ttk.Label(self.main_frame, textvariable=self.status_var).grid(row=3, column=0, columnspan=3)
        
        # Convert button
        self.convert_button = ttk.Button(self.main_frame, text="Convert", command=self.convert_files)
        self.convert_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Log text area
        self.log_text = tk.Text(self.main_frame, height=10, width=60)
        self.log_text.grid(row=5, column=0, columnspan=3, pady=10)
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
            
    def convert_files(self):
        if self.conversion_running:
            return
            
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder")
            return
            
        self.conversion_running = True
        self.convert_button.config(state='disabled')
        
        try:
            # Register HEIF opener
            register_heif_opener()
            
            # Get all HEIC files
            files = [f for f in os.listdir(folder) if f.lower().endswith('.heic')]
            total_files = len(files)
            
            if total_files == 0:
                messagebox.showinfo("Info", "No HEIC files found in the selected folder")
                return
                
            self.progress['maximum'] = total_files
            self.progress['value'] = 0
            
            self.log_message(f"Found {total_files} HEIC files")
            
            # Convert each file
            for i, filename in enumerate(files, 1):
                try:
                    input_path = os.path.join(folder, filename)
                    output_path = os.path.join(folder, os.path.splitext(filename)[0] + '.png')
                    
                    self.status_var.set(f"Converting {filename}")
                    self.log_message(f"Converting {filename}")
                    
                    image = Image.open(input_path)
                    image.save(output_path)
                    
                    if self.delete_originals.get():
                        os.remove(input_path)
                        self.log_message(f"Deleted {filename}")
                    
                    self.progress['value'] = i
                    self.root.update()
                    
                except Exception as e:
                    self.log_message(f"Error converting {filename}: {str(e)}")
                    
            self.status_var.set("Conversion completed!")
            messagebox.showinfo("Success", "Conversion completed!")
            
        finally:
            self.conversion_running = False
            self.convert_button.config(state='normal')
    
    def on_closing(self):
        if self.conversion_running:
            if messagebox.askokcancel("Quit", "Conversion is in progress. Do you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HeicConverterGUI(root)
    root.mainloop()