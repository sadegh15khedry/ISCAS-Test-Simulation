class Gate:
    def __init__(self, id, input_connections, output_connection, gate_type):
        self.id = id  # unique identifier for the gate
        self.input_connections = input_connections
        self.output_connection = output_connection
        self.gate_type = gate_type
        self.delay = 0
        
    def draw(self):
        input_names = [f"{conn.name} (ID: {conn.id})" for conn in self.input_connections]
        output_name = f"{self.output_connection.name} (ID: {self.output_connection.id})" if self.output_connection else "None"
        print(f"  Gate ID: {self.id}")
        print(f"    Type: {self.gate_type}")
        print(f"    Inputs: {', '.join(input_names)}")
        print(f"    Output: {output_name}\n")