# turing
An implementation of a Turing machine and finite state automaton in Py3, stdlib only.

## Usage

Declare a tape:

`Tape(alphabet, size, initial_data)`

Generate an FSA from a JSON file, set the initial state and compute over a tape.
```
fsm_from_json(file, encoding)
<FSA instance>.set_state(<string name of state>)
<FSA instance>.compute(<tape>)
```

JSON files take the following format:
```
{
    state_name:
        [
        [transition input, output, tape movement (-1, 0, or 1), new FSA state],
        ...
        ],
    ...
}
```
