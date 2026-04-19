class Optimizer:
    def __init__(self):
        self.optimized_ir = None

    def optimize(self, ir):
        """
        Simple Optimization pass:
        - Check if identical THEN and ELSE actions and eliminate branch.
        - Ensure condition logic is simplified.
        """
        print("[Optimizer] Running Optimization Passes...")
        self.optimized_ir = ir.copy()

        cond = self.optimized_ir.get('condition', {})
        then_act = cond.get('then')
        else_act = cond.get('else')

        if then_act and else_act:
            if then_act['type'] == else_act['type'] and then_act.get('message') == else_act.get('message'):
                print("[Optimizer] Dead Code Elimination: THEN and ELSE actions are identical. Branch unified.")
                # Action is same regardless of condition
                self.optimized_ir['action_unified'] = then_act
                del self.optimized_ir['condition']
        
        # In a real compiler, we'd also do constant folding if needed
        return self.optimized_ir
