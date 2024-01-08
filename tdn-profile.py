# ==============================================================================
# This script will generate a profile of tendon with default method : 
# 3D layout input, spline 
#==============================================================================#

import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Read the specific sheet into a DataFrame
sheet_name='TDN-PROFILE'
df = pd.read_excel(file_path, sheet_name)
# print(df)

g

# Iterate through unique NAME and TDN-GROUP combinations
for name_group, group_df in df.groupby(['NAME', 'TDN-GROUP']):
    print(f"NAME={name_group[0]}, 5S-12.7MM, 18to22, 0, SPLINE, 3D")
    print("\tTESTLINE, USER, 0, 0, NO,")
    print("\tELEMENT, END-I, 18, I-J")
    print("\t0, YES, 0, 0")

    # Print rows in the desired format
    for index, row in group_df.iterrows():
        print(f"\t{row['Y']}, {row['Z']}, {row['FIX']}, NO, 0, 0, 0")
    print()  # Add an empty line after each group

