# Sudoku
This python script can solve any Sudoku 9x9 size, you just need load up the excel file example "Sudoku.xls" when prompted, this file has a Sudoku to be solved.

Main idea of this algorithm is to solve any sudoku 9x9 size. The sudoku cells and sectors are split as following:
	
	  [0]		  [1]		  [2]	
	11 12 13	14 15 16  	17 18 19
	21 22 23	24 25 26	27 28 29
	31 32 33	34 35 36	37 38 39

	  [3]		  [4]		  [5]
	41 42 43  	44 45 46	47 48 49
	51 52 53  	54 55 56	57 58 59
	61 62 63  	64 65 66	67 68 69
	
	  [6]		  [7]		  [8] 
	71 72 73	74 75 76	77 78 79
	81 82 83	84 85 86  	87 88 89
	91 92 93	94 95 96  	97 98 99
