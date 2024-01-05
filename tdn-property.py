# ==============================================================================
# This script imports all of tendons properties with default strand parameter :
# wobble 6.6e-006
# friction 0.2
# fy/fu 1670/1860 MPa
# Material link 2 (please make ASTM A416-270 Low relaxation as MAT no id 2)!
# Draw in wedges 4 mm 
# relaxation method CEB-FIP 1990 (Midas reference number RM :8)
# post tension
#==============================================================================# 

wobble=6.6e-006 #1/mm
friction=0.2
fy =1670 #MPa
fu =1860 #MPa
MatID=2
drawin_begin=6 #mm
drawin_end=6 #mm
rm=8 #midas relaxation method ID - CEB FIB 1990
rc=2.5 #% relaxation

import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Read the specific sheet into a DataFrame
sheet_name='TDN-PROPERTY'
df = pd.read_excel(file_path, sheet_name)
# print(df)

# Iterate through DataFrame rows
for index, row in df.iterrows():
    strand = f"{row['STRAND']}s-{row['DIA']}"
    # You can format the other columns accordingly here to create the desired output line
    output_line = f"{strand}, INTERNAL, {MatID}, {row['AREA']}, {row['DUCT']}, {rm}, {rc}, {friction}, {wobble}, {fu}, {fy}, POST, {drawin_begin}, {drawin_end}, YES, 0, , , , 0, NO, 0, 0, 5e-006"
    print(output_line)