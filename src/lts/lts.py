from typing import Dict, Set, Tuple

from src import exception


class LabeledTransitionSystem:
    def __init__(self, init_state_name: str = None):
        if init_state_name is None:
            init_state_name = "S0"
        init_state = init_state_name
        self.labels: Set[str] = set()
        self.transitions: Dict[str, Dict[str, str]] = {init_state: {}}
        self.backwards: Dict[str, Set[Tuple[str, str]]] = {init_state: set()}
        self.init_state = init_state

    def get_init_state(self):
        return self.init_state

    def create_state(self, name: str = None):
        if name is None:
            num = len(self.transitions)
            while f"S{num}" in self.transitions:
                num += 1
            name = f"S{num}"
        self.transitions[name] = {}
        self.backwards[name] = set()
        return name

    def add_transition(self, source: str, label: str, target: str):
        if source not in self.transitions:
            raise exception.DoesNotExistException(source)
        self.labels.add(label)
        if target not in self.transitions:
            self.transitions[target] = {}
            self.backwards[target] = set()

        self.transitions[source][label] = target
        self.backwards[target].add((label, source))

    def clear_transition(self, source: str):
        if source not in self.transitions:
            raise exception.DoesNotExistException(source)
        for label in self.transitions[source]:
            target = self.transitions[source][label]
            self.backwards[target].remove((label, source))
        self.transitions[source] = {}

    def get_transition_state(self, source: str, label: str):
        if source not in self.transitions:
            raise exception.DoesNotExistException(source)
        if label not in self.transitions[source]:
            raise exception.DoesNotExistException(f"{source}から{label}による遷移")
        return self.transitions[source][label]

    def get_backwards(self, target:str):
        if target not in self.backwards:
            raise exception.DoesNotExistException(target)
        return self.backwards[target]

    def get_transition_label(self, state:str, index=0):
        if state not in self.transitions:
            raise exception.DoesNotExistException(state)
        # 存在しないインデックスへのアクセスはNoneを返却する
        if not index < len(self.transitions[state]):
            return None
        # WARNING: keysの順序は本来不定なのでif文のように順序付きを扱うのは不適？
        key = list(self.transitions[state].keys())[index]
        return key

    def __str__(self):
        lts_str = ""
        for state in self.transitions:
            lts_str += f"{str(state)} \n"
            for transition in self.transitions[state]:
                lts_str += f"  {str(transition)}-> {str(self.transitions[state][transition])} \n"
        return lts_str
