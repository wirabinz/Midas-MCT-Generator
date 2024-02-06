import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Read columns 'A' to 'H' of the 'CONLOAD' sheet into a DataFrame
sheet_name = 'CONLOAD'
columns_range = 'A:H'
df = pd.read_excel(file_path, sheet_name, usecols=columns_range)

# Drop rows with NaN values
df = df.dropna()

# print(df)

# Print the header for Load Group
print("*LOAD-GROUP    ; Load Group")
print("; NAME")

# Get unique values from column 'GROUP'
unique_groups = df['GROUP'].unique()

# Print each unique group
for group in unique_groups:
    print(f"{group}")
print("\n")

# Print the desired text format
print("*USE-STLD, FT")
print("\n*CONLOAD    ; Nodal Loads")
print("; NODE_LIST, FX, FY, FZ, MX, MY, MZ, GROUP")

# Iterate through each row in the DataFrame
for _, row in df.iterrows():
    print(f"{int(row['NODE_LIST'])}, {row['FX']}, {row['FY']}, {row['FZ']}, {row['MX']}, {row['MY']}, {row['MZ']}, {row['GROUP']}")

print("\n Reminder, please set unit configuration to kN-m before executing MCT command")