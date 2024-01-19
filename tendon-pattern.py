import numpy as np

def generate_parabolic_line(center_x, eccentricity_y, eccentricity_z, length, offset_y=0, num_points=5):
    # Define the parameter t
    t_values = np.linspace(-length/2, length/2, num_points)

    # Calculate X, Y, Z coordinates for the parabolic line
    x_values = center_x + t_values
    y_values = (1 - (t_values / (length / 2))**2) * eccentricity_y + offset_y
    z_values = (1 - (t_values / (length / 2))**2) * eccentricity_z

    return list(zip(x_values, y_values, z_values))

def generate_and_print_multiple_lines(center_x, eccentricity_y, eccentricity_z, length, offset_y=0, ecc_orient=0,  num_lines=1, addl_length=0, add_ecc_y=0, add_ecc_z=0, num_points=5):
    for _ in range(num_lines):
        # Generate a line using the generate_parabolic_line function
        line_points = generate_parabolic_line(center_x, eccentricity_y, eccentricity_z, length, offset_y, num_points)

        # Print the coordinates of the generated points
        for point in line_points:
            print(f"{point[0]:.2f} {ecc_orient*point[1]:.2f} {point[2]:.2f}")

        # Update parameters for the next line
        length += addl_length
        eccentricity_y += add_ecc_y
        # eccentricity_y*=ecc_orient
        eccentricity_z += add_ecc_z

# Input parameters
center_x = 55760
eccentricity_y = 1
eccentricity_z = 0.5
length = 10
num_lines = 2
addl_length = 2
add_ecc_y = 0.2
add_ecc_z = 0.1
offset_y = 0
ecc_orient = -1

# Generate and print multiple lines with offset_y
generate_and_print_multiple_lines(center_x, eccentricity_y, eccentricity_z, length, offset_y, num_lines, addl_length, add_ecc_y, add_ecc_z)
