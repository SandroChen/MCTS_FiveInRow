#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:43:54 2019

@author: root
"""

import random
import time
import numpy as np
from gameengine import place_intelligently
from fiveinarow import check_for_done, check_for_win

exploration_param = np.sqrt(2)
mcts_root = None


class Node():
    def __init__(self, state, parent, player):
        self.state = state
        self.parent = parent
        self.children = {}
        self.total_value = 0
        self.visited_number = 0
        self.player = player


def move(mat, player):
    mat_tmp = np.copy(mat)
    pos = place_intelligently(mat_tmp, player)
    mat_tmp[pos[0]][pos[1]] = player
    return mat_tmp

def monte_carlo_tree_search(root):
    time_start = time.time()
    counter = 0
    while True:
        if time.time() - time_start > 1:
            break
        leaf = traverse(root)  # leaf = unvisited node
        simulation_result = rollout(leaf)
        backpropagate(leaf, simulation_result)
        counter += 1
    pprint_tree(root)
    print(f'This steps run for {counter} time')
    for c in root.children.values():
        print("score:",c.total_value)
        print(c.state)
    return best_child(root)

def expand(node):
    if len(node.children.values()) < 5:
        mat_tmp = np.copy(node.state)
        for i in range(5-len(node.children.values())):
            if len(np.where(mat_tmp==0)[0]) == 0:
                break
            mat_child = np.copy(node.state)
            pos = place_intelligently(mat_tmp, node.player * -1)
            mat_child[pos[0]][pos[1]] = node.player * -1
            mat_tmp[pos[0]][pos[1]] = 99
            node.children[str(mat_child)] = Node(mat_child, parent=node, player=node.player * -1)



# For the traverse function, to avoid using up too much time or resources, you may start considering only
# a subset of children (e.g 5 children). Increase this number or by choosing this subset smartly later.
#New implemenataion
def traverse(node):
    while fully_expanded(node.parent if node.parent else node):
        node = best_uct(node)
        if len(node.children) == 0:
            break
    done, result = check_for_done(node.state)
    if done:
        return node
    if node.parent != None:
        if pick_unvisited(node.parent.children) != None:
            return pick_unvisited(node.parent.children)
        else:
            expand(node)
            return pick_unvisited(node.children)or node
    else:
            expand(node)
            return pick_unvisited(node.children)or node

def pick_unvisited(nodes):
    unvisited_node = []
    for node in nodes.values():
        if node.visited_number == 0:
            unvisited_node.append(node)
    if len(unvisited_node) != 0:
        return random.choice(unvisited_node)
    else:
        return None

def fully_expanded(node):
    return all([c.visited_number > 0 for c in node.children.values()])


def visulize_tree(root):
    print("====================================")
    q = [root]
    while q:
        root = q[0]
        q = q[1:]
        for c in root.children.values():
            q += [c]
        print("root type",root.player,"root value",root.visited_number, "num_child",len(root.children.values()))
        print([{"node type":x.player,"node value":x.total_value, "visited":x.visited_number, "score":uct_score(x)} for x in root.children.values()])

def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", uct_score(node), sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children.values())
    for i, child in enumerate(node.children.values()):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)

def rollout(node):
    done, result = check_for_done(node.state)
    if done:
        return node, result

    player_start = node.player
    mat_game = node.state

    simulation_result = None
    while True:
        done, simulation_result = check_for_done(mat_game)
        if done:
            return simulation_result
        mat_game = move(mat_game, player_start)
        player_start = player_start*-1


def backpropagate(node, result):
    if not (node):
        return
    update_stats(node, result)
    backpropagate(node.parent, result)







def is_root(node):
    return True if node.parent == None else False


def update_stats(node, result):
    if result == node.player:
        node.total_value += 1
        node.visited_number += 1
    elif result == 0.5:
        node.total_value += 0.5
        node.visited_number += 1
    else:
        node.visited_number += 1


#def best_child(node):
#    return max(node.children.values(), key=lambda x: x.total_value)
def best_child(node):
    for child in node.children.items():
        if check_for_win(child[1].state) == -1:
            return child[1]
    return max(node.children.values(), key=lambda x: x.visited_number)


def uct_score(node):
    if not node.parent or not node or node.visited_number == 0:
        return 0
    if node.parent.visited_number == 0:
        return node.total_value / node.visited_number
    else:
        return node.total_value / node.visited_number + exploration_param * np.sqrt(np.log(node.parent.visited_number)/ node.visited_number)


def best_uct(node):
    if len(node.children) > 0:
        return max(node.children.values(), key=lambda x: uct_score(x))
    else:
        return node


def update_root(mcts_root, mat):
    if str(mat) in mcts_root.children:
        new_root = mcts_root.children[str(mat)]
        new_root.parent = None
        return new_root
    else:
        return Node(mat, parent=None, player=1)
