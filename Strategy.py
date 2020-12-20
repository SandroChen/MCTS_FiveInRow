#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:39:35 2019

@author: root
"""
import numpy as np


# place stone according to how imminent the threat is
def rollout_policy(mat, player, step):
    m, n = mat.shape
    M = [3, 4, 5, 6, 2, 7, 1, 0]
    N = [3, 4, 5, 6, 2, 7, 1, 0]
    if step < 3:
        start = 3
    else:
        start = 5
    for stone_num in range(start, 1, -1):
        for i in range(m):
            for j in range(n):
                pos = broken(mat, M[i], N[j], player, stone_num)
                if pos and mat[pos[0]][pos[1]] == 0:
                    return pos
    value = np.where(mat == 0)
    return value[0][0], value[1][0]


def broken(mat, i, j, player, stone_len):
    m, n = mat.shape
    if j + stone_len <= m:
        side = mat[i][j:j + stone_len]
        if np.sum(side) == player * (stone_len - 1):
            return i, j + (mat[i][j:j + stone_len]).tolist().index(0)
        if np.sum(side) == -player * (stone_len - 1):
            return i, j + (mat[i][j:j + stone_len]).tolist().index(0)

    if i + stone_len <= m:
        vertical = mat[:, j][i:i + stone_len]
        if np.sum(vertical) == player * (stone_len - 1):
            return i + (vertical).tolist().index(0), j
        if np.sum(vertical) == -player * (stone_len - 1):
            return i + (vertical).tolist().index(0), j

    if j + stone_len <= m and i + stone_len <= n:
        back_diagonal = [mat[i + x][j + y] for x in range(stone_len) for y in range(stone_len) if x == y]
        if np.sum(back_diagonal) == player * (stone_len - 1):
            return i + back_diagonal.index(0), j + back_diagonal.index(0)
        if np.sum(back_diagonal) == -player * (stone_len - 1):
            return i + back_diagonal.index(0), j + back_diagonal.index(0)

    if j - stone_len >= 0 and i + stone_len <= n:
        diagonal = [mat[i + x][j - y] for x in range(stone_len) for y in range(stone_len) if x == y]
        if np.sum(diagonal) == player * (stone_len - 1):
            return i + diagonal.index(0), j - diagonal.index(0)
        if np.sum(diagonal) == -player * (stone_len - 1):
            return i + diagonal.index(0), j - diagonal.index(0)
    return None
