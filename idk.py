# -*- coding: utf-8 -*-

# Import Python libs
from __future__ import absolute_import
#import logging
import json
import requests
import rotate
import numpy
import copy
import sys

player_name = "idk"

#url = "http://0d477a73.ngrok.io"
url = "http://localhost:9292"
#turns = 100


def pick_from_possible(possibilities, board):
    # max = {}

    for col, value in possibilities.iteritems():
        # print("Col:")
        # print(col)
        # print("Value:")
        # print(value)
        for rotation, located in value.iteritems():
            if 'points' not in possibilities[col][rotation]:
                possibilities[col][rotation]['points'] = 0

            # GET POINTS FOR HEIGHT
            possibilities[col][rotation]['points'] = 19 - possibilities[col][rotation]['max']

            if possibilities[col][rotation]['max'] > 19:
                possibilities[col][rotation]['points'] = possibilities[col][rotation]['points'] - 100


            # GET POINTS FOR lines cleared
            possibilities[col][rotation]['points'] = possibilities[col][rotation]['points'] + possibilities[col][rotation]['cleared'] * 9

            # Get points for slopes

            # Get points for holes
            possibilities[col][rotation]['points'] = possibilities[col][rotation]['points'] - possibilities[col][rotation]['holes'] * 2




    print("Possible")
    print(possibilities)
    points = {}
    for col, value in possibilities.iteritems():
        # print("Col:")
        # print(col)
        # print("Value:")
        # print(value)
        # points[col] = {}
        for rotation, located in value.iteritems():
            # print("LOCATED:")
            # print(located['points'])
            if 'points' not in points:
                points = located
            if located['points'] > points['points']:
                points = located

    print("PICK")
    print(points)

    points['location'] = [i for i in points['location'] if 'shift' not in i]

    return points['location']


def print_board(board, current_piece, next_piece, score):
    print("Current Peice:" + current_piece + "    Next Peice: " + next_piece + "    Score: ", score)

    i = 19
    print("          ------------")
    while i > -1:
        j = 0
        line = '          |'
        while j < len(board[i]):
            if not board[i][j]:
                line = line + " "
            else:
                line = line + board[i][j]
            j = j + 1
        print(line + "|")
        i = i - 1
    print("          ------------")

    move = None
    return board

def shift_up(location):
    l = 0
    location.append({"shift": True})
    while l < len(location):
        if 'row' in location[l]:
            location[l]['row'] = location[l]['row'] + 1
        l = l + 1

    return location


def check_up(location, board):
    l = 0
    # print("location check_up:")
    # print(location)
    floor = get_floor(board)
    while l < len(location):
        # print("Column:")
        # print(location[l]['col'])
        # print("Row Height:")
        # print(location[l]['row'])
        # print("Floor Height:")
        # print(floor[location[l]['col'] + 1])
        # if location[l]['row'] > floor[location[l]['col'] + 1] + 1:
        #     print("check down:")
        #     print(l)
        #     print(location[l]['row'])
        #     print(floor[location[l]['col']])
        #     location[l].update({"shift": True})
        if 'row' in location[l]:
            if location[l]['row'] <= floor[location[l]['col'] + 1]:
                # print("Shift Up:")
                location = shift_up(location)
                check_up(location, board)
        # print(location)
        l = l + 1

    return location


def check_down(location, board):
    floor = get_floor(board)
    print("Floor")
    print(floor)
    print("Location")
    print(location)
    # min = min(location, key = lambda x: x['row'])['col']
    # max = max(location, key = lambda x: x['row'])['col']
    min_row = {}
    for index in location:
        if 'col' in index:
            if index['col'] not in min_row:
                min_row.update({index['col']: index['row']})
        # print(index)
        # print(min_row)
        if 'row' in index:
            if index['row'] < min_row[index['col']]:
                min_row.update({index['col']: index['row']})

    print("MIN ROW")
    print(min_row)
    for col in min_row:
        if min_row[col] - floor[col + 1] > 1:
            print("check down:")
            print("Column")
            print(col)
            print("Row min vs floor:")
            print(min_row[col])
            print(floor[col + 1])
            # print(location[l]['row'])
            # print(floor[location[l]['col']])
            location.append({"shift": True})

    return location


