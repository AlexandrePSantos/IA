import copy
import random
import time

SIZE = 600


class gamestate:
    N = 0
    sq = 0
    tabuleiro = []
    tipo = 3
    ai1diff = 0
    ai2diff = 0
    nMovs = 1
    vencedor = 0


class movimento:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    jog = 0
    tipo = 0


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


class save:
    game = []


def tabul():
    board = "tabuleiro/hex.txt"
    return board


def carrega_tabul(ficheiro):
    f = open(ficheiro)
    gamestate.N = int(f.readline())
    gamestate.sq = SIZE / gamestate.N
    tabuleiro = []
    for i in range(gamestate.N):
        tabuleiro.append(list(map(int, f.readline().split())))
    f.close()
    gamestate.tabuleiro = tabuleiro


def players():
    print("Player 1:")
    print("1) Random")
    print("2) Greedy")
    print("3) minimax")
    gamestate.ai1diff = int(input())
    print("Player 2:")
    print("1) Random")
    print("2) Greedy")
    print("3) minimax")
    gamestate.ai2diff = int(input())
    return


def copia():
    save.game = copy.deepcopy(gamestate.tabuleiro)


def restaura():
    gamestate.tabuleiro = save.game


def troca_jog(jog):
    if jog == 1:
        return 2
    else:
        return 1


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


def executa_movimento():
    gamestate.tabuleiro[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        gamestate.tabuleiro[movimento.yi][movimento.xi] = 0
    comer()


def adjacente(dist, classe):
    return(
        abs(classe.xi - classe.xf) == dist and abs(classe.yi - classe.yf) <= dist or
        abs(classe.yi - classe.yf) == dist and abs(classe.xi - classe.xf) <= dist)


def dentro(x, y):
    return 0 <= x <= gamestate.N - 1 and 0 <= y <= gamestate.N - 1


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


def conta_pecas(jog):
    pecas = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == jog:
                pecas += 1
    return pecas


def quad_validos():
    nmovs = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == 0:
                nmovs += 1
    return nmovs


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


def finaliza():
    if gamestate.vencedor != 0:
        if gamestate.vencedor == -1:
            resultados.vermelho += 1
        else:
            resultados.azul += 1
    else:
        resultados.empate += 1
    resultados.jogadas.append(gamestate.nMovs)


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


def algo_random():
    return random.randint(1, 10)


def algo_greedy():
    salt = random.random()
    return conta_pecas(movimento.jog) - conta_pecas(troca_jog(movimento.jog))+salt


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


class resultados:
    vermelho = 0
    azul = 0
    empate = 0
    jogadas = []
    diff = []
    media = 0


tabuleiro = tabul()
carrega_tabul(tabuleiro)
players()

total = int(input("Número de iterações a realizar: "))


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
print("Peças Player 1:", conta_pecas(1))
print("Peças Player 2:", conta_pecas(2))
print("Empates: ", resultados.empate)
print("Tempo de execução: %s" % (time.time() - start_time))
print("Win Rate Player 1: " + str(resultados.vermelho * 100.0 / total) + "%")
print("Win Rate Player 2: " + str(resultados.azul * 100.0 / total) + "%")

main()