from mycroft import MycroftSkill, intent_handler
from dataclasses import dataclass
import json
import numpy as np
from typing import List


@dataclass
class ModelState():
    fo: float
    constraint: List[float]
    decision_var: List[float]


class Model():
    dimensions = 3
    FILE_PATH = '/dev/shm/state.json'

    def __init__(self):
        self.vars = np.array(3 * [0])
        self.constraints_bounds = np.array(3 * [0])

    def actual_constrains_values(self) -> np.array:
        return self.constraints_bounds

    def solve(self) -> float:
        return 50.0

    def move_constraint(self, new_constraint: np.array) -> float:
        return 100.0

    def _get_state_rep(self) -> ModelState:
        return ModelState(
            fo=10.0,
            constraint=[2.0, 3.0],
            decision_var=[1.5]
        )

    def save_state(self):
        state = self._get_state_rep()
        with open(self.FILE_PATH, 'w') as f:
            f.write(json.dumps(dict(state)))

    def load_state(self) -> ModelState:
        with open(self.FILE_PATH, 'r') as f:
            state_str = f.read()
        state_dict = json.loads(state_str)
        return ModelState(**state_dict)


# hacer un bucle que pasa si donde se hagan cambios sobre el modelo resuelto
# feateure
#   preguntar solucion
#   que pasa si c1 cambia a tal valor
#   que pasa si b1 cambia a tal valor
#   cual es el rango de variacion de x parametro
# utilizar un diccionaro para leer la solucion en un lenguaje mas nautural?


def solve_model() -> str:
    # Supose a model minimize cost
    # given 3 restrictions
    m = Model()
    m.save_state()
    of_value = m.solve()
    constraints = m.actual_constrains_values()

    return f"""Your benefit will be {of_value} dollars
    given that you cannot spend more than {constraints[0]} dollars and
    cannot spend more than {constraints[1]} days
    """


class LinearSolver(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('solver.linear.intent')
    def handle_solver_linear(self, message):
        print(message)
        with open('/dev/shm/a.txt', 'w') as f:
            f.write(str(message))
            f.write(str(dir(message)))
            f.write(str(type(message)))

        if message == 'release planning problem':
            self.speak(solve_model())
        else:
            self.speak('Skill in progress')
        # self.speak_dialog('solver.linear')


def create_skill():
    return LinearSolver()
