class PatternException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class NamePatternException(PatternException):
    def __str__(self):
        return f"[{self.arg}]は名前に利用できません。各種名前は英字で開始し、英数字のみが利用できます。"


class NameNotDefinedException(PatternException):
    def __str__(self):
        return f"[{self.arg}]は変数として定義されていません。"


class DeclareException(PatternException):
    def __str__(self):
        return f"宣言の記述が不正です：{self.arg}"


class InvalidFormulaException(PatternException):
    def __str__(self):
        return f"式が不正です：{self.arg}"


class InvalidParenthesisException(PatternException):
    def __str__(self):
        return f'"("に対応する")"が存在しません。:{self.args}'
