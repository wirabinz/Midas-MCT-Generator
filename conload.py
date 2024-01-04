import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'conload.xls'

# Read the specific sheet into a DataFrame
data = pd.read_excel(file_path, sheet_name='right_cable')
#print(data.columns)

# Convert all column names to strings
data.columns = data.columns.astype(str)

# Get the columns containing the node numbers (3, 7, 11, 15, 19, 23, 27, 31)
node_columns = [col for col in data.columns if col.isdigit()]
#print(node_columns)

# Filter FX and FZ values for each case in every node column
for node_col in node_columns:
    fx_values = data[(data['Force Type'] == 'FX') & (data[node_col].notnull())][['Force Type', 'GROUP', node_col]]
    fz_values = data[(data['Force Type'] == 'FZ') & (data[node_col].notnull())][['Force Type', 'GROUP', node_col]]

    for idx in range(len(fx_values)):
        fx_group = fx_values.iloc[idx]['GROUP']
        fx_node_value = fx_values.iloc[idx][node_col]
        
        fz_group = fz_values.iloc[idx]['GROUP']
        fz_node_value = fz_values.iloc[idx][node_col]

        print(f"{node_col}, {fx_node_value}, 0, {fz_node_value}, 0, 0, 0, {fx_group}")



    # for idx, fx_row in fx_values.iterrows():
    #     fx_group = fx_row['GROUP']
    #     fx_node_value = fx_row[node_col]
    #     print(fx_node_value)
        
 
    # for idx, fz_row in fz_values.iterrows():
    #     fz_group = fz_row['GROUP']
    #     fz_node_value = fz_row[node_col]
    #     print(fz_node_value)



        # print(f"{node_col}, {fx_node_value},{fx_group}")
        # fz_row = fz_values[(fz_values['GROUP'] == fx_group) & (fz_values[node_col] == fx_node_value)]
        # fz_node_value = fz_row.iloc[0][node_col] if not fz_row.empty else 0
        
        # print(f"{node_col}, {fx_node_value}, 0, {fz_node_value}, 0, 0, 0, {fx_group}")

