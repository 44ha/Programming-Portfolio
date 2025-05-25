import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import traceback
import sys
from encryption_window import EncryptionWindow
from skipjack_algorithm import Skipjack
from rabin_algorithm import RabinCipher

def create_style(root):
    style = ttk.Style()
    style.theme_use('default')
    
    style.configure('TButton',
                   background='#333333',
                   foreground='#00ff00',
                   padding=10,
                   font=('Consolas', 11, 'bold'))
    
    style.map('TButton',
              background=[('active', '#404040')],
              foreground=[('active', '#00ff00')])
    
    style.configure('Action.TButton',
                   background='#333333',
                   foreground='#00ff00',
                   padding=10,
                   font=('Consolas', 12, 'bold'))
    
    style.map('Action.TButton',
              background=[('active', '#404040')],
              foreground=[('active', '#00ff00')])
    
    style.configure('TLabel',
                   background='#000000',
                   foreground='#00ff00',
                   font=('Consolas', 11))
    
    style.configure('Title.TLabel',
                   background='#000000',
                   foreground='#00ff00',
                   font=('Consolas', 24, 'bold'))
    
    style.configure('Main.TFrame',
                   background='#000000')
    
    style.configure('TCombobox',
                   background='#00ff00',
                   foreground='#00ff00',
                   selectbackground='#00cc00',
                   selectforeground='#00ff00',
                   fieldbackground='#1a1a1a',
                   arrowcolor='#00ff00',
                   padding=10,
                   font=('Consolas', 11))
    
    style.map('TCombobox',
              fieldbackground=[('readonly', '#1a1a1a')],
              selectbackground=[('readonly', '#333333')],
              background=[('readonly', '#00ff00')],
              foreground=[('readonly', '#00ff00')])
    
    root.option_add('*TCombobox*Listbox.font', ('Consolas', 11))
    root.option_add('*TCombobox*Listbox.background', '#1a1a1a')
    root.option_add('*TCombobox*Listbox.foreground', '#00ff00')
    root.option_add('*TCombobox*Listbox.selectBackground', '#333333')
    root.option_add('*TCombobox*Listbox.selectForeground', '#00ff00')
    
    return style

