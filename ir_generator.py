import json

class IRGenerator:
    def __init__(self):
        self.ir = {}

    def generate(self, node):
        node.accept(self)
        return self.ir

    def visit_ProgramNode(self, node):
        self.ir['model'] = None
        self.ir['inputs'] = []
        self.ir['features'] = []
        self.ir['threshold'] = 0.0
        self.ir['condition'] = {}
        
        node.model.accept(self)
        node.inputs.accept(self)
        node.features.accept(self)
        node.train.accept(self)
        node.condition.accept(self)

    def visit_ModelNode(self, node):
        self.ir['model'] = node.name

    def visit_InputNode(self, node):
        self.ir['inputs'] = node.inputs

    def visit_FeatureNode(self, node):
        self.ir['features'] = node.features

    def visit_TrainNode(self, node):
        self.ir['threshold'] = node.threshold

    def visit_ConditionNode(self, node):
        self.ir['condition']['variable'] = node.condition_var
        self.ir['condition']['operator'] = node.operator
        self.ir['condition']['then'] = self.process_action(node.then_action)
        self.ir['condition']['else'] = self.process_action(node.else_action)
    
    def process_action(self, node):
        return {
            'type': node.action_type,
            'message': node.message
        }

    def to_json(self):
        return json.dumps(self.ir, indent=2)
