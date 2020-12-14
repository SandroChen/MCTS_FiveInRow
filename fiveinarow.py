#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:36:53 2019

@author: root
"""
import pygame

M=8
import numpy as np
import pdb

def update_by_man(event, mat):
    """
    This function detects the mouse click on the game window. Update the state matrix of the game.
    input:
        event:pygame event, which are either quit or mouse click)
        mat: 2D matrix represents the state of the game
    output:
        mat: updated matrix
    """
    global M
    done=False
    if event.type==pygame.QUIT:
        done=True
    if event.type==pygame.MOUSEBUTTONDOWN:
        (x,y)=event.pos
        row = round((y - 40) / 40)
        col = round((x - 40) / 40)
        mat[row][col]=1
    return mat, done


def draw_board(screen):
    """
    This function draws the board with lines.
    input: game windows
    output: none
    """
    global M
    d=int(560/(M-1))
    black_color = [0, 0, 0]
    board_color = [ 241, 196, 15 ]
    screen.fill(board_color)
    for h in range(0, M):
        pygame.draw.line(screen, black_color,[40, h * d+40], [600, 40+h * d], 1)
        pygame.draw.line(screen, black_color, [40+d*h, 40], [40+d*h, 600], 1)
def draw_stone(screen, mat):
    """
    This functions draws the stones according to the mat. It draws a black circle for matrix element 1(human),
    it draws a white circle for matrix element -1 (computer)
    input:
        screen: game window, onto which the stones are drawn
        mat: 2D matrix representing the game state
    output:
        none
    """
    black_color = [0, 0, 0]
    white_color = [255, 255, 255]
    M=len(mat)
    d=int(560/(M-1))
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i][j]==1:
                pos = [40+d * j, 40+d* i ]
                pygame.draw.circle(screen, black_color, pos, 18,0)
            elif mat[i][j]==-1:
                pos = [40+d* j , 40+d * i]
                pygame.draw.circle(screen, white_color, pos, 18,0)



def render(screen, mat):
    """
    Draw the updated game with lines and stones using function draw_board and draw_stone
    input:
        screen: game window, onto which the stones are drawn
        mat: 2D matrix representing the game state
    output:
        none
    """
    draw_board(screen)
    draw_stone(screen, mat)
    pygame.display.update()

def check_for_done(mat):
    """
    please write your own code testing if the game is over. Return a boolean variable done. If one of the players wins
    or the tie happens, return True. Otherwise return False. Print a message about the result of the game.
    input:
        2D matrix representing the state of the game
    output:
        none
    """
    result = check_for_win(mat)
    if result:
        return True, result
    else:
        if len(np.where(mat==0)[0]) == 0:
            return True, 0.5
        else:
            return False, 0


def check_for_win(mat):
    m,n = mat.shape
    target1 = [1,1,1,1,1]
    target2 = [-1,-1,-1,-1,-1]
    for i in range(m):
        for j in range(n):
            if j + 5 <= m:
                sideway = mat[i][j:j+5]
                if (sideway == target1).all():
                    return 1
                if (sideway == target2).all():
                    return -1
            if i + 5 <= m:
                vert =mat[:,j][i:i+5]
                if (vert == target1).all():
                    return 1
                if (vert == target2).all():
                    return -1
            if j + 5 <= m and i + 5 <= n:
                diag = [mat[i+x][j+y] for x in range(5) for y in range(5) if x == y]
                if diag == target1:
                    return 1
                if diag == target2:
                    return -1
            if j - 5 >= 0 and i + 5 <= n:
                diag = [mat[i+x][j-y] for x in range(5) for y in range(5) if x == y]
                if diag == target1:
                    return 1
                if diag == target2:
                    return -1
