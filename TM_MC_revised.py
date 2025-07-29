"""
tm_mc_mapper

This module provides mapping functions for linking herbs, compounds, proteins, and diseases
based on the TM-MC 2.0 (Traditional Medicine - Molecular Compound) database.

Main Functionalities:
- Convert herb names (Korean ↔ Latin)
- Retrieve filtered or all compounds from herbs (via ADME filtering)
- Map compounds to proteins and vice versa
- Map proteins to diseases and vice versa
- Reverse screening: find herbs related to a given disease

Input files:
- herb name.xlsx
- medicinal_compound.xlsx
- chemical_property(PD).xlsx
- chemical_protein.xlsx
- protein_disease.xlsx

Output:
- Excel files containing compound/protein/herb mappings and overlaps
"""




import openpyxl
import pandas as pd

# 🔧 File paths
HERB_NAME_FILE = './TM_MC DB/herb name.xlsx'
COMPOUND_FILE = './TM_MC DB/medicinal_compound.xlsx'
CHEMICAL_PROPERTY_FILE = './TM_MC DB/chemical_property(PD).xlsx'
CHEMICAL_PROTEIN_FILE = './TM_MC DB/chemical_protein.xlsx'
PROTEIN_DISEASE_FILE = './TM_MC DB/protein_disease.xlsx'

# 📂 Load data
herb_df = pd.read_excel(HERB_NAME_FILE, sheet_name='Sheet1')
compound_df = pd.read_excel(COMPOUND_FILE, sheet_name='Sheet1')
chemical_property_df = pd.read_excel(CHEMICAL_PROPERTY_FILE, sheet_name='Sheet1')
chemical_protein_df = pd.read_excel(CHEMICAL_PROTEIN_FILE, sheet_name='Sheet1')
protein_disease_df = pd.read_excel(PROTEIN_DISEASE_FILE, sheet_name='Sheet1')


# =======================
# 🔁 Herb name conversions
# =======================

def korean_to_latin(korean_herb_name):
    """
    Convert Korean herb name to its Latin name.
    """
    korean_names = herb_df.iloc[:, 2].tolist()[1:]
    latin_names = herb_df.iloc[:, 0].tolist()[1:]

    if korean_herb_name in korean_names:
        return latin_names[korean_names.index(korean_herb_name)]
    else:
        return "No matching Latin name found."


def latin_to_compound_id(latin_name):
    """
    Get all compound IDs associated with a given Latin herb name.
    """
    compound_ids = compound_df[compound_df["LATIN"] == latin_name]["ID"].unique()
    return [cid for cid in compound_ids if cid != 0]


# =======================
# 🔁 Compound ↔ Protein
# =======================

def compound_to_protein(compound_ids):
    """
    Convert a list of compound IDs to associated protein IDs.
    """
    protein_ids = chemical_protein_df[chemical_protein_df["ID"].isin(compound_ids)]["PROTEINID"].unique()
    return protein_ids.tolist()


# =======================
# 🌿 Get ingredients (whole & filtered)
# =======================

def adme_filtering_2(herb_name):
    """
    Get compound IDs from a herb using ADME filtering (DL ≥ 0.18 and OB == 'Y').
    Also saves the filtered compound names to Excel.
    """
    latin_name = korean_to_latin(herb_name)
    compound_ids = latin_to_compound_id(latin_name)

    filtered = chemical_property_df[
        (chemical_property_df["ID"].isin(compound_ids)) &
        (chemical_property_df["DL"] >= 0.18) &
        (chemical_property_df["OB"] == 'Y')
    ]
    filtered_ids = filtered["ID"].unique()
    compound_names = compound_df[(compound_df["ID"].isin(filtered_ids)) & (compound_df["LATIN"] == latin_name)]["COMPOUND"].unique()

    result_df = pd.DataFrame(compound_names, columns=["Filtered Compounds"])
    result_df.to_excel(f'./Result/{herb_name}_filtered_compounds(TM-MC).xlsx', index=False)

    return filtered["ID"].tolist()


def Whole_ingredients_and_filtered(korean_herb_name):
    """
    Save both all and ADME-filtered ingredients of a herb to Excel files.
    """
    latin_name = korean_to_latin(korean_herb_name)
    all_compounds = compound_df[compound_df["LATIN"] == latin_name]["COMPOUND"].unique()

    df = pd.DataFrame(all_compounds, columns=["All Compounds"])
    df.to_excel(f"./Result/{korean_herb_name}_Whole_ingredients(TM-MC).xlsx", index=False)

    adme_filtering_2(korean_herb_name)


# =======================
# 🔁 Reverse mapping
# =======================

def disease_to_protein(disease_code):
    """
    Convert a disease code (UMLS CUI) to a list of protein IDs.
    """
    protein_ids = protein_disease_df[protein_disease_df["DISEASEID"] == disease_code]["PROTEIN"].unique()
    return protein_ids.tolist()


def protein_to_chemical(protein_ids):
    """
    Convert a list of protein IDs to associated compound IDs.
    """
    compound_ids = chemical_protein_df[chemical_protein_df["PROTEINID"].isin(protein_ids)]["ID"].unique()
    return compound_ids.tolist()


def chemical_to_latin(compound_ids):
    """
    Convert compound IDs to associated Latin herb names.
    """
    latin_names = compound_df[compound_df["ID"].isin(compound_ids)]["LATIN"].unique()
    return latin_names.tolist()


def latin_to_korean(latin_names):
    """
    Convert Latin herb names to Korean herb names.
    """
    korean_names = herb_df[herb_df["LATIN"].isin(latin_names)]["KOREAN"].unique()
    return korean_names.tolist()


def disease_compare_herb(disease_code):
    """
    Reverse-screen herbs related to a given disease based on shared compounds.
    Saves the results to an Excel file.
    """
    related_proteins = disease_to_protein(disease_code)
    related_compounds = protein_to_chemical(related_proteins)
    related_herbs = chemical_to_latin(related_compounds)

    result = pd.DataFrame(columns=['Herb (Korean)', 'Shared Compounds', 'Shared Count', 'Total Compounds', 'Overlap Ratio (%)'])

    for herb in related_herbs:
        try:
            herb_compounds = compound_df[compound_df["LATIN"] == herb]["ID"].unique().tolist()
            common_compounds = [cid for cid in herb_compounds if cid in related_compounds]
            korean_name = herb_df[herb_df["LATIN"] == herb]["KOREAN"].values[0]
            ratio = len(common_compounds) / len(herb_compounds) * 100

            result = result.append({
                'Herb (Korean)': korean_name,
                'Shared Compounds': common_compounds,
                'Shared Count': len(common_compounds),
                'Total Compounds': len(herb_compounds),
                'Overlap Ratio (%)': ratio
            }, ignore_index=True)
        except ZeroDivisionError:
            print(f"⚠️ Division by zero for herb: {herb}")

    result.to_excel(f'./Result/{disease_code}_reverse_screening.xlsx', index=False)


# =======================
# 🔁 Compound name to ID
# =======================

def comp_name_to_COMP_ID(comp_name):
    """
    Convert a compound name to its compound ID(s).
    """
    compound_ids = compound_df[compound_df["COMPOUND"].isin([comp_name])]["ID"].unique()
    return compound_ids
