from hashlib import new
from mycroft import MycroftSkill, intent_handler
from dataclasses import dataclass, asdict
import json
import numpy as np
import os
from typing import List, Dict


# Given a model of maximize profit in a factory.
# The factory produces cars and trucks
# The profit formula is f(x1,x2) = 10 * x1 + 20 * x2
# Given the cost constraint
# 2 * x1 + 5 * x2 <= 20
# x2 >= 1

# This model has an optimun point on (7.5, 1)


@dataclass
class ModelState():
    fo: float
    constraint: List[float]
    decision_var: List[float]
    slacks: List[float]


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
        return 95

    def _get_slack_map(self):
        return {
            0: 'costs',
            1: 'production of cars',
        }

    def get_slack_text(self) -> str:
        text = 'The slack values are'
        state = self.load_state()
        slacks = state.slacks
        slack_map = self._get_slack_map()

        for i, value in slack_map.items():
            text += f'{value} has slack of {slacks[i]}'
        return text

    def change_constraint(self, constraint, value) -> str:
        constraint_map = self._get_slack_map()
        index, _ = next(
            filter(lambda item: item[1] == constraint, constraint_map.items()))

        state = self.load_state()
        with open('/dev/shm/debug.txt', 'a') as f:
            f.write(f'El vector es: {state.constraint}\n')
            f.write(f'El tipo es: {type(state.constraint)}\n')
            f.write(f'El index es: {state.constraint[index]}\n')
            state.constraint[index] += int(value)
        new_value = state.constraint[index]

        # TODO: solve model with new constraint

        self.save_state(state)
        return f'Constraint {constraint} updated to {new_value}'

    def move_constraint(self, new_constraint: np.array) -> float:
        return 100.0

    def _get_state_rep(self) -> ModelState:
        return ModelState(
            fo=95,
            constraint=[20, 1],
            decision_var=[7.5, 1],
            slacks=[0, 0],
        )

    def save_state(self, state: ModelState = None):
        state = state or self._get_state_rep()
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

    @intent_handler('change_constraint.intent')
    def handle_change_constraint(self, message):
        constraint = message.data.get('constraint')
        value = message.data.get('value')
        text = self.model.change_constraint(constraint, value)
        self.speak(text)

    @intent_handler('slack.intent')
    def handle_say_slack(self, message):
        text = self.model.get_slack_text()
        self.speak(text)

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
