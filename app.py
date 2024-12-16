import tkinter as tk
from tkinter import ttk
import web_scraper as web

def fetchPokemonData():
    return web.get_pokedex()

class App():
    def __init__(self, root):
        self.pokemon_list,self.pokemon_ids = fetchPokemonData()
        root.title("GO Get Movesets")
        root.resizable(False, False)
        root.geometry("400x270")
        root.iconbitmap("icon.ico")
        root.configure(bg="#DEEFF5")
        self.create_main_frame(root)
        self.create_search_frame()
        self.create_label_frame()
        
    def create_main_frame(self, root):
        self.main_frame = tk.Frame(root, bg="#DEEFF5")
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        for i in range(5):
            self.main_frame.grid_rowconfigure(i, weight=1)
            self.main_frame.grid_columnconfigure(i, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=0)
        self.intro = tk.Label(self.main_frame, text="Search a pokemon!", font=("Arial",15), bg="#DEEFF5")
        self.intro.grid(row=0, column=2)
    
    def create_search_frame(self):
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
        if event.keysym == "Return":
            self.search()

    def search(self):
        try:
            fast, charge = web.get_moveset(self.combobox.get())
            self.fast_attack.config(text=fast)
            self.charged_attack.config(text=charge)
            self.combobox.set("")
        except:
            print("Pokemon doesn't exist")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()