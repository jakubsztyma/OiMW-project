import chess
import pytest

from main import *


@pytest.fixture
def solver():
    return Solver('minimal', 50, 5, 2, STOCKFISH_PATH)  # d is low to speed up tests


def test_get_output(solver):
    board = chess.Board()
    best_move = solver.engine.analyse(board, solver.limit)

    output = solver.get_output(board, [best_move])

    solver.engine.quit()
    assert output == ['rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq - 0 1']
