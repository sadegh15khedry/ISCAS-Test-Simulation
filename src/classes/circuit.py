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
    
    def run_podem(self):
        return self.podem_iterative()

    def podem_iterative(self):
        print("Starting PODEM algorithm...")
        # Activate fault
        if not self.assign_objective_for_fault():
            print("Failed to activate the fault.")
            return {}

        # Check if fault is detected after activation
        if self.fault_detected():
            print("Fault detected immediately after activation.")
            return self.extract_test_vector()

        # Attempt to propagate the fault iteratively
        success = self.fault_propagation_iterative()
        if success:
            print("PODEM found a test vector.")
            return self.extract_test_vector()
        else:
            print("PODEM could not find a test vector for the given stuck-at fault.")
            return {}
    
    def opposite_logic_state(self, state):
        """
        Get the opposite logic state.
        """
        if state == 1:
            return 0
        elif state == 0:
            return 1
        elif state == 'D':
            return "D'"
        elif state == "D'":
            return 'D'
        elif state in ['U', 'Z']:
            return state
        else:
            return 'U'

    def opposite(self, val):
        """
        Alias for opposite_logic_state.
        """
        return self.opposite_logic_state(val)

    def is_primary_input(self, connection):
        """
        Check if the connection is a primary input.
        """
        return connection in self.input_connections

    def fault_detected(self):
        for output in self.output_connections:
            if output.current_value in ['D', "D'"]:
                print(f"Fault detected at output {output.name}: {output.current_value}")
                return True
            elif output.current_value == 'D':
                print(f"Fault detected at output {output.name}: D (Logical: 1)")
                return True
            elif output.current_value == "D'":
                print(f"Fault detected at output {output.name}: D' (Logical: 0)")
                return True
        return False

    
    def all_assigned(self):
        """
        Check if all primary inputs have been assigned a definite value (0 or 1).
        """
        return all(conn.current_value in [0, 1] for conn in self.input_connections)

    def get_gate_for_connection(self, connection):
        """
        Get the gate that drives the given connection.
        """
        return connection.source if hasattr(connection, 'source') else None

    def gate_type(self, gate):
        """
        Get the type of the gate in lowercase.
        """
        return gate.gate_type.lower()

    def get_line_value(self, connection):
        """
        Get the current value of the connection.
        """
        return connection.current_value
    
    def get_D_frontier(self):
        """
        Identify the D-frontier gates: Gates that have D or D' at an input but not at output.
        """
        d_front = []
        for g in self.gates:
            input_vals = [self.get_line_value(i) for i in g.input_connections]
            out_val = self.get_line_value(g.output_connection)
            if (('D' in input_vals or "D'" in input_vals) and out_val not in ['D', "D'"]):
                d_front.append(g)
        return d_front
    
    def backtrace(self, line, value, visited=None):
        if visited is None:
            visited = set()
        
        if (line, value) in visited:
            print(f"Already visited {line.name} with value {value}. Skipping to prevent loop.")
            return False
        visited.add((line, value))
        
        # Convert symbolic value to logical value if necessary
        if isinstance(value, str):
            logical_val = self.symbolic_to_logical(value)
        else:
            logical_val = value
        
        if self.is_primary_input(line):
            if line.current_value not in [0, 1, 'U']:
                print(f"Backtrace failed: {line.name} already has value {line.current_value}, cannot assign {logical_val}")
                return False
            if line.current_value == 'U':
                print(f"Assigning primary input {line.name} to {logical_val} for {value}")
                line.update_value(logical_val, time=0)
            return True

        g = self.get_gate_for_connection(line)
        if g is None:
            print(f"Backtrace failed: No gate drives connection {line.name}")
            return False

        t = self.gate_type(g)
        inputs = g.input_connections

        if t == 'not':
            required_input = self.opposite_logic_state(value)
            logical_required = self.symbolic_to_logical(required_input)
            print(f"Backtracing NOT gate: Setting input of {inputs[0].name} to {required_input} (Logical: {logical_required})")
            return self.backtrace(inputs[0], logical_required, visited)

        if t == 'buf':
            print(f"Backtracing BUF gate: Setting input of {inputs[0].name} to {logical_val}")
            return self.backtrace(inputs[0], logical_val, visited)

        if t in ['and', 'nand', 'or', 'nor']:
            c_val = self.controlling_val(t)
            nc_val = self.non_controlling_val(t)

            if value in ['D', "D'"]:
                # To propagate D/D', set one input to D/D' and others to non-controlling
                for inp in inputs:
                    print(f"Backtracing gate {g.gate_type.upper()} for D/D': trying to set {value} to {inp.name}")
                    # Save current state
                    saved_values = {c: c.current_value for c in inputs}
                    
                    # Assign non-controlling values to other inputs
                    can_assign = True
                    for other in inputs:
                        if other is not inp and other.current_value not in [nc_val, 'U']:
                            can_assign = False
                            print(f"Cannot assign non-controlling value to {other.name}, already has {other.current_value}")
                            break
                    if not can_assign:
                        continue
                    
                    for other in inputs:
                        if other is not inp and other.current_value == 'U':
                            print(f"Assigning non-controlling value {nc_val} to {other.name}")
                            other.update_value(nc_val, time=0)
                    
                    # Backtrace the chosen input with D/D'
                    if self.backtrace(inp, value, visited):
                        return True
                    
                    # Revert assignments
                    for other in inputs:
                        other.update_value(saved_values[other], time=0)
            else:
                if value == c_val:
                    # Set one input to controlling value and others to non-controlling
                    for candidate in inputs:
                        print(f"Backtracing gate {g.gate_type.upper()} for normal objective: trying to set {c_val} to {candidate.name}")
                        # Save current state
                        saved_values = {c: c.current_value for c in inputs}
                        
                        # Assign non-controlling values to other inputs
                        can_assign = True
                        for other in inputs:
                            if other is not candidate and other.current_value not in [nc_val, 'U']:
                                can_assign = False
                                print(f"Cannot assign non-controlling value to {other.name}, already has {other.current_value}")
                                break
                        if not can_assign:
                            continue
                        
                        for other in inputs:
                            if other is not candidate and other.current_value == 'U':
                                print(f"Assigning non-controlling value {nc_val} to {other.name}")
                                other.update_value(nc_val, time=0)
                        
                        # Backtrace the chosen input
                        if self.backtrace(candidate, c_val, visited):
                            return True
                        
                        # Revert assignments
                        for other in inputs:
                            other.update_value(saved_values[other], time=0)
                elif value == nc_val:
                    # Set all inputs to non-controlling value
                    print(f"Backtracing gate {g.gate_type.upper()} for normal objective: setting all inputs to {nc_val}")
                    can_assign = True
                    for inp in inputs:
                        if inp.current_value not in [nc_val, 'U']:
                            can_assign = False
                            print(f"Cannot assign non-controlling value to {inp.name}, already has {inp.current_value}")
                            break
                    if not can_assign:
                        return False
                    for inp in inputs:
                        if inp.current_value == 'U':
                            print(f"Assigning non-controlling value {nc_val} to {inp.name}")
                            inp.update_value(nc_val, time=0)
                    return True
        return False



    def assign_objective_for_fault(self):
        """
        Assign the objective to activate the fault by setting the faulty connection to the appropriate value.
        """
        # print(f"fault_connection: {self.fault_connection.name}, stuck_at:{self.fault_connection.stuck_at}, fault_activation: {self.activation_val}")
        if self.fault_connection and self.activation_value:
            print(f"Assigning objective to activate fault: setting {self.fault_connection.name} to {self.activation_value}")
            # Map symbolic value to logical value before backtracing
            logical_val = self.symbolic_to_logical(self.activation_value)
            return self.backtrace(self.fault_connection, logical_val)
        else:
            print("No fault has been set.")
            return False


    def symbolic_to_logical(self, value):
        """
        Convert symbolic value to logical value.
        'D' -> 1
        "D'" -> 0
        Otherwise, return the value as is.
        """
        if value == 'D':
            return 1
        elif value == "D'":
            return 0
        else:
            return value

    def fault_propagation_iterative(self):
        """
        Attempt to propagate the fault through the circuit iteratively.
        """
        print("Attempting fault propagation...")
        d_front = self.get_D_frontier()
        print(f"D-Frontier Gates: {[g.output_connection.name for g in d_front]}")
        if not d_front:
            print("No D-frontier found. Cannot propagate fault.")
            return False

        queue = d_front.copy()
        MAX_ITERATIONS = 1000
        iteration = 0

        while queue and iteration < MAX_ITERATIONS:
            g = queue.pop(0)
            in_vals = [self.get_line_value(i) for i in g.input_connections]
            if 'D' in in_vals:
                obj_val = 'D'
            elif "D'" in in_vals:
                obj_val = "D'"
            else:
                continue  # No D/D' in inputs

            out_conn = g.output_connection
            print(f"Propagating fault through gate {g.gate_type.upper()} driving {out_conn.name} with objective {obj_val}")

            # Attempt to backtrace the objective
            success = self.backtrace(out_conn, obj_val)
            if not success:
                print(f"Failed to backtrace objective for gate {g.gate_type.upper()} driving {out_conn.name}")
                continue

            # Simulate and check if fault is detected
            if self.fault_detected():
                print("Fault detected after propagation.")
                return True

            # Update D-Frontier
            new_d_front = self.get_D_frontier()
            print(f"New D-Frontier Gates after propagation: {[gate.output_connection.name for gate in new_d_front]}")
            for new_gate in new_d_front:
                if new_gate not in queue:
                    queue.append(new_gate)
            
            iteration += 1

        if iteration >= MAX_ITERATIONS:
            print("Reached maximum iterations. Exiting to prevent infinite loop.")
        else:
            print("Failed to propagate fault through all D-frontier gates.")
        return False

    def controlling_val(self, gate_type):
        """
        Get the controlling value for the given gate type.
        
        Controlling values are:
        - AND/NAND: 1
        - OR/NOR: 1
        """
        controlling_values = {
            'and': 1,
            'nand': 1,
            'or': 1,
            'nor': 1
            # Add more gate types if necessary
        }
        return controlling_values.get(gate_type, None)

    def non_controlling_val(self, gate_type):
        """
        Get the non-controlling value for the given gate type.
        
        Non-controlling values are:
        - AND/NAND: 0
        - OR/NOR: 0
        """
        non_controlling_values = {
            'and': 0,
            'nand': 0,
            'or': 0,
            'nor': 0
            # Add more gate types if necessary
        }
        return non_controlling_values.get(gate_type, None)

    def extract_test_vector(self):
        """
        Extract the test vector from the primary input connections.
        """
        test_vector = {}
        for c in self.input_connections:
            val = c.current_value
            if val == 'D':
                logical_val = 1
            elif val == "D'":
                logical_val = 0
            elif val == 'U':
                logical_val = 0  # default to 0 for don't-care
            else:
                logical_val = val  # assume it's already a logical value
            test_vector[c.name] = logical_val
        print("PODEM found a test vector:", test_vector)
        return test_vector


    
    
    
    
    
    
    
    
    
    
    
    
    def set_stuck_at_fault(self, connection_name, stuck_at):
        done = False
        for connection in self.input_connections + self.net_connections + self.output_connections:
            if connection.name == connection_name:
                connection.stuck_at = stuck_at
                self.fault_connection = connection
                self.set_fault_activation_value(stuck_at)
                done = True
                print(f"Connection {connection.name} (ID: {connection.id}), stuck_at={connection.stuck_at} activation_value={self.activation_value}")
                break
        
        if not done:
            print(f"Connection with identifier {connection_name} not found in the circuit.")


    
    def remove_stuck_at_fault(self, connection_name):
        done = False
        for connection in self.input_connections:
            if connection.name == connection_name:
                connection.stuck_at = None
                done = True
                # print(f"Connection{connection.name}, stuck_at={connection.stuck_at} removed")
                break
        if done == False:
            for connection in self.net_connections:
                if connection.name == connection_name:
                    connection.stuck_at = None
                    done = True
                    # print(f"Connection{connection.name}, stuck_at={connection.stuck_at} removed")
                    break
        if done == False:
            for connection in self.output_connections:
                if connection.name == connection_name:
                    connection.stuck_at = None
                    # print(f"Connection{connection.name}, stuck_at={connection.stuck_at} removed")
                    break
    
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
        elif stuck_at == 1:
            self.activation_value = "D'"
    
    
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