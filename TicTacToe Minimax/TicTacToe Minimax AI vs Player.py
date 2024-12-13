import time
import math


def createTable():
    return [["" for _ in range(3)] for _ in range(3)]

def showTable(table):
    print("\nCurrent Table: ")
    for row in table:
        print(row)

def makeMove(table,row,column,player):
    if table[row][column] == "":
        if player:
            table[row][column] = "X"
        else:
            table[row][column] = "O"
            
def gameState(table):
    #Checking Rows
    for row in table:
        if row[0] != "" and row[0] == row[1] == row[2]:
            if row[0] == "X":
                return 5
            else:
                return -5
    #Checking Columns
    for col in range(3):
        if table[0][col] != "" and table[0][col] == table[1][col] == table[2][col]:
            if table[0][col] == "X":
                return 5
            else:
                return -5
    #Checking Diagonals
    if table[0][0] != "" and table[0][0] == table[1][1] == table[2][2]:
        if table[0][0] == "X":
            return 5
        else:
            return -5
        
    if table[2][0] != "" and table[2][0] == table[1][1] == table[0][2]:
        if table[2][0] == "X":
            return 5
        else:
            return -5
    #Checking if the table has no empty strings
    if all(cell for row in table for cell in row):
        #if so return 0 as a draw state
        return 0
    
    #If none of the prev conditions are met return 1 as an indication that the game is still on going
    return 1
        
def found_threat(table):
    #here we priorities the bot winning over blocking the player in situations where the player and the bot have only 1 move to win the game

    #looping through the table this checks if there is a game winning move for the bot
    for row in range(3):
        for col in range(3):
            if table[row][col] == "":
                table[row][col] = "O"
                if gameState(table) == -5:
                    table[row][col] = ""
                    return [row,col]
                table[row][col] = ""
                
   #looping through the table this checks if there is an immediate threat and the player is a move away from winning                  
    for row in range(3):
        for col in range(3):
            if table[row][col] == "":
                table[row][col] = "X"
                if gameState(table) == 5:
                    table[row][col] = ""
                    return [row,col] 
                table[row][col] = ""
                
                
    return None
    
def minimax(table,index,depth,isMax):
    #if the game is decided we return the current move 
    if gameState(table) != 1 or depth == 0:
        return [gameState(table),index[0],index[1]]
    
    #checking for threats
    threat = found_threat(table)
    if threat:
        return [gameState(table),threat[0],threat[1]]
    
    #if the itteration is currently maximising "Player's potential move" we implement the minimax algorithm and find the best evaluation that favors the player
    if isMax:
        maxEval = -math.inf
        choices = [(row,col) for row in range(3) for col in range(3) if table[row][col] == ""]
        cell = [-1,-1]
        for c in choices:
            table[c[0]][c[1]] = "X"
            temp = minimax(table,[c[0],c[1]],depth-1,isMax=False)
            table[c[0]][c[1]] = ""
            if maxEval < temp[0]:
                maxEval = temp[0]
                cell = [temp[1],temp[2]]
        return [maxEval,cell[0],cell[1]]
    
    
    #if the itteration is currently minimising "Bot's potential move" we implement the minimax algorithm and find the best evaluation that favors the bot
    else:
        minEval = math.inf
        choices = [(row,col) for row in range(3) for col in range(3) if table[row][col] == ""]
        cell = [-1,-1]
        for c in choices:
            table[c[0]][c[1]] = "O"
            temp = minimax(table,[c[0],c[1]],depth-1,isMax=True)
            table[c[0]][c[1]] = ""
            if minEval > temp[0]:
                minEval = temp[0]
                cell = [temp[1],temp[2]]
        return [minEval,cell[0],cell[1]]
           
def checkWinner(table):
    state = gameState(table)
    if state == 5:
        print("Player Wins!!")
    elif state == -5:
        print("Bot Wins!!")
    elif state == None:
        print("On Going")   
    elif state == 0:
        print("Draw")
        
        

table = createTable()

while gameState(table) == 1:
    try:
        move = list(map(int, input("Enter Next Move: ").split(" ")))
        if len(move) != 2 or table[move[0]][move[1]] != "" or 0 > move[0] > 2 or 0 > move[1] > 2:
            print("Please Enter A Valid Posiion")
            continue
    except:
        print("Please Enter A Valid Posiion")
        continue
        
    makeMove(table,move[0],move[1],player=True)
    showTable(table)
    checkWinner(table)
    
    time.sleep(1)
    
    optimalMove = minimax(table,[move[0],move[1]],6,False)
    makeMove(table,optimalMove[1],optimalMove[2],player=False)
    showTable(table)
    checkWinner(table)
    
        
        
    
    
    
    

