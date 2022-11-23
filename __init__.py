from hashlib import new
from pyomo.environ import SolverFactory, value
from mycroft import MycroftSkill, intent_handler
from dataclasses import dataclass, asdict
import json
import numpy as np
import os
from typing import List, Dict, Tuple

from .pareto_front_finder.nrp import NrpModel
from .pareto_front_finder.main import run


class ModelHandler():
    NRP_RES_FILE_PATH = '/dev/shm/nrp_state.json'

    def run_store_get_profit(self) -> float:
        model = NrpModel(
            '/opt/mycroft/skills/linear-solver-skill/pareto_front_finder/nrp_100c_140r.dat')
        solver = SolverFactory('cbc')
        res = run(model.model, solver, 0)
        with open(self.NRP_RES_FILE_PATH, 'w') as f:
            json.dump(asdict(res), f)

        return res.profit


class LinearSolver(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.model_handler = ModelHandler()

    def handle_change_constraint(self):
        raise NotImplementedError()

    def handle_say_slack(self):
        raise NotImplementedError()

    def handle_delete_state(self):
        self.model.delete_state()
        self.speak('Internal state deleted')

    def handle_init(self):
        profit = self.model_handler.run_store_get_profit()
        self.speak(f'Your profit will be {profit}')

    @intent_handler('next_req.intent')
    def handle_next_req(self):
        req_index = self.model.get_next_req_idx()
        self.speak(f'The next requirement to implement are {req_index}')

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

        if message_utt == 'next release problem':
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
