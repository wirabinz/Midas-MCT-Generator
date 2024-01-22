import numpy as np

def generate_parabolic_line(center_x, eccentricity_y, eccentricity_z, length, offset_y=0, offset_z=0, num_points=5):
    # Define the parameter t
    t_values = np.linspace(-length/2, length/2, num_points)

    # Calculate X, Y, Z coordinates for the parabolic line
    x_values = center_x + t_values + length/2
    y_values = (1 - (t_values / (length / 2))**2) * eccentricity_y + offset_y
    z_values = (1 - (t_values / (length / 2))**2) * eccentricity_z + offset_z

    return list(zip(x_values, y_values, z_values))

def generate_and_print_multiple_lines(center_x, eccentricity_y, eccentricity_z, length, offset_y=0, ecc_orient=0,  num_lines=1, addl_length=0, add_ecc_y=0, add_ecc_z=0, num_points=5):
    for _ in range(num_lines):
        # Generate a line using the generate_parabolic_line function
        line_points = generate_parabolic_line(center_x, eccentricity_y, eccentricity_z, length, offset_y,offset_z, num_points)

        # Print the constant eccentricity orientation
        # print(ecc_orient)
        
        # Print the coordinates of the generated points
        for point in line_points:
            print(f"{point[0]:.2f} {ecc_orient*point[1]:.2f} {point[2]:.2f}")

        # Update parameters for the next line
        length += addl_length
        eccentricity_y += add_ecc_y
        eccentricity_z += add_ecc_z
        ecc_orient*=toggler

# Input parameters

eccentricity_y = 542
eccentricity_z = 121
length = 12444
center_x = 0
num_lines = 14
addl_length = 5000
add_ecc_y = 297
add_ecc_z = 0
offset_y = 3780
offset_z= -360
ecc_orient = 1
toggler=-1


# Generate and print multiple lines with offset_y
generate_and_print_multiple_lines(center_x, eccentricity_y, eccentricity_z, length, offset_y, ecc_orient, num_lines, addl_length, add_ecc_y, add_ecc_z)



# ==============================================================================
# Parabolic - straight - parabolic
# ==============================================================================

# import numpy as np
# import matplotlib.pyplot as plt

# def generate_parabolic_coordinates(start, end, num_points):
#     t = np.linspace(0, 1, num_points)
#     x = start[0] + t * (end[0] - start[0])
#     y = start[1] + (t ** 2) * (end[1] - start[1])
#     z = start[2] + t * (end[2] - start[2])
#     return np.column_stack((x, y, z))

# def generate_straight_coordinates(start, end, num_points):
#     t = np.linspace(0, 1, num_points)
#     x = start[0] + t * (end[0] - start[0])
#     y = start[1] + t * (end[1] - start[1])
#     z = start[2] + t * (end[2] - start[2])
#     return np.column_stack((x, y, z))

# # Anchor points
# anchor1 = np.array([0, 0, 0])
# anchor2 = np.array([5, 5, 5])
# anchor3 = np.array([10, 0, 0])

# # First parabolic segment
# parabolic1 = generate_parabolic_coordinates(anchor1, anchor2, 50)

# # Second parabolic segment
# parabolic2 = generate_parabolic_coordinates(anchor2, anchor3, 50)

# # Combine segments
# tendon_coordinates = np.vstack((parabolic1, parabolic2))

# # Plot the tendon coordinates
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(tendon_coordinates[:, 0], tendon_coordinates[:, 1], tendon_coordinates[:, 2])
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()

