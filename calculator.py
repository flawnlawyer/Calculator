import tkinter as tk
from tkinter import font
import re


class CalculatorApp:
    """Main calculator application class"""
    
    def __init__(self, root):
        """Initialize the calculator application"""
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.root.minsize(350, 500)
        
        # Calculator state
        self.current_expression = ""
        self.memory = 0
        self.dark_mode = False
        
        # Color schemes
        self.light_theme = {
            'bg': '#f0f4f8',
            'display_bg': '#ffffff',
            'display_fg': '#1a202c',
            'button_bg': '#e2e8f0',
            'button_fg': '#2d3748',
            'button_hover': '#cbd5e0',
            'operator_bg': '#4299e1',
            'operator_fg': '#ffffff',
            'operator_hover': '#3182ce',
            'equals_bg': '#48bb78',
            'equals_fg': '#ffffff',
            'equals_hover': '#38a169',
            'memory_bg': '#ed8936',
            'memory_fg': '#ffffff',
            'memory_hover': '#dd6b20',
            'clear_bg': '#f56565',
            'clear_fg': '#ffffff',
            'clear_hover': '#e53e3e'
        }
        
        self.dark_theme = {
            'bg': '#1a202c',
            'display_bg': '#2d3748',
            'display_fg': '#00ffff',
            'button_bg': '#4a5568',
            'button_fg': '#e2e8f0',
            'button_hover': '#718096',
            'operator_bg': '#00bcd4',
            'operator_fg': '#000000',
            'operator_hover': '#00acc1',
            'equals_bg': '#00ff88',
            'equals_fg': '#000000',
            'equals_hover': '#00e676',
            'memory_bg': '#ff6b35',
            'memory_fg': '#000000',
            'memory_hover': '#ff5722',
            'clear_bg': '#ff1744',
            'clear_fg': '#ffffff',
            'clear_hover': '#d50000'
        }
        
        self.current_theme = self.light_theme
        
        # Create UI
        self.create_widgets()
        self.bind_keyboard()
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Dark mode toggle button (top right)
        self.dark_mode_btn = tk.Button(
            self.main_frame,
            text="🌙",
            font=('Arial', 16),
            command=self.toggle_dark_mode,
            relief=tk.FLAT,
            bd=0,
            cursor='hand2'
        )
        self.dark_mode_btn.grid(row=0, column=3, sticky='ne', padx=5, pady=5)
        
        # Display
        self.create_display()
        
        # Buttons
        self.create_buttons()
        
        # Configure grid weights
        for i in range(8):
            self.main_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)
    
    def create_display(self):
        """Create the calculator display"""
        display_frame = tk.Frame(
            self.main_frame,
            bg=self.current_theme['display_bg'],
            relief=tk.FLAT,
            bd=2
        )
        display_frame.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=5, pady=10)
        
        # Display label
        self.display = tk.Label(
            display_frame,
            text="0",
            font=('Segoe UI', 32, 'bold'),
            bg=self.current_theme['display_bg'],
            fg=self.current_theme['display_fg'],
            anchor='e',
            padx=20,
            pady=20
        )
        self.display.pack(fill=tk.BOTH, expand=True)
    
    def create_buttons(self):
        """Create all calculator buttons"""
        # Button definitions: (text, row, col, colspan, button_type)
        buttons = [
            # Memory row
            ('MC', 2, 0, 1, 'memory'),
            ('MR', 2, 1, 1, 'memory'),
            ('M-', 2, 2, 1, 'memory'),
            ('M+', 2, 3, 1, 'memory'),
            
            # Row 1
            ('C', 3, 0, 1, 'clear'),
            ('⌫', 3, 1, 1, 'operator'),
            ('/', 3, 2, 1, 'operator'),
            ('*', 3, 3, 1, 'operator'),
            
            # Row 2
            ('7', 4, 0, 1, 'number'),
            ('8', 4, 1, 1, 'number'),
            ('9', 4, 2, 1, 'number'),
            ('-', 4, 3, 1, 'operator'),
            
            # Row 3
            ('4', 5, 0, 1, 'number'),
            ('5', 5, 1, 1, 'number'),
            ('6', 5, 2, 1, 'number'),
            ('+', 5, 3, 1, 'operator'),
            
            # Row 4
            ('1', 6, 0, 1, 'number'),
            ('2', 6, 1, 1, 'number'),
            ('3', 6, 2, 1, 'number'),
            ('=', 6, 3, 1, 'equals'),
            
            # Row 5
            ('0', 7, 0, 2, 'number'),
            ('.', 7, 2, 1, 'number'),
        ]
        
        self.buttons = {}
        
        for btn_text, row, col, colspan, btn_type in buttons:
            # Determine button colors
            if btn_type == 'number':
                bg = self.current_theme['button_bg']
                fg = self.current_theme['button_fg']
                hover_bg = self.current_theme['button_hover']
            elif btn_type == 'operator':
                bg = self.current_theme['operator_bg']
                fg = self.current_theme['operator_fg']
                hover_bg = self.current_theme['operator_hover']
            elif btn_type == 'equals':
                bg = self.current_theme['equals_bg']
                fg = self.current_theme['equals_fg']
                hover_bg = self.current_theme['equals_hover']
            elif btn_type == 'memory':
                bg = self.current_theme['memory_bg']
                fg = self.current_theme['memory_fg']
                hover_bg = self.current_theme['memory_hover']
            elif btn_type == 'clear':
                bg = self.current_theme['clear_bg']
                fg = self.current_theme['clear_fg']
                hover_bg = self.current_theme['clear_hover']
            
            # Create button
            btn = tk.Button(
                self.main_frame,
                text=btn_text,
                font=('Segoe UI', 18, 'bold'),
                bg=bg,
                fg=fg,
                activebackground=hover_bg,
                activeforeground=fg,
                relief=tk.FLAT,
                bd=0,
                cursor='hand2',
                command=lambda t=btn_text: self.button_click(t)
            )
            
            # Grid placement
            rowspan = 2 if btn_text == '=' else 1
            btn.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,
                    sticky='nsew', padx=3, pady=3)
            
            # Store button reference
            self.buttons[btn_text] = {
                'widget': btn,
                'default_bg': bg,
                'hover_bg': hover_bg,
                'fg': fg
            }
            
            # Bind hover effects
            btn.bind('<Enter>', lambda e, b=btn, h=hover_bg: self.button_hover_enter(b, h))
            btn.bind('<Leave>', lambda e, b=btn, bg=bg: self.button_hover_leave(b, bg))
    
    def button_click(self, value):
        """Handle button click events"""
        if value == 'C':
            self.clear()
        elif value == '⌫':
            self.backspace()
        elif value == '=':
            self.calculate()
        elif value == 'MC':
            self.memory_clear()
        elif value == 'MR':
            self.memory_recall()
        elif value == 'M+':
            self.memory_add()
        elif value == 'M-':
            self.memory_subtract()
        else:
            # Add to expression
            if self.current_expression == "0" or self.current_expression == "Error":
                self.current_expression = ""
            self.current_expression += str(value)
            self.update_display(self.current_expression)
    
    def calculate(self):
        """Evaluate the current expression"""
        try:
            # Replace × and ÷ if used
            expression = self.current_expression.replace('×', '*').replace('÷', '/')
            
            # Safe evaluation - only allow numbers and basic operators
            if re.match(r'^[\d+\-*/().\s]+$', expression):
                result = eval(expression)
                # Format result
                if isinstance(result, float):
                    # Remove trailing zeros
                    result = f"{result:.10f}".rstrip('0').rstrip('.')
                self.current_expression = str(result)
                self.update_display(self.current_expression)
            else:
                self.update_display("Error")
                self.current_expression = "Error"
        except ZeroDivisionError:
            self.update_display("Error")
            self.current_expression = "Error"
        except Exception:
            self.update_display("Error")
            self.current_expression = "Error"
    
    def clear(self):
        """Clear the display"""
        self.current_expression = "0"
        self.update_display("0")
    
    def backspace(self):
        """Delete last character"""
        if self.current_expression and self.current_expression != "0":
            self.current_expression = self.current_expression[:-1]
            if not self.current_expression:
                self.current_expression = "0"
            self.update_display(self.current_expression)
    
    def memory_add(self):
        """Add current value to memory"""
        try:
            current_value = float(self.current_expression) if self.current_expression else 0
            self.memory += current_value
            self.flash_button('M+')
        except:
            pass
    
    def memory_subtract(self):
        """Subtract current value from memory"""
        try:
            current_value = float(self.current_expression) if self.current_expression else 0
            self.memory -= current_value
            self.flash_button('M-')
        except:
            pass
    
    def memory_recall(self):
        """Recall memory value"""
        self.current_expression = str(self.memory)
        self.update_display(self.current_expression)
        self.flash_button('MR')
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
        self.flash_button('MC')
    
    def flash_button(self, btn_text):
        """Flash animation for memory buttons"""
        if btn_text in self.buttons:
            btn = self.buttons[btn_text]['widget']
            original_bg = self.buttons[btn_text]['default_bg']
            btn.config(bg='#ffffff')
            self.root.after(100, lambda: btn.config(bg=original_bg))
    
    def update_display(self, text):
        """Update the display with new text"""
        # Limit display length
        if len(text) > 15:
            text = text[:15]
        self.display.config(text=text)
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.current_theme = self.dark_theme if self.dark_mode else self.light_theme
        
        # Update dark mode button
        self.dark_mode_btn.config(text="☀️" if self.dark_mode else "🌙")
        
        # Apply theme
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme to all widgets"""
        # Update root and main frame
        self.root.config(bg=self.current_theme['bg'])
        self.main_frame.config(bg=self.current_theme['bg'])
        
        # Update display
        self.display.config(
            bg=self.current_theme['display_bg'],
            fg=self.current_theme['display_fg']
        )
        self.display.master.config(bg=self.current_theme['display_bg'])
        
        # Update dark mode button
        self.dark_mode_btn.config(
            bg=self.current_theme['bg'],
            fg=self.current_theme['display_fg']
        )
        
        # Update all buttons
        for btn_text, btn_info in self.buttons.items():
            btn = btn_info['widget']
            
            # Determine button type and get new colors
            if btn_text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                bg = self.current_theme['button_bg']
                fg = self.current_theme['button_fg']
                hover_bg = self.current_theme['button_hover']
            elif btn_text in ['+', '-', '*', '/', '⌫']:
                bg = self.current_theme['operator_bg']
                fg = self.current_theme['operator_fg']
                hover_bg = self.current_theme['operator_hover']
            elif btn_text == '=':
                bg = self.current_theme['equals_bg']
                fg = self.current_theme['equals_fg']
                hover_bg = self.current_theme['equals_hover']
            elif btn_text in ['MC', 'MR', 'M+', 'M-']:
                bg = self.current_theme['memory_bg']
                fg = self.current_theme['memory_fg']
                hover_bg = self.current_theme['memory_hover']
            elif btn_text == 'C':
                bg = self.current_theme['clear_bg']
                fg = self.current_theme['clear_fg']
                hover_bg = self.current_theme['clear_hover']
            
            # Update button
            btn.config(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg)
            
            # Update stored colors
            self.buttons[btn_text]['default_bg'] = bg
            self.buttons[btn_text]['hover_bg'] = hover_bg
            self.buttons[btn_text]['fg'] = fg
    
    def button_hover_enter(self, button, hover_color):
        """Handle button hover enter - glow effect"""
        button.config(bg=hover_color)
        if self.dark_mode:
            button.config(relief=tk.RAISED, bd=2)
    
    def button_hover_leave(self, button, original_color):
        """Handle button hover leave - remove glow"""
        button.config(bg=original_color)
        if self.dark_mode:
            button.config(relief=tk.FLAT, bd=0)
    
    def bind_keyboard(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Key>', self.handle_keypress)
    
    def handle_keypress(self, event):
        """Handle keyboard input"""
        key = event.char
        keysym = event.keysym
        
        # Numbers and operators
        if key in '0123456789.+-*/':
            self.button_click(key)
        
        # Enter for equals
        elif keysym == 'Return':
            self.calculate()
        
        # Backspace
        elif keysym == 'BackSpace':
            self.backspace()
        
        # Escape for clear
        elif keysym == 'Escape':
            self.clear()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
