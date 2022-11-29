from hashlib import new
from re import L
import re
from pyomo.environ import SolverFactory, value
from mycroft import MycroftSkill, intent_handler
from dataclasses import dataclass, asdict
import json
import numpy as np
import os
from typing import List, Dict, Tuple

from .pareto_front_finder.nrp import NrpModel
from .pareto_front_finder.main import RunResult, run


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

    def _load_result_from_file(self) -> RunResult:
        with open(self.NRP_RES_FILE_PATH, 'r') as f:
            data = f.read()
        data_dict = json.loads(data)
        return RunResult(**data_dict)

    def get_next_req_idx(self) -> List[str]:
        result = self._load_result_from_file()
        req_indexes_with_none = filter(
            lambda t: t[1] == '1', enumerate(result.x)
        )
        indexes: List[str] = list(
            map(lambda t: str(t[0]), req_indexes_with_none)
        )
        return indexes

    def get_stakeholder_satisfied_idx(self) -> List[str]:
        result = self._load_result_from_file()
        stakeholder_indexes_with_none = filter(
            lambda t: t[1] == '1', enumerate(result.y)
        )
        indexes: List[str] = list(
            map(lambda t: str(t[0]), stakeholder_indexes_with_none)
        )
        return indexes

    def delete_internal_state(self):
        try:
            os.remove(self.NRP_RES_FILE_PATH)
        except OSError:
            pass

    def get_cost(self) -> float:
        result = self._load_result_from_file()
        return result.cost


class LinearSolver(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.model_handler = ModelHandler()

    @intent_handler('next_req.intent')
    def handle_next_req(self):
        req_index_all = self.model_handler.get_next_req_idx()
        req_index_short = req_index_all[:2]
        indexes = ','.join(req_index_short)
        self.speak(f'The next requirements to implement are {indexes}')

    @intent_handler('test.intent')
    def handle_smoke_intent(self, message):
        tomato_type = message.data.get('type')
        if tomato_type:
            self.speak(tomato_type)
        else:
            self.speal('Type not found')

    @intent_handler('stakeholder_satisfaction.intent')
    def handle_stakeholder_satisfaction_intent(self, message):
        idxs_all = self.model_handler.get_stakeholder_satisfied_idx()
        idxs_short = idxs_all[:2]
        idxs_str = ','.join(idxs_short)
        self.speak(f'Stakeholder satisfied are {idxs_str}')

    @intent_handler('delete_state.intent')
    def handle_delete_intent(self, message):
        self.model_handler.delete_internal_state()
        self.speak('Internal state deleted')

    @intent_handler('cost.intent')
    def handle_cost_intent(self, message):
        cost = self.model_handler.get_cost()
        self.speak(f'The cost will be {cost} dollares')

    @intent_handler('solver.linear.intent')
    def handle_solver_linear(self, message):
        profit = self.model_handler.run_store_get_profit()
        self.speak(f'Your profit will be {profit}')


def create_skill():
    return LinearSolver()
