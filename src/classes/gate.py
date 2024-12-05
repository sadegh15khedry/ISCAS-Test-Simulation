# from logic_state import LogicState
class Gate:
    def __init__(self, id, input_connections, output_connection, delay, gate_type):
        self.id = id  # unique identifier for the gate
        self.input_connections = input_connections
        self.output_connection = output_connection
        self.gate_type = gate_type
        self.delay = delay
        self.level = None
    


    
    def set_controlability(self):
        print(f"set_control for {self.id}")
        if self.can_set_controlability() == False:
            return
            
        elif self.gate_type == 'and':
            self.set_and_controlability()
        
        elif self.gate_type == 'nand':
            self.set_nand_controlability()
        
        elif self.gate_type == 'or':
            self.set_or_controlability()
        
        elif self.gate_type == 'nor':
            self.set_nor_controlability()
        
        elif self.gate_type == 'xor':
            self.set_xor_controlability()
        
        elif self.gate_type == 'xnor':
            self.set_xnor_controlability()
        
        elif self.gate_type == 'not':
            self.set_not_controlability()
        
        elif self.gate_type == 'buf':
            self.set_buf_controlability()
        
        else:
            raise ValueError(f"Unsupported gate type: {self.gate_type}")
    def set_xnor_controlability(self):
        pass
    def set_xor_controlability(self):
        pass
        # c0_0 = 0
        # c0_1 = 0

        # c1_0 = 0
        # c1_1 = 0
        # for connection in self.input_connections:
        #     c1 = connection.controlability_to_one
        
        # for connection in self.input_connections:
        #     c0 = connection.controlability_to_zero
            
        # c0 += 1
        # c1 += 1
            
        # self.output_connection.controlability_to_zero = c0
        # self.output_connection.controlability_to_one = c1
       
    def set_buf_controlability(self):
        c0 = 0
        c1 = 0
        for connection in self.input_connections:
            c1 = connection.controlability_to_one
        for connection in self.input_connections:
            c0 = connection.controlability_to_zero
            
        c0 += 1
        c1 += 1
            
        self.output_connection.controlability_to_zero = c0
        self.output_connection.controlability_to_one = c1 
    
    def set_not_controlability(self):
        c0 = 0
        c1 = 0
        for connection in self.input_connections:
            c0 = connection.controlability_to_one
        for connection in self.input_connections:
            c1 = connection.controlability_to_zero
            
        c0 += 1
        c1 += 1
            
        self.output_connection.controlability_to_zero = c0
        self.output_connection.controlability_to_one = c1 
        
    def set_nor_controlability(self):
        c0 = 0
        c1 = 10**1000
        for connection in self.input_connections:
            c0 = min(c1, connection.controlability_to_one)
        for connection in self.input_connections:
            c1 = c1 + connection.controlability_to_zero
            
        c0 += 1
        c1 += 1
            
        self.output_connection.controlability_to_zero = c0
        self.output_connection.controlability_to_one = c1      
    
    def set_or_controlability(self):
        c0 = 0
        c1 = 10**1000
        for connection in self.input_connections:
            c1 = min(c1, connection.controlability_to_one)
        for connection in self.input_connections:
            c0 = c0 + connection.controlability_to_zero
            
        c0 += 1
        c1 += 1
            
        self.output_connection.controlability_to_zero = c0
        self.output_connection.controlability_to_one = c1  
        
    def set_and_controlability(self):
        c0 = 10**1000
        c1 = 0
        for connection in self.input_connections:
            c0 = min(c0, connection.controlability_to_zero)
        for connection in self.input_connections:
            c1 = c1 + connection.controlability_to_one
            
        c0 += 1
        c1 += 1
            
        self.output_connection.controlability_to_zero = c0
        self.output_connection.controlability_to_one = c1 
        
    def set_nand_controlability(self):
        c0 = 0
        c1 = 10**1000
        for connection in self.input_connections:
            c1 = min(c1, connection.controlability_to_zero)
        for connection in self.input_connections:
            c0 = c0 + connection.controlability_to_one
            
        c0 += 1
        c1 += 1
            
        self.output_connection.controlability_to_zero = c0
        self.output_connection.controlability_to_one = c1  
    
    def set_level(self):
        max_input_level = 0
        for connection in self.input_connections:
                if connection.level == None:
                    max_input_level = None
                    break
                elif connection.level > max_input_level:
                    max_input_level = connection.level

        if max_input_level != None:
            self.level = max_input_level + 1
            self.output_connection.set_level(max_input_level + 1) 
                
    def draw(self):
        input_names = [f"{conn.name} (ID: {conn.id})" for conn in self.input_connections]
        output_name = f"{self.output_connection.name} (ID: {self.output_connection.id})" if self.output_connection else "None"
        print(f"  Gate ID: {self.id}")
        print(f"    Type: {self.gate_type}")
        print(f"    Delay: {self.delay}")
        print(f"    Level: {(self.level)}")
        print(f"    Inputs: {', '.join(input_names)}")
        print(f"    Output: {output_name}\n")
        
    def get_and_gate_output(self, inputs):
        # If any input is 0, output is 0
        if 0 in inputs:
            return 0

        # If all inputs are 1, output is 1
        if all(inp == 1 for inp in inputs):
            # print("all ones")
            return 1

        # If any input is 'U', output is 'U'
        if 'U' in inputs:
            return 'U'

        # If any input is 'Z', output is 'Z'
        if 'Z' in inputs:
            return 'Z'

        # Default to 'U' for any other unforeseen cases
        return 'U'

    def get_nand_gate_output(self, inputs):
        and_output = self.get_and_gate_output(inputs)
        return self.invert_logic_state(and_output)

    def get_or_gate_output(self, inputs):
        # If any input is 1, output is 1
        if 1 in inputs:
            return 1

        # If all inputs are 0, output is 0
        if all(inp == 0 for inp in inputs):
            return 0

        # If any input is 'U', output is 'U'
        if 'U' in inputs:
            return 'U'

        # If any input is 'Z', output is 'Z'
        if 'Z' in inputs:
            return 'Z'

        # Default to 'U' for any other unforeseen cases
        return 'U'

    def get_nor_gate_output(self, inputs):
        or_output = self.get_or_gate_output(inputs)
        return self.invert_logic_state(or_output)

    def get_xor_gate_output(self, inputs):
        count_one = inputs.count(1)
        count_zero = inputs.count(0)
        count_U = inputs.count('U')
        count_Z = inputs.count('Z')

        # If any input is 'U', output is 'U'
        if count_U > 0:
            return 'U'

        # If any input is 'Z' and not all are 'Z', output is 'U'
        if count_Z > 0 and count_Z != len(inputs):
            return 'U'

        # XOR is true if an odd number of inputs are 1
        if count_one % 2 == 1:
            return 1
        else:
            return 0

    def get_xnor_gate_output(self, inputs):
        xor_output = self.get_xor_gate_output(inputs)
        return self.invert_logic_state(xor_output)

    def get_not_gate_output(self, inputs):
        print(len(inputs), self.id)
        if len(inputs) != 1:
            raise ValueError("NOT gate must have exactly one input.")

        inp = inputs[0]

        if inp == 1:
            return 0
        elif inp == 0:
            return 1
        elif inp == 'U':
            return 'U'
        elif inp == 'Z':
            return 'Z'
        else:
            return 'U'

    def get_buf_gate_output(self, inputs):
        if len(inputs) != 1:
            raise ValueError("BUF gate must have exactly one input.")

        inp = inputs[0]
        return inp  # Buffer simply outputs the input as-is

    @staticmethod
    def invert_logic_state(state):
        if state == 1:
            return 0
        elif state == 0:
            return 1
        elif state in ['U', 'Z']:
            return state  
        else:
            return 'U'
    
    def get_inputs_with_delay(self, time):
        inputs = []
        acceptable_value_time = time - self.delay  
        for connection in self.input_connections:
            # print(connection.name)
            value = 'U'
            if connection.value_time < acceptable_value_time: #value is set before the delay
                value = connection.current_value
                        
                
            elif len(connection.history_of_values) > 0:
                for index, value_time in enumerate(connection.history_of_times):
                    if value_time <= acceptable_value_time:
                        value = connection.history_of_values[index]
                
            if value == '1' or value == '0':
                value = int(value)
                # print(f"value converted: {value}")    
            # print(f"value: {value}")    
            inputs.append(value)
        return inputs
          
    def get_inputs_without_delay(self, time):
        inputs = []
        for connection in self.input_connections:
                if connection.current_value == '1' or connection.current_value == '0':
                    inputs.append(int(connection.current_value))
                else:
                    inputs.append(connection.current_value)
        return inputs
    
    def pass_values(self, time, delay_consideration):

        inputs = []
        if delay_consideration is True:
            inputs = self.get_inputs_with_delay(time)
                       
        elif delay_consideration == False: # Without delay_consideration
            inputs = self.get_inputs_without_delay(time)
            
        output = None
        if self.gate_type == 'and':
            output = self.get_and_gate_output(inputs)
        elif self.gate_type == 'nand':
            output = self.get_nand_gate_output(inputs)
        elif self.gate_type == 'or':
            output = self.get_or_gate_output(inputs)
        elif self.gate_type == 'nor':
            output = self.get_nor_gate_output(inputs)
        elif self.gate_type == 'xor':
            output = self.get_xor_gate_output(inputs)
        elif self.gate_type == 'xnor':
            output = self.get_xnor_gate_output(inputs)
        elif self.gate_type == 'not':
            output = self.get_not_gate_output(inputs)
        elif self.gate_type == 'buf':
            output = self.get_buf_gate_output(inputs)
        else:
            raise ValueError(f"Unsupported gate type: {self.gate_type}")
        if self.output_connection:
            self.output_connection.update_value(output, time)

    
    def can_set_controlability(self):
        for connection in self.input_connections:
            if connection.controlability_to_one == None or connection.controlability_to_zero == None:
                return False
        return True
