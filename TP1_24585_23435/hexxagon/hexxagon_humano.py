# Libraries Used:
# numpy - from numpy, we just imported the 'unsignedinterger' to create a integer without value
# pygame - library designed to develop video games
# time - used to create time intervals in the code
# copy - set of functions that allow the copying of elements like lists
# random - generation of pseudo-random numbers

import pygame
import time
import copy
import random

# - We begin the pygame library, set the maximum FPS to 15 frames per second, and set the window size to 600 pixels

pygame.init()
SIZE = 600

# - Now we need a class to save the game state. This class will contain info like: 
#     - the chosen board and its size (N)
#     - the square size (dynamic by the screen size over the amount of squares of the board)
#     - the number of moves played
#     - the type of the game (if it is Human x Human, Human x PC or PC x PC), and, if any of the types involving the PC is chosen, the AI algorithm it'll have
#     - the recursivity depth (if the minmax algorithm is chosen)
#     - The winner

class gamestate:
    N = 0
    sq = 0
    tabuleiro = []
    tipo = 0
    ai1diff = 0
    ai2diff = 0
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


class minmaxmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    min = 0
    max = 0

# - This class solely saves the game before the computer move, so it can restore it after every try

class save:
    game = []

# - This function reads the chosen board by the player

def tabul():
    tabuleiro = "hex.txt"
    return tabuleiro

# - After the player has chosen the board this function loads it into the gamestate class

def carrega_tabul(ficheiro):
    f = open(ficheiro)
    gamestate.N = int(f.readline())
    gamestate.sq = SIZE / gamestate.N
    tabuleiro = []
    for i in range(gamestate.N):
        tabuleiro.append(list(map(int, f.readline().split())))
    f.close()
    gamestate.tabuleiro = tabuleiro

# - This function takes an input for the type of game the player wants to play

def tipo_jogo():
    print("Modo de jogo:")
    print("1 - Humano vs. Humano ")
    print("2 - Humano vs. Computador ")
    tipo = input()
    return tipo

# - When this function is called, we are prompted to choose the difficulty of the AI when it is the Human x PC game mode, or, if we chose to see a PC x PC game, which AI's will be playing.

def dificuldade():
    if gamestate.tipo == 1:
        return
    elif gamestate.tipo == 2:
        print("Dificuldade:")
        print("1 - Fácil (Random)")
        print("2 - Médio (Greedy)")
        print("3 - Difícil (Minimax)")
        gamestate.ai2diff = input()
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

# - For each valid square, said square is selected by creating 4 small circles inside it, in the corners

def assinala_quad(x, y, screen):
    if movimento.jog == 1:
        color = pygame.Color(220, 20, 60)
    else:
        color = pygame.Color(106, 90, 205)
    pygame.draw.ellipse(
        screen, color, (y*gamestate.sq+3, x*gamestate.sq+3, 6, 6))
    pygame.draw.ellipse(screen, color, (y*gamestate.sq +
                        gamestate.sq-11, x*gamestate.sq+3, 6, 6))
    pygame.draw.ellipse(screen, color, (y*gamestate.sq+3,
                        x*gamestate.sq+gamestate.sq-11, 6, 6))
    pygame.draw.ellipse(screen, color, (y*gamestate.sq +
                        gamestate.sq-11, x*gamestate.sq+gamestate.sq-11, 6, 6))


# - When called, updates the board in the UI

def mostra_tabul(screen):
    for r in range(gamestate.N):
        for c in range(gamestate.N):
            color = pygame.Color(255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(
                c * gamestate.sq, r * gamestate.sq, gamestate.sq - 2, gamestate.sq - 2))
            if gamestate.tabuleiro[r][c] == 8:
                pygame.draw.rect(screen, (128, 128, 128),
                                 (c * gamestate.sq, r * gamestate.sq, gamestate.sq - 2, gamestate.sq - 2))
            if gamestate.tabuleiro[r][c] == 1:
                pygame.draw.ellipse(screen, (220, 20, 60), pygame.Rect(

                    c * gamestate.sq + (gamestate.sq / 4), r * gamestate.sq + (gamestate.sq / 4), gamestate.sq / 2, gamestate.sq / 2))
            elif gamestate.tabuleiro[r][c] == 2:
                pygame.draw.ellipse(screen, (106, 90, 205), pygame.Rect(
                    c * gamestate.sq + (gamestate.sq / 4), r * gamestate.sq + (gamestate.sq / 4), gamestate.sq / 2, gamestate.sq / 2))

