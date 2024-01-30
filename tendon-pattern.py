import numpy as np
import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Read the specific sheet into a DataFrame
sheet_name='TDN-GEN'
df = pd.read_excel(file_path, sheet_name)
# print(df)


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
    point_a = f"{point_a[0] }, {point_a[1] + offset_y}, {point_a[2] + offset_z}"
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
        print(f"    {X+offset_x}, {Y}, {Z}, {'YES' if coord_label == 'D' else 'NO'}, 0, 0, 0")

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Read the specific sheet into a DataFrame
sheet_name='TDN-GEN'
df = pd.read_excel(file_path, sheet_name)

# Iterate through each row in the DataFrame
print("*TDN-PROFILE   ; Tendon Profile")
for index, row in df.iterrows():
    generate_and_print_coordinates(row)



