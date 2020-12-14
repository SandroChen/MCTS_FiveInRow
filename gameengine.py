#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:39:35 2019

@author: root
"""
import numpy as np


# place stone according to how imminent the threat is
def place_intelligently(mat, player):
    m, n = mat.shape
    for i in range(m):
        for j in range(n):
            pos = broken_four(mat, i, j, player)
            if pos and mat[pos[0]][pos[1]] == 0:
                return pos
    for i in range(m):
        for j in range(n):
            pos = broken_three(mat, i, j, player)
            if pos and mat[pos[0]][pos[1]] == 0:
                return pos
    for i in range(m):
        for j in range(n):
            pos = broken_two(mat, i, j,player)
            if pos and mat[pos[0]][pos[1]] == 0:
                return pos
    for i in range(m):
        for j in range(n):
            pos = broken_one(mat, i, j,player)
            if pos and mat[pos[0]][pos[1]] == 0:
                return pos
    value = np.where(mat==0)
    return value[0][0], value[1][0]


def broken_four(mat, i, j, player):
    m,n = mat.shape
    if j + 5 <= m:
        sideway = mat[i][j:j+5]
        if np.sum(sideway) == player*4:
            return i,j+(mat[i][j:j+5]).tolist().index(0)
        if np.sum(sideway) == -player*4:
            return i,j+(mat[i][j:j+5]).tolist().index(0)
        
    if i + 5 <= m:
        vert =mat[:,j][i:i+5]
        if np.sum(vert) == player*4:
            return i+(vert).tolist().index(0),j
        if np.sum(vert) == -player*4:
            return i+(vert).tolist().index(0),j
        
    if j + 5 <= m and i + 5 <= n:
        diag = [mat[i+x][j+y] for x in range(5) for y in range(5) if x == y]
        if np.sum(diag) == player*4:
            return i+diag.index(0),j+diag.index(0)
        if np.sum(diag) == -player*4:
            return i+diag.index(0),j+diag.index(0)
        
    if j - 5 >= 0 and i + 5 <= n:
        diag = [mat[i+x][j-y] for x in range(5) for y in range(5) if x == y]
        if np.sum(diag) == player*4:
            return i+diag.index(0),j-diag.index(0)
        if np.sum(diag) == -player*4:
            return i+diag.index(0),j-diag.index(0)
    return None


def broken_three(mat, i, j, player):
    m,n = mat.shape
    if j + 4 <= m:
        sideway = mat[i][j:j+4]
        if np.sum(sideway) == player*3:
            return i,j+(mat[i][j:j+4]).tolist().index(0)
        if np.sum(sideway) == -player*3:
            return i,j+(mat[i][j:j+4]).tolist().index(0)
        
    if i + 4 <= m:
        vert =mat[:,j][i:i+4]
        if np.sum(vert) == player*3:
            return i+(vert).tolist().index(0),j
        if np.sum(vert) == -player*3:
            return i+(vert).tolist().index(0),j
        
    if j + 4 <= m and i + 4 <= n:
        diag = [mat[i+x][j+y] for x in range(4) for y in range(4) if x == y]
        if np.sum(diag) == player*3:
            return i+diag.index(0),j+diag.index(0)
        if np.sum(diag) == -player*3:
            return i+diag.index(0),j+diag.index(0)
        
    if j - 4 >= 0 and i + 4 <= n:
        diag = [mat[i+x][j-y] for x in range(4) for y in range(4) if x == y]
        if np.sum(diag) == player*3:
            return i+diag.index(0),j-diag.index(0)
        if np.sum(diag) == -player*3:
            return i+diag.index(0),j-diag.index(0)
    return None




def broken_two(mat, i, j, player):
    m,n = mat.shape
    if j + 3 <= m:
        sideway = mat[i][j:j+3]
        if np.sum(sideway) == player*2:
            return i,j+(mat[i][j:j+3]).tolist().index(0)
        if np.sum(sideway) == -player*2:
            return i,j+(mat[i][j:j+3]).tolist().index(0)
        
    if i + 3 <= m:
        vert =mat[:,j][i:i+3]
        if np.sum(vert) == player*2:
            return i+(vert).tolist().index(0),j
        if np.sum(vert) == -player*2:
            return i+(vert).tolist().index(0),j
        
    if j + 3 <= m and i + 3 <= n:
        diag = [mat[i+x][j+y] for x in range(3) for y in range(3) if x == y]
        if np.sum(diag) == player*2:
            return i+diag.index(0),j+diag.index(0)
        if np.sum(diag) == -player*2:
            return i+diag.index(0),j+diag.index(0)
        
    if j - 3 >= 0 and i + 3 <= n:
        diag = [mat[i+x][j-y] for x in range(3) for y in range(3) if x == y]
        if np.sum(diag) == player*2:
            return i+diag.index(0),j-diag.index(0)
        if np.sum(diag) == -player*2:
            return i+diag.index(0),j-diag.index(0)
    return None

def broken_one(mat, i, j, player):
    m,n = mat.shape
    if j + 2 <= m:
        sideway = mat[i][j:j+2]
        if np.sum(sideway) == player:
            return i,j+(mat[i][j:j+2]).tolist().index(0)
        if np.sum(sideway) == -player:
            return i,j+(mat[i][j:j+2]).tolist().index(0)
        
    if i + 2 <= m:
        vert =mat[:,j][i:i+2]
        if np.sum(vert) == player:
            return i+(vert).tolist().index(0),j
        if np.sum(vert) == -player:
            return i+(vert).tolist().index(0),j
        
    if j + 2 <= m and i + 2 <= n:
        diag = [mat[i+x][j+y] for x in range(2) for y in range(2) if x == y]
        if np.sum(diag) == player:
            return i+diag.index(0),j+diag.index(0)
        if np.sum(diag) == -player:
            return i+diag.index(0),j+diag.index(0)
        
    if j - 2 >= 0 and i + 2 <= n:
        diag = [mat[i+x][j-y] for x in range(2) for y in range(2) if x == y]
        if np.sum(diag) == player:
            return i+diag.index(0),j-diag.index(0)
        if np.sum(diag) == -player:
            return i+diag.index(0),j-diag.index(0)
    return None

