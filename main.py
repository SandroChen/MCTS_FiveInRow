import numpy as np
import psutil
import pygame
import tkinter
import tkinter.messagebox

from fiveinarow import draw_board, render, check_for_done

from MCTS import Node, update_root, monte_carlo_tree_search


def update_by_pc(mat):
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
    mat = monte_carlo_tree_search(root).state
    return mat


def main():
    global M
    M = 8
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Five-in-a-Row')
    done = False
    mat = np.zeros((M, M))
    d = int(560 / (M - 1))
    draw_board(screen)
    pygame.display.update()

    result = None

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            render(screen, mat)
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = event.pos
                row = round((y - 40) / d)
                col = round((x - 40) / d)
                if mat[row][col] != 0:
                    continue
                mat[row][col] = 1
                render(screen, mat)
                done, result = check_for_done(mat)
                if done:
                    break
                else:
                    mat = update_by_pc(mat)
                done, result = check_for_done(mat)
                if done:
                    break
                print('CPU Usage:', psutil.cpu_percent())

    print("winner is:", result)
    def but():
        """
        Output the game result pop-up window
        """
        if result == 0:
            tkinter.messagebox.showinfo('获胜的是', '平局')
        elif result == 1:
            tkinter.messagebox.showinfo('获胜的是', '人')
        elif result == -1:
            tkinter.messagebox.showinfo('获胜的是', '电脑')
        else:
            tkinter.messagebox.showinfo('获胜的是', '未知')
    root=tkinter.Tk()
    root.title('查看结果')#标题
    root.geometry('200x150')#窗体大小
    root.resizable(False, False)#固定窗体
    tkinter.Button(root, text='点击该处',command=but).pack()
    root.mainloop()

if __name__ == '__main__':
    main()

