class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.symbol_table = {
            'inputs': [],
            'features': [],
            'threshold': None
        }

    def analyze(self, node):
        if hasattr(node, "accept"):
            node.accept(self)
        if self.errors:
            for error in self.errors:
                print(f"Semantic Error: {error}")
            raise Exception("Semantic Analysis Failed.")
        return True

    def visit_ProgramNode(self, node):
        node.model.accept(self)
        node.inputs.accept(self)
        node.features.accept(self)
        node.train.accept(self)
        node.condition.accept(self)

    def visit_ModelNode(self, node):
        if not node.name:
            self.errors.append("Model name cannot be empty.")

    def visit_InputNode(self, node):
        if not node.inputs:
            self.errors.append("At least one input must be declared.")
        self.symbol_table['inputs'].extend(node.inputs)

    def visit_FeatureNode(self, node):
        if not node.features:
            self.errors.append("At least one feature must be extracted.")
        self.symbol_table['features'].extend(node.features)

    def visit_TrainNode(self, node):
        if node.threshold < 0 or node.threshold > 1:
            self.errors.append(f"Threshold must be between 0.0 and 1.0. Got {node.threshold}")
        self.symbol_table['threshold'] = node.threshold

    def visit_ConditionNode(self, node):
        # We might check if condition_var is valid, typically 'anomaly'
        if node.condition_var not in ['anomaly'] and node.condition_var not in self.symbol_table['features']:
            self.errors.append(f"Undefined condition variable: '{node.condition_var}'. Expected 'anomaly' or extracted feature.")
        
        node.then_action.accept(self)
        node.else_action.accept(self)

    def visit_ActionNode(self, node):
        if node.action_type not in ['ALERT', 'LOG']:
            self.errors.append(f"Unknown action: {node.action_type}")
