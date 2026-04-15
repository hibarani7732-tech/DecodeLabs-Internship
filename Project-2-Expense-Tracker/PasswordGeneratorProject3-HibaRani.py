"""
RANDOM PASSWORD GENERATOR - NO EXTERNAL LIBRARIES NEEDED
DecodeLabs Internship Project
IPO Model: Input (password length) -> Process (generate random password) -> Output (display password)
"""

import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Random Password Generator - DecodeLabs")
        self.root.geometry("650x600")
        self.root.resizable(False, False)
        
        # Set background color
        self.root.configure(bg='#2c3e50')
        
        self.setup_gui()
        
    def setup_gui(self):
        """Create the user interface"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ========== TITLE SECTION ==========
        title_label = tk.Label(main_frame, text="🔐 RANDOM PASSWORD GENERATOR", 
                               font=('Arial', 18, 'bold'), 
                               fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 10))
        
        subtitle = tk.Label(main_frame, text="Generate strong, secure passwords instantly", 
                           font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50')
        subtitle.pack(pady=(0, 30))
        
        # ========== INPUT SECTION ==========
        input_frame = tk.LabelFrame(main_frame, text="📥 INPUT: Password Settings", 
                                    font=('Arial', 12, 'bold'), 
                                    fg='#ecf0f1', bg='#34495e', bd=2)
        input_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Password Length Input
        length_frame = tk.Frame(input_frame, bg='#34495e')
        length_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(length_frame, text="Password Length:", font=('Arial', 11), 
                fg='#ecf0f1', bg='#34495e').pack(side="left", padx=(0, 10))
        
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = tk.Spinbox(length_frame, from_=4, to=50, 
                                         textvariable=self.length_var,
                                         width=10, font=('Arial', 11))
        self.length_spinbox.pack(side="left", padx=(0, 20))
        
        tk.Label(length_frame, text="(Recommended: 12-16 characters)", 
                font=('Arial', 9), fg='#bdc3c7', bg='#34495e').pack(side="left")
        
        # Character Type Selection
        options_frame = tk.Frame(input_frame, bg='#34495e')
        options_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(options_frame, text="Include:", font=('Arial', 11, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor="w", pady=(0, 5))
        
        # Checkboxes for character types
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        checkbox_frame = tk.Frame(options_frame, bg='#34495e')
        checkbox_frame.pack(fill="x")
        
        tk.Checkbutton(checkbox_frame, text="Uppercase (A-Z)", variable=self.use_uppercase,
                      fg='#ecf0f1', bg='#34495e', selectcolor='#34495e').pack(side="left", padx=(0, 20))
        
        tk.Checkbutton(checkbox_frame, text="Lowercase (a-z)", variable=self.use_lowercase,
                      fg='#ecf0f1', bg='#34495e', selectcolor='#34495e').pack(side="left", padx=(0, 20))
        
        tk.Checkbutton(checkbox_frame, text="Numbers (0-9)", variable=self.use_digits,
                      fg='#ecf0f1', bg='#34495e', selectcolor='#34495e').pack(side="left", padx=(0, 20))
        
        tk.Checkbutton(checkbox_frame, text="Symbols (!@#$%^&*)", variable=self.use_symbols,
                      fg='#ecf0f1', bg='#34495e', selectcolor='#34495e').pack(side="left")
        
        # Quantity (how many passwords to generate)
        quantity_frame = tk.Frame(input_frame, bg='#34495e')
        quantity_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(quantity_frame, text="Number of passwords:", font=('Arial', 11), 
                fg='#ecf0f1', bg='#34495e').pack(side="left", padx=(0, 10))
        
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_spinbox = tk.Spinbox(quantity_frame, from_=1, to=10, 
                                          textvariable=self.quantity_var,
                                          width=10, font=('Arial', 11))
        self.quantity_spinbox.pack(side="left")
        
        # ========== PROCESS SECTION ==========
        process_frame = tk.LabelFrame(main_frame, text="⚙️ PROCESS: Generate Password", 
                                      font=('Arial', 12, 'bold'), 
                                      fg='#ecf0f1', bg='#34495e', bd=2)
        process_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Generate Button
        self.generate_btn = tk.Button(process_frame, text="🔐 GENERATE PASSWORD(S)", 
                                      command=self.generate_passwords,
                                      bg='#27ae60', fg='white', 
                                      font=('Arial', 12, 'bold'),
                                      height=2, cursor='hand2')
        self.generate_btn.pack(fill="x", pady=10, padx=20)
        
        # Password Strength Indicator
        strength_frame = tk.Frame(process_frame, bg='#34495e')
        strength_frame.pack(fill="x", pady=5, padx=20)
        
        tk.Label(strength_frame, text="Password Strength:", font=('Arial', 11), 
                fg='#ecf0f1', bg='#34495e').pack(side="left", padx=(0, 10))
        
        self.strength_label = tk.Label(strength_frame, text="Not generated yet", 
                                       font=('Arial', 11, 'bold'),
                                       fg='#f39c12', bg='#34495e')
        self.strength_label.pack(side="left")
        
        # ========== OUTPUT SECTION ==========
        output_frame = tk.LabelFrame(main_frame, text="📤 OUTPUT: Generated Passwords", 
                                     font=('Arial', 12, 'bold'), 
                                     fg='#ecf0f1', bg='#34495e', bd=2)
        output_frame.pack(fill="both", expand=True, padx=10)
        
        # Text widget to display passwords
        self.password_text = tk.Text(output_frame, height=8, width=50, 
                                     font=('Courier', 11), wrap=tk.WORD,
                                     bg='#ecf0f1', fg='#2c3e50')
        self.password_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar for text widget
        scrollbar = tk.Scrollbar(self.password_text, command=self.password_text.yview)
        self.password_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame for actions
        action_frame = tk.Frame(output_frame, bg='#34495e')
        action_frame.pack(fill="x", pady=10, padx=10)
        
        self.copy_btn = tk.Button(action_frame, text="📋 Copy to Clipboard", 
                                  command=self.copy_to_clipboard,
                                  bg='#3498db', fg='white', 
                                  font=('Arial', 10, 'bold'), state='disabled')
        self.copy_btn.pack(side="left", padx=5)
        
        self.clear_btn = tk.Button(action_frame, text="🗑️ Clear All", 
                                   command=self.clear_output,
                                   bg='#e74c3c', fg='white', 
                                   font=('Arial', 10, 'bold'))
        self.clear_btn.pack(side="left", padx=5)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, text="✅ Ready to generate passwords", 
                                     font=('Arial', 9), fg='#bdc3c7', bg='#2c3e50')
        self.status_label.pack(side="left")
        
        # Password tips
        tips_frame = tk.LabelFrame(main_frame, text="💡 Security Tips", 
                                   font=('Arial', 10, 'bold'), 
                                   fg='#ecf0f1', bg='#34495e', bd=2)
        tips_frame.pack(fill="x", pady=(10, 0), padx=10)
        
        tips_text = """• Use at least 12 characters for strong security
