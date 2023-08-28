class Model:
    defaults = {
        "INITIAL_ENRICHMENT":0.0156,
        "D2O_ENRICHMENT":99.8
    }

    def __init__(self):
        self.mass_substrate = None
        self.mw_substrate = None
        self.ex_H_substrate = None
        self.ex_H_moles = None
        self.init_enrich_substrate = None
        self.d2o_per_pass = None

        self.rxn_pass = []

    def add_pass(self):
        self.rxn_pass.append({})
        self.rxn_pass[-1]['d2o_mass'] = self.d2o_per_pass
        self.rxn_pass[-1]['d2o_enrichment'] = self.defaults["D2O_ENRICHMENT"]
        self.rxn_pass[-1]['d2o_D_moles'] = self.d2o_per_pass/20.03*2
        self.rxn_pass[-1]['total_moles'] = self.rxn_pass[-1]["d2o_D_moles"] + self.ex_H_moles

        if len(self.rxn_pass) == 1:
            substrate_enrichment = self.init_enrich_substrate
        else:
            substrate_enrichment = self.rxn_pass[-2]["final_enrichment"]
        substrate_H_moles = self.ex_H_moles
        moles_D = self.rxn_pass[-1]['d2o_D_moles']
        d2o_enrichment = self.rxn_pass[-1]['d2o_enrichment']
        total_moles = substrate_H_moles + moles_D
        final_enrichment = ((substrate_enrichment * substrate_H_moles) + (d2o_enrichment * moles_D)) / total_moles
        self.rxn_pass[-1]['final_enrichment'] = final_enrichment

    def recalculate(self):
        for i in range(len(self.rxn_pass)):
            self.rxn_pass[i]

if __name__ == '__main__':
    model = Model()
    model.mass_substrate = 300
    model.mw_substrate = 120.15
    model.ex_H_substrate = 3
    model.ex_H_moles = model.mass_substrate * model.ex_H_substrate / model.mw_substrate
    model.init_enrich_substrate = Model.defaults["INITIAL_ENRICHMENT"]
    model.d2o_per_pass = 250
    for i in range (10):
        model.add_pass()
        print(round(model.rxn_pass[-1]['final_enrichment'], 3))
