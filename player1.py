import sys

#funcao de debug
def printBoard(board):
    for i in board:
        print(i)
    print('------------------')

'''
funcao para gerar estados do tipo chaos
dado um determinado estado e uma cor
'''
def chaosGenerateStates(board, color_memory, color=None):
    for i in range(7):
        for j in range(7):
            newBoard = list(map(list, board))
            newColor_memory = color_memory.copy()
            if color and newBoard[i][j] == 0:
                newColor_memory[color - 1] -= 1
                newBoard[i][j] = color
                yield {
                    "board": newBoard,
                    "color_memory": newColor_memory,
                    "type": "chaos",
                    "next_function": orderGeneratorStates(newBoard, newColor_memory),
                    "move": [i, j]
                }
            elif color == None:
                for k in range(7):
                    if color_memory[i] > 0:
                        newColor_memory[k] -= 1
                        newBoard[i][j] = k + 1
                        yield {
                            "board": newBoard,
                            "color_memory": newColor_memory,
                            "type": "chaos",
                            "next_function": orderGeneratorStates(newBoard, newColor_memory),
                            "move": [i, j]
                        }


''' 
funcao para gerar estados do tipo ordem
dado um determinado estado
'''
def orderGeneratorStates(board, color_memory):
    for i in range(7):
        for j in range(7):
            if board[i][j] != 0:
                for k in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                    aux = 1
                    
                    #geracao de estados em um sentido, por exemplo se k == 0,1, sao gerados todos os estados para a direita, a partir de um ponto determinado
                    while 0 <= i + k[0] * aux < 7 and 0 <= j + k[1] * aux < 7 and board[i + k[0] * aux][j + k[1] * aux] == 0:         
                        newBoard = list(map(list, board))  #copia do tabuleiro original

                        #troca as posicoes da jogada gerada
                        newBoard[i + k[0] * aux][j + k[1] * aux], newBoard[i][j] = newBoard[i][j], newBoard[i + k[0] * aux][j + k[1] * aux]
                        
                        #cria nova jogada e espera a proxima iteracao
                        yield {
                            "board": newBoard,
                            "color_memory": color_memory,
                            "type": "order",
                            "next_function": chaosGenerateStates(newBoard, color_memory),
                            "move": [i, j, i + k[0] * aux, j + k[1] * aux]                 #movimento gerado
                        }
                        aux += 1


'''
Classe responsavel por gerar a arvore de estados
'''
class EntropyTree:
    def __init__(self, board, color_memory, generator, depth, value, maxmin = None, root=None):
        self.board = board                   #tabuleiro atual
        self.color_memory = color_memory     
        self.generator = generator           #Funcao geradora no orderGeneratorStates ou do chaosGenerateStates, mantendo a referencia.
        self.depth = depth                   #Profundidade do no
        self.value = value                   #Valor de utilidade do estado
        self.root = root                     #Referencia para a raiz
        self.maxmin = maxmin                 #Funcao lambda de comparacao

    ''' metodo de inicializacao da arvore, além de inserir novos nos ate uma determinada profundidade'''
    def newNode(self):
        for state in self.generator:
            tree = EntropyTree(state["board"], state["color_memory"], state["next_function"], self.depth - 1, self.root)
            if self.depth > 0:
                tree.newNode()
            else:
                value = eval(state["board"])
                if self.maxmin(self.root.value, value):
                    self.root.setValue(value)
                    self.root.best_move = state["move"]

    def setValue(self, value):
        self.value = value


