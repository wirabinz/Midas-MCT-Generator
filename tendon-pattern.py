import numpy as np

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

def generate_line_coordinates(ecc_y, ecc_z, l_par_y, b_x, length, offset_y=0, offset_z=0):
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
    point_d_z = ecc_z + offset_z
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
    print(point_a)
    print(point_b)
    print(point_c)
    print(point_d)
    print(point_e)
    print(point_f)
    print(point_g)

    return point_a, point_b, point_c, point_d, point_e, point_f, point_g

# Example usage:
ecc_y = 0.5
ecc_z = 0.2
l_par_y = 5
b_x = 2
length = 20
offset_y = 1
offset_z = 0.5

generate_line_coordinates(ecc_y, ecc_z, l_par_y, b_x, length, offset_y, offset_z)
