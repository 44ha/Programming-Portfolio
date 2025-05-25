import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from skipjack_algorithm import Skipjack
from rabin_algorithm import RabinCipher
from security_features import SecurityFeatures

class EncryptionWindow:
    def __init__(self, method, parent_window, operation):
        self.window = tk.Toplevel()
        self.window.title(f"{method} - {operation.capitalize()}")
        self.window.geometry("1000x600")
        self.window.minsize(1000, 600)
        self.window.configure(bg='#000000')
        self.parent = parent_window
        self.method = method
        self.security = SecurityFeatures()
        self.algorithm = RabinCipher() if method == "Rabin" else Skipjack()
        self.selected_file = None

        self.setup_styles()
        if operation == "encrypt":
            self.setup_encrypt_ui()
        else:
            self.setup_decrypt_ui()

        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TButton',
                           background='#333333',
                           foreground='#00ff00',
                           padding=10,
                           font=('Consolas', 11, 'bold'))

        self.style.map('TButton',
                      background=[('active', '#404040')],
                      foreground=[('active', '#00ff00')])

        self.style.configure('Action.TButton',
                           background='#333333',
                           foreground='#00ff00',
                           padding=10,
                           font=('Consolas', 12, 'bold'))

        self.style.configure('Back.TButton',
                           background='#333333',
                           foreground='#00ff00',
                           padding=10,
                           font=('Consolas', 12, 'bold'))

        self.style.map('Back.TButton',
                      background=[('active', '#404040')],
                      foreground=[('active', '#00ff00')])

        self.style.configure('TLabel',
                           background='#000000',
                           foreground='#00ff00',
                           font=('Consolas', 11))

        self.style.configure('Title.TLabel',
                           background='#000000',
                           foreground='#00ff00',
                           font=('Consolas', 24, 'bold'))

        self.style.configure('Hint.TLabel',
                           background='#000000',
                           foreground='#666666',
                           font=('Consolas', 10))

        self.style.configure('TLabelframe',
                           background='#000000')

        self.style.configure('TLabelframe.Label',
                           background='#000000',
                           foreground='#00ff00',
                           font=('Consolas', 12, 'bold'))

        self.style.configure('Main.TFrame',
                           background='#000000')

        self.style.configure('TEntry',
                           fieldbackground='#1a1a1a',
                           foreground='#00ff00',
                           font=('Consolas', 11))

        self.style.configure('TCombobox',
                           background='#00ff00',
                           foreground='#000000',
                           selectbackground='#00cc00',
                           selectforeground='#000000',
                           fieldbackground='#1a1a1a',
                           arrowcolor='#00ff00',
                           padding=10,
                           font=('Consolas', 11))

        self.style.map('TCombobox',
                      fieldbackground=[('readonly', '#1a1a1a')],
                      selectbackground=[('readonly', '#333333')],
                      background=[('readonly', '#00ff00')],
                      foreground=[('readonly', '#000000')])

        self.window.option_add('*TCombobox*Listbox.font', ('Consolas', 11))
        self.window.option_add('*TCombobox*Listbox.background', '#1a1a1a')
        self.window.option_add('*TCombobox*Listbox.foreground', '#00ff00')
        self.window.option_add('*TCombobox*Listbox.selectBackground', '#333333')
        self.window.option_add('*TCombobox*Listbox.selectForeground', '#00ff00')
        self.window.option_add('*TCombobox*Listbox.height', '5')

    def setup_encrypt_ui(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)
        main_frame.configure(style='Main.TFrame')

        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.configure(style='Main.TFrame')

        title = ttk.Label(title_frame, text=f"{self.method} - Encrypt", 
                         style='Title.TLabel')
        title.pack(pady=10)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True)
        content_frame.configure(style='Main.TFrame')
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # Left Column
        left_frame = ttk.Frame(content_frame)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=10)
        left_frame.configure(style='Main.TFrame')
        
        text_label = ttk.Label(left_frame, text="Enter text to encrypt:", 
                             style='TLabel')
        text_label.pack(pady=(0, 5), anchor='w')
        
        text_container = ttk.Frame(left_frame)
        text_container.pack(fill='both', expand=True)
        text_container.configure(style='Main.TFrame')
        
        self.text_input = tk.Text(text_container, height=3,
                                bg='#1a1a1a', fg='#00ff00',
                                font=('Consolas', 11),
                                insertbackground='#00ff00')
        self.text_input.pack(fill='both', expand=True)

        # Right Column
        right_frame = ttk.Frame(content_frame)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=10)
        right_frame.configure(style='Main.TFrame')

        key_frame = ttk.Frame(right_frame)
        key_frame.pack(fill='x', pady=5)
        key_frame.configure(style='Main.TFrame')

        key_label = ttk.Label(key_frame, text="Enter key:", 
                            style='TLabel')
        key_label.pack(side='left', padx=(0, 10))
        
        self.key_input = ttk.Entry(key_frame, style='TEntry')
        self.key_input.pack(side='left', fill='x', expand=True)

        if self.method == "Rabin":
            key_hint = ttk.Label(right_frame, text="Enter the public key (n)", 
                               style='Hint.TLabel')
            key_hint.pack(pady=5)

        output_frame = ttk.Frame(right_frame)
        output_frame.pack(fill='x', pady=10)
        output_frame.configure(style='Main.TFrame')

        output_label = ttk.Label(output_frame, text="Output:", 
                               style='TLabel')
        output_label.pack(side='left', padx=(0, 10))

        self.output_path = ttk.Label(output_frame, text="No location selected", 
                                   style='Hint.TLabel')
        self.output_path.pack(side='left', fill='x', expand=True)

        location_btn = ttk.Button(output_frame, text="Choose Location", 
                                command=self.choose_output_location_only,
                                style='Action.TButton')
        location_btn.pack(side='right', padx=5)

        # Security Options
        security_frame = ttk.LabelFrame(main_frame, text="Security Options", 
                                      style='TLabelframe')
        security_frame.pack(fill='x', padx=10, pady=10)

        security_content = ttk.Frame(security_frame)
        security_content.pack(fill='x', padx=10, pady=5)
        security_content.configure(style='Main.TFrame')
        security_content.grid_columnconfigure(0, weight=1)
        security_content.grid_columnconfigure(1, weight=1)

        # Left security options
        left_security = ttk.Frame(security_content)
        left_security.grid(row=0, column=0, sticky='nsew', padx=5)
        left_security.configure(style='Main.TFrame')

        expiry_frame = ttk.Frame(left_security)
        expiry_frame.pack(fill='x', pady=2)
        expiry_frame.configure(style='Main.TFrame')
        
        ttk.Label(expiry_frame, text="Expiry (hours):", 
                 style='TLabel').pack(side='left', padx=5)
        
        self.expiry_hours = tk.StringVar()
        expiry_entry = ttk.Entry(expiry_frame, textvariable=self.expiry_hours, 
                               width=8, style='TEntry')
        expiry_entry.pack(side='left', padx=5)

        attempts_frame = ttk.Frame(left_security)
        attempts_frame.pack(fill='x', pady=2)
        attempts_frame.configure(style='Main.TFrame')
        
        ttk.Label(attempts_frame, text="Max attempts:", 
                 style='TLabel').pack(side='left', padx=5)
        self.attempts_var = tk.StringVar()
        attempts_entry = ttk.Entry(attempts_frame, textvariable=self.attempts_var, 
                                 width=8, style='TEntry')
        attempts_entry.pack(side='left', padx=5)

        # Right security options
        right_security = ttk.Frame(security_content)
        right_security.grid(row=0, column=1, sticky='nsew', padx=5)
        right_security.configure(style='Main.TFrame')

        fake_frame = ttk.Frame(right_security)
        fake_frame.pack(fill='x', pady=2)
        fake_frame.configure(style='Main.TFrame')
        
        ttk.Label(fake_frame, text="Fake password:", 
                 style='TLabel').pack(side='left', padx=5)
        self.fake_pass_var = tk.StringVar()
        fake_pass_entry = ttk.Entry(fake_frame, textvariable=self.fake_pass_var, 
                                  width=20, style='TEntry')
        fake_pass_entry.pack(side='left', padx=5)

        fake_content_frame = ttk.Frame(security_frame)
        fake_content_frame.pack(fill='x', pady=5, padx=10)
        fake_content_frame.configure(style='Main.TFrame')
        
        ttk.Label(fake_content_frame, text="Fake content:", 
                 style='TLabel').pack(side='left', padx=5)
        self.fake_content = tk.Text(fake_content_frame, height=2,
                                  bg='#1a1a1a', fg='#00ff00',
                                  font=('Consolas', 11),
                                  insertbackground='#00ff00')
        self.fake_content.pack(side='left', padx=5, fill='x', expand=True)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        button_frame.configure(style='Main.TFrame')

        back_btn = ttk.Button(button_frame, text="Back", 
                            command=self.go_back,
                            style='Back.TButton')
        back_btn.pack(side='left', padx=5)

        encrypt_btn = ttk.Button(button_frame, text="Encrypt", 
                               command=self.encrypt,
                               style='Action.TButton')
        encrypt_btn.pack(side='right', padx=5)

    def setup_decrypt_ui(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)
        main_frame.configure(style='Main.TFrame')

        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.configure(style='Main.TFrame')

        title = ttk.Label(title_frame, text=f"{self.method} - Decrypt", 
                         style='Title.TLabel')
        title.pack(pady=10)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True)
        content_frame.configure(style='Main.TFrame')

        file_frame = ttk.Frame(content_frame)
        file_frame.pack(fill='x', pady=10)
        file_frame.configure(style='Main.TFrame')

        file_label = ttk.Label(file_frame, text="Input:", 
                             style='TLabel')
        file_label.pack(side='left', padx=(0, 10))

        self.file_label = ttk.Label(file_frame, text="No file selected", 
                                  style='Hint.TLabel')
        self.file_label.pack(side='left', fill='x', expand=True)

        file_btn = ttk.Button(file_frame, text="Choose File", 
                            command=self.choose_file,
                            style='Action.TButton')
        file_btn.pack(side='right', padx=5)

        key_frame = ttk.Frame(content_frame)
        key_frame.pack(fill='x', pady=10)
        key_frame.configure(style='Main.TFrame')

        if self.method == "Rabin":
            keys_frame = ttk.Frame(key_frame)
            keys_frame.pack(fill='x')
            keys_frame.configure(style='Main.TFrame')

            p_frame = ttk.Frame(keys_frame)
            p_frame.pack(fill='x', pady=2)
            p_frame.configure(style='Main.TFrame')

            p_label = ttk.Label(p_frame, text="Key p:", 
                              style='TLabel')
            p_label.pack(side='left', padx=(0, 10))
            
            self.p_input = ttk.Entry(p_frame, width=30, style='TEntry')
            self.p_input.pack(side='left', fill='x', expand=True)

            q_frame = ttk.Frame(keys_frame)
            q_frame.pack(fill='x', pady=2)
            q_frame.configure(style='Main.TFrame')

            q_label = ttk.Label(q_frame, text="Key q:", 
                              style='TLabel')
            q_label.pack(side='left', padx=(0, 10))
            
            self.q_input = ttk.Entry(q_frame, width=30, style='TEntry')
            self.q_input.pack(side='left', fill='x', expand=True)
        else:
            key_label = ttk.Label(key_frame, text="Enter key:", 
                                style='TLabel')
            key_label.pack(side='left', padx=(0, 10))
            
            self.key_input = ttk.Entry(key_frame, width=30, style='TEntry')
            self.key_input.pack(side='left', fill='x', expand=True)

        result_label = ttk.Label(content_frame, text="Decrypted text:", 
                               style='TLabel')
        result_label.pack(pady=(10, 2))
        
        self.result_text = tk.Text(content_frame, height=3,
                                 bg='#1a1a1a', fg='#00ff00',
                                 font=('Consolas', 11),
                                 insertbackground='#00ff00')
        self.result_text.pack(fill='both', expand=True, pady=(0, 10))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        button_frame.configure(style='Main.TFrame')

        back_btn = ttk.Button(button_frame, text="Back", 
                            command=self.go_back,
                            style='Back.TButton')
        back_btn.pack(side='left', padx=5)

        decrypt_btn = ttk.Button(button_frame, text="Decrypt", 
                               command=self.decrypt,
                               style='Action.TButton')
        decrypt_btn.pack(side='right', padx=5)

    def choose_output_location_only(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file = filename
            self.output_path.config(text=os.path.basename(filename))

    def choose_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file = filename
            self.file_label.config(text=os.path.basename(filename))

    def encrypt(self):
        try:
            if not self.selected_file:
                messagebox.showerror("Error", "Please choose an output location first")
                return

            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Error", "Please enter text to encrypt")
                return

            expiry_hours = None
            if self.expiry_hours.get().strip():
                try:
                    expiry_hours = float(self.expiry_hours.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid expiry hours")
                    return

            max_attempts = None
            if self.attempts_var.get().strip():
                try:
                    max_attempts = int(self.attempts_var.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid max attempts")
                    return

            fake_password = self.fake_pass_var.get().strip() or None
            fake_content = self.fake_content.get("1.0", tk.END).strip() or None

            if self.method == "Rabin":
                try:
                    public_key = int(self.key_input.get().strip())
                    encrypted = self.algorithm.encrypt(text, public_key)
                except ValueError:
                    messagebox.showerror("Error", "Invalid public key")
                    return
            else:
                key = self.key_input.get().strip()
                if not key:
                    messagebox.showerror("Error", "Please enter a key")
                    return
                encrypted = self.algorithm.encrypt(text, key)

            self.security.encrypt_with_security(
                self.selected_file,
                encrypted,
                expiry_hours=expiry_hours,
                max_attempts=max_attempts,
                fake_password=fake_password,
                fake_content=fake_content
            )
            
            messagebox.showinfo("Success", "Text encrypted successfully!")
            self.go_back()  # Return to main menu after successful encryption

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        try:
            if not self.selected_file:
                messagebox.showerror("Error", "Please choose a file to decrypt")
                return

            password = None
            if self.method == "Rabin":
                try:
                    p = int(self.p_input.get().strip())
                    q = int(self.q_input.get().strip())
                    password = f"{p}:{q}"
                except ValueError:
                    messagebox.showerror("Error", "Invalid private keys")
                    return
            else:
                key = self.key_input.get().strip()
                if not key:
                    messagebox.showerror("Error", "Please enter a key")
                    return
                password = key

            print(f"Attempting to decrypt with key: {password}")  # Debug log

            can_access, is_fake, message = self.security.check_security(
                self.selected_file, 
                password
            )

            print(f"Security check result: access={can_access}, fake={is_fake}, message={message}")  # Debug log

            if not can_access:
                messagebox.showerror("Error", message)
                return

            file_to_read = self.selected_file + '.fake' if is_fake else self.selected_file
            print(f"Reading from file: {file_to_read}")  # Debug log

            try:
                with open(file_to_read, 'r') as f:
                    encrypted_text = f.read().strip()
                
                print(f"Read encrypted text (first 50 chars): {encrypted_text[:50]}...")  # Debug log

                if self.method == "Rabin":
                    decrypted = self.algorithm.decrypt(encrypted_text, p, q)
                else:
                    print("Calling Skipjack decrypt...")  # Debug log
                    if is_fake:
                        encrypted_text = self.algorithm.encrypt(encrypted_text, key)
                    decrypted = self.algorithm.decrypt(encrypted_text, key)
                    print(f"Decryption successful, result length: {len(decrypted)}")  # Debug log

                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", decrypted)

                # Only show message if it's not about fake content
                if message and not is_fake:
                    messagebox.showinfo("Security Info", message)

            except Exception as e:
                print(f"Decryption error: {str(e)}")  # Debug log
                messagebox.showerror("Error", f"Failed to decrypt: {str(e)}")

        except Exception as e:
            print(f"General error: {str(e)}")  # Debug log
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.window.destroy()
        self.parent.deiconify() 