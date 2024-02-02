import pandas as pd
import numpy as np


# ==============================================================================
# This script generates nodals table input from excel file
# ==============================================================================

def node_gen(data):
    # Define a custom formatting function
    def custom_format(row):
        return ' '.join(f'{int(row[0])},{row[1]:.5f},{row[2]:.5f},{row[3]:.5f}'.    split())

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

        opoly_values = group[['OPOLY X', 'OPOLY Y']].dropna().values.flatten()
        opoly = ','.join(str(val) for val in opoly_values)

        ipoly_values = group[['IPOLY X', 'IPOLY Y']].dropna().values.flatten()
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
        print(f" {row['TDN GROUP']}")

def parabolic_segment(ecc_y, ecc_z, l_par_y, b_x, offset_y=0, offset_z=0):
    """
    Calculates the coefficients of a second-order polynomial and the coordinates of points A, B, and C.

    Parameters:
    - ecc_y: Eccentricity of the parabolic curve along the y-axis.
    - ecc_z: Eccentricity of the parabolic curve along the z-axis.
    - l_par_y: Length of the half parabolic curve from A to C (symmetric to E to G).
    - b_x: X-coordinate of point B.
    - offset_y: Offset to be applied to y-coordinates (default is 0).
    - offset_z: Offset to be applied to z-coordinates (default is 0).

    Returns:
    - Coefficients of the second-order polynomial (a, b, c).
    - Coordinates of points A, B, and C.
    """
    # Coordinates of points A, C, and E
    point_a = (0, 0, 0)
    point_c = (l_par_y, ecc_y, ecc_z)
    point_e = (2 * l_par_y, 0, ecc_z)

    # Set up a system of equations to solve for a, b, and c
    A = np.array([
        [point_a[0]**2, point_a[0], 1],
        [point_c[0]**2, point_c[0], 1],
        [point_e[0]**2, point_e[0], 1]
    ])

    B = np.array([point_a[1], point_c[1], point_e[1]])

    # Solve the system of equations
    coefficients = np.linalg.solve(A, B)

    # Function to calculate y-coordinate given x-coordinate
    def calculate_y(x):
        return coefficients[0] * x**2 + coefficients[1] * x + coefficients[2]

    # Calculate y-coordinate of point B when b_x is given
    b_y = calculate_y(b_x) + offset_y

    # Coordinates of points A, B, and C
    point_a = f"{point_a[0]}, {point_a[1] + offset_y}, {point_a[2] + offset_z}"
    point_b = f"{b_x}, {b_y}, {ecc_z + offset_z}"
    point_c = f"{point_c[0]}, {point_c[1] + offset_y}, {point_c[2] + offset_z}"

    return coefficients, point_a, point_b, point_c

def generate_line_coordinates(ecc_y, ecc_z, l_par_y,mid_par_z,b_x, length, offset_y=0, offset_z=0, ):
    """
    Generates coordinates for points A, B, C, D, E, F, and G based on the given parameters.

    Parameters:
    - ecc_y: Eccentricity of the parabolic curve along the y-axis.
    - ecc_z: Eccentricity of the parabolic curve along the z-axis.
    - l_par_y: Length of the half parabolic curve from A to C (symmetric to E to G).
    - b_x: X-coordinate of point B.
    - length: Total length of the line.
    - offset_y: Offset to be applied to y-coordinates (default is 0).
    - offset_z: Offset to be applied to z-coordinates (default is 0).

    Returns:
    - Coordinates of points A, B, C, D, E, F, and G.
    """
    # Calculate the parabolic segment
    coefficients, point_a, point_b, point_c = parabolic_segment(ecc_y, ecc_z, l_par_y, b_x, offset_y, offset_z)

    # Function to calculate y-coordinate given x-coordinate
    def calculate_y(x):
        return coefficients[0] * x**2 + coefficients[1] * x + coefficients[2]

    # Calculate point D as the midpoint of the line
    point_d_x = 0.5 * length 
    point_d_y = ecc_y + offset_y
    point_d_z = ecc_z + offset_z + mid_par_z
    point_d = f"{point_d_x}, {point_d_y}, {point_d_z}"

    # Mirror points A, B, C with respect to point D
    point_e_x = 2 * point_d_x - float(point_c.split(',')[0])
    point_e_y = float(point_c.split(',')[1])
    point_e_z = ecc_z + offset_z
    point_e = f"{point_e_x}, {point_e_y}, {point_e_z}"

    point_f_x = 2 * point_d_x - float(point_b.split(',')[0])
    point_f_y = float(point_b.split(',')[1])
    point_f_z = ecc_z + offset_z
    point_f = f"{point_f_x}, {point_f_y}, {point_f_z}"

    point_g_x = 2 * point_d_x - float(point_a.split(',')[0])
    point_g_y = float(point_a.split(',')[1]) 
    point_g_z = float(point_a.split(',')[2]) 
    point_g = f"{point_g_x}, {point_g_y}, {point_g_z}"

    # Print the results
    # print(point_a)
    # print(point_b)
    # print(point_c)
    # print(point_d)
    # print(point_e)
    # print(point_f)
    # print(point_g)

    return point_a, point_b, point_c, point_d, point_e, point_f, point_g

