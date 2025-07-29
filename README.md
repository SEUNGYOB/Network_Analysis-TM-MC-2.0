# Network_Analysis-TM-MC-2.0-
TM-MC 2.0 DB based Network Analysis

Using TM-Mc 2.0 DB (https://tm-mc.kr/)

1. Find disease CUI from Disgenet (https://disgenet.com/)

2. Exampkle Usage in Network Analysis(TM_MC).py
   
   # Herbal complex example
    complex = ["인삼", "괄루근", "백지"]
    Matchcount_complex("C0151908", complex)

    # Individual herb comparison
    for herb in complex:
        Matchcount_solo("C0151908", herb)

    # Compound example
    compound_disease("C0409959", "emodin")


3. 
