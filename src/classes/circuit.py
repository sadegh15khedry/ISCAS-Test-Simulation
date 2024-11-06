class Circuit:
    def __init__(self, gates, input_connections, output_connections, fanouts):
        self.gates = gates
        self.input_connections = input_connections
        self.output_connections = output_connections
        self.fanouts = fanouts
        self.max_gate_level = 0
    
    
    def set_levels(self):
        for connection in self.input_connections:
            connection.set_level(0) 
            
        for fanout in self.fanouts:
            fanout.set_level()
            
        for gate in self.gates:
            gate.set_level()
        

    def set_max_gate_level(self):
        for gate in self.gates:
            if gate.level > self.max_gate_level:
                self.max_gate_level = gate.level
    
            
    def set_ciruit_inputs(self, input_file, time):
        for connection in self.input_connections:
            for index, row in input_file.iterrows():
                # print(row['id'])
                if int(connection.name) == int(row.id):
                    connection.update_value(row['value'], time)
                    # print(f"Initialized input {connection.name} with value {row['value']} at time step {time}")
                    
    def pass_values_to_output(self, time, delay_consideration):
        self.set_max_gate_level()
        for fanout in self.fanouts:
            fanout.pass_values(time)
            
        for level in range(self.max_gate_level+1):
            print(f"Level {level} started:\n")
            for gate in self.gates:
                if gate.level == level:
                    gate.pass_values(time, delay_consideration)
            
            for fanout in self.fanouts:
                        fanout.pass_values(time)        

    
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
            gate.draw()
            
        
        # Print fanouts
        if self.fanouts:
            print("Fanouts:")
            for fanout in self.fanouts:
                fanout.draw()
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
             
    def print_output(self, time):
        for output in self.output_connections:
            output.print_output(time)
     
