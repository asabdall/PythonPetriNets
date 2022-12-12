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
        self.status = str(np.transpose(state))

    def __str__(self, level=0):  # defining the printout of the class
        ret = "\t" * level + str(level) + " Fire: " + self.status + "\n"
        for children in self.child_branches:
            if children=='Not Fired':
                ret += "\t"*(level+1)+str(level+1) + " Fire: "+ 'Not Fired' + "\n"
            else:
                ret += children.__str__(level + 1)
        return ret

    def __repr__(self):
        return self.state

    def calculate_incident_matrix(self):
        self.incident_matrix = np.subtract(self.output_incident_matrix, self.input_incident_matrix)

    def calculate_transition_count(self):
        self.transitions = len(self.output_incident_matrix[0])

    def check_duplicate(self):
        if np.size(self.previous_states) == 0:
            return
        for i in range(0, (int)((np.size(self.previous_states) / self.transitions) - 1)):
            if np.equal(self.state, np.delete(np.insert(np.zeros((12, 1), dtype=int), 0,
                                                        self.previous_states[:, i], axis=1), 1, axis=1)).all():
                self.status = str(np.transpose(self.state))+'Duplicate'

    def find_transition_states(self):
        times_fired = 0
        if 'Duplicate' in self.status :
            self.child_branches = np.array([])
            return
        for i in range(0, self.transitions):
            firing_input = np.delete(np.insert(np.zeros((12, 1), dtype=int), 0,
                                               self.input_incident_matrix[:, i], axis=1), 1, axis=1)
            if np.greater_equal(self.state, firing_input).all():
                token_move = np.delete(np.insert(np.zeros((12, 1), dtype=int), 0,
                                                 self.incident_matrix[:, i], axis=1), 1, axis=1)
                self.child_branches = np.append(self.child_branches,
                                                CoverabilityTree(self.input_incident_matrix,
                                                                 self.output_incident_matrix,
                                                                 self.state + token_move))

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
            self.status =str(np.transpose(self.state))+'Terminal Node'
            self.child_branches = np.array([])


def create_coverability_tree(initial_node):
    if initial_node is None:
        return
    if initial_node == 'Not Fired':
        return
    initial_node.calculate_incident_matrix()
    initial_node.calculate_transition_count()
    initial_node.check_duplicate()
    initial_node.find_transition_states()
    if np.size(initial_node.child_branches) == 0:
        return
    for children in initial_node.child_branches:
        create_coverability_tree(children)


p1_i = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
p2_i = np.array([0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
p3_i = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
p4_i = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
p5_i = np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
p6_i = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
p7_i = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
p8_i = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0])
p9_i = np.array([0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0])
p10_i = np.array([1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0])
p11_i = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1])
p12_i = np.array([0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
p1_o = np.array([0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
p2_o = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
p3_o = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
p4_o = np.array([0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0])
p5_o = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
p6_o = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0])
p7_o = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1])
p8_o = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
p9_o = np.array([1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
p10_o = np.array([0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0])
p11_o = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0])
p12_o = np.array([0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0])
input_incident_matrix = np.array([p1_i, p2_i, p3_i, p4_i, p5_i, p6_i, p7_i, p8_i, p9_i, p10_i, p11_i, p12_i])
output_incident_matrix = np.array([p1_o, p2_o, p3_o, p4_o, p5_o, p6_o, p7_o, p8_o, p9_o, p10_o, p11_o, p12_o])
initial_state = np.array([[0], [1], [0], [0], [1], [0], [0], [0], [0], [0], [1], [1]])
cat_mouse_coverability_tree = CoverabilityTree(input_incident_matrix, output_incident_matrix, initial_state)
create_coverability_tree(cat_mouse_coverability_tree)
print(cat_mouse_coverability_tree)
