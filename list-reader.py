# ==============================================================================
# This script will read LIST command result from autocad
#===============================================================================

import pandas as pd
import re

# Replace 'your_excel_file.xlsx' with the actual path to your Excel file
excel_file_path = 'mctgenerator.xls'
sheet_name = 'LIST-READER'  # Replace with the actual sheet name

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# Print column names to identify the correct column
# print(df.columns)

# Define a function to extract X, Y, and Z values from a string
def extract_xyz(row):
    match = re.search(r"X= *(-?\d+\.\d+) *Y= *(-?\d+\.\d+) *Z= *(-?\d+\.\d+)", row)
    if match:
        x_value = float(match.group(1))
        y_value = float(match.group(2))
        z_value = float(match.group(3))
        return x_value, y_value, z_value
    return None

# Apply the function to the column containing the data
xyz_data = df['AUTOCAD DATA'].apply(extract_xyz)

# Drop rows where extraction failed (returned None)
xyz_data = xyz_data.dropna()

# Create separate columns for 'NODE', 'X', 'Y', and 'Z'
df[['X', 'Y', 'Z']] = pd.DataFrame(xyz_data.tolist(), index=xyz_data.index)

# Create a new column 'NODE' starting from 1
df['NODE'] = range(1, len(df) + 1)

# Reorder columns to have 'NODE' before 'X', 'Y', and 'Z'
df = df[['NODE', 'X', 'Y', 'Z']]

# Print the results
# Display the results with specified precision
pd.set_option('display.float_format', lambda x: '%.4f' % x)  # Setprecision to 4 decimal places
print(df)


