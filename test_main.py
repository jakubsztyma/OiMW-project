import chess
import pytest
from chess.engine import Cp, PovScore

from main import *


@pytest.fixture
def solver():
    return Solver('minimal', 50, 5, 2, STOCKFISH_PATH)  # d is low to speed up tests


def get_info_obj(score):
    pov_score = PovScore(Cp(score), chess.WHITE)
    return dict(score=pov_score)


def test_get_output(solver):
    board = chess.Board()
    best_move = solver.engine.analyse(board, solver.limit)

    output = solver.get_output(board, [best_move])

    assert output == ['rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq - 0 1']


@pytest.mark.parametrize('score1, score2, exprected_result', [
    [50, 0, True],
    [49, 0, False],
])
def test_meets_conditions(solver, score1, score2, exprected_result):
    best_move = get_info_obj(score1)
    second_best_move = get_info_obj(score2)

    result = solver.meets_conditions(best_move, second_best_move)

    assert result == exprected_result


def test_handle_game(solver):
    with open('test_pgn.pgn') as pgn_file:
        game = pgn.read_game(pgn_file)

    result = solver.handle_game(game)

    assert len(result) == 24
