BLANK = u"\u25A1"

from collections import namedtuple
import json

class Tape:
    def __init__(self, alphabet: str, size: int, init_data: str = None):
        self.alphabet = set(alphabet + BLANK)
        self.size = size
        if init_data is None:
            self.data = [BLANK for x in range(size)]
        else:
            assert len(init_data) <= size and set(init_data).issubset(self.alphabet)
            self.data = list(init_data) + [BLANK for x in range(size - len(init_data))]
        self.head = 0
        
    def write(self, char):
        if not (char in self.alphabet):
            raise ValueError
        self.data[self.head] = char

    read = lambda self: self.data[self.head]
    display = lambda self: "".join(self.data) + "\n"

    def move_head(self, magnitude):
        if not(magnitude in {-1, 0, 1}):
            raise ValueError
        new_pos = self.head + magnitude
        if not(new_pos in range(0, self.size + 1)):
            raise ValueError
        else:
            self.head = new_pos
            return True

    def set_head(self, pos):
        if not(pos in range(0, self.size + 1)):
            raise IndexError
        self.head = pos
        return True
    
Transition = namedtuple("Transition", ["inp", "out", "mv", "state"])

class State:
    def __init__(self, name, transitions: set):
        self.name = name
        self.transitions = set()
        for t in transitions:
            assert type(t) is Transition
            self.add_transition(t)
        
    def add_transition(self, transition):
        assert transition.mv in {-1, 0, 1}
        self.transitions.add(transition)


class FSM:
    def __init__(self):
        self.states = dict()
        self.current_state = None

    def add_state(self, state): self.states[state.name] = state
    
    def set_state(self, state: str):
        if not (state in self.states.keys()):
            return False
        else:
            self.current_state = self.states[state]

    def compute(self, tape: Tape):
        while self.current_state != None:
            char = tape.read()
            for transition in self.current_state.transitions:
                if char == transition.inp:
                    try:
                        tape.write(transition.out)
                    except ValueError:
                        print("Computation halted, invalid char written to tape")
                        tape.display()
                        break
                    print("δ({0}, {1}) ↦ ({2.out}, {2.mv:>2}, {2.state})  |  {3}".format(self.current_state.name, char, \
                                                            transition, tape.display()), end="")
                    try:
                        tape.move_head(transition.mv)
                    except IndexError:
                        print("Tape head moved off of tape")
                        tape.display()
                        break
                    
                    try:
                        self.set_state(transition.state)
                    except KeyError:
                        print("Computation failed in state transition from", self.current_state)
                        tape.display()
                        break
                    break
            else:
                self.current_state = None
                print("Computation terminated |  {}".format(tape.display()))
        tape.display()
        

    


def fsm_from_json(f, enc):
    F = FSM()
    for state_name, transitions in json.load(open(f, "r", encoding=enc)).items():
        F.add_state(State(state_name, set(Transition(*t) for t in transitions)))
    return F
