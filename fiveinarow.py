#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:36:53 2019

@author: root
"""
import pygame
import numpy as np

M = 8


def check_for_done(mat):
    """
    please write your own code testing if the game is over. Return a boolean variable done. If one of the players wins
    or the tie happens, return True. Otherwise return False. Print a message about the result of the game.
    input:
        2D matrix representing the state of the game
    output:
        none
    """
    result = game_result(mat)
    if result:
        return True, result
    else:
        if len(np.where(mat == 0)[0]) == 0:
            return True, 0.5
        else:
            return False, 0


def game_result(board):
    # check if game is over
    rowcum = np.cumsum(board, 0)
    colcum = np.cumsum(board, 1)

    rowsum = rowcum[4:, :] - np.vstack((np.zeros(M), rowcum[:M - 5, :]))
    colsum = colcum[:, 4:] - np.hstack((np.zeros((M, 1)), colcum[:, :M - 5]))
    diag_tl = np.array([
        board[i:i + 5, j:j + 5]
        for i in range(M - 4)
        for j in range(M - 4)
    ])
    diag_sum_tl = diag_tl.trace(axis1=1, axis2=2)
    diag_sum_tr = diag_tl[:, ::-1].trace(axis1=1, axis2=2)

    player_one_wins = 5 in rowsum
    player_one_wins += 5 in colsum
    player_one_wins += 5 in diag_sum_tl
    player_one_wins += 5 in diag_sum_tr

    if player_one_wins:
        return 1

    player_two_wins = -5 in rowsum
    player_two_wins += -5 in colsum
    player_two_wins += -5 in diag_sum_tl
    player_two_wins += -5 in diag_sum_tr

    if player_two_wins:
        return -1

    if np.all(board != 0):
        return 0.

    # if not over - no result
    return None
