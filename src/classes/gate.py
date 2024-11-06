from logic_state import LogicState
class Gate:
    def __init__(self, id, input_connections, output_connection, delay, gate_type):
        self.id = id  # unique identifier for the gate
        self.input_connections = input_connections
        self.output_connection = output_connection
        self.gate_type = gate_type
        self.delay = delay
        self.level = None
        
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
        """
        Calculates the output of an AND gate based on its inputs.

        Parameters:
            inputs (list): The inputs to the AND gate.

        Returns:
            The output of the AND gate (1, 0, 'X', or 'Z').
        """
        # If any input is 0, output is 0
        if 0 in inputs:
            return 0

        # If all inputs are 1, output is 1
        if all(inp == 1 for inp in inputs):
            print("all ones")
            return 1

        # If any input is 'X', output is 'X'
        if 'X' in inputs:
            return 'X'

        # If any input is 'Z', output is 'Z'
        if 'Z' in inputs:
            return 'Z'

        # Default to 'X' for any other unforeseen cases
        return 'X'

    def get_nand_gate_output(self, inputs):
        """
        Calculates the output of a NAND gate based on its inputs.

        Parameters:
            inputs (list): The inputs to the NAND gate.

        Returns:
            The output of the NAND gate (1, 0, 'X', or 'Z').
        """
        and_output = self.get_and_gate_output(inputs)
        return self.invert_logic_state(and_output)

    def get_or_gate_output(self, inputs):
        """
        Calculates the output of an OR gate based on its inputs.

        Parameters:
            inputs (list): The inputs to the OR gate.

        Returns:
            The output of the OR gate (1, 0, 'X', or 'Z').
        """
        # If any input is 1, output is 1
        if 1 in inputs:
            return 1

        # If all inputs are 0, output is 0
        if all(inp == 0 for inp in inputs):
            return 0

        # If any input is 'X', output is 'X'
        if 'X' in inputs:
            return 'X'

        # If any input is 'Z', output is 'Z'
        if 'Z' in inputs:
            return 'Z'

        # Default to 'X' for any other unforeseen cases
        return 'X'

    def get_nor_gate_output(self, inputs):
        """
        Calculates the output of a NOR gate based on its inputs.

        Parameters:
            inputs (list): The inputs to the NOR gate.

        Returns:
            The output of the NOR gate (1, 0, 'X', or 'Z').
        """
        or_output = self.get_or_gate_output(inputs)
        return self.invert_logic_state(or_output)

    def get_xor_gate_output(self, inputs):
        """
        Calculates the output of an XOR gate based on its inputs.

        Parameters:
            inputs (list): The inputs to the XOR gate.

        Returns:
            The output of the XOR gate (1, 0, 'X', or 'Z').
        """
        count_one = inputs.count(1)
        count_zero = inputs.count(0)
        count_X = inputs.count('X')
        count_Z = inputs.count('Z')

        # If any input is 'X', output is 'X'
        if count_X > 0:
            return 'X'

        # If any input is 'Z' and not all are 'Z', output is 'X'
        if count_Z > 0 and count_Z != len(inputs):
            return 'X'

        # XOR is true if an odd number of inputs are 1
        if count_one % 2 == 1:
            return 1
        else:
            return 0

    def get_xnor_gate_output(self, inputs):
        """
        Calculates the output of an XNOR gate based on its inputs.

        Parameters:
            inputs (list): The inputs to the XNOR gate.

        Returns:
            The output of the XNOR gate (1, 0, 'X', or 'Z').
        """
        xor_output = self.get_xor_gate_output(inputs)
        return self.invert_logic_state(xor_output)

    def get_not_gate_output(self, inputs):
        """
        Calculates the output of a NOT gate based on its input.

        Parameters:
            inputs (list): The inputs to the NOT gate.

        Returns:
            The output of the NOT gate (1, 0, 'X', or 'Z').
        """
        if len(inputs) != 1:
            raise ValueError("NOT gate must have exactly one input.")

        inp = inputs[0]

        if inp == 1:
            return 0
        elif inp == 0:
            return 1
        elif inp == 'X':
            return 'X'
        elif inp == 'Z':
            return 'Z'
        else:
            return 'X'

    def get_buf_gate_output(self, inputs):
        """
        Calculates the output of a BUF (Buffer) gate based on its input.

        Parameters:
            inputs (list): The inputs to the BUF gate.

        Returns:
            The output of the BUF gate (1, 0, 'X', or 'Z').
        """
        if len(inputs) != 1:
            raise ValueError("BUF gate must have exactly one input.")

        inp = inputs[0]
        return inp  # Buffer simply outputs the input as-is

    @staticmethod
    def invert_logic_state(state):
        """
        Inverts the given logic state.

        Parameters:
            state: The logic state to invert (1, 0, 'X', or 'Z').

        Returns:
            The inverted logic state (1, 0, 'X', or 'Z').
        """
        if state == 1:
            return 0
        elif state == 0:
            return 1
        elif state in ['X', 'Z']:
            return state  # 'X' and 'Z' remain the same
        else:
            return 'X'
    
    def get_inputs_with_delay(self, time):
        inputs = []
        acceptable_value_time = time - self.delay
        print(f"time: {time}, delay: {self.delay}, acceptable_value_time: {acceptable_value_time}")    
        for connection in self.input_connections:
            print(connection.name)
            value = 'X'
            print(f"connection:{connection.name}, time: {time}, delay: {self.delay}, value_time: {connection.value_time}")    
            if connection.value_time < acceptable_value_time: #value is set before the delay
                print(f" value has been set yet for the connection {connection.name} at time {connection.value_time} whcih is more than the delay {self.delay}")
                value = connection.current_value
                        
                
            elif len(connection.history_of_values) > 0:
                for index, value_time in enumerate(connection.history_of_times):
                    if value_time < acceptable_value_time:
                        print("here")
                        value = connection.history_of_values[index]
                
                
            if value == '1' or value == '0':
                value = int(value)
                # print(f"value converted: {value}")    
            print(f"value: {value}")    
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
            
            
        
        print(f"Gate: {self.id} type: {self.gate_type} , Inputs: {inputs}")
        
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

    def set_level(self):
        max_input_level = 0
        for connection in self.input_connections:
                if connection.level == None:
                    max_input_level = None
                    # print(f"{connection.name} has None conneciotn")
                    break
                elif connection.level > max_input_level:
                    max_input_level = connection.level
                    # print(f"conneciton name: {connection.name} level:{connection.level}")
        if max_input_level != None:
            self.level = max_input_level
            self.output_connection.set_level(max_input_level + 1) 

