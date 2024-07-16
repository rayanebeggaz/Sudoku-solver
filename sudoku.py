# un module permettant la gestion des matrice de dimension 9 x 9 #
import random
import copy
import os

def emptySudoku():
    m = [['.' for _ in range(9)] for _ in range(9)]
    return m

def add(m, row, col, val):
    try:
        val = int(val)
    except ValueError:
        val = '.'

    if isinstance(val, int):
        if 1 <= val <= 9:
            m[row][col] = val
        else:
            while True:
                val = input("ERREUR. Veuillez entrer une valeur entre 1 et 9, ou une autre touche pour indiquer une case vide: ")
                if val.isdigit():
                    val = int(val)
                    if 1 <= val <= 9:
                        m[row][col] = val
                        print("Valeur ajoutée")
                        break
                else:
                    m[row][col] = '.'
                    print("Case vide ajoutée")
                    break
    else:
        m[row][col] = '.'


def printSudoku(m) :
    for row in range(9) :
        if((row ==3) | (row == 6) ):
            print('-' *7*3,)
        for column in range(9) :
            if ((column == 2) | (column == 5) ):
                print(m[row][column], end=' | ') 
            else:
                print(m[row][column], end=' ')
        print()
    print()



def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def fillSudoku():
    m= emptySudoku()
    for row in range(0,9):
        for col in range(0,9):
            m[row][col]='?'
            printSudoku(m)
            print("-Veuillez entrer une valeur entre 1 et 9," 
                    "ou une autre touche pour indiquer une case vide.")
            print("pour corriger une erreur entrez -r R C oldV newV")
            elem = input(f"Entrez la valeur pour la case [{row}][{col}]: ")   
            #cas d'erreur de saisie
            if(len(elem) > 1 and elem[0]=='-'and elem[1]=='r'):
                message=""
                while(len(elem)!=10):
                    elem =input("erreur la repense doit etre de la forme suivante :-r R C V1 V2")  
                r=elem[3]
                c=elem[5]
                oldV=elem[7]
                v=elem[9]
                try:
                    r = int(r)
                    c = int(c)
                    oldV = int(oldV)
                    v= int(v)
                except ValueError:
                    val = '.'   
                if(oldV!= m[r][c]):
                    rep=' '
                    while (rep !="y") and (rep!= "n"):
                        rep=input(f"vous vouliez dire {m[r][c]} ? taper n pour annuler.... y/n ") 
                    v = oldV if rep == "n" else v
                    message=f"[{r}][{c}] modifié avec succes"
                add(m,r,c,v) 
                clear_terminal()    
                printSudoku(m)
                print(message)
                elem = input(f"Entrez la valeur pour la case [{row}][{col}]: ")      
            add(m,row,col,elem)
            clear_terminal()
    return m
def count_non_empty_elements(sudoku_grid):
    count = 0
    for row in sudoku_grid:
        for element in row:
            if element != '.':
                count += 1
    return count

# renvoie les valeurs possible a une cases donné  
def posibilityValues(m ,row ,col):
    values = {1,2,3,4,5,6,7,8,9}
    for i in range(9):
        element = m[row][i]
        if element in values:
            values.remove(element)
        element = m[i][col]
        if element in values:
            values.remove(element)
    x = 3 * (row // 3)
    y = 3 * (col // 3)
    for r in range(x,x+3):
        for c in range(y,y+3):
            element = m[r][c]
            if element in values:
                values.remove(element)  
    return values   
 
#prend m en parametre renvoi un tableau des solutions possibles du sudoku 
def sodokuPosibily(m,mult):
    t = copy.deepcopy(m)
    solutions = []
    def solve(t):
        if not mult:
            if len(solutions) >= 1:
                    return
        for r in range(9):
            for c in range(9):
                if t[r][c] == '.':
                    possibility = posibilityValues(t, r, c)
                    for p in possibility:
                        t[r][c] = p
                        solve(copy.deepcopy(t))
                    return
        # Si nous arrivons ici, cela signifie que nous avons trouvé une solution complète
        solutions.append(copy.deepcopy(t))
    solve(t)
    return solutions 

 



# prend t comme paramétre la matrice des posibilités
#  actualise le sudoku en remplacent les . par les solution unique  
def eval_uniq(t):
    solved = True
    tDistinct=t
    for r in range(9):
        for c in range(9):
            if (isinstance(tDistinct[r][c], set) )and (len(tDistinct[r][c]) != 1):
                tDistinct[r][c]='.'
                solved = False
            else :
                 if (isinstance(tDistinct[r][c], set)) and (len(tDistinct[r][c]) == 1):
                    tDistinct[r][c] = list(tDistinct[r][c])[0]
                    print("add ",r,c)
    return tDistinct,solved

def is_valid_sudoku(sudoku_grid):
    # Vérifie les lignes
    for row in sudoku_grid:
        if not is_valid_group(row):
            return False

    # Vérifie les colonnes
    for col in range(9):
        column = [sudoku_grid[row][col] for row in range(9)]
        if not is_valid_group(column):
            return False

    # Vérifie les sous-grilles 3x3
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            block = [sudoku_grid[row][col]
                     for row in range(start_row, start_row + 3)
                     for col in range(start_col, start_col + 3)]
            if not is_valid_group(block):
                return False

    return True

def is_valid_group(group):
    elements = [element for element in group if element != '.']
    return len(elements) == len(set(elements))


#print(is_valid_sudoku(sudoku_grid))  # Devrait retourner True si le Sudoku est valide


def main (sudoku):
    clear_terminal()
    m = sudoku
    print("sodoku:")
    printSudoku(m)
    print(is_valid_sudoku(m))  
    if(count_non_empty_elements(m)<17):
        print("le sudoku n'admet pas de solution , un sudoku doit avoir au minimum 17 valeur ")
        return
    mult=''
    while(mult !='y' and mult !='n'):
        mult = input("vouliez vous chercher toute les solutions existante  .. y/n")
    if(mult=='y'):
        mult=True
    else:
        mult =False
    res = sodokuPosibily(m,True)
    i = 1
    if len(res) == 0:
        print("le sudoku n'admets aucune solution")
    else:
        for s in res:
            print("solotion :",i)
            printSudoku(s) 
            i+=1


main(fillSudoku())