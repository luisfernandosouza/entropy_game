board = [[0 for _ in range(7)] for _ in range(7)]
color_memory = [7 for i in range(7)]

def orderGeneratorStates(board, color_memory):
    for i in range(7):
        for j in range(7):
            if board[i][j] != 0:
                for k in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                    aux = 1
                    while 0 <= i + k[0]*aux < 7 and 0 <= j + k[1]*aux < 7 and board[i + k[0]*aux][j + k[1]*aux] == 0:
                        newBoard = list(map(list, board))
                        newBoard[i + k[0]*aux][j + k[1]*aux], newBoard[i][j] = newBoard[i][j], newBoard[i + k[0]*aux][j + k[1]*aux]
                        aux += 1

                        yield {"board": newBoard, "color_memory": color_memory}
                        

def printBoard(board):
    for i in board:
        print(i)

board[2][3] = 2
board[2][5] = 4
ogs = orderGeneratorStates(board, color_memory)
for i in ogs:
    printBoard(i["board"])
    print('-----------------------------')