• Include a mix of uppercase, lowercase, numbers, and symbols
• Never reuse passwords across different accounts
• Change passwords every 3-6 months
• Never share your passwords with anyone"""
        
        tips_label = tk.Label(tips_frame, text=tips_text, font=('Arial', 9), 
                             fg='#bdc3c7', bg='#34495e', justify="left")
        tips_label.pack(pady=10, padx=10)
        
        # Store generated passwords
        self.generated_passwords = []
    
    # ========== PROCESS ENGINE ==========
    
    def generate_passwords(self):
        """Main process: Generate random passwords based on user input"""
        
        # INPUT: Get user preferences
        length = self.length_var.get()
        quantity = self.quantity_var.get()
        
        # Poka-Yoke: Input validation
        if length < 4:
            messagebox.showwarning("Weak Password", 
                                  "Password length should be at least 4 characters!\n\n"
                                  "Short passwords are easy to crack. Using 8+ characters is recommended.")
            return
        
        if length > 50:
            messagebox.showwarning("Too Long", 
                                  "Password length cannot exceed 50 characters!")
            return
        
        # Check if at least one character type is selected
        if not (self.use_uppercase.get() or self.use_lowercase.get() or 
                self.use_digits.get() or self.use_symbols.get()):
            messagebox.showwarning("No Character Type", 
                                  "Please select at least one character type!\n\n"
                                  "Your password needs some characters to be generated.")
            return
        
        # Clear previous output
        self.password_text.delete(1.0, tk.END)
        
        # PROCESS: Generate passwords
        passwords = []
        for i in range(quantity):
            password = self.generate_single_password(length)
            passwords.append(password)
            
            # Display with numbering
            if quantity > 1:
                self.password_text.insert(tk.END, f"{i+1}. {password}\n\n")
            else:
                self.password_text.insert(tk.END, f"{password}\n\n")
        
        # Store for copying
        self.generated_passwords = passwords
        
        # OUTPUT: Display results and feedback
        if passwords:
            self.update_strength_indicator(passwords[0])
            self.status_label.config(text=f"✅ Generated {quantity} password(s) successfully!", fg='#2ecc71')
            self.copy_btn.config(state='normal')
        else:
            self.copy_btn.config(state='disabled')
    
    def generate_single_password(self, length):
        """Generate a single random password"""
        
        # Build character pool based on user selection
        character_pool = ""
        
        if self.use_uppercase.get():
            character_pool += string.ascii_uppercase
        if self.use_lowercase.get():
            character_pool += string.ascii_lowercase
        if self.use_digits.get():
            character_pool += string.digits
        if self.use_symbols.get():
            character_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure password has at least one character from each selected type
        password_chars = []
        
        # Add one character from each selected type (for complexity)
        if self.use_uppercase.get():
            password_chars.append(random.choice(string.ascii_uppercase))
        if self.use_lowercase.get():
            password_chars.append(random.choice(string.ascii_lowercase))
        if self.use_digits.get():
            password_chars.append(random.choice(string.digits))
        if self.use_symbols.get():
            password_chars.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill the rest randomly
        remaining_length = length - len(password_chars)
        if remaining_length > 0:
            for _ in range(remaining_length):
                password_chars.append(random.choice(character_pool))
        
        # Shuffle to avoid predictable pattern
        random.shuffle(password_chars)
        
        # Join characters into a string
        password = ''.join(password_chars)
        
        return password
    
    def update_strength_indicator(self, password):
        """Evaluate and display password strength"""
        
        if not password:
            return
        
        score = 0
        length = len(password)
        
        # Length check
        if length >= 12:
            score += 3
        elif length >= 8:
            score += 2
        elif length >= 6:
            score += 1
        
        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        score += sum([has_upper, has_lower, has_digit, has_symbol])
        
        # Determine strength
        if score >= 7:
            strength = "💪 VERY STRONG"
            color = "#27ae60"
        elif score >= 5:
            strength = "✅ STRONG"
            color = "#3498db"
        elif score >= 3:
            strength = "⚠️ MEDIUM"
            color = "#f39c12"
        else:
            strength = "❌ WEAK"
            color = "#e74c3c"
        
        self.strength_label.config(text=strength, fg=color)
    
    def copy_to_clipboard(self):
        """Copy generated password to clipboard using tkinter's built-in method"""
        try:
            # Get the first password from the text widget
            password_text = self.password_text.get(1.0, tk.END).strip()
            
            if password_text:
                # Remove numbering if present
                lines = password_text.split('\n')
                first_password = lines[0].split('. ')[-1] if '. ' in lines[0] else lines[0]
                
                # Use tkinter's built-in clipboard method (no external library needed)
                self.root.clipboard_clear()
                self.root.clipboard_append(first_password)
                self.root.update()  # Keep clipboard content after app closes
                
                self.status_label.config(text=f"✅ Copied to clipboard: {first_password}", fg='#2ecc71')
                messagebox.showinfo("Copied!", "Password copied to clipboard!")
            else:
                messagebox.showwarning("No Password", "Generate a password first!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy to clipboard: {str(e)}")
    
    def clear_output(self):
        """Clear the output text area"""
        self.password_text.delete(1.0, tk.END)
        self.strength_label.config(text="Not generated yet", fg='#f39c12')
        self.status_label.config(text="✅ Output cleared", fg='#bdc3c7')
        self.copy_btn.config(state='disabled')
        self.generated_passwords = []

