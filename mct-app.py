#====== LIBRARY MIDAS MCT GENERATOR =====#

import pandas as pd
import function_compilation as fc

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'mctgenerator.xls'

# Dictionary mapping options to script names, function names, and sheet names
options = {
    '1': {'option_name':'Structure Group Generator', 'function': 'str_group', 'sheet_name': 'GROUP'},
    '2': {'option_name':'Section PSC generator','function': 'psc_valuegen', 'sheet_name': 'SectionInput'},
    # Add more options here as needed
}

def main():
    # Replace with the actual file path
    file_path = 'mctgenerator.xls'
    print("Welcome to MCT App!")
    print("Select an option:")

    for key, value in options.items():
        print(f"{key}. {value['option_name']}")

    choice = input("Enter your choice:\n")


    if choice in options:
        selected_option = options[choice]
        sheet_name = selected_option['sheet_name']
        function_name = selected_option['function']
        
        # Read the specific sheet into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Execute the selected function from the function_compilation module
        getattr(fc, function_name)(df)
    else:
        print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

#====================================#
#     STRUCTURE GROUP GENERATOR      #
#====================================#

# # Create nodes numbers and element numbers and group them into structure group
# # import elemdata
# sheet_name='GROUP'

# # Read the specific sheet into a DataFrame
# df = pd.read_excel(file_path, sheet_name)

# # Execute structure group generator script 
# fc.str_group(df)

#====================================#
#        SECTION PSC GENERATOR       #
#====================================#

# # import section_psc
# # sheet_name='SectionInput'

# # Read the specific sheet into a DataFrame
# df = pd.read_excel(file_path, sheet_name)

# # Execute structure group generator script 
# fc.psc_valuegen(df)