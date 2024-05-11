board = [[0 for _ in range(7)] for _ in range(7)]
color_memory = [7 for i in range(7)]



def chaosGenerateStates(board, color_memory, color = None):
    for i in range(7):
        for j in range(7):
            if color and not board[i][j]:
                newBoard = list(map(list, board))
                newBoard[i][j] = color + 1 
                newColor_memory = color_memory.copy()
                newColor_memory[color] -= 1
                yield {"board": newBoard, "color_memory": newColor_memory}
            else:
                for k in range(7):
                    if color_memory[i] > 0:
                        newBoard = list(map(list, board))
                        newColor_memory = color_memory.copy()
                        newColor_memory[k] -= 1
                        newBoard[i][j] = k + 1 
                        yield {"board": newBoard, "color_memory": newColor_memory}


chs = chaosGenerateStates(board, color_memory)
for i in chs:
    print(i["board"])
    print(i["color_memory"])
    print('-----------------------------')