# ========== COMMAND LINE VERSION (No GUI) ==========

def command_line_version():
    """Simple command-line version of password generator"""
    print("\n" + "="*60)
    print("🔐 RANDOM PASSWORD GENERATOR - CLI Version")
    print("="*60)
    
    # INPUT: Get password length with validation
    while True:
        try:
            length = int(input("\n📥 Enter password length (8-32): "))
            if 8 <= length <= 32:
                break
            else:
                print("❌ Please enter a length between 8 and 32 characters!")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
    
    # INPUT: Get complexity options
    print("\n📝 Select character types to include:")
    use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_digits = input("Include numbers? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
    
    # Validate at least one type selected
    if not (use_upper or use_lower or use_digits or use_symbols):
        print("\n⚠️ No character type selected! Using default (lowercase + numbers)")
        use_lower = True
        use_digits = True
    
    # PROCESS: Generate password
    character_pool = ""
    if use_upper:
        character_pool += string.ascii_uppercase
    if use_lower:
        character_pool += string.ascii_lowercase
    if use_digits:
        character_pool += string.digits
    if use_symbols:
        character_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one from each selected type
    password_chars = []
    if use_upper:
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password_chars.append(random.choice(string.digits))
    if use_symbols:
        password_chars.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(random.choice(character_pool))
    
    random.shuffle(password_chars)
    password = ''.join(password_chars)
    
    # OUTPUT: Display password
    print("\n" + "="*60)
    print("📤 YOUR GENERATED PASSWORD:")
    print("="*60)
    print(f"\n🔐 {password}\n")
    print("="*60)
    
    # Password strength analysis
    strength_score = 0
    if length >= 12:
        strength_score += 3
    elif length >= 8:
        strength_score += 2
    
    if use_upper and use_lower and use_digits:
        strength_score += 2
    if use_symbols:
        strength_score += 1
    
    if strength_score >= 6:
        strength_text = "💪 VERY STRONG"
    elif strength_score >= 4:
        strength_text = "✅ STRONG"
    elif strength_score >= 2:
        strength_text = "⚠️ MEDIUM"
    else:
        strength_text = "❌ WEAK"
    
    print(f"Strength: {strength_text}")
    print("\n💡 Tip: Never share this password with anyone!")
    print("="*60 + "\n")

# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    print("\n🔐 RANDOM PASSWORD GENERATOR - DecodeLabs Internship Project")
    print("="*50)
    print("Choose interface:")
    print("1. GUI Version (Graphical Interface)")
    print("2. CLI Version (Command Line)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "2":
        command_line_version()
    else:
        root = tk.Tk()
        app = PasswordGenerator(root)
        root.mainloop()