class KeyGenerationWindow:
    def __init__(self, parent_window):
        self.window = tk.Toplevel()
        self.window.title("Key Generation")
        self.window.geometry("500x600")
        self.window.minsize(500, 600)
        self.window.configure(bg='#000000')
        self.parent = parent_window
        
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, style='Main.TFrame')
        main_frame.pack(expand=True, fill='both', padx=40, pady=(30, 40))
        
        title = ttk.Label(main_frame, text="Key Generation", style='Title.TLabel')
        title.pack(pady=20)
        
        algorithm_frame = ttk.Frame(main_frame, style='Main.TFrame')
        algorithm_frame.pack(fill='x', pady=10)
        
        algorithm_label = ttk.Label(algorithm_frame, text="Algorithm:", style='TLabel')
        algorithm_label.pack(side='left', padx=5)
        
        self.algorithm_var = tk.StringVar(value="Skipjack")
        algorithm_combo = ttk.Combobox(algorithm_frame,
                                     textvariable=self.algorithm_var,
                                     values=["Rabin", "Skipjack"],
                                     state='readonly',
                                     style='TCombobox',
                                     font=('Consolas', 11),
                                     height=5,
                                     justify='center')
        algorithm_combo.pack(side='left', fill='x', expand=True, padx=5)
        
        key_frame = ttk.Frame(main_frame, style='Main.TFrame')
        key_frame.pack(fill='x', pady=20)
        
        self.key_var = tk.StringVar()
        key_label = ttk.Label(key_frame, text="Generated Key:", style='TLabel')
        key_label.pack(anchor='w', pady=(0, 5))
        
        self.key_display = tk.Text(key_frame, 
                                 height=3,
                                 wrap=tk.WORD,
                                 bg='#1a1a1a',
                                 fg='#00ff00',
                                 font=('Consolas', 11),
                                 insertbackground='#00ff00')
        self.key_display.pack(fill='x', pady=5)
        self.key_display.configure(state='disabled')
        
        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(fill='x', pady=20)
        
        generate_btn = ttk.Button(button_frame, text="Generate New Key",
                                command=self.generate_key,
                                style='Action.TButton')
        generate_btn.pack(pady=10, fill='x')
        
        save_btn = ttk.Button(button_frame, text="Save Key to File",
                            command=self.save_to_file,
                            style='Action.TButton')
        save_btn.pack(pady=10, fill='x')
        
        close_btn = ttk.Button(button_frame, text="Close",
                             command=self.close,
                             style='Action.TButton')
        close_btn.pack(pady=10, fill='x')
    
    def save_to_file(self):
        if not self.key_var.get():
            messagebox.showwarning("Warning", "Generate a key first!")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".key",
                filetypes=[("Key files", "*.key"), ("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Key File"
            )
            
            if not file_path:
                return
                
            with open(file_path, 'w') as f:
                if self.algorithm_var.get() == "Skipjack":
                    f.write(f"Algorithm: Skipjack\n")
                    f.write(f"Key: {self.key_var.get()}")
                else:
                    key_dict = eval(self.key_var.get())
                    f.write(f"Algorithm: Rabin\n")
                    f.write(f"Public Key (n): {key_dict['public_key']}\n")
                    f.write(f"Private Keys (p,q): {key_dict['private_keys'][0]}, {key_dict['private_keys'][1]}")
            
            messagebox.showinfo("Success", f"Key saved to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save key: {str(e)}")

    def generate_key(self):
        if self.algorithm_var.get() == "Skipjack":
            cipher = Skipjack()
            key = cipher._generate_key()
        else:
            cipher = RabinCipher()
            key = cipher.generate_keys()
            
        self.key_var.set(str(key))
        
        self.key_display.configure(state='normal')
        self.key_display.delete('1.0', tk.END)
        
        if isinstance(key, dict):
            formatted_key = f"Public Key (n): {key['public_key']}\nPrivate Keys (p,q): {key['private_keys'][0]}, {key['private_keys'][1]}"
            self.key_display.insert('1.0', formatted_key)
        else:
            self.key_display.insert('1.0', key)
            
        self.key_display.configure(state='disabled')
    
    def close(self):
        self.window.destroy()
        self.parent.deiconify()

class MainMenu:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("Encryption App")
            self.root.geometry("600x600")
            self.root.minsize(600, 600)
            self.root.configure(bg='#000000')
            
            self.style = create_style(self.root)
            
            main_frame = ttk.Frame(self.root, style='Main.TFrame')
            main_frame.pack(expand=True, fill='both', padx=40, pady=30)
            
            title_label = ttk.Label(main_frame, text="Encryption Application", 
                                  style='Title.TLabel')
            title_label.pack(pady=20)
            
            subtitle_label = ttk.Label(main_frame, text="Choose Encryption Method", 
                                     style='TLabel')
            subtitle_label.pack(pady=(0, 15))
            
            algorithm_frame = ttk.Frame(main_frame, style='Main.TFrame')
            algorithm_frame.pack(fill='x', padx=50)
            
            self.algorithm_var = tk.StringVar(value="Skipjack")
            algorithm_combo = ttk.Combobox(algorithm_frame,
                                         textvariable=self.algorithm_var,
                                         values=["Rabin", "Skipjack"],
                                         state='readonly',
                                         style='TCombobox',
                                         font=('Consolas', 11),
                                         height=5,
                                         justify='center')
            algorithm_combo.pack(fill='x', pady=15)
            
            button_frame = ttk.Frame(main_frame, style='Main.TFrame')
            button_frame.pack(fill='x', padx=50, pady=20)
            
            encrypt_btn = ttk.Button(button_frame, text="Encrypt",
                                   command=lambda: self.open_encryption("encrypt"),
                                   style='Action.TButton')
            encrypt_btn.pack(pady=10, fill='x')
            
            decrypt_btn = ttk.Button(button_frame, text="Decrypt",
                                   command=lambda: self.open_encryption("decrypt"),
                                   style='Action.TButton')
            decrypt_btn.pack(pady=10, fill='x')
            
            generate_key_btn = ttk.Button(button_frame, text="Generate Key",
                                        command=self.open_key_generation,
                                        style='Action.TButton')
            generate_key_btn.pack(pady=10, fill='x')
            
            exit_btn = ttk.Button(button_frame, text="Exit",
                                command=self.root.destroy,
                                style='Action.TButton')
            exit_btn.pack(pady=10, fill='x')
            
        except Exception as e:
            error_msg = f"Failed to initialize application:\n{str(e)}\n\nDetails:\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
            raise
    
    def open_key_generation(self):
        self.root.withdraw()
        KeyGenerationWindow(self.root)
    
    def open_encryption(self, operation):
        try:
            self.root.withdraw()
            EncryptionWindow(self.algorithm_var.get(), self.root, operation)
        except Exception as e:
            error_msg = f"Failed to open encryption window:\n{str(e)}"
            print(error_msg)
            self.root.deiconify()
            messagebox.showerror("Error", error_msg)
    
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            error_msg = f"Application crashed:\n{str(e)}\n\nDetails:\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
            raise

def main():
    try:
        app = MainMenu()
        app.run()
    except Exception as e:
        error_msg = f"Fatal error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        
        error_window = tk.Tk()
        error_window.title("Error")
        error_window.geometry("600x400")
        
        text_widget = tk.Text(error_window, wrap=tk.WORD, bg='white', fg='red')
        text_widget.pack(expand=True, fill='both', padx=10, pady=10)
        text_widget.insert('1.0', error_msg)
        
        def close_app():
            error_window.destroy()
            sys.exit(1)
        
        close_button = tk.Button(error_window, text="Close", command=close_app)
        close_button.pack(pady=10)
        
        error_window.mainloop()

if __name__ == "__main__":
    main() 