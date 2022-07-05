from mycroft import MycroftSkill, intent_handler
from dataclasses import dataclass, asdict
import json
import numpy as np
import os
from typing import List, Dict


@dataclass
class ModelState():
    fo: float
    constraint: List[float]
    decision_var: List[float]


class Model():
    dimensions = 3
    FILE_PATH = '/dev/shm/state.json'

    def __init__(self):
        self.vars = np.array(2 * [0])
        self.constraints_bounds = np.array(3 * [0])

    def _variables_pos_to_meaning_map(self) -> Dict[int, str]:
        return {
            0: 'Cars',
            1: 'Trucks',
        }

    def _get_decision_vars(self) -> List[float]:
        state = self.load_state()
        return state.decision_var

    def decisions_vars_text(self) -> str:
        map_data = self._variables_pos_to_meaning_map()
        decision_vars = self._get_decision_vars()

        text = 'The variable values are '

        for i, value in enumerate(decision_vars):
            text += f'{value} {map_data[i]} '

        return text

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
            decision_var=[1.5, 3.5]
        )

    def save_state(self):
        state = self._get_state_rep()
        with open(self.FILE_PATH, 'w') as f:
            f.write(json.dumps(asdict(state)))

    def load_state(self) -> ModelState:
        with open(self.FILE_PATH, 'r') as f:
            state_str = f.read()
        state_dict = json.loads(state_str)
        return ModelState(**state_dict)

    def delete_state(self):
        try:
            os.remove(self.FILE_PATH)
        except OSError:
            pass


# hacer un bucle que pasa si donde se hagan cambios sobre el modelo resuelto
# feateure
#   preguntar solucion
#   que pasa si c1 cambia a tal valor
#   que pasa si b1 cambia a tal valor
#   cual es el rango de variacion de x parametro
# utilizar un diccionaro para leer la solucion en un lenguaje mas nautural?


class LinearSolver(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.model = Model()

    def handle_change_constraint(self):
        raise NotImplementedError()

    def handle_say_slack(self):
        raise NotImplementedError()
        self.model.get_slacks()

    def handle_delete_state(self):
        self.model.delete_state()
        self.speak('Internal state deleted')

    def handle_init(self):
        self.model.delete_state()
        fitness = self.model.solve()
        self.model.save_state()
        self.speak(f'Your benefit will be {fitness} monetary units')

    @intent_handler('variables.intent')
    def handle_say_variables(self, message):
        text = self.model.decisions_vars_text()
        self.speak(text)

    @intent_handler('test.intent')
    def handle_test_intent(self, message):
        tomato_type = message.data.get('type')
        if tomato_type:
            self.speak(tomato_type)
        else:
            self.speal('Type not found')

    @intent_handler('solver.linear.intent')
    def handle_solver_linear(self, message):
        message_utt = message.data.get('utterance', None)

        if message_utt == 'release planning problem':
            self.handle_init()
            return
        elif message_utt == 'delete state':
            self.handle_delete_state()
            return
        elif message_utt == 'variable values of saved model':
            with open('/dev/shm/vartext.txt', 'a') as f:
                f.write('Entro aca antes del hadnlesay \n')
            variable_str = self.handle_say_variables()
            with open('/dev/shm/vartext.txt', 'a') as f:
                f.write(variable_str)
            self.speak(variable_str)
            return

        # self.speak(solve_model())
        # self.speak_dialog('solver.linear')


def create_skill():
    return LinearSolver()
