# ==============================================================================
# This script generates element table input from excel file 
# ==============================================================================

import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Read the specific sheet into a DataFrame
data = pd.read_excel(file_path, sheet_name='ELEMENT')


df = pd.DataFrame(data)

# Create a new DataFrame with the desired format
new_columns = ['ELEMENT', 'BEAM', 'MATERIAL', 'SECTION NUMBER', 'NODE-1', 'NODE-2', 'Extra_Text']
new_df = pd.DataFrame(columns=new_columns)

# Iterate through the original DataFrame and append rows to the new DataFrame
for index, row in df.iterrows():
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