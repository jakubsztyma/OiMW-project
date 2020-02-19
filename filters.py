from copy import deepcopy

from chess import Move


# Test if the move is not the only valid move
#
# ARGS:
# evaluated_moves -> processed output of stockfish evaluation

def not_only_move(evaluated_moves):
    if len(evaluated_moves) < 2:
        return False
    return True


# Test if the move is not losing
#
# ARGS:
# evaluated_moves -> processed output of stockfish evaluation
def not_losing(evaluated_moves):
    if "cp" not in evaluated_moves[0]:
        return True
    return int(evaluated_moves[0]["cp"]) > -200


#   _   _       _                 _             _   _
#  | \ | |     | |               | |           | | (_)
#  |  \| | ___ | |_    __ _   ___| |_ __ _ _ __| |_ _ _ __   __ _   _ __ ___   _____   _____
#  | . ` |/ _ \| __|  / _` | / __| __/ _` | '__| __| | '_ \ / _` | | '_ ` _ \ / _ \ \ / / _ \
#  | |\  | (_) | |_  | (_| | \__ \ || (_| | |  | |_| | | | | (_| | | | | | | | (_) \ V /  __/
#  \_| \_/\___/ \__|  \__,_| |___/\__\__,_|_|   \__|_|_| |_|\__, | |_| |_| |_|\___/ \_/ \___|
#                                                            __/ |
#                                                           |___/
# Test if the move was made at the beggining of the game.
#
# ARGS:
# board -> current board state
# n_ignore -> the number of first fullmoves to ignore from evaluation


def not_a_starting_move(board, n_ignore):
    return board.fullmove_number >= n_ignore


#  ______      _   _              _   _                                                _
#  | ___ \    | | | |            | | | |                                              | |
#  | |_/ / ___| |_| |_ ___ _ __  | |_| |__   __ _ _ __    ___  ___  ___ ___  _ __   __| |
#  | ___ \/ _ \ __| __/ _ \ '__| | __| '_ \ / _` | '_ \  / __|/ _ \/ __/ _ \| '_ \ / _` |
#  | |_/ /  __/ |_| ||  __/ |    | |_| | | | (_| | | | | \__ \  __/ (_| (_) | | | | (_| |
#  \____/ \___|\__|\__\___|_|     \__|_| |_|\__,_|_| |_| |___/\___|\___\___/|_| |_|\__,_|
#
# Test if the best move is sufficiently better than the second-best move.
#
# ARGS:
# evaluated_moves -> processed output of stockfish evaluation
# min_diff -> minimum of how much cp of the best move should be greater to be considered sufficiently better


def better_than_second(evaluated_moves, min_diff):
    if len(evaluated_moves) < 2:
        return False
    if "cp" not in evaluated_moves[0] or "cp" not in evaluated_moves[1]:
        return True
    best_move = evaluated_moves[0]["cp"]
    second_move = evaluated_moves[1]["cp"]

    return int(best_move) >= int(second_move) + min_diff


#               _         _                             _                _                      _            _   _
#              | |       | |                           (_)              (_)                    | |          | | | |
#   _ __   ___ | |_   ___| |_ _ __ ___  _ __   __ _     _ _ __      __ _ ___   _____ _ __    __| | ___ _ __ | |_| |__
#  | '_ \ / _ \| __| / __| __| '__/ _ \| '_ \ / _` |   | | '_ \    / _` | \ \ / / _ \ '_ \  / _` |/ _ \ '_ \| __| '_ \
#  | | | | (_) | |_  \__ \ |_| | | (_) | | | | (_| |   | | | | |  | (_| | |\ V /  __/ | | || (_| |  __/ |_) | |_| | | |
#  |_| |_|\___/ \__| |___/\__|_|  \___/|_| |_|\__, |   |_|_| |_|   \__, |_| \_/ \___|_| |_| \__,_|\___| .__/ \__|_| |_|
#                ______                        __/ |_____    ______ __/ |               ______        | |
#               |______|                      |___/______|  |______|___/               |______|       |_|
# Test if the best move that is considered  wasn't strong at the target depth.
# Can be used to check if the move is strong only after the evaluatiion reached deeper levels.
#
# ARGS:
# evaluated_moves -> processed output of stockfish evaluation
# depth -> depth at which the moves are to be compared
# best_move -> move that is considered the best and is checked against the best move of chosen depth


def not_strong_in_given_depth(all_evaluated, depth, best_move):
    if depth not in all_evaluated or len(all_evaluated[depth]) == 1:
        return True
    best_at_depth = all_evaluated[depth]
    if best_at_depth[0]["pv"] != best_move:
        return True
    CP_THRESHOLD = 20
    if "cp" not in best_at_depth[0] or "cp" not in best_at_depth[1]:
        return True
    return int(best_at_depth[0]["cp"]) < CP_THRESHOLD + int(best_at_depth[1]["cp"])


#   _   _       _          _               _
#  | \ | |     | |        | |             | |
#  |  \| | ___ | |_    ___| |__   ___  ___| | __
#  | . ` |/ _ \| __|  / __| '_ \ / _ \/ __| |/ /
#  | |\  | (_) | |_  | (__| | | |  __/ (__|   <
#  \_| \_/\___/ \__|  \___|_| |_|\___|\___|_|\_\
#
# Test if the best move results in check or the current possition is a checkmate.
#
# ARGS:
# board -> current board state
# best_move -> move that is considered


def not_check(board, best_move):
    board_copy = deepcopy(board)
    board_copy.push(Move.from_uci(best_move))
    return not board_copy.is_check()


# Check if there are moves that capture pieces of at least the same strength.
#
# ARGS:
# board -> current board state
# best_move -> move that is considered

#   _                   _     _               _                     _            _       _                _
#  (_)                 | |   | |             | |                   | |          (_)     | |              (_)
#   _ ___   _ __   ___ | |_  | |__   ___  ___| |_   _ __ ___   __ _| |_ ___ _ __ _  __ _| |    __ _  __ _ _ _ __
#  | / __| | '_ \ / _ \| __| | '_ \ / _ \/ __| __| | '_ ` _ \ / _` | __/ _ \ '__| |/ _` | |   / _` |/ _` | | '_ \
#  | \__ \ | | | | (_) | |_  | |_) |  __/\__ \ |_  | | | | | | (_| | ||  __/ |  | | (_| | |  | (_| | (_| | | | | |
#  |_|___/ |_| |_|\___/ \__| |_.__/ \___||___/\__| |_| |_| |_|\__,_|\__\___|_|  |_|\__,_|_|   \__, |\__,_|_|_| |_|
#      ______            ______                ______                                   ______ __/ |
#     |______|          |______|              |______|                                 |______|___/
def is_not_best_material_gain(board, best_move):
    best_move = Move.from_uci(best_move)
    piece_at_target = board.piece_at(best_move.to_square)
    if piece_at_target is None:
        return True

    if len(list(board.legal_moves)) == 1:
        return True

    move_value = piece_at_target.piece_type
    best_legal_value = max([
        board.piece_type_at(move.to_square) or 0
        for move in board.legal_moves
        if move != best_move
    ])
    return best_legal_value >= move_value

# text generated using: http://patorjk.com/software/taag/#p=display&v=2&c=bash&f=Doom
