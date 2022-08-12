#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 00:00:00 2022

@author: Alec Lowi
"""


import pandas as pd

def apply_scheme(filenam,  # filename
                 num_stu,  # number of students
                 num_HWs,  # number of homeworks
                 HW_tots,  # list of homework totals
                 mid_tot,  # midterm total
                 fin_tot,  # final total
                 scheme1={'HW': 35, 'Midterm': 30, 'Final': 35},
                 scheme2={'HW': 35, 'Midterm':  0, 'Final': 65}
                 ):

    assert num_HWs == len(HW_tots)

    names = ["Status", "Name", "UID", "Section", *
             map(lambda n: f"HW{n+1}", range(num_HWs)), "Midterm", "Final"]
    tot_cols = len(names)
    cols_type = {name:float for name in names[4:]}

    gr = pd.read_excel(io = filenam,
                       header = None,
                       skiprows = 7, 
                       usecols = list(range(tot_cols)), 
                       index_col = 2, 
                       names = names,
                       nrows = num_stu,
                       na_values=["", " ", "  "], 
                       dtype=cols_type)

    gr = gr.fillna(0.0)

    gr = gr[gr["Status"] == "Enrolled"]
    gr = gr.drop(columns=["Section", "Status"])
    
    scaled_HWs = pd.DataFrame({'HW' + str(i+1) : gr['HW' + str(i+1)] / HW_tots[i] for i in range(num_HWs)})

    gr.insert(num_HWs + 1, 'HWA', 100 * scaled_HWs.sum(axis = 1) / num_HWs)
    sm_loc = gr.columns.get_loc(f"Midterm") + 1
    gr.insert(sm_loc, "SM", gr["Midterm"] / mid_tot * 100)

    gr["SF"] = gr["Final"] / fin_tot * 100
    
    gr['Scheme 1'] = (gr["HWA"] * scheme1["HW"] + gr["SM"] * scheme1["Midterm"] + gr["SF"] * scheme1["Final"]) / 100
    gr['Scheme 2'] = (gr["HWA"] * scheme2["HW"] + gr["SM"] * scheme2["Midterm"] + gr["SF"] * scheme2["Final"]) / 100
    gr["Best"] = gr[["Scheme 1", "Scheme 2"]].max(axis=1)

    gr = gr.sort_values("Best", ascending=False)
    return gr
gr = apply_scheme(filenam = 'made_up.xlsx',
                      num_stu = 18,
                      num_HWs = 4,
                      HW_tots = [10, 10, 12, 14],
                      mid_tot = 40,
                      fin_tot = 50)



# It is probably best to work in Jupyter Notebook
# where typing gr and pressing "shift, enter"
# displays the dataframe in a pretty format.
