import pandas as pd

# # Example DataFrame
# data = {
#     'NODE-1': [1, 2, 3, 4],
#     'NODE-2': [2, 3, 4, 5],
#     'ELEMENT': [1, 2, 3, 4],
#     'STR-GROUP': ['END-SPAN A1', 'END-SPAN A1', 'END-SPAN A1', 'A1-CLOSURE']
# }

# df = pd.DataFrame(data)

# # Grouping the DataFrame by 'STR-GROUP' and merging the columns
# grouped = df.groupby('STR-GROUP').agg(lambda x: list(set(x))).reset_index()

# # Loop through the grouped data and print the desired format
# for index, row in grouped.iterrows():
#     nodes = list(set(row['NODE-1'] + row['NODE-2']))
#     nodes.sort()  # Sort nodes
#     nodes_str = ' '.join(map(str, nodes))
#     elements = ' '.join(map(str, row['ELEMENT']))
#     print(f"{row['STR-GROUP']}, {nodes_str}, {elements}, 0")


# # Replace 'your_file.xlsx' with the path to your Excel file
# file_path = 'mctgenerator.xls'

# # Read the specific sheet into a DataFrame
# data = pd.read_excel(file_path, sheet_name='GROUP')
# df = data
# #print(data)

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
