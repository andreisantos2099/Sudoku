
"""SudokuLib.py: This library solve any sudoku 9x9 size"""

__author__      = "Andrei Alves"
__copyright__   = "Copyright 2021, Dark Matter is the future!"

import xlrd # for excel file reading
from datetime import datetime, timedelta

# Main idea of this algorithm is to solve any sudoku 9x9 size. The sudoku cells and sectors are split as following:
#     [0]              [1]              [2]
#   11	12	13  	14	15	16  	17	18	19
#   21	22	23  	24	25	26  	27	28	29
#   31	32	33  	34	35	36  	37	38	39

#     [3]              [4]              [5]
#   41	42	43  	44	45	46  	47	48	49
#   51	52	53  	54	55	56  	57	58	59
#   61	62	63  	64	65	66  	67	68	69

#     [6]              [7]              [8]
#   71	72	73  	74	75	76  	77	78	79
#   81	82	83  	84	85	86  	87	88	89
#   91	92	93  	94	95	96  	97	98	99

class Sudoku:
    # it contains the  sudoku loaded from file
    dic_LoadedSudoku =dict()
    # it contains the sector map cell for each location (e.g. 0[11,12,13,21,22,23,31,32,33])
    dic_SectorMap =dict()
    # it contains the allowed list values for each cell example (e.g. 11:[1,2,7], 45:[1,3,4,6,8,9])
    dic_CellAllowedValues = dict()
    # it contains the allowed values lenght  (e.g. 11:[3], 45:[6])
    dic_CellAllowedValuesLenght = dict()
    # it contains a solution based on the allowed values combination (e.g. 11:[1], 45:[8])
    dic_SudokuCombinationValues = dict()
    #Final sudoku solution p_dictionary
    dic_FinalSudokuSolution = dict()

    i_init_time =  datetime.now()

    # Valid Cell values range
    tup_ValidValues = (1,2,3,4,5,6,7,8,9)
    # Sector Start Cell list
    tup_SectorStartCell = (11,14,17,41,44,47,71,74,77)

    i_AllCombinations = 1

    def __init__(self):
        #create sectors locations:
        self.func_CreateSector()

    def func_CreateSector(self):
        #create the Sudoku Sector Map
        lst_temp = list()
        i_sectorcnt = 0
        i_idx = 0

        #For each sector there is a start cell:
        #example 11,14,17 is start cell for the sectors below
        #   11	12	13		14	15	16		17	18	19
        #   21	22	23		24	25	26		27	28	29
        #   31	32	33		34	35	36		37	38	39
        for i_startcell in self.tup_SectorStartCell:

            i_row = i_startcell
            i_col = i_startcell
            i_sectorcnt = 0

            for i_rowidx in range(i_row, i_row + 40, 10):
                for i_colidx in range(i_col, i_col + 3):
                    lst_temp.append(str(i_rowidx)[0]+str(i_colidx)[1])
                i_col +=10

                if(i_sectorcnt >= 2):
                    break
                else:
                    i_sectorcnt +=1
            #Create the Sector dictionary
            self.dic_SectorMap[i_idx] = self.dic_SectorMap.get(i_idx, lst_temp[:])

            i_idx += 1
            lst_temp.clear()
            if i_idx == 10:
                break




    def func_StartSudoku(self):
        p_sudokufile = input("Please type the Sudoku excel file name(e.g. Sudoku.xls): ")
        i_value = 0
        key =''

            # Open the Spreadhsheet
        workbook = xlrd.open_workbook(p_sudokufile)


        # Open the worksheet
        worksheet = workbook.sheet_by_index(0)
        # Iterate the rows and columns from Excel file to fill up the loade sudoku dictionary
        for row in range(1, 10):
         for col in range(1, 10):
             try:
                 i_value = worksheet.cell_value(row, col)
                 key = str(row)+str(col)
                 self.dic_LoadedSudoku[key] = self.dic_LoadedSudoku.get(key,int(i_value))
             except:
                 #if value is blank or not defined then fill up the cell with zero
                 self.dic_LoadedSudoku[key] = self.dic_LoadedSudoku.get(key,0)

             #create some dictionaries
             self.dic_CellAllowedValues[key] = self.dic_CellAllowedValues.get(key,0)
             self.dic_CellAllowedValuesLenght[key] = self.dic_CellAllowedValuesLenght.get(key,0)
             self.dic_SudokuCombinationValues[key] = self.dic_SudokuCombinationValues.get(key,0)
             self.dic_FinalSudokuSolution  = self.dic_LoadedSudoku.copy()


        self.func_AllowedValuesList()






    def func_AllowedValuesList(self):


        lst_sectorIdx = list()
        lst_FobbidenValues = list()
        lst_AllowedValues = list()
        dic_temp = dict()
        i_idx_sector = 0

        dic_temp.clear()
        dic_temp = self.dic_LoadedSudoku.copy()
        self.i_AllCombinations  = 1

        #Read the entire sudoku
        for key, value in dic_temp.items():


            lst_FobbidenValues.clear()
            lst_AllowedValues.clear()
            str_idx_sector = 0

            if value == 0:

                #find related row to specific place in assessment.
                str_row = key[0]
                str_row = str_row +"1"
                for i in range(int(str_row), (int(str_row)+9)):
                    lst_FobbidenValues.append(dic_temp[str(i)])


                #find related col to specific place in assessment.
                str_col = key[1]
                str_col = "1"+str_col
                for i in range(int(str_col), (int(str_col)+89), 10):
                    lst_FobbidenValues.append(dic_temp[str(i)])

                #locate the sector where the cell is set.
                for ks,vs in self.dic_SectorMap.items():
                    if key in vs:
                        #get sector
                        str_idx_sector = ks
                        break
                lst_sectorIdx = self.dic_SectorMap[str_idx_sector]

                #load sector values
                for x in lst_sectorIdx:
                    lst_FobbidenValues.append(dic_temp[x])

                #order by crescent order
                lst_FobbidenValues = list(set(lst_FobbidenValues))

                #Set the allowed values list
                for i in self.tup_ValidValues:
                    if i not in lst_FobbidenValues:
                        lst_AllowedValues.append(i)

                self.dic_CellAllowedValues[key] = lst_AllowedValues[:]
                self.dic_CellAllowedValuesLenght[key] = len(lst_AllowedValues)

                # Calculate all combinations possible
                self.i_AllCombinations *= len(lst_AllowedValues)
            else:
                self.dic_CellAllowedValues[key] = 0
                self.dic_CellAllowedValuesLenght[key] = 0

        print("\n\n")
        print("Solve the following Sudoku: \n")
        self.func_printSudoku(self.dic_LoadedSudoku)


        print("Total combinations calculated: ", f"{self.i_AllCombinations:,}")


        self.func_SudokuSolution()



    def func_SudokuSolution(self):
        str_FirstK = '' #it holds the first key
        str_LastK  = '' #it holds the last key
        str_PrevK  = '' #it holds the previous key


        b_ReloadFlag = False
        b_ReloadFlag_First = False

        b_CheckFinalSoduFlag = False
        lst_row_values = list()
        dic_TempLenght = dict()
        dic_TempCombination = dict()




        # finding the first and last keys
        for k,v in self.dic_CellAllowedValues.items():

            if((v != 0) and (str_FirstK == '')):
                str_FirstK = k
            if(v != 0):
                str_LastK = k


        #Initializing the sequence:
        str_PrevK = str_FirstK

        dic_TempLenght = self.dic_CellAllowedValuesLenght.copy()
        dic_TempCombination = self.dic_SudokuCombinationValues.copy()

        # For a solution, experiment with all possible combinations
        # from Allowed values
        i_counter  = self.i_AllCombinations

        while (i_counter > 0):
            dic_TempCombination.clear()
            dic_TempCombination = self.dic_SudokuCombinationValues.copy()
            str_PrevK = str_FirstK
            lst_row_values.clear()


            b_ValueRepatedFlag = False
            b_CheckFinalSoduFlag = False

            for k,v in self.dic_CellAllowedValues.items():

                if v != 0:
                    #Check to see if it is the first allowed sequence of values.
                    if k == str_FirstK:
                        if(b_ReloadFlag_First == True):
                            b_ReloadFlag = True
                            b_ReloadFlag_First = False

                        #Update Temp Combination dictionary
                        dic_TempCombination[k] = v[dic_TempLenght[k] - 1]

                        #Reload again if value reached the mininum value (zero)
                        if (dic_TempLenght[k] - 1) <= 0:
                            dic_TempLenght[k] = self.dic_CellAllowedValuesLenght[k]
                            b_ReloadFlag_First = True
                            #print(dic_TempLenght[k])
                        else:
                            #decrement the value for next cycle.
                            dic_TempLenght[k]  -= 1



                    else:
                        #if reload is requested then reload the previous one
                        if b_ReloadFlag == True:
                            b_ReloadFlag = False

                            #decrement the value for next cycle.
                            dic_TempLenght[k]  -= 1

                            #Reload again if value reached minimum limit(lenght == 0)
                            if dic_TempLenght[k] <= 0:
                                dic_TempLenght[k] = self.dic_CellAllowedValuesLenght[k]
                                b_ReloadFlag = True

                            #Update Temp Combination dictionary
                            dic_TempCombination[k] = v[dic_TempLenght[k] - 1]

                        else:

                            if (dic_TempLenght[k] - 1) >= 0:
                                dic_TempCombination[k] = v[dic_TempLenght[k] - 1]


                        #Check if row has any repeated value
                        if(k[0] == str_PrevK[0]):
                            lst_row_values.append(dic_TempCombination[k])
                            if len(lst_row_values) != len(set(lst_row_values)):
                                lst_row_values.clear()
                                b_ValueRepatedFlag = True
                        else:
                            lst_row_values.clear()

                    #Save valid previous k and value is different from zero in Cell Allowed Values dictionary
                    str_PrevK = k


                # if combination ended up in the last K then move forward to final check
                if (k == str_LastK) and (b_ValueRepatedFlag == False):
                    b_CheckFinalSoduFlag = True
                    break


            if(b_CheckFinalSoduFlag == True):

                #Check func_SudokuSolution
                self.dic_FinalSudokuSolution.clear()
                self.dic_FinalSudokuSolution  = self.dic_LoadedSudoku.copy()
                for k,v in  self.dic_LoadedSudoku.items():
                    self.dic_FinalSudokuSolution[k] = self.dic_FinalSudokuSolution[k] + dic_TempCombination[k]

                #check if sudoku is solved:
                if(self.func_CheckSudoku(self.dic_FinalSudokuSolution) == True):
                    print("\n\n")
                    print("Sudoku puzzle solved in the combination #: ", f"{i_counter:,}")
                    print("\n")
                    self.func_printSudoku(self.dic_FinalSudokuSolution)
                    print("Time elapsed:", (datetime.now() - self.i_init_time))
                    break

            i_counter -= 1
            if((i_counter % 50000) == 0):
                print("Combination : ", f"{i_counter:,}", end='\r')



    def func_CheckSudoku(self, p_dictionary):
        #check if sudoku is solved:
        i_row_total = 0
        i_col_total = 0
        b_flag = True
        dic_temp = dict()
        dic_temp = p_dictionary.copy()

        #Read the entire sudoku
        for key, value in p_dictionary.items():

            i_row_total = 0
            i_col_total = 0
            str_key = str(key)

            if (str_key[0] == str_key[1]):

                #find related row to sum all values
                str_row = key[0]
                str_row = str_row +"1"
                for i in range(int(str_row), (int(str_row)+9)):
                    i_row_total += dic_temp[str(i)]

                #check if the sum is 45 for row and col
                if((i_row_total != 45 )):
                    b_flag = False
                    break


                #find related col to sum all values.
                str_col = key[1]
                str_col = "1"+str_col
                for i in range(int(str_col), (int(str_col)+89), 10):
                    i_col_total += dic_temp[str(i)]

                #check if the sum is 45 for row and col
                if((i_col_total != 45 )):
                    b_flag = False
                    break

        return b_flag



    def func_printSudoku(self,p_dictionary):
        i_counter = 0
        lst_print = list()

        for kk, vv in p_dictionary.items():

            # print(kk,vv)
            lst_print.append(vv)
            if i_counter == 8:
                i_counter = 0
                print(lst_print,'\t')
                lst_print.clear()
            else:
                i_counter += 1
        print("\n\n")




nova = Sudoku()
nova.func_StartSudoku()
