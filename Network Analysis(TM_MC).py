"""
herb_disease_overlap_analysis.py

This script analyzes gene-level overlaps between:
- Individual herbs and diseases
- Herbal complexes and diseases
- Individual compounds and diseases

It uses functions from the TM_MC_revised module to map:
1. Diseases to associated genes
2. Herbs to their filtered compounds (via ADME rules)
3. Compounds to target proteins (genes)

Results are printed to console and saved as Excel files in the ./Result/ directory.
"""

import pandas as pd
import TM_MC_revised


import os
import pandas as pd

def Matchcount_solo(_Disease_code_name_for_Analyzing, _herbname):
    """
    Analyze the number of overlapping genes between a single herb and a given disease.
    """
    dis_related_protein = list(set(TM_MC_revised.disease_to_protein(_Disease_code_name_for_Analyzing)))
    Latin_name = TM_MC_revised.korean_to_latin(_herbname)
    Compound_list = TM_MC_revised.adme_filtering_2(_herbname)
    Protein_list = TM_MC_revised.compound_to_protein(Compound_list)
    herb_related_protein = list(set(Protein_list))

    intersection_lists = list(set(dis_related_protein) & set(herb_related_protein))

    print('Number of overlapping genes:', len(intersection_lists))
    print('Number of herb-related genes:', len(herb_related_protein))
    print('Number of disease-related genes:', len(dis_related_protein))
    print('Overlap ratio (%):', len(intersection_lists) / len(herb_related_protein) * 100)

    dic = {
        'Common Gene': intersection_lists,
        'Disease Genes': dis_related_protein,
        'Herb Genes': herb_related_protein
    }
    herb_disease_common_gene_list = pd.DataFrame.from_dict(dic, orient='index').transpose()

    os.makedirs('./Result', exist_ok=True)
    file_name = f'./Result/{_Disease_code_name_for_Analyzing}_{_herbname}_common_gene_list.xlsx'
    herb_disease_common_gene_list.to_excel(file_name)


def Matchcount_complex(_Disease_code_name_for_Analyzing, _herb_name_list):
    """
    Analyze the number of overlapping genes between a complex (multiple herbs) and a given disease.
    """
    dis_related_protein = TM_MC_revised.disease_to_protein(_Disease_code_name_for_Analyzing)

    compl_herb_protein = []
    for herb in _herb_name_list:
        Latin_name = TM_MC_revised.korean_to_latin(herb)
        Compound_list = TM_MC_revised.latin_to_compound_id(Latin_name)
        Protein_list = TM_MC_revised.compound_to_protein(Compound_list)
        compl_herb_protein.extend(Protein_list)

    herb_related_protein = list(set(compl_herb_protein))
    intersection_lists = list(set(dis_related_protein) & set(herb_related_protein))

    print("Disease Genes:", dis_related_protein)
    print("Complex Genes:", herb_related_protein)
    print("Common Genes:", intersection_lists)
    print('Number of overlapping genes:', len(intersection_lists))
    print('Number of complex-related genes:', len(herb_related_protein))
    print('Number of disease-related genes:', len(dis_related_protein))
    print('Overlap ratio (%):', len(intersection_lists) / len(herb_related_protein) * 100)

    dic = {
        'Common Gene': intersection_lists,
        'Disease Genes': dis_related_protein,
        'Complex Genes': herb_related_protein
    }
    herb_disease_common_gene_list = pd.DataFrame.from_dict(dic, orient='index').transpose()

    os.makedirs('./Result', exist_ok=True)
    file_name = f'./Result/{_Disease_code_name_for_Analyzing}_{_herb_name_list}_common_gene_list.xlsx'
    herb_disease_common_gene_list.to_excel(file_name)


def compound_disease(_Disease_code_name_for_Analyzing, compound):
    """
    Analyze the number of overlapping genes between a single compound and a given disease.
    """
    dis_related_protein = TM_MC_revised.disease_to_protein(_Disease_code_name_for_Analyzing)
    comp_ID = TM_MC_revised.comp_name_to_COMP_ID(compound)
    comp_related_proteins = TM_MC_revised.compound_to_protein([comp_ID])
    intersection_lists = list(set(dis_related_protein) & set(comp_related_proteins))

    print('Number of overlapping genes:', len(intersection_lists))
    print('Number of compound-related genes:', len(comp_related_proteins))
    print('Number of disease-related genes:', len(dis_related_protein))
    print('Overlap ratio (%):', len(intersection_lists) / len(comp_related_proteins) * 100)

    dic = {
        'Common Gene': intersection_lists,
        'Disease Genes': dis_related_protein,
        'Compound Genes': comp_related_proteins
    }
    herb_disease_common_gene_list = pd.DataFrame.from_dict(dic, orient='index').transpose()

    os.makedirs('./Result', exist_ok=True)
    file_name = f'./Result/{_Disease_code_name_for_Analyzing}_{compound}_common_gene_list.xlsx'
    herb_disease_common_gene_list.to_excel(file_name)


# Example usage
if __name__ == "__main__":
    # Herbal complex example
    complex = ["인삼", "괄루근", "백지"]
    Matchcount_complex("C0151908", complex)

    # Individual herb comparison
    for herb in complex:
        Matchcount_solo("C0151908", herb)

    # Compound example
    compound_disease("C0409959", "emodin")
