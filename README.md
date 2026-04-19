# NeuroScript Compiler

**NeuroScript** is an advanced, domain-specific programming language designed for Edge AI and IoT anomaly detection systems. 
It provides a high-level, human-readable syntax that seamlessly compiles down to Python executables (with extensibility to C/LLVM).

---

## 🎯 Architecture & Compiler Pipeline

The NeuroScript Compiler uses a multi-phase compilation approach:

1. **Phase 1: Language Design** (BNF Grammar & Syntax)
2. **Phase 2: Lexical Analyzer** (PLY-based Tokenization)
3. **Phase 3: Parsing & AST Construction** (PLY Yacc Tree Parsing)
4. **Phase 4: Semantic Analysis** (Type-checking and Context bounds)
5. **Phase 5: Intermedia Representation** (JSON-like structured IR)
6. **Phase 6: Optimization** (Dead code elimination and control flow graph tuning)
7. **Phase 7: Code Generation** (Translation to targeted runtime Python code)
8. **Phase 8: CLI Engine** (CLI runtime tool executing scripts)
9. **Phase 9: Visualization** (GraphViz Abstract Syntax Tree dump)

---

## 📄 Formal Grammar (EBNF)

```text
Program      ::= ModelDecl InputDecl FeatureDecl TrainDecl ConditionDecl
ModelDecl    ::= "MODEL" IDENTIFIER
InputDecl    ::= "INPUT" IdentList
FeatureDecl  ::= "FEATURE" "extract" IdentList
TrainDecl    ::= "TRAIN" "model" "USING" "threshold" NUMBER
ConditionDecl::= "IF" IDENTIFIER ">" "THRESHOLD" "THEN" Action "ELSE" Action
               | "IF" IDENTIFIER "<" "THRESHOLD" "THEN" Action "ELSE" Action
               | "IF" IDENTIFIER "==" "THRESHOLD" "THEN" Action "ELSE" Action
Action       ::= "ALERT" | "LOG" STRING
IdentList    ::= IDENTIFIER | IDENTIFIER "," IdentList
```

---

## 💻 Sample Program

```ns
MODEL anomaly_detector
INPUT sound, vibration
FEATURE extract RMS, variance
TRAIN model USING threshold 0.7
IF anomaly > THRESHOLD THEN ALERT
ELSE LOG "Normal"
```

---

## 🚀 How to Run

### Requirements
- Python 3+
- `pip install ply graphviz`
- Note: For PNG AST visualization, the `dot` GraphViz binary must be installed on your System PATH. Otherwise, `.dot` source falls back safely.

### CLI Usage

Compile a script into an executable (`output/generated.py`):
```bash
python cli.py build examples/sample.ns
```

Compile and run immediately:
```bash
python cli.py run examples/sample.ns
```

Generate the AST Source Visualization Graph (`visuals/ast.dot` | `visuals/ast.png`):
```bash
python cli.py build examples/sample.ns -v
```
