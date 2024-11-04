class Gate:
    def __init__(self, id, input_connections, output_connection, gate_type):
        self.id = id  # unique identifier for the gate
        self.input_connections = input_connections
        self.output_connection = output_connection
        self.gate_type = gate_type
        self.delay = 0
        
        