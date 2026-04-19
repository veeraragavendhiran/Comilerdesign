import argparse
import sys
import os
from graphviz import Digraph

from parser import parse, ParserError
from ast_nodes import ModelNode, ConditionNode, InputNode, FeatureNode, TrainNode, ActionNode
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from codegen import CodeGenerator

def generate_ast_graph(node, graph=None, parent_id=None, node_id_gen=None):
    if graph is None:
        graph = Digraph(comment='Abstract Syntax Tree')
        node_id_gen = iter(range(1, 10000))

    my_id = str(next(node_id_gen))
    
    # Extract label based on node type
    label = node.__class__.__name__
    if isinstance(node, ModelNode):
        label += f"\\n{node.name}"
    elif isinstance(node, ConditionNode):
        label += f"\\n{node.condition_var} {node.operator} THRESHOLD"
    elif isinstance(node, InputNode):
        label += f"\\n[{', '.join(node.inputs)}]"
    elif isinstance(node, FeatureNode):
        label += f"\\n[{', '.join(node.features)}]"
    elif isinstance(node, TrainNode):
        label += f"\\n{node.threshold}"
    elif isinstance(node, ActionNode):
        label += f"\\n{node.action_type}"
        if node.message:
            label += f" {node.message}"

    graph.node(my_id, label)

    if parent_id is not None:
        graph.edge(parent_id, my_id)

    # Recursively visit children
    for attr in dir(node):
        if not attr.startswith('__') and not callable(getattr(node, attr)):
            child = getattr(node, attr)
            if hasattr(child, 'accept'):  # it's a Node
                generate_ast_graph(child, graph, my_id, node_id_gen)

    return graph

def compile_source(source_code, output_file, visualize=False, visuals_dir='visuals'):
    print("=== NeuroScript Compiler Phase 1-3: Lexing & Parsing ===")
    try:
        ast = parse(source_code)
        print("[Parser] AST successfully generated.")
    except Exception as e:
        print(f"Compilation terminated during parsing: {e}")
        sys.exit(1)

    if visualize:
        try:
            print("=== Visualization Phase ===")
            os.makedirs(visuals_dir, exist_ok=True)
            graph = generate_ast_graph(ast)
            try:
                graph.render(os.path.join(visuals_dir, 'ast'), format='png', cleanup=True)
                print(f"[Visualizer] AST graph rendered to {visuals_dir}/ast.png")
            except Exception as render_err:
                # Fallback to saving dot source
                dot_path = os.path.join(visuals_dir, 'ast.dot')
                with open(dot_path, 'w') as f:
                    f.write(graph.source)
                print(f"[Visualizer] Warning: Could not render PNG (Graphviz dot executable not found).")
                print(f"[Visualizer] Saved raw AST graph to {dot_path} instead.")
                
        except Exception as e:
            print(f"[Visualizer] Warning: Could not generate graph - {e}")

    print("\n=== Phase 4: Semantic Analysis ===")
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("[Semantic] Passed all semantic checks.")

    print("\n=== Phase 5: Intermediate Representation (IR) ===")
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    print("[IRGen] Generated IR successfully.")

    print("\n=== Phase 6: Optimization ===")
    opt = Optimizer()
    optimized_ir = opt.optimize(ir)
    print("[Optimizer] Optimization complete.")

    print("\n=== Phase 7: Code Generation ===")
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    codegen = CodeGenerator(optimized_ir, target='python')
    codegen.generate(output_file)
    print("\nCompilation completed successfully!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NeuroScript Compiler')
    parser.add_argument('source', help='Source .ns file')
    parser.add_argument('-o', '--output', default='output/generated.py', help='Output Python file')
    parser.add_argument('-v', '--visualize', action='store_true', help='Generate AST visualization')

    args = parser.parse_args()

    try:
        with open(args.source, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File {args.source} not found.")
        sys.exit(1)

    compile_source(source_code, args.output, args.visualize)
