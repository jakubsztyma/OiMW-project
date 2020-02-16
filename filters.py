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
# state -> False if any conditions proceeding this one was False
# evaluated_moves -> processed output of stockfish evaluation
#
# n_ignore -> the number of first fullmoves to ignore from evaluation


def not_a_starting_move(state, board, n_ignore):
    if not state or board.fullmove_number < n_ignore:
        return False
    else:
        return True


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
# state -> False if any conditions proceeding this one was False
# evaluated_moves -> processed output of stockfish evaluation
#
# depth -> depth at which the moves are to be compared
# min_diff -> minimum of how much cp of the best move should be greater to be considered sufficiently better


def better_than_second(state, evaluated_moves, depth, min_diff):
    if not state:
        return False
    best_move = evaluated_moves[(depth - 1) * 2]["cp"]
    second_move = evaluated_moves[(depth - 1) * 2 + 1]["cp"]

    if int(best_move) >= int(second_move) + min_diff:
        return True
    else:
        return False


#   _____ _   _ _ _   _   _            _               _
#  /  ___| | (_) | | | | | |          | |             | |
#  \ `--.| |_ _| | | | |_| |__   ___  | |__   ___  ___| |_   _ __ ___   _____   _____
#   `--. \ __| | | | | __| '_ \ / _ \ | '_ \ / _ \/ __| __| | '_ ` _ \ / _ \ \ / / _ \
#  /\__/ / |_| | | | | |_| | | |  __/ | |_) |  __/\__ \ |_  | | | | | | (_) \ V /  __/
#  \____/ \__|_|_|_|  \__|_| |_|\___| |_.__/ \___||___/\__| |_| |_| |_|\___/ \_/ \___|
#
# Test if the best move that is considered is still the best at the target depth.
# Can be used to check if the move is the best on multiple depths.
#
# ARGS:
# state -> False if any conditions proceeding this one was False
# evaluated_moves -> processed output of stockfish evaluation
#
# depth -> depth at which the moves are to be compared
# best_move -> move that is considered the best and is checked against the best move og choosen depth


def still_the_best_move(state, evaluated_moves, depth, best_move):
    a = evaluated_moves[(depth - 1) * 2]["pv"][0]
    b = best_move
    if not state or evaluated_moves[(depth - 1) * 2]["pv"][0] != best_move:
        return False
    else:
        return True


# text generated using: http://patorjk.com/software/taag/#p=display&v=2&c=bash&f=Doom
