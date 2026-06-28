try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
except ModuleNotFoundError:
    tk = None
    messagebox = None
    scrolledtext = None

from recipe_generator import RecipeGenerator


# =========================
# GUI DESIGN AND USER INTERACTION
# =========================
class RecipeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.generator = RecipeGenerator()

        self.root.title("AI Powered Recipe Generator")
        self.root.geometry("850x650")    
        self.root.minsize(750, 560)      
        self.root.configure(bg="#f5f7fb")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="AI Powered Recipe Generator",
            font=("Arial", 22, "bold"),
            bg="#f5f7fb",
            fg="#1f2937",
        )
        title_label.pack(pady=(18, 5))

        subtitle_label = tk.Label(
            self.root,
            text="Enter the ingredients you have and get smart recipe suggestions.",
            font=("Arial", 11),
            bg="#f5f7fb",
            fg="#4b5563",
        )
        subtitle_label.pack(pady=(0, 15))

        input_frame = tk.Frame(self.root, bg="#f5f7fb")
        input_frame.pack(fill="x", padx=24)

        ingredient_label = tk.Label(
            input_frame,
            text="Available Ingredients",
            font=("Arial", 12, "bold"),
            bg="#f5f7fb",
            fg="#111827",
        )
        ingredient_label.pack(anchor="w")

        self.ingredient_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            relief="solid",
            bd=1,
            bg="#111827",
            fg="white",
            insertbackground="white",
        )
        self.ingredient_entry.pack(fill="x", pady=(6, 8), ipady=7)
        self.ingredient_entry.insert(0, "rice, tomato, onion, chicken")

        button_frame = tk.Frame(self.root, bg="#f5f7fb")
        button_frame.pack(fill="x", padx=24, pady=8)

        self.generate_button = self.create_black_button(
            button_frame,
            "Generate Recipes",
            self.generate_recipes,
        )
        self.generate_button.pack(side="left", padx=(0, 8))

        self.substitute_button = self.create_black_button(
            button_frame,
            "Find Substitute",
            self.find_substitute,
        )
        self.substitute_button.pack(side="left", padx=8)

        self.view_all_button = self.create_black_button(
            button_frame,
            "View All Recipes",
            self.view_all_recipes,
        )
        self.view_all_button.pack(side="left", padx=8)

        self.clear_button = self.create_black_button(
            button_frame,
            "Clear",
            self.clear_screen,
        )
        self.clear_button.pack(side="left", padx=8)

        self.exit_button = self.create_black_button(
            button_frame,
            "Exit",
            self.root.destroy,
        )
        self.exit_button.pack(side="right")

        result_label = tk.Label(
            self.root,
            text="Recipe Suggestions",
            font=("Arial", 12, "bold"),
            bg="#f5f7fb",
            fg="#111827",
        )
        result_label.pack(anchor="w", padx=24, pady=(12, 0))

        self.result_area = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 11),
            wrap=tk.WORD,
            relief="solid",
            bd=1,
            bg="white",
            fg="#111827",
        )
        self.result_area.pack(fill="both", expand=True, padx=24, pady=(6, 20))

        welcome_text = (
            "Welcome!\n\n"
            "Type your ingredients separated by commas, then click Generate Recipes.\n"
            "Example: rice, tomato, onion, chicken\n\n"
            "This project uses OOP and smart rule-based AI logic to rank recipes "
            "and suggest substitutes."
        )
        self.display_result(welcome_text)

    def create_black_button(self, parent, text, command):
        button = tk.Label(
            parent,
            text=text,
            bg="black",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=14,
            pady=9,
            cursor="hand2",
        )

        button.bind("<Button-1>", lambda event: command())
        button.bind("<Enter>", lambda event: button.config(bg="#222222"))
        button.bind("<Leave>", lambda event: button.config(bg="black"))
        return button

    def generate_recipes(self):
        ingredient_text = self.ingredient_entry.get()
        result = self.generator.format_recipe_suggestions(ingredient_text)
        self.display_result(result)

    def find_substitute(self):
        ingredient_text = self.ingredient_entry.get()

        if "," in ingredient_text:
            messagebox.showinfo(
                "Substitute Tip",
                "For substitute search, enter only one ingredient at a time.",
            )
            return

        result = self.generator.format_substitutes(ingredient_text)
        self.display_result(result)

    def view_all_recipes(self):
        self.display_result(self.generator.format_all_recipes())

    def clear_screen(self):
        self.ingredient_entry.delete(0, tk.END)
        self.display_result("Screen cleared. Enter new ingredients to begin.")

    def display_result(self, text):
        self.result_area.config(state="normal")
        self.result_area.delete("1.0", tk.END)
        self.result_area.insert(tk.END, text)
        self.result_area.config(state="disabled")


def main():
    if tk is None:
        print(
            "Tkinter is not available in this Python installation. "
            "Install or enable Tkinter, then run this file again."
        )
        return

    root = tk.Tk()
    RecipeGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
