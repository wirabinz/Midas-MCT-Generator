import pandas as pd

# ==============================================================================
# This script generates nodals table input from excel file
# ==============================================================================

def node_gen(data):
    # Define a custom formatting function
    def custom_format(row):
        return ' '.join(f'{int(row[0])},{row[1]:.1f},{row[2]:.1f},{row[3]:.1f}'.    split())

    # Apply the custom formatting function to each row
    formatted_output = data.apply(custom_format, axis=1)

    # Print the formatted output
    for line in formatted_output:
        print(line)

# ==============================================================================
# This script will generates frame element where each has 2 nodes and assign STRUCTURE GROUP to the element 
# ==============================================================================

def str_group(data):
    # Grouping the DataFrame by 'STR-GROUP' and merging the columns
    grouped = data.groupby('STR-GROUP').agg(lambda x: list(set(x))).reset_index()

    # Loop through the grouped data and print the desired format
    for index, row in grouped.iterrows():
        nodes = list(set(row['NODE-1'] + row['NODE-2']))
        nodes.sort()  # Sort nodes
        nodes_str = ' '.join(map(str, nodes))
        elements = ' '.join(map(str, row['ELEMENT']))
        print(f"{row['STR-GROUP']}, {nodes_str}, {elements}, 0")

# ==============================================================================
# This script will generates section PSC using coordinates input (OPOLY/IPOLY)
# By default, location of center of a section is 'CENTER TOP'
# ==============================================================================
        
def psc_valuegen(data):

    # Grouping by 'SECTION NUMBER' and 'SECTION NAME'
    grouped = data.groupby(['SECTION NUMBER', 'SECTION NAME'])

    for name, group in grouped:
        sect = name[0]
        psc = name[1]

        opoly_values = group[['OPOLY X', 'OPOLY Y']].values.flatten()
        opoly = ','.join(str(val) for val in opoly_values)

        ipoly_values = group[['IPOLY X', 'IPOLY Y']].values.flatten()
        ipoly = ','.join(str(val) for val in ipoly_values)

        print(f"SECT= {sect}, PSC, {psc}, CB, 0, 0, 0, 0, 0, 0, YES, NO, VALU")
        print(f"       0, 0, 0, 0, 0, 0")
        print(f"       1, 1, 1, 1, 1, 1, 1, 1, 1, 1")
        print(f"       1, 1, 1, 1, 1, 1, 1, 1")
        print(f"       100, 100, 100, 100")
        print(f"       YES, 0, 0, YES, , YES, , YES, , 0, YES, , YES, , YES, ")
        print(f"       OPOLY={opoly}")
        print(f"       IPOLY={ipoly}\n")

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

def tdn_property(data):
    wobble=6.6e-006 #1/mm
    friction=0.2
    fy =1670 #MPa
    fu =1860 #MPa
    MatID=2
    drawin_begin=6 #mm
    drawin_end=6 #mm
    rm=8 #midas relaxation method ID - CEB FIB 1990
    rc=2.5 #% relaxation

    # Iterate through DataFrame rows
    for index, row in data.iterrows():
        strand = f"{row['STRAND']}s-{row['DIA']}"
        # You can format the other columns accordingly here to create the desired   output line
        output_line = f"{strand}, INTERNAL, {MatID}, {row['AREA']}, {row['DUCT']},  {rm}, {rc}, {friction}, {wobble}, {fu}, {fy}, POST, {drawin_begin},  {drawin_end}, YES, 0, , , , 0, NO, 0, 0, 5e-006"
        print(output_line)
        
    print("\nPlease carefully review the tendon properties parameter!")
    print("Freely adjust the variable in the function script whenever needed.")

# ==============================================================================
# This script will generate a profile of tendon with default method : 
# 3D layout input, spline , element as the referrence
# Tendon group names are required before generating the tendon profile 
# So make sure TENDON-GROUP are also provided in excel file
#==============================================================================#

def tendon_group():
    #====== TENDON GROUP GENERATION =====
    # Replace 'your_file.xlsx' with the path to your Excel file
    file_path = 'mctgenerator.xls'

    # Read the specific sheet into a DataFrame
    df = pd.read_excel(file_path, 'TENDON-GROUP')
    # print(df)
    
    # Text generation
    print("*TENDON-GROUP    ; Tendon Group")
    print("; NAME")
    
    # Iterating through each row in the DataFrame
    for index, row in df.iterrows():
        print(f" {row['GROUP']}")


def tdn_profile(data):
    tendon_group()
    
    # Grouping data by 'NAME'
    grouped = data.groupby('NAME')

    # Loop through each group and construct the formatted output
    print("*TDN-PROFILE   ; Tendon Profile")
    for name, group in grouped:
        print(f"NAME={name}, {group['TDN-PROP'].iloc[0]}, {group['ASSIGNEE'].iloc   [0]}, 0, 0, SPLINE, 3D")
        print("\tTESTLINE, USER, 0, 0, NO,")
        print("\tELEMENT, END-I, 18, I-J")
        print(f"\t0, YES, 0, 0")

        # Get unique coordinates for each group
        unique_coords = group[['X', 'Y', 'Z','FIX']].drop_duplicates()


        # Output unique coordinates
        for _, row in unique_coords.iterrows():
            print(f"\t{row['X']}, {row['Y']}, {row['Z']}, {row['FIX']}, 0, 0, 0")