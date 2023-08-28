class Presenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.set_defaults()
        self.connect_listeners()

    def run(self):
        self.view.mainloop()

    def initial_dialog_next_button_listener(self):
        self.model.mass_substrate = float(self.view.initial_dialog.entries["mass_substrate"].get())
        self.model.mw_substrate = float(self.view.initial_dialog.entries["mw_substrate"].get())
        self.model.ex_H_substrate = int(self.view.initial_dialog.entries["ex_H_substrate"].get())
        self.model.init_enrich_substrate = float(self.view.initial_dialog.entries["init_enrich_substrate"].get())
        self.model.d2o_per_pass = float(self.view.initial_dialog.entries["d2o_per_pass"].get())
        for rxn_pass in self.view.passes:
            rxn_pass["stringVar_mass"].set(self.view.initial_dialog.entries["d2o_per_pass"].get())
        self.model.ex_H_moles = self.model.mass_substrate * self.model.ex_H_substrate / self.model.mw_substrate

        self.view.initial_dialog.destroy()
        self.view.deiconify()
        for i in range(10):
            self.model.add_pass()

        self.update_view_results()

    def connect_listeners(self):
        self.view.initial_dialog.button_next.configure(command=self.initial_dialog_next_button_listener)

    def update_view_results(self):
        for i in range(len(self.model.rxn_pass)):
            self.view.passes[i]["stringVar_result"].set(f"""{round(self.model.rxn_pass[i]["final_enrichment"], 3):.3f}""")


    def set_defaults(self):
        self.view.initial_dialog.entries["init_enrich_substrate"].set(Model.defaults["INITIAL_ENRICHMENT"])
        for rxn_pass in self.view.passes:
            rxn_pass["stringVar_enrichment"].set(Model.defaults["D2O_ENRICHMENT"])


from view import MainView
from model import Model
if __name__ == '__main__':
    view = MainView()
    model = Model()
    app = Presenter(view, model)
    app.run()
