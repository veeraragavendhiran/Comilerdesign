import sys
import subprocess
import os
from main import compile_source

def print_help():
    print("NeuroScript Compiler CLI")
    print("Usage: neuroscript <command> [options]")
    print()
    print("Commands:")
    print("  build <file.ns> [-v, --visualize]    Compile NeuroScript file, optionally visualize AST.")
    print("  run <file.ns>                        Compile and immediately run the generated output.")
    print()

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "build":
        if len(sys.argv) < 3:
            print("Error: Missing file argument.")
            sys.exit(1)
        source = sys.argv[2]
        visualize = '-v' in sys.argv or '--visualize' in sys.argv
        
        with open(source, 'r') as f:
            code = f.read()
        compile_source(code, output_file='output/generated.py', visualize=visualize)
        
    elif command == "run":
        if len(sys.argv) < 3:
            print("Error: Missing file argument.")
            sys.exit(1)
        source = sys.argv[2]
        output_file = 'output/generated.py'
        
        try:
            with open(source, 'r') as f:
                code = f.read()
            compile_source(code, output_file, visualize=False)
            
            print("\n=== Phase 8: Execution Engine ===")
            print(f"Running {output_file}...\n")
            subprocess.run([sys.executable, output_file])
            
        except FileNotFoundError:
            print(f"Error: File {source} not found.")
            sys.exit(1)
            
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
