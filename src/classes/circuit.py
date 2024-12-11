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
        self.d_frontier = []
        self.podem_state = 'initial'
        self.is_all_values_justified = True
        self.target = None
        self.remaining_targets = []
        self.backward_gates = []
        self.pushed_forward = False
        
    def run_podem(self):   
        test_vector = None
        if(self.fault_connection in self.input_connections):
            self.podem_state = 'forward' 
        else:
            self.podem_state = 'backward'
            
        print(f"initial state: {self.podem_state}")
        self.iterative_podem()
        test_vector = self.get_the_end_result_test_vector()
        return test_vector
    
    def iterative_podem(self):
        is_podem_over = self.is_podem_over()
        prev_gate = self.get_fault_previous_gate()
        if self.fault_connection not in self.input_connections:
            self.add_target(self.fault_connection, self.activation_value)
                
        if prev_gate != None:
            self.backward_gates.append(prev_gate)

        self.pushed_forward = False
        iteration_counter = 1
        while (is_podem_over == False and iteration_counter < 100):
            print(f"iteration: {iteration_counter}*************************************************")
            print(f"State: {self.podem_state}")

            if (len(self.remaining_targets) > 0 and self.podem_state == 'forward' and self.pushed_forward == True):
                self.podem_state = 'backward'
                self.target = self.remaining_targets.pop(0)
                gate = self.get_gate_by_output_connection(self.target['connection_name'])
                print(f"new Back Gate: {gate.id}")
                self.backward_gates.append(gate)
                print(f"New target has been set => connection:{self.target['connection_name']}, value:{self.target['value']}")
                
            elif self.podem_state == 'backward' and len(self.backward_gates) > 0:
                gate = self.backward_gates.pop(0)
                if gate is not None:
                    print(f"backward gate: {gate.id}")
                    self.backtrace_from_output(gate)
            
            elif self.podem_state == 'backward' and len(self.backward_gates) == 0:
                print("finished backward and moving to forward")
                # self.update_all_gates_values()
                # self.update_d_frontier()
                self.podem_state = 'forward'
                self.pushed_forward = False
                
            elif self.podem_state == 'forward' and self.pushed_forward == False:
                print("moving forward")
                self.pushed_forward = True
                self.feed_forward_all_gates()    
                    
            #from forward to backward
            elif self.podem_state == 'forward' and len(self.remaining_targets) > 0:
                target = self.remaining_targets[0]
                print(f"target connection:{target['connection_name']}, target_value:{target['value']}")
                output_connection = self.get_gate_by_output_connection_name(target['connection_name'])
                gate = self.get_gate_by_output_connection(output_connection)
                gate.output_connection.current_value = target['value']
                self.backward_gates.append(gate)
                self.podem_state = 'backward'
            
            
            
            self.check_target()
            # self.update_d_frontier()
            iteration_counter += 1
            # self.print_d_frontier()
            is_podem_over = self.is_podem_over()
            
        print("Podem ended")
        for output in self.output_connections:
            output.print_output()
    
    def feed_forward_all_gates(self):
        for level in range(self.max_gate_level + 1):
            for gate in self.gates:
                if gate.level == level:
                    self.set_other_inputs(gate)
                    self.propagate(gate)
    
    
    #TODO Add fanout backtrace
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
        elif gate.gate_type == 'nand' and gate.output_connection.current_value == 1:
            min_c0_connection = None
            min_c0 = 10**100
            for connection in gate.input_connections:
                if connection.controlability_to_zero < min_c0:
                    min_c0_connection = connection
                    min_c0 = connection.controlability_to_zero      
            min_c0_connection.current_value = 0
        
        
                
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
            # Fault activation condition: output should be 1.
            # Set all inputs to 0 or all to 1.
            if gate.output_connection.current_value == 'D':
                for input in gate.input_connections:
                    input.current_value = 0  # Set all inputs to 0
        elif gate.gate_type == 'xnor' and gate.output_connection.current_value == "D'":
            # Ensure an odd number of inputs have value D' or 1
            for input in gate.input_connections:
                input.current_value = 1
            min_c0_connection = min(gate.input_connections, key=lambda x: x.controlability_to_zero)
            min_c0_connection.current_value = 0
    
        for input_connection in gate.input_connections:
            if input_connection not in self.input_connections and input_connection.current_value in [0, 1, "D", "D'"]:
                prev_gate = self.get_gate_by_output_connection(input_connection.name)
                self.backward_gates.append(prev_gate)
                print(f"Gate: {prev_gate.id} has been added to backward gate list")
    
    def update_d_frontier(self):
        for gate in self.gates:
            for input in gate.input_connections:
                if input.current_value == 'D' or input.current_value == "D'":
                    if gate not in self.d_frontier:
                        self.d_frontier.append(gate)
    
    
    def is_podem_over(self):
        # print(self.fault_connection.current_value)
        # print(f"justifyed:{self.is_all_values_justified}")
        # print(f"input:{self.has_assigned_values_to_inputs()}")
        # print(f"output:{self.has_fault_reached_outputs()}")
        
        if self.is_all_values_justified == True and self.has_assigned_values_to_inputs() == True and self.has_fault_reached_outputs() == True and self.podem_state != 'backward':
            return True
        return False
    
    def set_other_inputs(self, gate):
        input_list = self.get_input_list(gate)
        if ('D' not in input_list and "D'" not in input_list):
            return
                
        elif gate.gate_type == 'nand' or gate.gate_type == 'and':
            for input_connection in gate.input_connections:
                if (input_connection.current_value == 'D' or input_connection.current_value == "D'"):
                    continue
                else:
                    self.assign_value_to_other_connection_in_forward(input_connection, 1)
                    # input_connection.current_value = 1
        elif gate.gate_type == 'nor' or gate.gate_type == 'or':
            for input_connection in gate.input_connections:
                if (input_connection.current_value == 'D' or input_connection.current_value == "D'"):
                    continue
                else:
                    self.assign_value_to_other_connection_in_forward(input_connection, 0)
                    # input_connection.current_value = 0
        
        elif gate.gate_type == 'xor' or gate.gate_type == 'xnor':
            for input_connection in gate.input_connections:
                if (input_connection.current_value == 'D' or input_connection.current_value == "D'"):
                    continue
                else:
                    self.assign_value_to_other_connection_in_forward(input_connection, 0)
                    # input_connection.current_value = 0
    
    
    #TODO Add fanout propagation  
    def propagate(self, gate): 
        input_values = self.get_input_list(gate)
        if gate.output_connection.current_value in ['D', "D'"]:
            return
        elif gate.gate_type == 'nand':
            if 'D' in input_values and 0 not in input_values and 'U' not in input_values:
                # If there's both a 1 and a D, output is D'
                gate.output_connection.current_value = "D'"
            elif "D'" in input_values and 0 not in input_values and 'U' not in input_values:
                # If there's both a 1 and a D', output is D
                gate.output_connection.current_value = 'D'
            elif all(value == 1 for value in input_values) :
                # If all inputs are 1, output is 0 for NAND
                gate.output_connection.current_value = 0
            elif any(value == 0 for value in input_values):
                # Otherwise, output is 1
                gate.output_connection.current_value = 1

        elif gate.gate_type == 'and':
            if 'D' in input_values and 0 not in input_values and 'U' not in input_values:
                # If any input is D, output is D
                gate.output_connection.current_value = 'D'
            elif "D'" in input_values and 0 not in input_values and 'U' not in input_values:
                # If any input is D', output is D'
                gate.output_connection.current_value = "D'"
            elif all(value == 1 for value in input_values):
                # If all inputs are 1, output is 1 for AND
                gate.output_connection.current_value = 1
            elif any(value == 0 for value in input_values):
                gate.output_connection.current_value = 0
        
        elif gate.gate_type == 'or':
            if 'D' in input_values and 1 not in input_values and 'U' not in input_values:
                gate.output_connection.current_value = 'D'
            elif "D'" in input_values and 1 not in input_values and 'U' not in input_values:
                gate.output_connection.current_value = "D'"
            elif any(value == 1 for value in input_values):
                gate.output_connection.current_value = 1
            elif all(value == 0 for value in input_values):
                gate.output_connection.current_value = 0

        elif gate.gate_type == 'nor':
            if 'D' in input_values and 1 not in input_values and 'U' not in input_values:
                gate.output_connection.current_value = "D'"
            elif "D'" in input_values and 1 not in input_values and 'U' not in input_values:
                gate.output_connection.current_value = 'D'
            elif any(value == 1 for value in input_values):
                gate.output_connection.current_value = 0
            elif all(value == 0 for value in input_values):
                gate.output_connection.current_value = 1

        elif gate.gate_type == 'xor':
            d_count = input_values.count('D')
            d_prime_count = input_values.count("D'")
            one_count = input_values.count(1)
            if (d_count + one_count) % 2 == 1:
                gate.output_connection.current_value = 'D'
            elif (d_prime_count + one_count) % 2 == 1:
                gate.output_connection.current_value = "D'"
            elif sum(value == 1 for value in input_values) % 2 == 1:
                gate.output_connection.current_value = 1
            elif sum(value == 1 for value in input_values) % 2 == 0:
                gate.output_connection.current_value = 0

        elif gate.gate_type == 'xnor':
            d_count = input_values.count('D')
            d_prime_count = input_values.count("D'")
            one_count = input_values.count(1)
            if (d_count + one_count) % 2 == 0:
                gate.output_connection.current_value = 'D'
            elif (d_prime_count + one_count) % 2 == 0:
                gate.output_connection.current_value = "D'"
            elif sum(value == 1 for value in input_values) % 2 == 0:
                gate.output_connection.current_value = 1
            elif sum(value == 1 for value in input_values) % 2 == 1:
                gate.output_connection.current_value = 0

        elif gate.gate_type == 'not':
            if input_values[0] == 'D':
                gate.output_connection.current_value = "D'"
            elif input_values[0] == "D'":
                gate.output_connection.current_value = 'D'
            elif input_values[0] == 1:
                gate.output_connection.current_value = 0
            elif input_values[0] == 0:
                gate.output_connection.current_value = 1
            elif input_values[0] != 1 and input_values[0] != 0:
                gate.output_connection.current_value = 1 if input_values[0] == 0 else 0

        elif gate.gate_type == 'buf':
            if input_values[0] == 'D':
                gate.output_connection.current_value = 'D'
            elif input_values[0] == "D'":
                gate.output_connection.current_value = "D'"
            elif input_values[0] == 1:
                gate.output_connection.current_value = 1
            elif input_values[0] == 0:
                gate.output_connection.current_value = 0
            elif input_values[0] != 1 and input_values[0] != 0:
                gate.output_connection.current_value = input_values[0]
        
        if gate.output_connection.current_value != 'U':
            print(f"assigned output_connection: {gate.output_connection.name}, value:{gate.output_connection.current_value}:")
        
    def assign_value_to_other_connection_in_forward(self, connection, value):
        if connection in self.input_connections:
            connection.current_value = value
            print(f"Connection: {connection.name}, value:{connection.current_value}")
        else:
            self.add_target(connection, value)

    def check_if_target_reached(self):
        if self.target is None:
            return True
        
        for connection in self.input_connections + self.net_connections + self.output_connections:
            if connection.name == self.target['connection_name'] and connection.current_value == self.target['value']:
                return True
            elif connection.name == self.target['connection_name'] and connection.current_value != self.target['value']:
                return False
        return False

    def add_target(self, connection, value):
        target = {"connection_name":connection.name, "value":value, "attempted":False}
        self.remaining_targets.append(target)
        print(f"Target added: Connection: {target['connection_name']}, value:{target['value']}")
        
    
    def check_target(self):
        if self.target is None:
            return True
        
        if (self.target is None or self.check_if_target_reached() == True) and len(self.remaining_targets) > 0 :
            self.target = None
            # print("target reached")
            # self.target = self.remaining_targets.pop(0)
        elif self.check_if_target_reached() == True and len(self.target) == 0 :
            print("All targets reached")
        # print(f"Target_connection:{self.target['connection_name']} Target_value:{self.target['value']}")
                    
    def get_gate_by_output_connection_name(self, name):
        for connection in self.input_connections + self.net_connections + self.output_connections:
             if connection.name == name:
                 return connection
             
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
    
    def get_fanout_by_input_connection(self, connection):
        for fanout in self.fanouts:
            if fanout.input_connection == connection:
                return fanout
        return None
        
    def check_if_fault_reached_output(self):
        for connection in self.output_connections:
            if connection.current_value == 'D' or connection.current_value == "D'":
                return True
        return False
    
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
    
    def get_gate_by_output_connection(self, gate_output_connection_name):
        for gate in self.gates:
            if gate.output_connection.name == gate_output_connection_name:
                return gate
        print("no gate found")
    
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
            if output.current_value in ['D', "D'"]:
                return True
        return False    
        
    def has_assigned_values_to_inputs(self):
        input_list = []
        for input_connection in self.input_connections:
                input_list.append(input_connection.current_value)       
    
        if 0 in input_list or 1 in input_list:
                return True
        return False
    
    def get_input_list(self, gate):
        input_values = []
        for input_connection in gate.input_connections:
                input_values.append(input_connection.current_value)       
        return input_values
    
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
     
    def print_d_frontier(self):
        id_list = []
        for gate in self.d_frontier:
            id_list.append(gate.id) 
        print(f"d-frontier: {id_list}")
