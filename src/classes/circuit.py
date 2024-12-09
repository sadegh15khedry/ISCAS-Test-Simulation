class Circuit:
    def __init__(self, gates, input_connections, output_connections, fanouts):
        self.gates = gates
        self.input_connections = input_connections
        self.output_connections = output_connections
        self.net_connections = []
        self.fanouts = fanouts
        self.max_gate_level = 0
        self.fault_connection = None  # Connection object where fault is set
        self.activation_value = None  # 'D' or "D'"
        
        self.initialize_net_connections()
        self.set_levels()
        self.D_frontier = []
    
    
    def run_podem(self):
        
            
        test_vector = None
        if(self.fault_connection in self.input_connections):
             print("fault on input connection")
             self.fault_on_input_connection()
             test_vector = self.get_the_end_result_test_vector()
             return test_vector
        else:
            self.default_podem()
            test_vector = self.get_the_end_result_test_vector()
            return test_vector
    
    def default_podem(self):

        prev_gate = self.get_fault_previous_gate()
        if prev_gate is not None:
            self.backtrace_from_output(prev_gate)
            print(f"previous gate is gate:{prev_gate.id}")
            
                # elif fanout is not None:
        #     pass
        
        
        
        if self.is_all_values_justified() == True and self.has_assigned_values_to_inputs() == True and self.has_fault_reached_outputs() == True:
            
            print("algoritm is finished")    
        
    def fault_on_input_connection(self):
        gate = self.get_gate_by_input_connection(self.fault_connection)
        gate.set_other_inputs()
        # print(gate.id)
        gate.propagate()
        
        if self.check_if_podem_is_finished() == True:
            print(f"gate_output: {gate.output_connection.current_value}")
            return True
    
    def backtrace_from_output(self, gate):
        if gate.gate_type == 'nand' and gate.output_connection.current_value == 'D':
            min_c0_connection = None
            min_c0 = 10**100
            for connection in gate.input_connections:
                if connection.controlability_to_zero < min_c0:
                    min_c0_connection = connection
                    min_c0 = connection.controlability_to_zero      
            min_c0_connection.current_value = 0
            print (f"backtracking gate:{gate.id}, input:{min_c0_connection.name}  assigned_value:{min_c0_connection.current_value}")
        elif gate.gate_type == 'nand' and gate.output_connection.current_value == "D'":
            for input in gate.input_connections:
                input.current_value = 1
                
        elif gate.gate_type == 'and' and gate.output_connection.current_value == 'D':
            for input in gate.input_connections:
                input.current_value = 1
        elif gate.gate_type == 'and' and gate.output_connection.current_value == "D'":
            min_c0_connection = None
            min_c0 = 10**100
            for connection in gate.input_connections:
                if connection.controlability_to_zero < min_c0:
                    min_c0_connection = connection
                    min_c0 = connection.controlability_to_zero      
            min_c0_connection.current_value = 0
            
        elif gate.gate_type == 'or' and gate.output_connection.current_value == 'D':
            min_c1_connection = None
            min_c1 = 10**100
            for connection in gate.input_connections:
                if connection.controlability_to_zero < min_c1:
                    min_c1_connection = connection
                    min_c1 = connection.controlability_to_one     
            min_c1_connection.current_value = 1
        elif gate.gate_type == 'or' and gate.output_connection.current_value == "D'":
            for input in gate.input_connections:
                input.current_value = 0
                
        elif gate.gate_type == 'nor' and gate.output_connection.current_value == 'D':
            for input in gate.input_connections:
                input.current_value = 0
            
        elif gate.gate_type == 'nor' and gate.output_connection.current_value == "D'":
            min_c1_connection = None
            min_c1 = 10**100
            for connection in gate.input_connections:
                if connection.controlability_to_zero < min_c1:
                    min_c1_connection = connection
                    min_c1 = connection.controlability_to_one     
            min_c1_connection.current_value = 1
            
        elif (gate.gate_type == 'not' and gate.output_connection.current_value == "D'") or  (gate.gate_type == 'buf' and gate.output_connection.current_value == "D"):
            for input in gate.input_connections:
                input.current_value = 1
        
        elif (gate.gate_type == 'not' and gate.output_connection.current_value == "D" ) or  (gate.gate_type == 'buf' and gate.output_connection.current_value == "D'"):
            for input in gate.input_connections:
                input.current_value = 0 

        elif gate.gate_type == 'xor' and gate.output_connection.current_value == "D":
            # Ensure an odd number of inputs have value D or 1
            for input in gate.input_connections:
                input.current_value = 0
            min_c1_connection = min(gate.input_connections, key=lambda x: x.controlability_to_one)
            min_c1_connection.current_value = 'D'
        elif gate.gate_type == 'xor' and gate.output_connection.current_value == "D'":
            # Ensure an even number of inputs have value D' or 1
            for input in gate.input_connections:
                input.current_value = 0
            min_c1_connection = min(gate.input_connections, key=lambda x: x.controlability_to_one)
            min_c1_connection.current_value = "D'"
        elif gate.gate_type == 'xnor' and gate.output_connection.current_value == "D":
            # Ensure an even number of inputs have value D or 1
            for input in gate.input_connections:
                input.current_value = 1
            min_c0_connection = min(gate.input_connections, key=lambda x: x.controlability_to_zero)
            min_c0_connection.current_value = 0
        elif gate.gate_type == 'xnor' and gate.output_connection.current_value == "D'":
            # Ensure an odd number of inputs have value D' or 1
            for input in gate.input_connections:
                input.current_value = 1
            min_c0_connection = min(gate.input_connections, key=lambda x: x.controlability_to_zero)
            min_c0_connection.current_value = 0
            
            
            
    def get_the_end_result_test_vector(self):
        result = []
        for connection in self.input_connections:
            if connection.current_value == "D":
                connection.current_value = 1
            elif connection.current_value == "D'":
                connection.current_value = 0
            elif connection.current_value == "U":
                connection.current_value = "X"
            row = {"connection":connection.name, "value":connection.current_value}
            result.append(row)
        return result
    
    def check_if_podem_is_finished(self):
        for connection in self.output_connections:
            if connection.current_value == 'D' or connection.current_value == "D'":
                return True
    
    def get_fault_previous_fanout_input(self):
        # print("gate check")
        for fanout in self.fanouts:
            for output in fanout.output_connections:
                if output == self.fault_connection:
                    return output.input_connection
         
    def get_gate_by_input_connection(self, gate_input_connection):
        for gate in self.gates:
            for input in gate.input_connections:
                if input == gate_input_connection:
                    return gate
                
    def get_fault_previous_gate(self):
        for gate in self.gates:
            if gate.output_connection == self.fault_connection:
                return gate
            
    def set_stuck_at_fault(self, connection_name, stuck_at):
        done = False
        for connection in self.input_connections + self.net_connections + self.output_connections:
            if connection.name == connection_name:
                connection.stuck_at = stuck_at
                self.fault_connection = connection
                self.set_fault_activation_value(stuck_at)
                self.fault_connection.current_value = self.activation_value
                connection.current_value = self.activation_value
                done = True
                print(f"Connection {connection.name} (ID: {connection.id}), stuck_at={connection.stuck_at} value:{self.fault_connection.current_value} activation_value={self.activation_value}")
                break
        
        if not done:
            print(f"Connection with identifier {connection_name} not found in the circuit.")
    
    def has_fault_reached_outputs(self):
        for output in self.output_connections:
            if output.current_value not in ['D', "D'"]:
                return True
        return False    
    
    def is_all_values_justified(self):
        return True
        
    def has_assigned_values_to_inputs(self):
        result = False
        for input in self.input_connections:
            if  input.current_value != 'U':
                return True
        return False
    
    def clear_faulty_circuit(self):
        done = False
        for connection in self.input_connections + self.output_connections + self.net_connections:
            connection.stuck_at = None
            connection.current_value = "U"
    
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
    
    def set_fault_activation_value(self, stuck_at):
        if stuck_at == 0:
            self.activation_value = 'D'
            # self.fault_connection.current_value = 1
            
        elif stuck_at == 1:
            self.activation_value = "D'"
            # self.fault_connection.current_value = 0
    
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
     
