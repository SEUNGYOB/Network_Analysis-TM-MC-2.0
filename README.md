# Network_Analysis-TM-MC-2.0
TM-MC 2.0 DB based Network Analysis

Using TM-Mc 2.0 DB (https://tm-mc.kr/), Data files(TM_MC_DB) were downloaded 

1. Find disease CUI from Disgenet (https://disgenet.com/)

2. Example usage in Network Analysis(TM_MC).py
   
   # Herbal complex example
    complex = ["인삼", "괄루근", "백지"]
    Matchcount_complex("C0151908", complex)

    # Individual herb comparison
    for herb in complex:
        Matchcount_solo("C0151908", herb)

    # Compound example
    compound_disease("C0409959", "emodin")

**Requirements**

numpy	2.3.1	2.3.2

openpyxl	3.1.5	3.1.5

pandas	2.3.1	2.3.1

pip	25.1.1	25.1.1

python-dateutil	2.9.0.post0	2.9.0.post0

pytz	2025.2	2025.2

six	1.17.0	1.17.0

tzdata	2025.2	2025.2
