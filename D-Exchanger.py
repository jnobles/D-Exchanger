D_NAT_ABUNDANCE = 0.0156
STD_D2O_ENRICHMENT = 99.8
D2O_MW = 20.03


grams_substrate = 300
mw_substrate = 120.15
H_to_exchange = 3

mole_H_to_exchange = (grams_substrate * H_to_exchange) / mw_substrate

grams_d2o = 250
mole_d_available = (grams_d2o / D2O_MW) * 2

total_moles_of_exchanging_atoms = mole_H_to_exchange + mole_d_available


def calculate_pass():
    output = ((mole_d_available * STD_D2O_ENRICHMENT) + (mole_H_to_exchange * D_NAT_ABUNDANCE)) / total_moles_of_exchanging_atoms
    print(output)

if __name__ == "__main__":
    calculate_pass()
