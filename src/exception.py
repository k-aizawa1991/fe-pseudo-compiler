class PatternException(Exception):
    message = ""

    def __init__(self, arg="", line_num=None):
        self.arg = arg
        self.line_num = line_num

    def __str__(self):
        line = f"{self.line_num+1}行目:" if self.line_num is not None else ""
        return f"{line}{self.message}"


class FuncStartPatternException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.mesage = (
            f'[{self.arg}]は関数ではありません。関数は"◯"から開始してください。'
        )


class FuncNameException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"[{self.arg}]は関数に利用できません。"


class InvalidFuncDeclareException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"{self.arg}の関数定義が正しくありません。"


class FuncArgNotFoundException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"[{self.arg}]に関数の引数が見つかりません。"


class InvalidFuncCallException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "関数の呼び出しが正しくありません。"


class NamePatternException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"[{self.arg}]は名前に利用できません。各種名前は英字で開始し、英数字のみが利用できます。"


class NameNotDefinedException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"[{self.arg}]は変数として定義されていません。"


class DeclareException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"宣言の記述が不正です：{self.arg}"


class InvalidFormulaException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"式が不正です：{self.arg}"


class InvalidParenthesisException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f'"("に対応する")"が存在しません。:{self.arg}'


class InvalidSquareBracketException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = '"["に対応する"]"が存在しません。'


class InvalidCurlyBracketException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = '"{"に対応する"}"が存在しません。'


class InvalidArrayException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"{self.arg}は配列ではありません。"


class InvalidArrayIndexException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = f"{self.arg}の配列外にアクセスしています。"


class InvalidIfBlockException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "if文が正しく終了しませんでした。"


class InvalidWhileBlockException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "while文が正しく終了しませんでした。"


class InvalidDoWhileBlockException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "do while文が正しく終了しませんでした。"


class InvalidForBlockException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "for文が正しく終了しませんでした。"


class InvalidForSentenceException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "for文の繰り返しの定義が正しくありません。"


class InvalidArrayAppendException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "配列への値の追加文が正しくありません。"


class InvalidIndentException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "インデントに誤りがあります。"


class InvalidVarAssignException(PatternException):
    def __init__(self, arg="", line_num=None):
        super().__init__(arg, line_num)
        self.message = "代入文が正しくありません。"


class LtsException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class DoesNotExistException(LtsException):
    def __str__(self):
        return f"{self.arg}はLTSに存在しません。"
