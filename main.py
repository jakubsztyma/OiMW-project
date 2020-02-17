from time import time

import fire
import filters as ff
from chess import engine as chess_engine, pgn

from uci_http_client import UCIHttpClient


class Solver:
    CONCISE_HEADERS = {"White", "Black", "Site", "Date"}

    def __init__(self, h, cp, d, cpu_cores, **kwargs):
        self.h = h
        self.cpu_cores = cpu_cores
        self.cp = cp
        self.limit = chess_engine.Limit(depth=d)
        self.engine = UCIHttpClient()

    def __del__(self):
        pass
        # self.engine.quit()

    def get_desired_headers(self, game_headers):
        if self.h == "minimal":
            return {}
        elif self.h == "concise":
            result = {
                key: val
                for key, val in game_headers.items()
                if key in self.CONCISE_HEADERS
            }
            return result
        elif self.h == "all":
            return game_headers
        else:
            raise Exception("Invalid h parameter")

    def get_output(self, headers, board, real_move, best_move, second_best):
        
        board_fen = board.fen()
        board_num = board.fullmove_number
        best_move_data = (board_num, best_move["pv"][0], best_move["cp"], real_move == best_move["pv"][0])
        second_move_data = (board_num, second_best["pv"][0], second_best["cp"], real_move == second_best["pv"][0])

        return (board_fen, best_move_data, [second_move_data])


    def handle_game(self, game):
        positions = []
        board = game.board()
        headers = self.get_desired_headers(game.headers)

        for move in game.mainline_moves():
            evaluated_moves = self.engine.analyse(
                board.fen(), self.limit, cores=self.cpu_cores
            )

            depth = 5
            if len(evaluated_moves) < depth * 2:
                continue  # because the game is bound to end before achieving that depth?

            best_move = evaluated_moves[(depth - 1) * 2]["pv"][0]
            state = True

            state = ff.not_a_starting_move(state, board, n_ignore=2)
            state = ff.not_check(state, board, best_move=best_move)
            state = ff.better_than_second(
                state, evaluated_moves, depth=depth, min_diff=5
            )
            state = ff.wasnt_best_move(
                state, evaluated_moves, depth=2, best_move=best_move
            )
            state = ff.wasnt_best_move(
                state, evaluated_moves, depth=3, best_move=best_move
            )
            state = ff.better_material_gain(state, board, best_move)

            if state:  # then all conditions are met and the move is noteworthy
                print(f"Move found {best_move}")
                node_output = self.get_output(headers, board, move.uci(), evaluated_moves[(depth - 1) * 2], evaluated_moves[(depth - 1) * 2 + 1])
                positions.append(node_output)
                pass

            board.push(move)
        return positions


def entrypoint(
    input_path="test_pgn.pgn",
    output_path="out.test",
    h="minimal",
    cp=50,  # this arg should probably be placed with filters only
    d=10,
    cpu_cores=2,
    **kwargs,
):

    print(input_path, output_path, h, cp, d, cpu_cores)  # Show selected params
    solver = Solver(h, cp, d, cpu_cores, **kwargs)

    with open(input_path, "r") as input_, open(output_path, "w") as output:
        game = pgn.read_game(input_)
        # while game:
        start = time()
  
        positions = solver.handle_game(game)
        for p in positions:
            output.write("\n[FEN '{}'] \n".format(p[0]))
            to_print = "{}. {} {{{}}}{} ".format(p[1][0], p[1][1], p[1][2], "{{G}}" if p[1][3] else "")
            for k in p[2]:
                to_print += "({}. {} {{{}}}{}) ".format(k[0], k[1], k[2], "{{G}}" if k[3] else "")
            print("[FEN {}]".format(p[0]) + "\n" + to_print)
            output.write(to_print)

        print(time() - start)


if __name__ == "__main__":
    fire.Fire(entrypoint)
