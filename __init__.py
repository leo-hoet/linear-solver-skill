from mycroft import MycroftSkill, intent_file_handler


class LinearSolver(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('solver.linear.intent')
    def handle_solver_linear(self, message):
        self.speak_dialog('solver.linear')


def create_skill():
    return LinearSolver()