def num_cleared_lines(location, board):
    '''
    find cleared lines
    '''
    cleared = 0
    # print("Board")
    # print(board)
    # print("Location")
    # print(location)
    next_move = copy.deepcopy(board)

    for block in location:
        # print("Block")
        # print(block)
        if 'row' in block:
            if block['row'] in next_move and block['col'] in next_move:
                next_move[block['row']][block['col']] = 'X'

    # print("Next Move")
    # print(next_move)
    for row in next_move:
        # print(row)
        if None not in row:
            cleared = cleared + 1

    # print("cleared:")
    # print(cleared)
    return cleared

def get_max(possibilities):
    for col, value in possibilities.iteritems():
        # print("Col:")
        # print(col)
        # print("Value:")
        # print(value)
        for rotation, located in value.iteritems():
            # print("Rotation:")
            # print(rotation)
            # print("Located")
            # print(located)
            # print(located[0])
            max = -5
            for block in located['location']:
                # print("Pos")
                # print(pos)
                if 'row' in block:
                    # print(possibilities[col][rotation])
                    if 'max' not in possibilities[col][rotation]:
                        max = block['row']
                    # print(possibilities[col][rotation])
                    if max < block['row']:
                        max = block['row']

                possibilities[col][rotation].update({"max": max})

    return possibilities


def get_lines_cleared(possibilities, board):
    for col, value in possibilities.iteritems():
        # print("Col:")
        # print(col)
        # print("Value:")
        # print(value)
        for rotation, located in value.iteritems():
            # print("located1")
            # print(located)
            # print(rotation)
            possibilities[col][rotation].update(
                    {'cleared': num_cleared_lines(located['location'], board)})

    return possibilities


def get_right(possibilities):
    for col, value in possibilities.iteritems():
        for rotation, located in value.iteritems():
            right = -5
            for block in located['location']:
                if 'col' in block:
                    if 'right' not in possibilities[col][rotation]:
                        right = block['col']
                    if right < block['col']:
                        right = block['col']

                possibilities[col][rotation].update({"right": right})

    return possibilities


def get_holes(possibilities, board):
    floor = get_floor(board)

    for col, value in possibilities.iteritems():
        for rotation, located in value.iteritems():
            min_row = {}
            for index in located['location']:
                if 'col' in index:
                    if index['col'] not in min_row:
                        min_row.update({index['col']: index['row']})
                # print(index)
                # print(min_row)
                if 'row' in index:
                    if index['row'] < min_row[index['col']]:
                        min_row.update({index['col']: index['row']})

            # print("MIN ROW")
            # print(min_row)
            for column in min_row:
                if 'holes' not in possibilities[col][rotation]:
                    possibilities[col][rotation].update({"holes": 0})
                if min_row[column] - floor[column + 1] - 1 > possibilities[col][rotation]['holes']:
                    possibilities[col][rotation].update(
                            {"holes": min_row[column] - floor[column + 1] - 1 + possibilities[col][rotation]['holes']})

    return possibilities

def get_left(possibilities):
    for col, value in possibilities.iteritems():
        for rotation, located in value.iteritems():
            left = -5
            for block in located['location']:
                if 'row' in block:
                    if 'left' not in possibilities[col][rotation]:
                        left = block['col']
                    if left > block['col']:
                        left = block['col']

                possibilities[col][rotation].update({"left": left})

    return possibilities


def get_slopes(possibilities, board):
    '''
    get cliffs after possible move
    '''
    possibilities = get_left(possibilities)
    possibilities = get_right(possibilities)
    floor = get_floor(board)
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    # print(floor_diff)
    # print(possibilities)
    for col, value in possibilities.iteritems():
        for rotation, located in value.iteritems():
            possibilities[col][rotation].update({"l_slope": floor_diff[possibilities[col][rotation]['left']]})
            possibilities[col][rotation].update({"r_slope": floor_diff[possibilities[col][rotation]['right'] + 1]})

    return possibilities


