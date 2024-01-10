# ==============================================================================
# This script will generate a profile of tendon with default method : 
# 3D layout input, spline , element as the referrence
# Tendon group names are required before generating the tendon profile 
# So make sure TENDON-GROUP are also provided in excel file
#==============================================================================#

import pandas as pd

# Your DataFrame
data = pd.DataFrame({
    'NAME': ['A DUMMY 3', 'A DUMMY 3', 'A DUMMY 3', 'A DUMMY 3', 'A DUMMY 3', 'A DUMMY 4', 'A DUMMY 4', 'A DUMMY 4', 'A DUMMY 4', 'A DUMMY 4'],
    'TDN-GROUP': ['TESTLINE', 'TESTLINE', 'TESTLINE', 'TESTLINE', 'TESTLINE', 'TESTLINE', 'TESTLINE', 'TESTLINE', 'TESTLINE', 'TESTLINE'],
    'TDN-PROP': ['5S-12.7MM', '5S-12.7MM', '5S-12.7MM', '5S-12.7MM', '5S-12.7MM', '5S-12.7MM', '5S-12.7MM', '5S-12.7MM', '5S-12.7MM', '5S-12.7MM'],
    'ASSIGNEE': ['18to22', '18to22', '18to22', '18to22', '18to22', '18to22', '18to22', '18to22', '18to22', '18to22'],
    'INSERTION': [18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
    'X': [0, 5250, 10500, 15750, 21000, 0, 5250, 10500, 15750, 21000],
    'Y': [-500, -500, -500, -500, -500, 500, 500, 500, 500, 500],
    'Z': [1000, 1000, 500, 1000, 1000, 1000, 1000, 500, 1000, 1000],
    'FIX': ['NO', 'NO', 'YES', 'NO', 'NO', 'NO', 'NO', 'YES', 'NO', 'NO']
})


# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

def tendon_group():
    #====== TENDON GROUP GENERATION =====
    # Read the specific sheet into a DataFrame
    
    df = pd.read_excel(file_path, 'TENDON-GROUP')
    # print(df)
    
    # Text generation
    print("*TENDON-GROUP    ; Tendon Group")
    print("; NAME")
    
    # Iterating through each row in the DataFrame
    for index, row in df.iterrows():
        print(f" {row['GROUP']}")


#====== TENDON PROFILE GENERATION =======
# Read the specific sheet into a DataFrame
sheet_name='TDN-PROFILE'
df = pd.read_excel(file_path, sheet_name)
# print(df.columns)

# Grouping data by 'NAME'
grouped = df.groupby('NAME')

# Loop through each group and construct the formatted output
print("*TDN-PROFILE   ; Tendon Profile")
for name, group in grouped:
    print(f"NAME={name}, {group['TDN-PROP'].iloc[0]}, {group['ASSIGNEE'].iloc[0]}, 0, 0, SPLINE, 3D")
    print("\tTESTLINE, USER, 0, 0, NO,")
    print("\tELEMENT, END-I, 18, I-J")
    print(f"\t0, YES, 0, 0")

    # Get unique coordinates for each group
    unique_coords = group[['X', 'Y', 'Z','FIX']].drop_duplicates()
    

    # Output unique coordinates
    for _, row in unique_coords.iterrows():
        print(f"\t{row['X']}, {row['Y']}, {row['Z']}, {row['FIX']}, 0, 0, 0")
