class Circuit:
    def __init__(self, gates, input_connections, output_connections, fanouts):
        self.gates = gates
        self.input_connections = input_connections
        self.output_connections = output_connections
        self.net_connections = []
        self.fanouts = fanouts
        self.max_gate_level = 0
    
    def initialize_net_connections(self):
        result = []
        for gate in self.gates:
            for input_connection in gate.input_connections:
                if input_connection not in self.input_connections and input_connection not in result:
                    result.append(input_connection)
       
            if gate.output_connection not in self.output_connections and gate.output_connection not in result:
                result.append(gate.output_connection)
        # print(self.fanouts)        
        for fanout in self.fanouts:
            for output_connection in fanout.output_connections:
                if output_connection not in self.output_connections and output_connection not in result:
                    result.append(output_connection)
                    
            if fanout.input_connection not in self.input_connections and fanout.input_connection not in result:
                result.append(fanout.input_connection)
        # result2 = []
        # [result2.append(x) for x in result if x not in result2]
        self.net_connections = result
    
    def does_all_output_connections_have_level(self):
        for connection in self.output_connections:
            if(connection.level == None):
                return False
        return True
    
    def set_levels(self):
        while self.does_all_output_connections_have_level() == False:
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
    
    def set_circuit_inputs(self, input_file, time):
        if input_file.empty:
            return
        else:
            print("New inputs detected!!!!!!!!")
            for connection in self.input_connections:
                value = input_file[connection.name].squeeze()
                print(f"connection: {connection.name} new value:{value}")
                connection.update_value(value, time)

    def set_observability(self):
        for connection in self.output_connections:
            connection.observability = 0
            
        for fanout in self.fanouts:
                fanout.set_observability()
        
        for level in range(self.max_gate_level, -1, -1):
            print("level: ", level)
            for gate in self.gates:
                if gate.level == level:
                    gate.set_observability()
            for fanout in self.fanouts:
                fanout.set_observability()
                
    
    def set_controlability(self):
        self.set_max_gate_level()
        
        for connection in self.input_connections:
            connection.controlability_to_zero = 1
            connection.controlability_to_one = 1
        
        for fanout in self.fanouts:
                fanout.set_controlability()
        
        for level in range(self.max_gate_level+1):
            for gate in self.gates:
                if gate.level == level:
                    gate.set_controlability()
            for fanout in self.fanouts:
                fanout.set_controlability()
                    
    def pass_values_to_output(self, time, delay_consideration):
        self.set_max_gate_level()
        for fanout in self.fanouts:
            fanout.pass_values(time)
            
        for level in range(self.max_gate_level+1):
            # print(f"Level {level} started:\n")
            for gate in self.gates:
                if gate.level == level:
                    gate.pass_values(time, delay_consideration)
            
            for fanout in self.fanouts:
                fanout.pass_values(time)        

    def check_delays(self):
        for gate in self.gates:
            if gate.delay is None:
                gate.delay = 0
    
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
            print(f"  {conn.name} (ID: {conn.id}) controlability:({conn.controlability_to_zero} , {conn.controlability_to_one}) observability:{conn.observability}")
        print()
        
        # Print primary outputs
        print("Primary Outputs:")
        for conn in self.output_connections:
            print(f"  {conn.name} (ID: {conn.id}) controlability:({conn.controlability_to_zero} , {conn.controlability_to_one}) observability:{conn.observability}")
        print()
        
        
        
        print("Net connections:")
        for conn in self.net_connections: 
            print(f"  {conn.name} (ID: {conn.id}) controlability:({conn.controlability_to_zero} , {conn.controlability_to_one}) observability:{conn.observability}")
        print()
        
        # print("Fanout connections:")
        # for fanout in self.fanouts:
        #     print(f"  {fanout.input_connection.name} (ID: {fanout.input_connection.id}) controlability:({fanout.input_connection.controlability_to_zero} , {fanout.input_connection.controlability_to_one}) observability:{fanout.input_connection.observability}")
        #     for conn in fanout.output_connections:
        #         print(f"  {conn.name} (ID: {conn.id}) controlability:({conn.controlability_to_zero} , {conn.controlability_to_one}) observability:{conn.observability}")
                
        print()
             
    def print_inputs(self):
        for input in self.input_connections:
            print(f" input:{input.name}, value: {input.current_value}")
            
    def print_net_connections(self):
        for net in self.net_connections:
            print(f" net:{net.name}, value: {net.current_value}")
     
    def print_outputs(self):
        for output in self.output_connections:
            print(f" output:{output.name}, value: {output.current_value}")
            
    def print_connections_values(self):
        self.print_inputs()
        print(" ")
        self.print_net_connections()
        print(" ")
        self.print_outputs()