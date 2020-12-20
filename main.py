import numpy as np
import pygame

from fiveinarow import check_for_done, game_result
from MCTSearch import Node, monte_carlo_tree_search


def update_by_pc(mat, step):
    # global mcts_root

    """
    This is the core of the game. Write your code to give the computer the intelligence to play a Five-in-a-Row game
    with a human
    input:
        2D matrix representing the state of the game.
    output:
        2D matrix representing the updated state of the game.
    """
    root = Node(mat, parent=None, player=1)
    mat = monte_carlo_tree_search(root, 1, step).state
    return mat


def draw_board(screen, size):
    screen.fill((230, 185, 70))
    for x in range(size):
        pygame.draw.line(screen, [0, 0, 0], [25 + 50 * x, 25], [25 + 50 * x, size*50-25], 1)
        pygame.draw.line(screen, [0, 0, 0], [25, 25 + 50 * x], [size*50-25, 25 + 50 * x], 1)
    pygame.display.update()


def update_board(screen, state):
    indices = np.where(state != 0)
    for (row, col) in list(zip(indices[0], indices[1])):
        if state[row][col] == 1:
            pygame.draw.circle(screen, [0, 0, 0], [25 + 50 * col, 25 + 50 * row], 15, 15)
        elif state[row][col] == -1:
            pygame.draw.circle(screen, [255, 255, 255], [25 + 50 * col, 25 + 50 * row], 15, 15)
    pygame.display.update()


def main():
    global M
    M = 8
    pygame.init()
    screen = pygame.display.set_mode((50*M, 50*M))
    pygame.display.set_caption('Five-in-a-Row')
    mat = np.zeros((M, M))
    draw_board(screen, M)
    pygame.display.update()
    done = False
    pc_step = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            update_board(screen, mat)
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = event.pos
                col = round((x - 25) / 50)
                row = round((y - 25) / 50)
                if mat[row][col] != 0:
                    continue
                mat[row][col] = 1
                update_board(screen, mat)
                done, _ = check_for_done(mat)
                if done:
                    break
                else:
                    pc_step += 1
                    mat = update_by_pc(mat, pc_step)
                done, _ = check_for_done(mat)

        if game_result(mat) is not None:
            myfont = pygame.font.Font(None, 40)
            text = ""
            if game_result(mat) == 1:
                text = "Human player wins!"
            elif game_result(mat) == -1:
                text = "Computer player wins!"
            else:
                text = "Nobody wins!"
            textImage = myfont.render(text, True, (255, 255, 255))
            screen.blit(textImage, (int(M*50/2)-len(text)*8, int(M*50/2)-20))
            pygame.display.update()


if __name__ == '__main__':
    main()

