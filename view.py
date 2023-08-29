import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.initial_dialog = InitialDialog(self)
        self.passes = []

        self.create_view()

        self.title("Pass Calculator")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.resizable(False, False)

        self.eval("tk::PlaceWindow . center")
        self.eval(f"tk::PlaceWindow {str(self.initial_dialog)} center")

    def add_pass_row(self):
        stringVar_mass = tk.StringVar()
        stringVar_enrichment = tk.StringVar()
        stringVar_result = tk.StringVar()
        self.passes.append({
            "label_number":ttk.Label(self, text=len(self.passes)+1),
            "stringVar_mass":stringVar_mass, 
            "stringVar_enrichment":stringVar_enrichment,
            "entry_mass":ttk.Entry(self, textvariable=stringVar_mass), 
            "entry_mass_unit":ttk.Label(self, text="g", background="white"),
            "entry_enrichment":ttk.Entry(self, textvariable=stringVar_enrichment),
            "entry_enrichment_unit":ttk.Label(self, text="%", background="white"),
            "stringVar_result":stringVar_result,
            "entry_result":ttk.Entry(self, textvariable=stringVar_result, state="disabled"),
        })

        last_row = self.grid_size()[1]
        self.passes[-1]["label_number"].grid(row=last_row, column=0)
        self.passes[-1]["entry_mass"].grid(row=last_row, column=1)
        self.passes[-1]["entry_mass_unit"].grid(row=last_row, column=1, sticky="e", padx=(0,3))
        self.passes[-1]["entry_enrichment"].grid(row=last_row, column=2)
        self.passes[-1]["entry_enrichment_unit"].grid(row=last_row, column=2, sticky="e", padx=(0,3))
        self.passes[-1]["entry_result"].grid(row=last_row, column=3)
        self.button_add.grid(row=last_row+1, column=2, sticky="nsew")
        self.button_remove.grid(row=last_row+1, column=1, sticky="nsew")
        self.button_recalculate.grid(row=last_row+1, column=3, sticky="nsew")


    def remove_pass_row(self):
        if len(self.passes) <= 1:
            return
        row = self.passes.pop()
        for key in row.keys():
            if key.startswith("stringVar"):
                continue
            row[key].destroy()


    def create_view(self):
        ttk.Label(self, text="Pass #").grid(row=0, column=0)
        ttk.Label(self, text="Mass D2O").grid(row=0, column=1)
        ttk.Label(self, text="Enrichment of D2O").grid(row=0, column=2)
        ttk.Label(self, text="Resulting Enrichment").grid(row=0, column=3)
        self.button_remove = ttk.Button(self, text="-", command=self.remove_pass_row)
        self.button_remove.grid(row=1, column=1, sticky="nsew")
        self.button_add = ttk.Button(self, text="+", command=self.add_pass_row)
        self.button_add.grid(row=1, column=2, sticky="nsew")
        self.button_recalculate = ttk.Button(self, text="Recalculate")
        self.button_recalculate.grid(row=1, column=3, sticky="nsew")

        for i in range(10):
            self.add_pass_row()


class InitialDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.entries = {}
        self.create_view()

        self.title("Input Data")
        self.protocol("WM_DELETE_WINDOW", self.parent.destroy)
        self.resizable(False, False)

    def create_view(self):
        ttk.Label(self, text="Mass of Substrate").grid(row=0, column=0, sticky="e")
        self.entries["mass_substrate"] = tk.StringVar()
        entry_mass_substrate = ttk.Entry(self, textvariable=self.entries["mass_substrate"], width=20)
        entry_mass_substrate.grid(row=0, column=1)
        ttk.Label(self, text="g", background="white").grid(row=0, column=1, sticky="e", padx=(0,3))

        ttk.Label(self, text="MW of Substrate").grid(row=1, column=0, sticky="e")
        self.entries["mw_substrate"] = tk.StringVar()
        entry_mw_substrate = ttk.Entry(self, textvariable=self.entries["mw_substrate"], width=20)
        entry_mw_substrate.grid(row=1, column=1)
        ttk.Label(self, text="g/mol", background="white").grid(row=1, column=1, sticky="e", padx=(0,3))

        ttk.Label(self, text="Exchanging H's").grid(row=2, column=0, sticky="e")
        self.entries["ex_H_substrate"] = tk.StringVar()
        entry_ex_H_substrate = ttk.Entry(self, textvariable=self.entries["ex_H_substrate"], width=20)
        entry_ex_H_substrate.grid(row=2, column=1)
        ttk.Label(self, text="H's", background="white").grid(row=2, column=1, sticky="e", padx=(0,3))

        ttk.Label(self, text="D2O per Pass").grid(row=3, column=0, sticky="e")
        self.entries["d2o_per_pass"] = tk.StringVar()
        entry_init_enrich_substrate = ttk.Entry(self, textvariable=self.entries["d2o_per_pass"], width=20)
        entry_init_enrich_substrate.grid(row=3, column=1)
        ttk.Label(self, text="g", background="white").grid(row=3, column=1, sticky="e", padx=(0,3))

        ttk.Label(self, text="Initial Enrichment").grid(row=4, column=0, sticky="e")
        self.entries["init_enrich_substrate"] = tk.StringVar()
        entry_init_enrich_substrate = ttk.Entry(self, textvariable=self.entries["init_enrich_substrate"], width=20)
        entry_init_enrich_substrate.grid(row=4, column=1)
        ttk.Label(self, text="%", background="white").grid(row=4, column=1, sticky="e", padx=(0,3))

        self.button_next = ttk.Button(self, text="Next")
        self.button_next.grid(row=5, column=0, columnspan=2, sticky="nsew")


if __name__ == "__main__":
    view = MainView()
    view.mainloop()
