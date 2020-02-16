from chess import Move


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
# board -> current board state
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
    if not state or len(evaluated_moves) < depth * 2:
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
    if (
        not state
        or len(evaluated_moves) < depth * 2
        or evaluated_moves[(depth - 1) * 2]["pv"][0] != best_move
    ):
        return False
    else:
        return True


#   _    _                 _     _               _
#  | |  | |               | |   | |             | |
#  | |  | | __ _ ___ _ __ | |_  | |__   ___  ___| |_   _ __ ___   _____   _____
#  | |/\| |/ _` / __| '_ \| __| | '_ \ / _ \/ __| __| | '_ ` _ \ / _ \ \ / / _ \
#  \  /\  / (_| \__ \ | | | |_  | |_) |  __/\__ \ |_  | | | | | | (_) \ V /  __/
#   \/  \/ \__,_|___/_| |_|\__| |_.__/ \___||___/\__| |_| |_| |_|\___/ \_/ \___|
#
# Test if the best move that is considered  wasn't the best at the target depth. Reversed "still_the_best_move".
# Can be used to check if the move is only better after the evaluatiion reached deeper levels.
#
# ARGS:
# state -> False if any conditions proceeding this one was False
# evaluated_moves -> processed output of stockfish evaluation
#
# depth -> depth at which the moves are to be compared
# best_move -> move that is considered the best and is checked against the best move og choosen depth


def wasnt_best_move(state, evaluated_moves, depth, best_move):
    if (
        not state
        or len(evaluated_moves) < depth * 2
        or evaluated_moves[(depth - 1) * 2]["pv"][0] == best_move
    ):
        return False
    else:
        return True


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
# state -> False if any conditions proceeding this one was False
# board -> current board state
#
# best_move -> move that is considered


def not_check(state, board, best_move):
    if (
        not state
        or board.is_checkmate()
        or board.is_into_check(Move.from_uci(best_move))
    ):
        return False
    else:
        return True


#   _   _                         _            _       _               _
#  | \ | |                       | |          (_)     | |             (_)
#  |  \| | ___    _ __ ___   __ _| |_ ___ _ __ _  __ _| |   __ _  __ _ _ _ __
#  | . ` |/ _ \  | '_ ` _ \ / _` | __/ _ \ '__| |/ _` | |  / _` |/ _` | | '_ \
#  | |\  | (_) | | | | | | | (_| | ||  __/ |  | | (_| | | | (_| | (_| | | | | |
#  \_| \_/\___/  |_| |_| |_|\__,_|\__\___|_|  |_|\__,_|_|  \__, |\__,_|_|_| |_|
#                                                           __/ |
#                                                          |___/
# Check if move results in material gain.
# Incompatible with "no_better_gain"
#
# ARGS:
# state -> False if any conditions proceeding this one was False
# board -> current board state
#
# best_move -> move that is considered


def no_material_gain(state, board, best_move):
    if not state:
        return False
    target = Move.from_uci(best_move).to_square
    piece_at_target = board.piece_at(target)
    if piece_at_target is not None:
        return False
    else:
        return True


#  ______      _   _                              _            _       _               _
#  | ___ \    | | | |                            | |          (_)     | |             (_)
#  | |_/ / ___| |_| |_ ___ _ __   _ __ ___   __ _| |_ ___ _ __ _  __ _| |   __ _  __ _ _ _ __
#  | ___ \/ _ \ __| __/ _ \ '__| | '_ ` _ \ / _` | __/ _ \ '__| |/ _` | |  / _` |/ _` | | '_ \
#  | |_/ /  __/ |_| ||  __/ |    | | | | | | (_| | ||  __/ |  | | (_| | | | (_| | (_| | | | | |
#  \____/ \___|\__|\__\___|_|    |_| |_| |_|\__,_|\__\___|_|  |_|\__,_|_|  \__, |\__,_|_|_| |_|
#                                                                           __/ |
#                                                                          |___/
# Check if player is able to take better pieces.
# Incompatible with "no_material_gain".
#
# ARGS:
# state -> False if any conditions proceeding this one was False
# board -> current board state
#
# best_move -> move that is considered


def better_material_gain(state, board, best_move):
    if not state:
        return False

    target = Move.from_uci(best_move).to_square
    piece_type_moving = Move.from_uci(best_move).from_square
    piece_at_target = board.piece_at(target)
    if piece_at_target is None:
        return True

    best_move_value = piece_at_target.piece_type
    best_legal_value = max(
        [board.piece_type_at(move.to_square) or 0 for move in board.legal_moves]
    )

    if best_legal_value <= best_move_value:
        return False
    else:
        return True


# text generated using: http://patorjk.com/software/taag/#p=display&v=2&c=bash&f=Doom
