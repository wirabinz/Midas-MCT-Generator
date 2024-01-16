# ==============================================================================
# This script generates nodals table input from excel file
# ==============================================================================

import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Read the specific sheet into a DataFrame
data = pd.read_excel(file_path, sheet_name='NODE')
df = data
print(data)

# Define a custom formatting function
def custom_format(row):
    return ' '.join(f'{int(row[0])},{row[1]:.1f},{row[2]:.1f},{row[3]:.1f}'.split())

# Apply the custom formatting function to each row
formatted_output = df.apply(custom_format, axis=1)

# Print the formatted output
# for line in formatted_output:
#     print(line)
