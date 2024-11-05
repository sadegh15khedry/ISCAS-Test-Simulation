class Circuit:
    def __init__(self, gates, input_connections, output_connections, fanouts):
        self.gates = gates
        self.input_connections = input_connections
        self.output_connections = output_connections
        self.fanouts = fanouts
    
    def set_levels(self):
        for connection in self.input_connections:
            connection.level = 0
            print (f"{connection.id} level: {connection.level}") 

        for gate in self.gates:
            max_input_level = 0
            for conneciton in gate.input_connections:
                if connection.level == None:
                    max_input_level = None
                    break
                elif connection.level > max_input_level:
                    max_input_level = connection.level
            gate.level = max_input_level
            
            if gate.level:
                print (f"gate {gate.id} level: {gate.level}")
                
    
    def set_input_value(self, input_file, time):
        # print(input_file)
        
            # print("idex ",index)
        for connection in self.input_connections:
            for index, row in input_file.iterrows():
                # print(row['id'])
                if int(connection.name) == int(row.id):
                    connection.update_value(row['value'], time)
                    print(f"Initialized input {connection.name} with value {row['value']} at time step {time}")
                    
    def pass_values_to_output(self, time):
        for connection in self.input_connections:
            gate = connection.destination
            if gate:
                gate.update_output(time)
    
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
     