def get_rank(possibilities):
    print(possibilities)

    return possibilities

def rank_possibilities(possibilities, board):
    '''
    rank every position to make best pick
    '''
    # print("Possible")
    # print(possibilities)
    # print("get_lines_cleared")
    possibilities = get_lines_cleared(possibilities, board)
    # print(possibilities)
    # print("get_max")
    possibilities = get_max(possibilities)
    # print(possibilities)
    # print("get_slopes")
    possibilities = get_slopes(possibilities, board)
    # print(possibilities)
    # print("get_rank")
    possibilities = get_rank(possibilities)
    # print(possibilities)
    possibilities = get_holes(possibilities, board)

    return possibilities


def get_floor(board):
    i = 19
    floor = [30, None, None, None, None, None, None, None, None, None, None, 30]
    while i > -1:
        j = 0
        while j < len(board[i]):
            if not floor[j + 1]:
                if board[i][j]:
                    floor[j + 1] = i
            j = j + 1
        i = i - 1
    floor = [-1 if x is None else x for x in floor]
    # print("Floor:")
    # print(floor)
    return floor


def place_o(board, gid, token):
    lowest = 0
    location = []
    floor = get_floor(board)
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    sorted = numpy.argsort(floor)

    # print("Floor Diff:")
    # print(floor_diff)
    # print("Sorted Index:")
    # print(sorted)

    possibilities = {}
    col = 1
    while col < len(floor) - 2:
        possibilities[col] = {}
        # print("Posibilities")
        # print(possibilities)
        position = 1
        while position <= 1:
            possibilities[col][position] = {}
            # print("col:")
            # print(col)
            # print("position:")
            # print(position)
            locate = rotate.rotate_o(rotation=position, row=floor[col] + 1, col=col - 1)
            # print("Locate:")
            # print(locate)
            # print("Board:")
            # print(board)
            possibilities[col][position]['location'] = check_up(locate, board)
            possibilities[col][position]['location'] = check_down(locate, board)
            # print("Locate2:")
            # print(possibilities[col][position])
            position = position + 1
        col = col + 1

    # print(json.dumps(possibilities, indent=2))
    possibilities = rank_possibilities(possibilities, board)
    location = pick_from_possible(possibilities, board)

    print("Location")
    print(location)
    location = check_up(location, board)
    print("Location")
    print(location)
    locations = {"locations": location}
    print(locations)
    move = requests.post(url=url + gid + "/moves",
                         headers={"Content-Type": "application/json",
                                  "Accept": "application/json",
                                  "X-Turn-Token": token},
                         data=json.dumps(locations)
                         )
    return move


