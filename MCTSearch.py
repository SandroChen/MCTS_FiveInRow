import random
import time
import numpy as np
from Strategy import rollout_policy
from fiveinarow import check_for_done, game_result


class Node:
    def __init__(self, state, parent, player):
        self.state = state
        self.player = player
        # total win times
        self.m = 0
        # n
        self.n = 0
        self.parent = parent
        self.children = {}


def monte_carlo_tree_search(root, end_seconds, step):
    time_start = time.time()
    simulation_times = 0
    while True:
        if time.time() - time_start > end_seconds:
            break
        leaf = traverse(root, step)  # leaf = unvisited node
        simulation_result = rollout(leaf, step)
        backpropagate(leaf, simulation_result)
        step += 1
        simulation_times += 1
    print(f'Simulation times: {simulation_times} in {end_seconds} s.')
    return best_child(root)


def expand(node, step):
    if len(node.children.values()) < 5:
        mat_tmp = np.copy(node.state)
        for i in range(5 - len(node.children.values())):
            if len(np.where(mat_tmp == 0)[0]) == 0:
                break
            mat_child = np.copy(node.state)
            x, y = rollout_policy(mat_tmp, -1 * node.player, step)
            mat_child[x][y] = -1 * node.player
            mat_tmp[x][y] = 999
            node.children[str(mat_child)] = Node(mat_child, parent=node, player=-1 * node.player)


# For the traverse function, to avoid using up too much time or resources, you may start considering only
# a subset of children (e.g 5 children). Increase this number or by choosing this subset smartly later.
# New implemenataion
def traverse(node, step):
    while fully_expanded(node.parent if node.parent else node):
        node = best_uct(node)
        if len(node.children) == 0:
            break
    done, result = check_for_done(node.state)
    if done:
        return node
    if node.parent is not None:
        if pick_unvisited(node.parent.children) is not None:
            return pick_unvisited(node.parent.children)
        else:
            expand(node, step)
            return pick_unvisited(node.children) or node
    else:
        expand(node, step)
        return pick_unvisited(node.children) or node


def pick_unvisited(nodes):
    unvisited_node = []
    for node in nodes.values():
        if node.n == 0:
            unvisited_node.append(node)
    if len(unvisited_node) != 0:
        return random.choice(unvisited_node)
    else:
        return None


def fully_expanded(node):
    return all([c.n > 0 for c in node.children.values()])


def move(mat, player, step):
    mat_tmp = np.copy(mat)
    x, y = rollout_policy(mat_tmp, player, step)
    mat_tmp[x][y] = player
    return mat_tmp


def rollout(node, step):
    done, result = check_for_done(node.state)
    if done:
        return node, result

    player_start = node.player
    mat_game = node.state

    while True:
        done, simulation_result = check_for_done(mat_game)
        if done:
            return simulation_result
        mat_game = move(mat_game, player_start, step)
        player_start = player_start * -1


def backpropagate(node, result):
    if not node:
        return
    update_states(node, result)
    backpropagate(node.parent, result)


def is_root(node):
    return True if node.parent is None else False


def update_states(node, result):
    if result == node.player:
        node.m += 1
        node.n += 1
    elif result == 0.5:
        node.m += 0.5
        node.n += 1
    else:
        node.n += 1


def best_child(node):
    for child in node.children.items():
        if game_result(child[1].state) == -1:
            return child[1]
    return max(node.children.values(), key=lambda x: x.n)


def uct_score(node, c_value):
    if not node.parent or not node or node.n == 0:
        return 0
    if node.parent.n == 0:
        return node.m / node.n
    else:
        return node.m / node.n + c_value * np.sqrt(
            np.log(node.parent.n) / node.n)


def best_uct(node):
    if len(node.children) > 0:
        return max(node.children.values(), key=lambda x: uct_score(x, np.sqrt(2)))
    else:
        return node
