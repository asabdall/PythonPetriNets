import numpy as np


class CoverabilityTree(object):
    def __init__(self, place_to_transitions, transitions_to_place, state):
        self.input_incident_matrix = place_to_transitions
        self.output_incident_matrix = transitions_to_place
        self.state = state
        self.incident_matrix = 0
        self.previous_states = np.array([])
        self.child_branches = np.array([])
        self.transitions = 0
        self.places = 0
        self.status = str(np.transpose(state))

    def __str__(self, level=0):  # defining the printout of the class
        ret = "\t" * level + str(level) + " Fire: " + str.replace(self.status, '-3', 'w') + "\n"
        for children in self.child_branches:
            if children == 'Not Fired':
                ret += "\t" * (level + 1) + str(level + 1) + " Fire: " + 'Not Fired' + "\n"
            else:
                ret += children.__str__(level + 1)
        return ret

    def __repr__(self):
        return self.state

    def calculate_incident_matrix(self):
        self.incident_matrix = np.subtract(self.output_incident_matrix, self.input_incident_matrix)

    def calculate_transition_count(self):
        self.transitions = len(self.output_incident_matrix[0])

    def calculate_place_count(self):
        self.places = int(np.size(self.output_incident_matrix) / self.transitions)

    def check_duplicate(self):
        if np.size(self.previous_states) == 0:
            return
        for i in range(0,int((np.size(self.previous_states) / self.places))):
            if np.equal(self.state, np.delete(np.insert(np.zeros((self.places, 1), dtype=int), 0,
                                                        self.previous_states[:, i], axis=1), 1, axis=1)).all():
                if 'Duplicate' not in self.status:
                    self.status = self.status + 'Duplicate'

    def check_dominance(self):
        if np.size(self.previous_states) == 0:
            return
        state_count = int((np.size(self.previous_states) / self.places) - 1)
        for i in range(0, state_count):
            previous_state = np.delete(np.insert(np.zeros((self.places, 1), dtype=int), 0,
                                                 self.previous_states[:, i], axis=1), 1, axis=1)
            dominance = np.zeros(np.size(self.state))
            for j in range(0, np.size(self.state)):
                if self.state[j] == -3:
                    dominance[j] = True
                elif self.state[j] >= previous_state[j]:
                    dominance[j] = True
                else:
                    dominance[j] = False
            if dominance.all():
                for g in range(0, np.size(self.state)):
                    if self.state[g] > previous_state[g]:
                        self.state[g] = -3
                        self.status = str(np.transpose(self.state))

    def transition_fire(self, fire):
        dominant_places = np.zeros(np.size(self.state))
        for j in range(0, np.size(self.state)):
            if self.state[j] == -3:
                dominant_places[j] = True
            elif self.state[j] >= fire[j]:
                dominant_places[j] = True
            else:
                dominant_places[j] = False
        return dominant_places.all()

    def new_state(self, tokens):
        child = np.zeros((np.size(self.state), 1), dtype=int)
        for j in range(0, np.size(self.state)):
            if self.state[j] == -3:
                child[j] = -3
            else:
                child[j] = self.state[j] + tokens[j]
        return child

    def find_transition_states(self):
        times_fired = 0
        if 'Duplicate' in self.status:
            self.child_branches = np.array([])
            return
        for i in range(0, self.transitions):
            firing_input = np.delete(np.insert(np.zeros((self.places, 1), dtype=int), 0,
                                               self.input_incident_matrix[:, i], axis=1), 1, axis=1)
            if self.transition_fire(firing_input):
                token_move = np.delete(np.insert(np.zeros((self.places, 1), dtype=int), 0,
                                                 self.incident_matrix[:, i], axis=1), 1, axis=1)
                self.child_branches = np.append(self.child_branches,
                                                CoverabilityTree(self.input_incident_matrix,
                                                                 self.output_incident_matrix,
                                                                 self.new_state(token_move)))

                if np.size(self.previous_states) == 0:
                    self.child_branches[i].previous_states = self.state
                else:
                    self.child_branches[i].previous_states = np.concatenate([self.previous_states, self.state], axis=1)
                times_fired = times_fired + 1
            else:
                if np.size(self.child_branches) == 0:
                    self.child_branches = np.array(['Not Fired'])
                else:
                    self.child_branches = np.concatenate([self.child_branches, ['Not Fired']])
        if times_fired == 0:
            self.status = str(np.transpose(self.state)) + 'Terminal Node'
            self.child_branches = np.array([])


def create_coverability_tree(initial_node):
    if initial_node is None:
        return
    if initial_node == 'Not Fired':
        return
    initial_node.calculate_incident_matrix()
    initial_node.calculate_transition_count()
    initial_node.calculate_place_count()
    initial_node.check_dominance()
    initial_node.check_duplicate()
    initial_node.find_transition_states()
    if np.size(initial_node.child_branches) == 0:
        return
    for children in initial_node.child_branches:
        create_coverability_tree(children)


p1_i = np.array([1, 0, 0])
p2_i = np.array([1, 0, 0])
p3_i = np.array([0, 1, 0])
p4_i = np.array([0, 0, 1])
p1_o = np.array([0, 1, 0])
p2_o = np.array([0, 1, 1])
p3_o = np.array([1, 0, 0])
p4_o = np.array([0, 1, 0])
input_incident_matrix = np.array([p1_i, p2_i, p3_i, p4_i])
output_incident_matrix = np.array([p1_o, p2_o, p3_o, p4_o])
initial_state = np.array([[1], [1], [0], [0]])
cat_mouse_coverability_tree = CoverabilityTree(input_incident_matrix, output_incident_matrix, initial_state)
create_coverability_tree(cat_mouse_coverability_tree)
print(cat_mouse_coverability_tree)