# - This function deals with taking of the opponent pieces, after a movement is done, any adjacent pieces are swapped
#     - Note: Every if in the try...except is to stop taking from across the board because tabuleiro[-1] = tabuleiro[N]

def comer():
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

# - This function simply executes the movement, if the movement type is jumping,
# it also removes the piece from its old location, and then checks for piece taking


def executa_movimento():
    gamestate.tabuleiro[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        gamestate.tabuleiro[movimento.yi][movimento.xi] = 0
    comer()

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
    if abs(classe.yf - classe.yi) == 2 and abs(classe.xf - classe.xi) == 1 or abs(classe.xf - classe.xi) == 2 and abs(classe.yf - classe.yi) == 1:
        return False
    if not dentro(classe.xi, classe.yi) or not dentro(classe.xf, classe.yf):
        return False
    if gamestate.tabuleiro[classe.yi][classe.xi] == movimento.jog and gamestate.tabuleiro[classe.yf][classe.xf] == 0 and adjacente(1, classe):
        classe.tipo = 0
        return True
    if gamestate.tabuleiro[classe.yi][classe.xi] == movimento.jog and gamestate.tabuleiro[classe.yf][classe.xf] == 0 and adjacente(2, classe):
        classe.tipo = 1
        return True


# - This function takes the square we clicked and, if it has a piece we can move, it checks all the possible moves and selects them

def jogadas_validas_pos(jog, yi, xi, screen):
    if gamestate.tabuleiro[yi][xi] == jog:
        for k in range(gamestate.N):
            for l in range(gamestate.N):
                movimento.jog = jog
                movimento.yi = yi
                movimento.xi = xi
                movimento.yf = k
                movimento.xf = l
                if movimento_valido(movimento):
                    assinala_quad(k, l, screen)

# - This function checks the amount of valid moves a player has and returns its value. This will come in handy as if one player has zero moves, it skips his turn.

def jogadas_validas_total(jog):
    nmovs = 0
    for yi in range(gamestate.N):
        for xi in range(gamestate.N):
            if gamestate.tabuleiro[yi][xi] == jog:
                for yf in range(gamestate.N):
                    for xf in range(gamestate.N):
                        movimento.jog = jog
                        totalmov.yi = yi
                        totalmov.xi = xi
                        totalmov.yf = yf
                        totalmov.xf = xf
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

def quad_vazios():
    nmovs = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == 0:
                nmovs += 1
    return nmovs

# -  Checks if the game has reached its end conditions, depending on which one it is, it sets the winner as one of the players or as a draw.

def fim_jogo():
    n = quad_vazios()
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
            print("Jogador vermelho ganha !")
        else:
            print("Jogador azul ganha !")
    else:
        print("Empate!")

# - Manages the human player movement by:
#   If it has no valid moves, it skips the player's turn
#   Seeing if it is the first or the second click, and saving it as the initial coords or final coords, respectively
#   Selecting the clicked piece and all the valid moves

def jogada_Humano(cl, px, py, screen):
    if cl == 0:
        movimento.xi = px
        movimento.yi = py
        assinala_quad(py, px, screen)
        jogadas_validas_pos(movimento.jog, py, px, screen)
    elif cl == 1:
        movimento.xf = px
        movimento.yf = py

# - Manages the computer made movements:
#   For each piece it has, it tries every possivle move, by doing it, evaluating it, and restoring the game to before the move
#   for each evaluation, it saves the movement with the best evaluation score and then, after every move has been played
#   it does the said best move

def jogada_PC():
    bestav = -1000
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
                                av = avalia(gamestate.ai2diff)
                            else:
                                av = avalia(gamestate.ai1diff)
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
            minmaxmov.min = 1
            minmaxmov.max = 2
        else:
            movimento.jog = 2
            minmaxmov.min = 2
            minmaxmov.max = 1
        minmaxmov.yi = movimento.yi
        minmaxmov.xi = movimento.xi
        minmaxmov.yf = movimento.yf
        minmaxmov.xf = movimento.xf
        alfa = -100000
        beta = 100000
        score = algo_minmax(0, True, alfa, beta)
        movimento.yi = minmaxmov.yi
        movimento.xi = minmaxmov.xi
        movimento.yf = minmaxmov.yf
        movimento.xf = minmaxmov.xf
    elif tipo > 3:
        score = random.random()
    return score

# Random Algorithm: Evaluates a move with a random value from 1 to 10.

def algo_random():
    return random.randint(1, 10)

# Greedy Algorithm: Evaluates a move based on the difference of pieces

def algo_greedy():
    salt = random.random()
    return conta_pecas(movimento.jog) - conta_pecas(troca_jog(movimento.jog)) + salt

# Minmax Algorithm: Paired with the greedy heuristic, 
# it plays every possible sequence of moves in a depth-first tree search, 
# up to a certain depth, and then evaluates the ending states, then after every state is done 
# (or, if a state doesn't meet the alpha-beta pruning requirements, in which is skipped), 
# it plays the one with the most favorable outcome for the computer

def algo_minmax(depth, minimizer, alfa, beta):
    if depth == 3 or fim_jogo() == -1:
        return algo_greedy() * (-1)

    if minimizer:
        movimento.jog = minmaxmov.min
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
                                evaluation = algo_minmax(
                                    depth + 3, False, alfa, beta)
                                gamestate.tabuleiro = temp
                                value = min(value, evaluation)
                                beta = min(beta, evaluation)
                                if beta <= alfa:
                                    break
        movimento.jog = minmaxmov.max
        return value
    else:
        movimento.jog = minmaxmov.max
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
                                evaluation = algo_minmax(
                                    depth + 3, True, alfa, beta)
                                gamestate.tabuleiro = temp
                                value = max(value, evaluation)
                                alfa = max(alfa, evaluation)
                                if beta <= alfa:
                                    break
        movimento.jog = minmaxmov.min
        return value

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
    cl = 0
    movimento.jog = 1
    gamestate.tipo = int(tipo_jogo())
    dificuldade()
    tabuleiro = tabul()
    carrega_tabul(tabuleiro)
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    mostra_tabul(screen)
    clock.tick(30)
    pygame.display.flip()
    running = True

    while running:
        if jogadas_validas_total(movimento.jog) == 0:
            gamestate.nMovs += 1
            movimento.jog = troca_jog(movimento.jog)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                time.sleep(2)
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:

                click = pygame.mouse.get_pos()
                yi = int(click[1] // gamestate.sq)
                xi = int(click[0] // gamestate.sq)

                if gamestate.nMovs % 2 == 1:

                    if gamestate.tipo <= 2:
                        if cl == 0 and gamestate.tabuleiro[yi][xi] == movimento.jog:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            if movimento_valido(movimento):
                                executa_movimento()

                                gamestate.nMovs += 1
                                movimento.jog = 2

                            mostra_tabul(screen)
                else:

                    if gamestate.tipo == 1:
                        if cl == 0 and gamestate.tabuleiro[yi][xi] == movimento.jog:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            if movimento_valido(movimento):
                                executa_movimento()
                                gamestate.nMovs += 1
                                movimento.jog = 1
                            mostra_tabul(screen)
            try:
                pygame.display.flip()
            except pygame.error:
                pass

        if gamestate.nMovs % 2 != 1 and gamestate.tipo >= 2:
            jogada_PC()
            gamestate.nMovs += 1
            mostra_tabul(screen)
            movimento.jog = 1
            time.sleep(1)
            pygame.display.flip()

        try:
            pygame.display.flip()
        except pygame.error:
            pass

        fim = fim_jogo()
        if fim == -1:
            print("\n")
            print("Jogador Vermelho:", conta_pecas(1))
            print("Jogador Azul:", conta_pecas(2))
            finaliza()
            time.sleep(1)
            pygame.quit()
            running = False

main()
