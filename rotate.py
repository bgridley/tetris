# -*- coding: utf-8 -*-
'''
Module file: rotate.py
'''

def rotate_o(rotation, row, col):
    '''
    rotate L
    '''
    location = []
    # OO
    # OO
    if rotation == 1:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 1,
                     "col": col + 1}
                    ]
    return location

def rotate_i(rotation, row, col):
    '''
    rotate I
    '''
    location = []

    # LL
    #  L
    #  L
    if rotation == 1:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 2,
                     "col": col},
                    {"row": row + 3,
                     "col": col}
                    ]
    if rotation == 2:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row,
                     "col": col + 2},
                    {"row": row,
                     "col": col + 3}
                    ]
    return location

def rotate_l(rotation, row, col):
    '''
    rotate L
    '''
    location = []

    # LL
    #  L
    #  L
    if rotation == 1:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 2,
                     "col": col},
                    {"row": row + 2,
                     "col": col - 1}
                    ]
    # L
    # L
    # LL
    elif rotation == 2:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 2,
                     "col": col}
                    ]
    # LLL
    # L
    elif rotation == 3:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 1,
                     "col": col + 1},
                    {"row": row + 1,
                     "col": col + 2}
                    ]
    #   L
    # LLL
    else:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row,
                     "col": col + 2},
                    {"row": row + 1,
                     "col": col + 2}
                    ]

    return location


def rotate_j(rotation, row, col):
    location = []

    # JJ
    # J
    # J
    if rotation == 1:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 2,
                     "col": col},
                    {"row": row + 2,
                     "col": col + 1}
                    ]
    #  J
    #  J
    # JJ
    elif rotation == 2:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row + 1,
                     "col": col + 1},
                    {"row": row + 2,
                     "col": col + 1}
                    ]
    # JJJ
    #   J
    elif rotation == 3:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 1,
                     "col": col - 1},
                    {"row": row + 1,
                     "col": col - 2}
                    ]
    # J
    # JJJ
    else:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row,
                     "col": col + 2}
                    ]

    return location


def rotate_s(rotation, row, col):
    location = []

    # S
    # SS
    #  S
    if rotation == 1:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 1,
                     "col": col - 1},
                    {"row": row + 2,
                     "col": col - 1}
                    ]
    #  SS
    # SS
    elif rotation == 2:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row + 1,
                     "col": col + 1},
                    {"row": row + 1,
                     "col": col + 2}
                    ]

    return location


def rotate_z(rotation, row, col):
    location = []

    #  Z
    # ZZ
    # Z
    if rotation == 1:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 1,
                     "col": col + 1},
                    {"row": row + 2,
                     "col": col + 1}
                    ]
    # ZZ
    #  ZZ
    elif rotation == 2:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 1,
                     "col": col - 1}
                    ]

    return location


def rotate_t(rotation, row, col):
    '''
    rotate T
    '''
    location = []

    # T
    # TT
    # T
    if rotation == 1:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 2,
                     "col": col},
                    {"row": row + 1,
                     "col": col + 1}
                    ]
    #  T
    # TT
    #  T
    elif rotation == 2:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 2,
                     "col": col},
                    {"row": row + 1,
                     "col": col - 1}
                    ]
    #  T
    # TTT
    elif rotation == 3:
        location = [{"row": row,
                     "col": col},
                    {"row": row,
                     "col": col + 1},
                    {"row": row,
                     "col": col + 2},
                    {"row": row + 1,
                     "col": col + 1}
                    ]
    # TTT
    #  T
    else:
        location = [{"row": row,
                     "col": col},
                    {"row": row + 1,
                     "col": col - 1},
                    {"row": row + 1,
                     "col": col},
                    {"row": row + 1,
                     "col": col + 1}
                    ]

    return location
