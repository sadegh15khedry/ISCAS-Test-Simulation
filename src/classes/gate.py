class Gate:
    def __init__(self, inputs, output, gate_type):
        self.inputs = inputs
        self.output = output
        self.gate_type = gate_type
        self.delay = 0
        
        