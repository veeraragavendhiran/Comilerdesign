class ASTNode:
    def accept(self, visitor, *args, **kwargs):
        method_name = f'visit_{self.__class__.__name__}'
        visitor_method = getattr(visitor, method_name, self.generic_visit)
        return visitor_method(self, *args, **kwargs)

    def generic_visit(self, visitor, *args, **kwargs):
        raise Exception(f'No visit_{self.__class__.__name__} method defined in {visitor.__class__.__name__}')

class ProgramNode(ASTNode):
    def __init__(self, model, inputs, features, train, condition):
        self.model = model
        self.inputs = inputs
        self.features = features
        self.train = train
        self.condition = condition

class ModelNode(ASTNode):
    def __init__(self, name):
        self.name = name

class InputNode(ASTNode):
    def __init__(self, inputs):
        self.inputs = inputs

class FeatureNode(ASTNode):
    def __init__(self, features):
        self.features = features

class TrainNode(ASTNode):
    def __init__(self, threshold):
        self.threshold = threshold

class ConditionNode(ASTNode):
    def __init__(self, condition_var, operator, then_action, else_action):
        self.condition_var = condition_var
        self.operator = operator
        self.then_action = then_action
        self.else_action = else_action

class ActionNode(ASTNode):
    def __init__(self, action_type, message=None):
        self.action_type = action_type
        self.message = message
