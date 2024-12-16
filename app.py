import tkinter as tk
from tkinter import ttk
import web_scraper as web

def fetchPokemonData():
    """
    Function Description:
        Fetches list of pokemon names and list of their corresponding ids
    Return:
        tuple: List of pokemon names and list of their corresponding ids
    """
    return web.get_pokedex()

class App():
    def __init__(self, root):
        # Fetch Pokemon data
        self.pokemon_list,self.pokemon_ids = fetchPokemonData()
        # Set up window
        root.title("GO Get Movesets")
        root.resizable(False, False)
        root.geometry("400x270")
        root.iconbitmap("icon.ico")
        root.configure(bg="#DEEFF5")
        self.create_main_frame(root)
        self.create_search_frame()
        self.create_label_frame()
        
    def create_main_frame(self, root):
        """
        Function Description:
            Create main frame for application
        Parameters:
            root (tk.Tk): Root window
        """
        self.main_frame = tk.Frame(root, bg="#DEEFF5")
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        for i in range(5):
            self.main_frame.grid_rowconfigure(i, weight=1)
            self.main_frame.grid_columnconfigure(i, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=0)
        self.intro = tk.Label(self.main_frame, text="Search a pokemon!", font=("Arial",15), bg="#DEEFF5")
        self.intro.grid(row=0, column=2)
    
    def create_search_frame(self):
        """
        Function Description:
            Create search frame to get Pokemon's name from user
        """
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.grid(row=1, column=2, sticky="S")
        self.search_frame.grid_rowconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=1)

        self.combobox = ttk.Combobox(self.search_frame, value=self.pokemon_list, width=20, height=10, font=("Arial", 20))
        self.combobox.grid(row=0, column=0)
        self.combobox.bind("<KeyRelease>", self.updateCombobox)
        self.combobox.bind("<KeyPress>", self.enter)

        self.search_icon = tk.PhotoImage(master=self.search_frame, file="search.png")
        self.search_button = tk.Button(self.search_frame, image=self.search_icon, width=32, height=32, command=self.search)
        self.search_button.grid(row=0, column=1)
    
    def create_label_frame(self):
        """
        Function Description:
            Create label frame to display optimal fast and charged attacks
        """
        self.label_frame = tk.Frame(self.main_frame, bg="#DEEFF5")
        self.label_frame.grid(row=2, column=2, sticky="NSEW")
        for i in range(2):
            self.label_frame.grid_columnconfigure(i, weight=1)
            self.label_frame.grid_rowconfigure(i, weight=1)

        self.fast_label = tk.Label(self.label_frame, text="Fast Attack: ", font=("Arial", 18), bg="#DEEFF5")
        self.fast_label.grid(row=0, column=0, sticky="SW")
        self.fast_attack = tk.Label(self.label_frame, text="", font=("Arial", 18), bg="#DEEFF5")
        self.fast_attack.grid(row=0, column=1, sticky="SW")
        self.charged_label = tk.Label(self.label_frame, text="Charged Attack: ", font=("Arial", 18), bg="#DEEFF5")
        self.charged_label.grid(row=1, column=0, sticky="NW")
        self.charged_attack = tk.Label(self.label_frame, text="", font=("Arial", 18), bg="#DEEFF5")
        self.charged_attack.grid(row=1, column=1, sticky="NW")

    def updateCombobox(self,event):
        """
        Function Description:
            Updates combobox suggestions as user types
        Parameters:
            event (tk.Event): Event triggered by key release
        """
        value = event.widget.get()
        if value == "":
            self.combobox["value"] = self.pokemon_list
        else: 
            data = []
            for pokemon in self.pokemon_list:
                if value.lower() in pokemon.lower()[0:len(value)]:
                    data.append(pokemon)
            self.combobox["value"] = data   

    def enter(self,event):
        """
        Function Description:
            Triggers search for Pokemon's moveset when enter key is pressed
        Parameters:
            event (tk.Event): Event triggered by key press
        """
        if event.keysym == "Return":
            self.search()

    def clear_label_config(self):
        """
        Function Description:
            Reset label after error message is displayed
        """
        self.intro.config(text="Search a pokemon!", fg="black", font=("Arial", 15))

    def search(self):
        """
        Function Description:
            Searches for searched Pokemon's fast and charged attacks, and displays results by updating labels     
        """
        try:
            fast, charge = web.get_moveset(self.combobox.get())
            self.fast_attack.config(text=fast)
            self.charged_attack.config(text=charge)
            self.combobox.set("")
        except:
            # Show error message if pokemon cannot be found in website's database
            self.intro.configure(text="Error: Pokemon does not exist in database.", font=("Arial", 14), fg="red")
            root.after(1500, self.clear_label_config)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()