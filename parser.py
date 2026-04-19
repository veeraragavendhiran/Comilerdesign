import ply.yacc as yacc
from lexer import tokens, lexer
from ast_nodes import ProgramNode, ModelNode, InputNode, FeatureNode, TrainNode, ConditionNode, ActionNode

class ParserError(Exception):
    pass

def p_program(p):
    '''program : model_decl input_decl feature_decl train_decl condition_decl'''
    p[0] = ProgramNode(p[1], p[2], p[3], p[4], p[5])

def p_model_decl(p):
    '''model_decl : MODEL IDENTIFIER'''
    p[0] = ModelNode(p[2])

def p_input_decl(p):
    '''input_decl : INPUT ident_list'''
    p[0] = InputNode(p[2])

def p_feature_decl(p):
    '''feature_decl : FEATURE EXTRACT ident_list'''
    p[0] = FeatureNode(p[3])

def p_train_decl(p):
    '''train_decl : TRAIN R_MODEL USING R_THRESHOLD NUMBER'''
    p[0] = TrainNode(p[5])

def p_condition_decl(p):
    '''condition_decl : IF IDENTIFIER GT THRESHOLD THEN action ELSE action
                      | IF IDENTIFIER LT THRESHOLD THEN action ELSE action
                      | IF IDENTIFIER EQ THRESHOLD THEN action ELSE action'''
    p[0] = ConditionNode(p[2], p[3], p[6], p[8])

def p_action(p):
    '''action : ALERT
              | LOG STRING_LITERAL'''
    if p[1] == 'ALERT':
        p[0] = ActionNode('ALERT')
    else:
        p[0] = ActionNode('LOG', p[2])

def p_ident_list_single(p):
    '''ident_list : IDENTIFIER'''
    p[0] = [p[1]]

def p_ident_list_multi(p):
    '''ident_list : IDENTIFIER COMMA ident_list'''
    p[0] = [p[1]] + p[3]

def p_error(p):
    if p:
        msg = f"Syntax error at '{p.value}' (line {p.lineno})"
        print(msg)
        raise ParserError(msg)
    else:
        msg = "Syntax error at EOF"
        print(msg)
        raise ParserError(msg)

parser = yacc.yacc()

def parse(data):
    # Reset lexer state
    lexer.lineno = 1
    return parser.parse(data, lexer=lexer)
