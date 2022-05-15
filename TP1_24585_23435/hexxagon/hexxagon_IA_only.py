#inclui funções de cópia
import copy
#inclui função para gerar valor aleatório
import random
#inclui função para contar tempo que demora a executar as jogadas
import time

# - Now we need a class to save the game state. This class will contain info like:
#     - the chosen board and its size (N)
#     - the square size (dynamic by the screen size over the amount of squares of the board)
#     - the number of moves played
#     - the type of the game (if it is Human x Human, Human x PC or PC x PC), and, if any of the types involving the PC is chosen, the AI algorithm it'll have
#     - the recursivity depth (if the minmax algorithm is chosen)
#     - The winner

class gamestate:
    N = 0
    tabuleiro = []
    tipo = 3
    player1 = 0
    player2 = 0
    nMovs = 1
    vencedor = 0

# - We will save movement data in a class aswell, saving the X and Y of the initial square, the X and Y of the final square, the player who moved and the type of movement (Jump or Multiply)

class movimento:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    jog = 0
    tipo = 0

# - These classes sre temporary data savers:
#     - The first one is used just to test if said move is possible
#     - The second one saves the best move the computer can play
#     - The minmaxmov its just used to save the movement in every node of the minmax tree

class totalmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    tipo = 0

class bestmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0

class minimaxmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    min = 0
    max = 0

# - This class solely saves the game before the computer move, so it can restore it after every try

class save:
    game = []

# This function tracks the results of the game

class resultados:
    vermelho = 0
    azul = 0
    empate = 0
    jogadas = []
    diff = []
    media = 0

# - This function reads the chosen board by the player

def tabul():
    board = "hex.txt"
    return board

# - After the player has chosen the board this function loads it into the gamestate class

def carrega_tabul(ficheiro):
    f = open(ficheiro)
    gamestate.N = int(f.readline())
    tabuleiro = []
    for i in range(gamestate.N):
        tabuleiro.append(list(map(int, f.readline().split())))
    f.close()
    gamestate.tabuleiro = tabuleiro

# - This function takes an input for the type of game the player wants to play

def players():
    print("Player 1:")
    print("1 - Random")
    print("2 - Greedy")
    print("3 - Minimax")
    gamestate.player1 = int(input())
    print("Player 2:")
    print("1 - Random")
    print("2 - Greedy")
    print("3 - Minimax")
    gamestate.player2 = int(input())
    return

# - These next 2 functions save the gamestate and restores it when called, respectively

def copia():
    save.game = copy.deepcopy(gamestate.tabuleiro)

def restaura():
    gamestate.tabuleiro = save.game

# - This function changes the player turn

def troca_jog(jog):
    if jog == 1:
        return 2
    else:
        return 1

# Comment

def Infetar():
    dx = -1
    dy = -1
    for dx in range(dx, 2):
        for dy in range(dy, 2):
            try:
                if movimento.yf + dy == -1 and movimento.xf + dx == -1:
                    if gamestate.tabuleiro[0][0] == troca_jog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy +
                                            1][movimento.xf + dx+1] = movimento.jog
                elif movimento.yf + dy == -1:
                    if gamestate.tabuleiro[0][movimento.xf + dx] == troca_jog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy +
                                            1][movimento.xf + dx] = movimento.jog
                elif movimento.xf + dx == -1:
                    if gamestate.tabuleiro[movimento.yf + dy][0] == troca_jog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy][movimento.xf +
                                                               dx+1] = movimento.jog
                elif gamestate.tabuleiro[movimento.yf + dy][movimento.xf + dx] == troca_jog(movimento.jog):
                    gamestate.tabuleiro[movimento.yf +
                                        dy][movimento.xf + dx] = movimento.jog
            except IndexError:
                pass
        dy = -1

# Comment

