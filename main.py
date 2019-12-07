import collections

import fire
from chess import engine as chess_engine, pgn


STOCKFISH_PATH = 'stockfish-10/Linux/stockfish_10_x64'


class Solver:
    def __init__(self, h, cp, d, n, e):
        self.h = h
        self.n = n
        self.cp = cp
        self.limit = chess_engine.Limit(depth=d)
        self.engine = chess_engine.SimpleEngine.popen_uci(e)

    def get_output(self, board, moves):
        # TODO format output accordingly to specification
        result = []
        for move in moves:
            uci_move = move['pv'][0]
            board.push(uci_move)
            result.append(board.fen())
            board.pop()
        return result

    def meets_conditions(self, best_move, second_best_move):
        # TODO add other constraints
        # Moves are sorted starting by the best
        score1 = best_move['score'].white().score()
        score2 = second_best_move['score'].white().score()
        return score1 - score2 >= self.cp

    def handle_game(self, game):
        positions = []
        board = game.board()

        for move in game.mainline_moves():
            evaluated_moves = self.engine.analyse(board, self.limit, multipv=self.n)
            best_move, second_best_move = evaluated_moves[:2]
            if self.meets_conditions(best_move, second_best_move):
                print(f'Move found {best_move["pv"][0]}')
                node_output = self.get_output(board, evaluated_moves)
                positions.extend(node_output)
            board.push(move)
        return positions


def entrypoint(
        input_path,
        output_path,
        h='minimal',
        cp=50,
        d=30,
        n=2,
        e=STOCKFISH_PATH,
        # TODO chess engine params
):
    print(input_path, output_path, h, cp, d, n, e)  # Show selected params
    solver = Solver(h, cp, d, n, e)

    with open(input_path, 'r') as input_, open(output_path, 'w') as output:
        game = pgn.read_game(input_)
        # while game:
        for _ in range(10):
            try:
                positions = solver.handle_game(game)
                for position in positions:
                    output.write(position + '\n')
            except Exception as ex:
                print(ex)
            finally:
                game = pgn.read_game(input_)

    solver.engine.quit()


if __name__ == '__main__':
    fire.Fire(entrypoint)
