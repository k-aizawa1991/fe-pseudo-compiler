import argparse
import json
from pathlib import Path
from src.interpreter import Interpreter


class InterpreterManager:
    def __init__(self):
        self.interpreter = Interpreter()
        self.file_lines = None

    def read_file(self, file: str):
        filepath = Path(file)
        if not filepath.exists():
            print("指定されたパスは存在しません。")
            return
        with open(filepath) as f:
            self.file_lines = f.readlines()

    def compile_lines(self):
        self.interpreter.interpret_main_process(self.file_lines)

    def read_and_compile(self, file: str):
        self.read_file(file)
        self.compile_lines()

    def execute_code(self):
        self.interpreter.execute_lts()

    def execute_line(self):
        if self.interpreter.is_ended():
            self.interpreter.init_execution()
        self.interpreter.execute_line()

    def show_current(self):
        if len(self.interpreter.calling_stack) > 0:
            func_name, state = self.interpreter.calling_stack[-1]
            print("呼び出し関数：", self.interpreter.calling_stack)
            print("実行関数：", func_name)
            print("状態：", state)
        else:
            print("実行中ではありません")

    def show_all_func_names(self):
        print(list(self.interpreter.func_lts_map.keys()))

    def show_func(self, func_name: str):
        if func_name not in self.interpreter.func_lts_map:
            print("入力された名前の関数存在しません")
            return
        else:
            lts = self.interpreter.func_lts_map[func_name]
        print("LTS:")
        print(lts)
        print("実行中引数：", lts.name_val_map)

    def save_execution(self, target: str = "execution_info.json"):
        target_path = Path(target)
        target_data = self.interpreter.get_execution_dict()
        with open(target_path, "w") as f:
            json.dump(target_data, f, indent=4, ensure_ascii=False)

    def load_execution(self, source: str = "execution_info.json"):
        source_path = Path(source)
        with open(source_path) as f:
            self.interpreter.set_lts_dict(json.load(f))

    def interactive_mode(self):
        command = ""
        while command != "E":
            print(
                "キーを入力してください: F: ファイルをコンパイルする / C:現在の状態を表示する / S: 現在の状態を保存する / R:保存されている状態を読み込む / N:次の状態に進む / A:全処理を実行する / E:終了"
            )
            command = input()
            if command == "F":
                print("ファイルパスを入力してください。")
                file_path = input()
                self.read_and_compile(file_path)
            elif command == "C":
                self.show_current()
                command = print("D:詳細 / E:表示終了")
                command = input()
                if command == "D":
                    print("関数名一覧：")
                    self.show_all_func_names()
                    print("表示する関数を入力（終了する場合はE）：")
                    func_name = input()
                    while func_name != "E":
                        self.show_func(func_name)
                        print("表示する関数を入力（終了する場合はE）：")
                        func_name = input()
                    command = ""
            elif command == "S":
                print("保存先のファイルパスを入力してください。（未入力の場合はexecution_info.json）")
                target = input()
                if len(target) == 0:
                    target = "execution_info.json"
                self.save_execution(target)
            elif command == "R":
                print("保存先のファイルパスを入力してください。（未入力の場合はexecution_info.json）")
                target = input()
                if len(target) == 0:
                    target = "execution_info.json"
                self.load_execution(target)
            elif command == "N":
                self.execute_line()
                self.save_execution()
            elif command == "A":
                self.execute_code()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--command",
        help="コマンドの種別",
        choices=["execute_file", "execute_line", "interactive"],
    )
    parser.add_argument(
        "--source_code",
        help="ソースコードのパス",
        type=str,
        required=False,
        default="source.txt",
    )

    args = parser.parse_args()
    manager = InterpreterManager()
    if args.command == "execute_file":
        manager.read_and_compile(args.source_code)
        manager.execute_code()
    elif args.command == "execute_line":
        manager.load_lts(args.source_lts)
    elif args.command == "interactive":
        manager.interactive_mode()
    else:
        parser.print_help()
