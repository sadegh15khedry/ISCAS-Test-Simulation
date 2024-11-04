class Circuit:
    def __init__(self, gates, input_connections, output_connections, fanouts):
        self.gates = gates
        self.input_connections = input_connections
        self.output_connections = output_connections
        self.fanouts = fanouts
        
    def draw_circuit(self):
        print("Circuit Representation:\n")
        
        # Print primary inputs
        print("Primary Inputs:")
        for conn in self.input_connections:
            print(f"  {conn.name} (ID: {conn.id})")
        print()
        
        # Print gates and their connections
        print("Gates:")
        for gate in self.gates:
            gate.draw_gate()
            
        
        # Print fanouts
        if self.fanouts:
            print("Fanouts:")
            for fanout in self.fanouts:
                input_conn_name = f"{fanout.input_connection.name} (ID: {fanout.input_connection.id})"
                output_conn_names = [f"{conn.name} (ID: {conn.id})" for conn in fanout.output_connections]
                print(f"  Fanout ID: {fanout.id}")
                print(f"    Input: {input_conn_name}")
                print(f"    Outputs: {', '.join(output_conn_names)}\n")
        else:
            print("No Fanouts in the Circuit.\n")
        
        # Print primary outputs
        print("Primary Inputs:")
        for conn in self.input_connections:
            print(f"  {conn.name} (ID: {conn.id})")
        print()
        
        # Print primary outputs
        print("Primary Outputs:")
        for conn in self.output_connections:
            print(f"  {conn.name} (ID: {conn.id})")
        print()
