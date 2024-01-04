# ==============================================================================
# This script will generates section PSC using coordinates input (OPOLY/IPOLY)
# By default, location of center of a section is 'CENTER TOP'
# ==============================================================================

# Sample input :
#  SECT=   57, PSC       , TEST                , CB, 0, 0, 0, 0, 0, 0, YES, NO, VALU
#        0, 0, 0, 0, 0, 0
#        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
#        1, 1, 1, 1, 1, 1, 1, 1
#        1, 1, 1, 1
#        YES, 0, 0, YES, , YES, , YES, , 0, YES, , YES, , YES, 
#        OPOLY=1553, 0, 2000, 2534, 3350, 2784, 3350, 3034, -3350, 3034, -3350, 2784
#              -2000, 2534, -1553, 0
#        IPOLY=-1039, 456, -1134, 500, -1492, 2534, -742, 2784, 742, 2784, 1492, 2534
#              1134, 500, 1039, 456

# import pandas as pd

# # Replace 'your_file.xlsx' with the path to your Excel file
# file_path = 'mctgenerator.xls'

# # Read the specific sheet into a DataFrame
# sheet_name='SectionInput'
# df = pd.read_excel(file_path, sheet_name)
# # print(df)

def psc_valuegen(data):

    # Grouping by 'SECTION NUMBER' and 'SECTION NAME'
    grouped = data.groupby(['SECTION NUMBER', 'SECTION NAME'])

    for name, group in grouped:
        sect = name[0]
        psc = name[1]

        opoly_values = group[['OPOLY X', 'OPOLY Y']].values.flatten()
        opoly = ','.join(str(val) for val in opoly_values)

        ipoly_values = group[['IPOLY X', 'IPOLY Y']].values.flatten()
        ipoly = ','.join(str(val) for val in ipoly_values)

        print(f"SECT= {sect}, PSC, {psc}, CB, 0, 0, 0, 0, 0, 0, YES, NO, VALU")
        print(f"       0, 0, 0, 0, 0, 0")
        print(f"       1, 1, 1, 1, 1, 1, 1, 1, 1, 1")
        print(f"       1, 1, 1, 1, 1, 1, 1, 1")
        print(f"       100, 100, 100, 100")
        print(f"       YES, 0, 0, YES, , YES, , YES, , 0, YES, , YES, , YES, ")
        print(f"       OPOLY={opoly}")
        print(f"       IPOLY={ipoly}\n")


# *SECT-PSCVALUE    ; PSC Value, General Section, Composite PC, Composite General
# ; SECT=iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE, bBU, bEQ                    ; 1st line
# ;      [STIFF1]                                                                  ; 2nd line
# ;      [STIFF2]                                                                  ; 3rd line
# ;      [STIFF3]                                                                  ; 4th line
# ;      T1, T2, BT, HT                                                            ; 5th line(PSC)
# ;      bSHEARCHK, [SCHK], [WT]                                                   ; 6th line(PSC)
# ;      SW, GN, CTC, Bc, Tc, Hh, EsEc, DsDc, Ps, Pc                               ; 7th line(COMPOSITE-PC)
# ;      OPOLY=X1, Y1, X2, Y2, ..., Xn, Yn                                         ; Outer Polygon(PLANE)
# ;      IPOLY=X1, Y1, X2, Y2, ..., Xn, Yn                                         ; Inner Polygon(PLANE)
# ;      ...
# ;      IPOLY=X1, Y1, X2, Y2, ..., Xn, Yn                                         ; Inner Polygon(PLANE)
# ;      VERTEX=X1, Y1, X2, Y2, ..., Xn, Yn                                        ; Vertex(General-LINE)
# ;      LINE=VI1, VJ1, dTHIK1, iALIGN1                                            ; Line(General-LINE)
# ;      ...
# ;      LINE=VIn, VJn, dTHIKn, iALIGNn                                            ; Line(General-LINE)
# ;      LOOP=COUNT1, LIX11, LIX12, ..., LIXn                                      ; Line(General-LINE)
# ;      ...
# ;      LOOP=COUNTn, LIXn1, LIXn2, ..., LIXnn   

# iSEC : section number 
# TYPE : PSC 
# SNAME ; Section name
# [OFFSET]
#  = OFFSET: Location of center of a section
#      LT : Left-Top
#      CT : Center-Top
#      RT : Right-Top
#      LC : Left-Center
#     CC : Center-Center
#      RC : Right-Center
#      LB : Left-Bottom
#      CB : Center-Bottom
#      RB : Right-Bottom
# bSD: whether or not to consider shear deformation (YES/NO)