'''
funcao de avaliacao que retorna a utilidade de um estado
'''
def eval(vetor):
    # return 1
    def CountPS(str, n):
        dp = [[0 for x in range(n)]
              for y in range(n)]
        P = [[False for x in range(n)]
             for y in range(n)]
        for i in range(n):
            P[i][i] = True
        for i in range(n - 1):
            if (str[i] == str[i + 1]):
                P[i][i + 1] = True
                dp[i][i + 1] = 1
        for gap in range(2, n):
            for i in range(n - gap):
                j = gap + i
                if (str[i] == str[j] and P[i + 1][j - 1]):
                    P[i][j] = True
    
                if (P[i][j] == True):
                    dp[i][j] = (dp[i][j - 1] +
                                dp[i + 1][j] + 1 - dp[i + 1][j - 1])
                else:
                    dp[i][j] = (dp[i][j - 1] +
                                dp[i + 1][j] - dp[i + 1][j - 1])
        return dp[0][n - 1]
    string = ''
    count = 0

    cop = list(map(list, vetor))
    aux = -1
    for i in range(7):
        for j in range(7):
            if cop[i][j] == 0:
                cop[i][j] = aux
                aux -=1

    for i in range(7):
        for j in range(7):
            string += str(cop[i][j])

        count += CountPS(string, 7)
        string = ''
    
    for i in range(7):
        for j in range(7):
            string += str(cop[j][i])

        count += CountPS(string, 7)
        string = ''
    
    return count-7


'''
Funcao de adaptador, 
recebe uma string no formato Aa num range de A ~ G
retorna uma lista no formato [0, 0] num range de 0 ~ 6
'''
def adapt_str_int(string):
    adapter = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}
    adapter_caps = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}

    return [adapter_caps[string[0]], adapter[string[1]]]

'''
Funcao de adaptador, 
recebe uma lista no formato [0, 0] num range de 0 ~ 6
retorna uma string no formato Aa num range de A ~ G
'''
def adapt_int_str(lis):
    adapter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g'}
    adapter_caps = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G'}

    return adapter_caps[lis[0]] + adapter[lis[1]]


'''
Recebe o board e uma jogada do tipo order e atualiza o board com a jogada
'''
def changeboardOrder(move,board):
    board[move[2]][move[3]] = board[move[0]][move[1]]
    if move[0] != move[2] or move[3] != move[1]:
        board[move[0]][move[1]] = 0

'''
Recebe o board, a cor e uma jogada do tipo chaos e atualiza o board com a jogada
'''
def changeboardChaos(color, move, board):
    board[move[0]][move[1]] = color


def main():
    board = [[0 for _ in range(7)] for _ in range(7)]
    color_memory = [7 for i in range(7)]
    start = sys.stdin.readline().strip()

    #decisao de qual tipo de jogador a IA eh
    player = 'order'
    if start == 'Start':
        player = 'chaos'

    #loop principal
    while True:

        if player == 'chaos':
            color = sys.stdin.readline().strip()

            #parada
            if color == 'Quit':
                break

            color = int(color)
            
            #instanciacao da arvore
            et = EntropyTree(board, color_memory, chaosGenerateStates(board, color_memory, color), 0, float('+inf'), maxmin = lambda x, y: x > y)
            et.root = et
            et.newNode()
            
            #Atualizando tabuleiro
            board[et.best_move[0]][et.best_move[1]] = color
            
            #melhor jogada e printar
            bm = adapt_int_str(et.best_move)
            print(bm)
            sys.stdout.flush()
            
            #le jogada
            move = sys.stdin.readline().strip()
            move = adapt_str_int(move[0:2]) + adapt_str_int(move[2:])

            #atualiza board
            board[move[2]][move[3]] = board[move[0]][move[1]]
            if move[0] != move[2] or move[3] != move[1]:
                board[move[0]][move[1]] = 0

        else:
            color = int(start[0])
            move = start[1:]
            move = adapt_str_int(move)

            #Atualizando tabuleiro
            changeboardChaos(color, move, board)
            
            #instanciacao da arvore
            et = EntropyTree(board, color_memory, orderGeneratorStates(board, color_memory), 0, float('-inf'), lambda x, y: x < y)
            et.root = et
            et.newNode()
            
            #melhor jogada
            bm = adapt_int_str(et.best_move[:2]) + adapt_int_str(et.best_move[2:])
            
            #Atualizando tabuleiro
            changeboardOrder(et.best_move,board)
            
            #mostra melhor jogada
            print(bm)
            sys.stdout.flush()
            start = sys.stdin.readline().strip()

            #parada
            if start == 'Quit':
                break


if __name__ == '__main__':
    main()