def place_i(board, gid, token):
    col = 0
    lowest = 0
    location = []
    floor = get_floor(board)
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    floor_same = {i:floor.count(i) for i in floor}
    lowest = floor.index(min(floor))
    sorted = numpy.argsort(floor)


    possibilities = {}
    col = 1
    while col < len(floor) - 1:
        possibilities[col] = {}
        # print("Posibilities")
        # print(possibilities)
        position = 1
        while position <= 2:
            # print("col:")
            # print(col)
            # print("position:")
            # print(position)
            if position == 1 and col < 11 and col > 0:
                possibilities[col][position] = {}
                locate = rotate.rotate_i(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 2 and col < 8:
                possibilities[col][position] = {}
                locate = rotate.rotate_i(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            position = position + 1
        col = col + 1

    # print(json.dumps(possibilities, indent=2))
    possibilities = rank_possibilities(possibilities, board)
    location = pick_from_possible(possibilities, board)


    print(location)
    locations = {"locations": location}
    print(locations)
    move = requests.post(url=url + gid + "/moves",
                         headers={"Content-Type": "application/json",
                                  "Accept": "application/json",
                                  "X-Turn-Token": token},
                         data=json.dumps(locations)
                         )
    return move


def place_l(board, gid, token):
    col = 0
    lowest = 0
    location = []
    floor = get_floor(board)
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    # floor_same = {i:floor.count(i) for i in floor}
    lowest = floor.index(min(floor))
    sorted = numpy.argsort(floor)

    # print("Floor Diff:")
    # print(floor_diff)
    # print("Sorted Index:")
    # print(sorted)

    possibilities = {}
    col = 1
    while col < len(floor) - 1:
        possibilities[col] = {}
        # print("Posibilities")
        # print(possibilities)
        position = 1
        while position <= 4:
            # print("col:")
            # print(col)
            # print("position:")
            # print(position)
            if position == 1 and col < 11 and col > 1:
                possibilities[col][position] = {}
                locate = rotate.rotate_l(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 2 and col < 10:
                possibilities[col][position] = {}
                locate = rotate.rotate_l(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if (position == 3 or position == 4) and col < 9:
                possibilities[col][position] = {}
                locate = rotate.rotate_l(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])

            position = position + 1
        col = col + 1

    # print(json.dumps(possibilities, indent=2))
    possibilities = rank_possibilities(possibilities, board)
    location = pick_from_possible(possibilities, board)

    print("location")
    print(location)
    location = check_up(location, board)
    print("location")
    print(location)
    locations = {"locations": location}
    print(locations)
    move = requests.post(url=url + gid + "/moves",
                         headers={"Content-Type": "application/json",
                                  "Accept": "application/json",
                                  "X-Turn-Token": token},
                         data=json.dumps(locations)
                         )
    return move


def place_j(board, gid, token):
    col = 0
    lowest = 0
    location = []
    floor = get_floor(board)
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    # floor_same = {i:floor.count(i) for i in floor}
    # lowest = floor.index(min(floor))
    lower = [i for i, x in enumerate(floor) if x == min(floor)]
    lowest = max(lower)
    sorted = numpy.argsort(floor)

    # print("Floor Diff:")
    # print(floor_diff)
    # print("Lowest:")
    # print(lowest)
    # print("Sorted Index:")
    # print(sorted)

    possibilities = {}
    col = 1
    while col < len(floor) - 1:
        possibilities[col] = {}
        # print("Posibilities")
        # print(possibilities)
        position = 1
        while position <= 4:
            # print("col:")
            # print(col)
            # print("position:")
            # print(position)
            if position == 1 and col < 10 and col > 0:
                possibilities[col][position] = {}
                locate = rotate.rotate_j(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 2 and col > 0 and col < 9:
                possibilities[col][position] = {}
                locate = rotate.rotate_j(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 3 and col > 2 and col < 11:
                possibilities[col][position] = {}
                locate = rotate.rotate_j(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 4 and col < 9:
                possibilities[col][position] = {}
                locate = rotate.rotate_j(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])

            position = position + 1
        col = col + 1

    # print(json.dumps(possibilities, indent=2))
    possibilities = rank_possibilities(possibilities, board)
    location = pick_from_possible(possibilities, board)

    print("location")
    print(location)
    location = check_up(location, board)
    print("location")
    print(location)
    print("Move:")
    locations = {"locations": location}
    print(locations)
    move = requests.post(url=url + gid + "/moves",
                         headers={"Content-Type": "application/json",
                                  "Accept": "application/json",
                                  "X-Turn-Token": token},
                         data=json.dumps(locations)
                         )
    return move


def place_s(board, gid, token):
    col = 0
    lowest = 0
    location = []
    floor = get_floor(board)
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    floor_same = {i:floor.count(i) for i in floor}
    # print(floor_diff)
    lowest = floor.index(min(floor))

    sorted = numpy.argsort(floor)

    # print("Floor Diff:")
    # print(floor_diff)
    # print(lowest)
    # print("Sorted Index:")
    # print(sorted)

    possibilities = {}
    col = 1
    while col < len(floor) - 1:
        possibilities[col] = {}
        # print("Posibilities")
        # print(possibilities)
        position = 1
        while position <= 2:
            # print("col:")
            # print(col)
            # print("position:")
            # print(position)
            if position == 1 and col < 11 and col > 1:
                possibilities[col][position] = {}
                locate = rotate.rotate_s(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 2 and col > 0 and col < 9:
                possibilities[col][position] = {}
                locate = rotate.rotate_s(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])

            position = position + 1
        col = col + 1

    # print(json.dumps(possibilities, indent=2))
    possibilities = rank_possibilities(possibilities, board)
    location = pick_from_possible(possibilities, board)

    print(location)
    location = check_up(location, board)
    print("Move:")
    print(location)
    locations = {"locations": location}
    print(locations)
    move = requests.post(url=url + gid + "/moves",
                         headers={"Content-Type": "application/json",
                                  "Accept": "application/json",
                                  "X-Turn-Token": token},
                         data=json.dumps(locations)
                         )
    return move

def place_z(board, gid, token):
    col = 0
    lowest = 0
    location = []
    floor = get_floor(board)
    # lowest = floor.index(min(floor))
    # print("Lowest: %s" % lowest)
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    floor_same = {i:floor.count(i) for i in floor}
    # print(floor_diff)
    # lowest = floor.index(min(floor))
    lower = [i for i, x in enumerate(floor) if x == min(floor)]
    lowest = max(lower)

    sorted = numpy.argsort(floor)

    # print("Floor Diff:")
    # print(floor_diff)
    # print(lowest)
    # print("Sorted Index:")
    # print(sorted)

    possibilities = {}
    col = 1
    while col < len(floor) - 1:
        possibilities[col] = {}
        # print("Posibilities")
        # print(possibilities)
        position = 1
        while position <= 2:
            # print("col:")
            # print(col)
            # print("position:")
            # print(position)
            if position == 1 and col < 10 and col > 0:
                possibilities[col][position] = {}
                locate = rotate.rotate_z(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 2 and col > 1 and col < 10:
                possibilities[col][position] = {}
                locate = rotate.rotate_z(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])

            position = position + 1
        col = col + 1
    # print(json.dumps(possibilities, indent=2))
    possibilities = rank_possibilities(possibilities, board)
    location = pick_from_possible(possibilities, board)

    print("Move:")
    print(location)
    locations = {"locations": location}
    print(locations)
    move = requests.post(url=url + gid + "/moves",
                         headers={"Content-Type": "application/json",
                                  "Accept": "application/json",
                                  "X-Turn-Token": token},
                         data=json.dumps(locations)
                         )
    return move


def place_t(board, gid, token):
    col = 0
    lowest = 0
    location = []
    floor = get_floor(board)
    # lowest = floor.index(min(floor))
    floor_diff = [j-i for i, j in zip(floor[:-1], floor[1:])]
    floor_same = {i:floor.count(i) for i in floor}
    # print(floor_diff)
    # lowest = floor.index(min(floor))
    lower = [i for i, x in enumerate(floor) if x == min(floor)]
    lowest = max(lower)

    sorted = numpy.argsort(floor)

    # print("Floor Diff:")
    # print(floor_diff)
    # print(lowest)
    # print("Sorted Index:")
    # print(sorted)

    possibilities = {}
    col = 1
    while col < len(floor) - 1:
        possibilities[col] = {}
        # print("Posibilities")
        # print(possibilities)
        position = 1
        while position <= 4:
            # print("col:")
            # print(col)
            # print("position:")
            # print(position)
            if position == 1 and col < 10 and col > 0:
                possibilities[col][position] = {}
                locate = rotate.rotate_t(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 2 and col > 1 and col < 11:
                possibilities[col][position] = {}
                locate = rotate.rotate_t(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 3 and col > 0 and col < 9:
                possibilities[col][position] = {}
                locate = rotate.rotate_t(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])
            if position == 4 and col > 1 and col < 10:
                possibilities[col][position] = {}
                locate = rotate.rotate_t(rotation=position, row=floor[col] + 1, col=col - 1)
                # print("Locate:")
                # print(locate)
                # print("Board:")
                # print(board)
                possibilities[col][position]['location'] = check_up(locate, board)
                possibilities[col][position]['location'] = check_down(locate, board)
                # print("Locate2:")
                # print(possibilities[col][position])

            position = position + 1
        col = col + 1

    # print(json.dumps(possibilities, indent=2))
    possibilities = rank_possibilities(possibilities, board)
    location = pick_from_possible(possibilities, board)

    print(location)
    location = check_up(location, board)
    print("Move:")
    print(location)
    locations = {"locations": location}
    print(locations)
    move = requests.post(url=url + gid + "/moves",
                         headers={"Content-Type": "application/json",
                                  "Accept": "application/json",
                                  "X-Turn-Token": token},
                         data=json.dumps(locations)
                         )
    return move


# START PROGRAM
arg_names = ['name', 'seats', 'gid']
args = dict(zip(arg_names, sys.argv))
player_num = 1

if 'seats' not in args:
    print("ERROR: No Arguments supplied")
    print("")
    print("Usage: %s <num_players> <GID Optional>" % args['name'])
    print("    Example: %s 2 /cea44986" % args['name'])
    exit()

# IF no game id is passed then create a game
if 'gid' not in args:
    # Create Game
    create = {
      "seats": int(args['seats']),
      "initial_garbage": 0
      }
    print(create)
    game = requests.post(url=url,
                         headers={"Content-Type": "application/json", "Accept": "application/json"},
                         data=json.dumps(create)
                         )
    print(game.headers)
    print(game.text)
    args['gid'] = game.headers['location']
    player_num = 0

print(args['gid'])
player = {
  "name": player_name
  }
# print(game.headers)
# print(game.text)

# Joint The Game
game = requests.post(url=url + args['gid'] + '/players',
                     headers={"Content-Type": "application/json", "Accept": "application/json"},
                     data=json.dumps(player)
                     )

token = game.headers['X-Turn-Token']

# print(game.headers)
# print(game.text)
state = json.loads(game.text)
# print(state)
board = state['players'][player_num]['board']
score = state['players'][player_num]['score']
# print(json.dumps(state['players'][0]['board'], indent=2))
current_piece = state['current_piece']
next_piece = state['next_piece']
print_board(board, current_piece, next_piece, score)


# Make the first move
if current_piece == 'O':
    move = place_o(board, args['gid'], token)
elif current_piece == 'I':
    move = place_i(board, args['gid'], token)
elif current_piece == 'L':
    move = place_l(board, args['gid'], token)
elif current_piece == 'J':
    move = place_j(board, args['gid'], token)
elif current_piece == 'S':
    move = place_s(board, args['gid'], token)
elif current_piece == 'Z':
    move = place_z(board, args['gid'], token)
elif current_piece == 'T':
    move = place_t(board, args['gid'], token)


print("Move")
print(move)
print(move.headers)
print(move.text)

state = json.loads(move.text)
# print(state)
board = state['players'][player_num]['board']
score = state['players'][player_num]['score']
# print(json.dumps(state['players'][0]['board'], indent=2))
current_piece = state['current_piece']
next_piece = state['next_piece']
token = move.headers['X-Turn-Token']
print_board(board, current_piece, next_piece, score)
token = move.headers['X-Turn-Token']
moves = 0

# Continue making moves until game over
while board:
    print("Board:")
    print(board)
    if current_piece == 'O':
        move = place_o(board, args['gid'], token)
    elif current_piece == 'I':
        move = place_i(board, args['gid'], token)
    elif current_piece == 'L':
        move = place_l(board, args['gid'], token)
    elif current_piece == 'J':
        move = place_j(board, args['gid'], token)
    elif current_piece == 'S':
        move = place_s(board, args['gid'], token)
    elif current_piece == 'Z':
        move = place_z(board, args['gid'], token)
    elif current_piece == 'T':
        move = place_t(board, args['gid'], token)

    print("Move")
    print(move)
    print(move.headers)
    print(move.text)

    state = json.loads(move.text)
    # print(state)
    board = state['players'][player_num]['board']
    score = state['players'][player_num]['score']
    # print(json.dumps(state['players'][0]['board'], indent=2))
    current_piece = state['current_piece']
    next_piece = state['next_piece']
    token = move.headers['X-Turn-Token']
    print_board(board, current_piece, next_piece, score)
