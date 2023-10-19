class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.set_defaults()
        self.connect_listeners()

    def run(self):
        self.view.withdraw()
        self.view.mainloop()

    def initial_dialog_next_button_listener(self, *args):
        self.model.mass_substrate = float(self.view.initial_dialog.stringVars["mass_substrate"].get())
        self.model.mw_substrate = float(self.view.initial_dialog.stringVars["mw_substrate"].get())
        self.model.ex_H_substrate = int(self.view.initial_dialog.stringVars["ex_H_substrate"].get())
        self.model.init_enrich_substrate = float(self.view.initial_dialog.stringVars["init_enrich_substrate"].get())
        self.model.d2o_per_pass = float(self.view.initial_dialog.stringVars["d2o_per_pass"].get())
        for rxn_pass in self.view.passes:
            rxn_pass["stringVar_mass"].set(self.view.initial_dialog.stringVars["d2o_per_pass"].get())
        self.model.ex_H_moles = self.model.mass_substrate * self.model.ex_H_substrate / self.model.mw_substrate

        self.view.label_substrate_mass.configure(text=f"Mass of Substrate: {self.model.mass_substrate} g")
        self.view.label_substrate_mw.configure(text=f"MW of Substrate: {self.model.mw_substrate} g/mol")
        self.view.label_substrate_ex_H.configure(text=f"Exchanging H's: {self.model.ex_H_substrate}")
        self.view.label_substrate_initial_enrichment.configure(text=f"Initial Enrichment: {self.model.init_enrich_substrate} %")

        self.view.initial_dialog.destroy()
        self.view.deiconify()
        for i in range(len(self.view.passes)):
            self.model.add_pass()
        self.update_view_results()

    def view_add_pass_button_listener(self):
        self.view.add_pass_row()
        self.model.add_pass()
        self.view.passes[-1]["stringVar_mass"].set(self.model.rxn_pass[-1]["d2o_mass"])
        self.view.passes[-1]["stringVar_enrichment"].set(self.model.rxn_pass[-1]["d2o_enrichment"])
        self.update_view_results()

    def view_remove_pass_button_listener(self):
        self.view.remove_pass_row()
        self.model.remove_pass()
        self.update_view_results()

    def connect_listeners(self):
        self.view.initial_dialog.button_next.configure(command=self.initial_dialog_next_button_listener)
        self.view.initial_dialog.bind("<Return>", self.initial_dialog_next_button_listener)

        self.view.button_add.configure(command=self.view_add_pass_button_listener)
        self.view.button_remove.configure(command=self.view_remove_pass_button_listener)
        self.view.button_recalculate.configure(command=self.update_view_results)
        self.view.bind("<Return>", self.update_view_results)

        validate_command = (self.view.register(self.entry_validation), "%P")
        for key in self.view.initial_dialog.entries.keys():
            self.view.initial_dialog.entries[key].configure(validate="all", validatecommand=validate_command)
        for i in range(len(self.view.passes)):
            for key in self.view.passes[i].keys():
                if key.startswith("entry_"):
                    self.view.passes[i][key].configure(validate="all", validatecommand=validate_command)

    def update_view_results(self, *args):
        for i in range(len(self.view.passes)):
            self.model.rxn_pass[i]["d2o_mass"] = float(self.view.passes[i]["stringVar_mass"].get())
            self.model.rxn_pass[i]["d2o_enrichment"] = float(self.view.passes[i]["stringVar_enrichment"].get())
            self.model.rxn_pass[i]["d2o_D_moles"] = self.model.rxn_pass[i]["d2o_mass"]/20.03*2
            self.model.rxn_pass[i]["total_moles"] = self.model.ex_H_moles + self.model.rxn_pass[i]["d2o_D_moles"]
        self.model.recalculate()
        for i in range(len(self.model.rxn_pass)):
            self.view.passes[i]["stringVar_result"].set(f"""{round(self.model.rxn_pass[i]["final_enrichment"], 3):.3f}""")

    def set_defaults(self):
        self.view.initial_dialog.stringVars["init_enrich_substrate"].set(Model.defaults["INITIAL_ENRICHMENT"])
        for rxn_pass in self.view.passes:
            rxn_pass["stringVar_enrichment"].set(Model.defaults["D2O_ENRICHMENT"])

    def entry_validation(self, value):
        try:
            float(value)
        except ValueError:
            return False
        return True


from view import MainView
from model import Model
if __name__ == '__main__':
    view = MainView()
    model = Model()
    app = Controller(view, model)
    try:
        import pyi_splash
        pyi_splash.close()
    except ModuleNotFoundError:
        pass
    app.run()
