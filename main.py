from time import time

import fire
import filters as ff
from chess import engine as chess_engine, pgn, Move

from uci_http_client import UCIHttpClient

#python3 -m pipenv run main.py --depth=4


class Solver:
    CONCISE_HEADERS = {"White", "Black", "Site", "Date"}

    def __init__(self, h, cp, depth, alt, cpu_cores, **kwargs):
        self.h = h
        # self.cpu_cores = cpu_cores
        self.cp = cp
        self.depth = depth
        # self.limit = chess_engine.Limit(depth=depth)
        self.alternatives = alt
        self.engine = UCIHttpClient(alt, cpu_cores)

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

    def get_comment(self, move, real_move_uci):
        cp = move["cp"]
        was_played = move["cp"] == real_move_uci
        if was_played:
            return f"{cp} G"
        return cp

    def get_output(self, headers, board, real_move_uci, moves):
        output_headers = {"FEN": board.fen(), **headers}
        game = pgn.Game(headers=output_headers)

        best_move = moves[0]
        game.add_main_variation(Move.from_uci(best_move["pv"]), comment=self.get_comment(best_move, real_move_uci))

        for move in moves[1:]:
            game.add_variation(Move.from_uci(move["pv"]), comment=self.get_comment(move, real_move_uci))
        return str(game)

    def handle_game(self, game):
        positions = []
        board = game.board()
        headers = self.get_desired_headers(game.headers)

        for move in game.mainline_moves():
            print(move)
            evaluated_moves = self.engine.analyse(board.fen(), self.depth)

            depth = self.depth
            if depth not in evaluated_moves:
                print("moves for selected depth were not generated")
                board.push(move)
                continue

            evaluated_deep = evaluated_moves[depth]
            best_move = evaluated_deep[0]["pv"]

            if all([
                ff.not_a_starting_move(board, n_ignore=8),
                ff.not_check(board, best_move=best_move),
                ff.better_than_second(evaluated_deep, min_diff=self.cp),
                ff.not_strong_in_given_depth(evaluated_moves, depth=4, best_move=best_move),
                ff.is_not_best_material_gain(board, best_move)
            ]):
                print(f"Move found {best_move}")
                node_output = self.get_output(headers, board, move.uci(), evaluated_deep)
                positions.append(node_output)

            board.push(move)
        return positions


def entrypoint(
        input_path="test_pgn.pgn",
        output_path="out.test",
        h="minimal",
        cp=50,  # this arg should probably be placed with filters only
        depth=7,
        alt=3,
        cpu_cores=2,
        **kwargs
):
    print(input_path, output_path, h, cp, depth, alt, cpu_cores)  # Show selected params
    solver = Solver(h, cp, depth, alt, cpu_cores, **kwargs)

    with open(input_path, "r") as input_, open(output_path, "w") as output:
        start = time()

        while True:
            game = pgn.read_game(input_)
            if game is None:
                break
            for p in solver.handle_game(game):
                output.write(str(p))
                output.write("\n\n")

        print(time() - start)


if __name__ == "__main__":
    fire.Fire(entrypoint)