# # Example usage:
# ecc_y = 764
# ecc_z = -300
# l_par_y = 4000
# b_x = 2500
# length = 12520
# offset_y = 3556
# offset_z = -460

# generate_line_coordinates(ecc_y, ecc_z, l_par_y, b_x, length, offset_y, offset_z)



def generate_and_print_coordinates(row):
    ecc_y = row['ECC Y']
    ecc_z = row['ECC Z']
    l_par_y = row['l_par_y']
    b_x = row['b_x']
    mid_par_z = row['mid_par_z']
    length = row['LENGTH']
    offset_y = row['OFFSET Y']
    offset_z = row['OFFSET Z']
    offset_x = row['OFFSET X']

    # Call generate_line_coordinates function
    coordinates = generate_line_coordinates(ecc_y, ecc_z, l_par_y, mid_par_z, b_x, length, offset_y, offset_z)

    # Print the results in the desired format
    print(f"NAME={row['NAME']}, {row['TDN-PROP']}, {row['FROM']}to{row['TO']}, 0, 0, SPLINE, 3D")
    print(f"    {row['TDN GROUP']}, USER, 0, 0, NO,")
    print(f"    ELEMENT, END-I, {row['FROM']}, I-J")
    print("    0, YES, 0, 0")

    # Access coordinates directly
    point_a, point_b, point_c, point_d, point_e, point_f, point_g = coordinates

    # Extract X, Y, and Z components for each point
    points = [point_a, point_b, point_c, point_d, point_e, point_f, point_g]
    coordinates_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for coord_label, point in zip(coordinates_labels, points):
        X, Y, Z = map(float, point.split(', '))
        print(f"    {X+1200}, {Y}, {Z}, {'YES' if coord_label == 'D' else 'NO'}, 0, 0, 0")


def tendon_layout_gen(data):
    # Iterate through each row in the DataFrame
    print("*TDN-PROFILE   ; Tendon Profile")
    for index, row in data.iterrows():
        generate_and_print_coordinates(row)

def tdn_profile(data):
    tendon_group()
    
    tendon_layout_gen(data)

# ==============================================================================
# This script will read LIST command result from autocad
#===============================================================================
            
def list_reader(data):
    import re
    # Print column names to identify the correct column
    # print(data.columns)

    # Define a function to extract X, Y, and Z values from a string
    def extract_xyz(row):
        if 'Press ENTER to continue:' not in row:
            match = re.search(r"X= *(-?\d+\.\d+) *Y= *(-?\d+\.\d+) *Z= *(-?\d+\.\d+)", row)
            if match:
                x_value = float(match.group(1))
                y_value = float(match.group(2))
                z_value = float(match.group(3))
                return x_value, y_value, z_value
        return None

    # Apply the function to the column containing the data
    xyz_data = data['AUTOCAD DATA'].apply(extract_xyz)

    # Drop rows where extraction failed (returned None)
    xyz_data = xyz_data.dropna()

    # Create separate columns for X, Y, and Z
    data[['X', 'Y', 'Z']] = pd.DataFrame(xyz_data.tolist(), index=xyz_data.index)

    # Drop rows where any of X, Y, Z is NaN using .loc
    data = data.loc[~data[['X', 'Y', 'Z']].isna().any(axis=1)]

    # Create a new column 'NODE' starting from 1
    data['NODE'] = range(1, len(data) + 1)

    # Create a new variable holding the subset of the DataFrame
    xyz_subset = data[['NODE', 'X', 'Y', 'Z']]

    # Print the results
    # print(xyz_subset)

    node_gen(xyz_subset)


# ==============================================================================
# This script will generates necessary database for concrete bridge material
#===============================================================================
    
def material(data):
    # Iterate through each row in the DataFrame
        for index, row in data.iterrows():
            # Iterate through each cell in the row
            for cell_value in row:
                print(str(cell_value), end=' ')  # Print the text content of the cell
            print()  # Move to the next line after printing the entire row


# ==============================================================================
# This script generates element table input from excel file 
# ==============================================================================

def element_gen(data):
    # Create a new DataFrame with the desired format
    new_columns = ['ELEMENT', 'BEAM', 'MATERIAL', 'SECTION NUMBER', 'NODE-1',   'NODE-2', 'Extra_Text']
    new_df = pd.DataFrame(columns=new_columns)

    # Iterate through the original DataFrame and append rows to the new DataFrame
    for index, row in data.iterrows():
        new_row = {
            'ELEMENT': row['ELEMENT'],
            'BEAM': 'BEAM',
            'MATERIAL': row['MATERIAL'],
            'SECTION NUMBER': row['SECTION NUMBER'],
            'NODE-1': row['NODE-1'],
            'NODE-2': row['NODE-2'],
            'Extra_Text': '0, 0'  # Add the desired text as a string
        }
        new_df = new_df.append(new_row, ignore_index=True)

    # Print the resulting DataFrame in CSV-like format
    csv_like_string = new_df.to_csv(index=False).replace('"', '')
    print(csv_like_string)