def executa_movimento():
    gamestate.tabuleiro[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        gamestate.tabuleiro[movimento.yi][movimento.xi] = 0
    Infetar()

# - Checks if the movement choice is either a jump or a multiplication

def adjacente(dist, classe):
    return(
        abs(classe.xi - classe.xf) == dist and abs(classe.yi - classe.yf) <= dist or
        abs(classe.yi - classe.yf) == dist and abs(classe.xi - classe.xf) <= dist)

# - Checks if the move is inside the board limits

def dentro(x, y):
    return 0 <= x <= gamestate.N - 1 and 0 <= y <= gamestate.N - 1

# - Using the last 2 functions, this one checks if the move is totally valid
#     - Note: the first 'if' removes the L like movement

def movimento_valido(classe):
    if abs(classe.yf - classe.yi) == 2 \
            and abs(classe.xf - classe.xi) == 1 \
            or abs(classe.xf - classe.xi) == 2 \
            and abs(classe.yf - classe.yi) == 1:
        return False
    if not dentro(classe.xi, classe.yi) or not dentro(classe.xf, classe.yf):
        return False
    if gamestate.tabuleiro[classe.yi][classe.xi] == movimento.jog \
            and gamestate.tabuleiro[classe.yf][classe.xf] == 0 \
            and adjacente(1, classe):
        classe.tipo = 0
        return True
    if gamestate.tabuleiro[classe.yi][classe.xi] == movimento.jog \
            and gamestate.tabuleiro[classe.yf][classe.xf] == 0 \
            and adjacente(2, classe):
        classe.tipo = 1
        return True

# - This function checks the amount of valid moves a player has and returns its value. This will come in handy as if one player has zero moves, it skips his turn.

def jogadas_validas_total(jog):
    nmovs = 0
    for y in range(gamestate.N):
        for x in range(gamestate.N):
            if gamestate.tabuleiro[y][x] == jog:
                for k in range(gamestate.N):
                    for l in range(gamestate.N):
                        movimento.jog = jog
                        totalmov.yi = y
                        totalmov.xi = x
                        totalmov.yf = k
                        totalmov.xf = l
                        if movimento_valido(totalmov):
                            nmovs += 1
    return nmovs

# - Function that counts the amount of pieces the called player has

def conta_pecas(jog):
    pecas = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == jog:
                pecas += 1
    return pecas

# - Function that returns the amount of empty squares

def quad_validos():
    nmovs = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == 0:
                nmovs += 1
    return nmovs

# -  Checks if the game has reached its end conditions, depending on which one it is, it sets the winner as one of the players or as a draw.

def fim_jogo():
    n = quad_validos()
    if conta_pecas(1) == 0 or conta_pecas(2) == 0:
        if conta_pecas(1) == 0:
            gamestate.vencedor = 1
            return -1
        else:
            gamestate.vencedor = -1
            return -1
    if n == 0:
        if conta_pecas(1) - conta_pecas(2) >= 0:
            gamestate.vencedor = -1
            return -1
        if conta_pecas(1) - conta_pecas(2) < 0:
            gamestate.vencedor = 1
            return -1
        else:
            gamestate.vencedor = 0
            return -1
    else:
        return 0

# - And after setting the winner (or draw), it prints it to the console.

def finaliza():
    if gamestate.vencedor != 0:
        if gamestate.vencedor == -1:
            resultados.vermelho += 1
        else:
            resultados.azul += 1
    else:
        resultados.empate += 1
    resultados.jogadas.append(gamestate.nMovs)

# - Manages the computer made movements:
#   For each piece it has, it tries every possivle move, by doing it, evaluating it, and restoring the game to before the move
#   for each evaluation, it saves the movement with the best evaluation score and then, after every move has been played
#   it does the said best move

def jogada_pc():
    bestav = -100
    for yi in range(gamestate.N):
        for xi in range(gamestate.N):
            if gamestate.tabuleiro[yi][xi] == movimento.jog:
                for k in range(0, gamestate.N):
                    for l in range(0, gamestate.N):
                        movimento.yi = yi
                        movimento.xi = xi
                        movimento.yf = l
                        movimento.xf = k
                        if movimento_valido(movimento):
                            copia()
                            executa_movimento()
                            if gamestate.nMovs % 2 != 1:
                                av = avalia(gamestate.player2)
                            else:
                                av = avalia(gamestate.player1)
                            restaura()
                            if av >= bestav:
                                bestav = av
                                bestmov.yi = movimento.yi
                                bestmov.xi = movimento.xi
                                bestmov.yf = movimento.yf
                                bestmov.xf = movimento.xf
    movimento.yi = bestmov.yi
    movimento.xi = bestmov.xi
    movimento.yf = bestmov.yf
    movimento.xf = bestmov.xf
    if movimento_valido(movimento):
        executa_movimento()

# - When the computer asks to evaluate a play, if firstly asks which algorithm will be used for the evaluation (depending on the difficulty/algorithm chosen).

def avalia(tipo):
    tipo = int(tipo)
    score = 0
    if tipo == 1:
        score = algo_random()
    elif tipo == 2:
        score = algo_greedy()
    elif tipo == 3:
        if gamestate.nMovs % 2 != 1:
            movimento.jog = 1
            minimaxmov.min = 1
            minimaxmov.max = 2
        else:
            movimento.jog = 2
            minimaxmov.min = 2
            minimaxmov.max = 1
        minimaxmov.yi = movimento.yi
        minimaxmov.xi = movimento.xi
        minimaxmov.yf = movimento.yf
        minimaxmov.xf = movimento.xf
        alfa = -100000
        beta = 100000
        score = algo_minimax(0, True, alfa, beta)
        movimento.yi = minimaxmov.yi
        movimento.xi = minimaxmov.xi
        movimento.yf = minimaxmov.yf
        movimento.xf = minimaxmov.xf
    elif tipo > 3:
        score = random.random()
    return score

# Random Algorithm: Evaluates a move with a random value from 1 to 10.

def algo_random():
    return random.randint(1, 10)

# Greedy Algorithm: Evaluates a move based on the difference of pieces

def algo_greedy():
    salt = random.random()
    return conta_pecas(movimento.jog) - conta_pecas(troca_jog(movimento.jog))+salt

# Minmax Algorithm: Paired with the greedy heuristic,
# it plays every possible sequence of moves in a depth-first tree search,
# up to a certain depth, and then evaluates the ending states, then after every state is done
# (or, if a state doesn't meet the alpha-beta pruning requirements, in which is skipped),
# it plays the one with the most favorable outcome for the computer

def algo_minimax(depth, minimizer, alfa, beta):
    if depth == 3 or fim_jogo == -1:
        return algo_greedy() * (-1)

    if minimizer:
        movimento.jog = minimaxmov.min
        value = +1000
        for yi in range(gamestate.N):
            for xi in range(gamestate.N):
                if gamestate.tabuleiro[yi][xi] == movimento.jog:
                    for k in range(0, gamestate.N):
                        for l in range(0, gamestate.N):
                            movimento.yi = yi
                            movimento.xi = xi
                            movimento.yf = l
                            movimento.xf = k
                            if movimento_valido(movimento):
                                temp = copy.deepcopy(gamestate.tabuleiro)
                                executa_movimento()
                                evaluation = algo_minimax(
                                    depth + 1, False, alfa, beta)
                                gamestate.tabuleiro = temp
                                value = min(value, evaluation)
                                beta = min(beta, evaluation)
                                if beta <= alfa:
                                    break
        movimento.jog = minimaxmov.max
        return value
    else:
        movimento.jog = minimaxmov.max
        value = -1000
        for yi in range(gamestate.N):
            for xi in range(gamestate.N):
                if gamestate.tabuleiro[yi][xi] == movimento.jog:
                    for k in range(0, gamestate.N):
                        for l in range(0, gamestate.N):
                            movimento.yi = yi
                            movimento.xi = xi
                            movimento.yf = l
                            movimento.xf = k
                            if movimento_valido(movimento):
                                temp = copy.deepcopy(gamestate.tabuleiro)
                                executa_movimento()
                                evaluation = algo_minimax(
                                    depth + 1, True, alfa, beta)
                                gamestate.tabuleiro = temp
                                value = max(value, evaluation)
                                alfa = max(alfa, evaluation)
                                if beta <= alfa:
                                    break
        movimento.jog = minimaxmov.min
        return value


tabuleiro = tabul()
carrega_tabul(tabuleiro)
players()

total = int(input("Número de iterações: "))

# - Main function, executes:
#    - The type and board selection functions,
#    - Generates the window and the board,
#    - Begins the loop that sets the game playing.

# - While the game plays (inside the `while running:` ), it checks for 2 different events:

#     - If the player has no turns, it skips his turn;

#     - If the X is pressed, the game exits;

#     - If a click is made, it begins the piece-moving chain of events;

#     - Checks if a player has no moves, and if he does, skips his turn;


# - On the `MOUSEBUTTONDOWN` event, we firstly get the pixel coordinates of the click and then we convert them to the coordinates of the squares we clicked.

#     - As the variable `nMovs` is updated after each move, when the variable is odd, it means it is the first player moving, or else it is the second player's turn. Might aswell note that, if a player has no legal moves, we add another unit to `nMovs` and change the player who gets to play in order to skip a turn.

#     - Now depending on the game type chosen earlier, it will accept either 2 click or 4 clicks, 4 clicks if it is a Human vs Human game, or 2 click if it is a Human vs PC game. The clicks are taken in pairs because, for each turn, we need 1 click to select the piece and another one to select the final position, thats the use of the cl variable, when the first click is made, it is set to 1, when the second click is made, it resets to 0.

#     - After both clicks are made and the move is executed, we change the player's turn and update the board matrix with the new piece layout.

#     - And to finish off the player's turn, we update the screen with the new board.
# - While the game is still running, after each loop, we execute the functions that verify if the game is over and, if it has, we finish it.

def main():
    movimento.jog = 1
    carrega_tabul(tabuleiro)
    running = True

    while running:

        if jogadas_validas_total(movimento.jog) == 0:
            gamestate.nMovs += 1
            movimento.jog = troca_jog(movimento.jog)

        if gamestate.nMovs % 2 != 1:
            jogada_pc()
            gamestate.nMovs += 1
            movimento.jog = troca_jog(movimento.jog)
        else:
            jogada_pc()
            gamestate.nMovs += 1
            movimento.jog = troca_jog(movimento.jog)

        fim = fim_jogo()
        if fim == -1:
            resultados.diff.append(conta_pecas(1) - conta_pecas(2))
            finaliza()
            running = False


# Função para retornar tempo de execução
start_time = time.time()
# Repete o jogo em função do numero de iterações que o user quer (variável 'total')
for i in range(total):
    main()

print("\n")
print("Vitórias do Player 1: ", resultados.vermelho)
print("Vitórias do Player 2: ", resultados.azul)
print("Empates: ", resultados.empate)
print("Tempo de execução: %s" % (time.time() - start_time))
print("Win Rate Player 1: " + str(resultados.vermelho * 100.0 / total) + "%")
print("Win Rate Player 2: " + str(resultados.azul * 100.0 / total) + "%")
