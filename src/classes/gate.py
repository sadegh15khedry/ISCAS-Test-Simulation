from logic_state import LogicState
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
        
    # # def get_and_gate_output(self, inputs):
    # def get_and_gate_output(self, inputs):
    #     """
    #     Calculates the output of an AND gate based on its inputs.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the AND gate.

    #     Returns:
    #         LogicState: The output of the AND gate.
    #     """
    #     # If any input is ZERO, the output is ZERO
    #     if any(inp == LogicState.ZERO for inp in inputs):
    #         return LogicState.ZERO

    #     # If all inputs are ONE, the output is ONE
    #     elif all(inp == LogicState.ONE for inp in inputs):
    #         return LogicState.ONE

    #     # If any input is UNKNOWN, the output is UNKNOWN
    #     elif any(inp == LogicState.UNKNOWN for inp in inputs):
    #         return LogicState.UNKNOWN

    #     # If any input is HIGH_IMPEDANCE, the output is HIGH_IMPEDANCE
    #     elif any(inp == LogicState.HIGH_IMPEDANCE for inp in inputs):
    #         return LogicState.HIGH_IMPEDANCE

    #     # Default to UNKNOWN for any other unforeseen cases
    #     else:
    #         return LogicState.UNKNOWN

    # def get_nand_gate_output(self, inputs):
    #     """
    #     Calculates the output of a NAND gate based on its inputs.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the NAND gate.

    #     Returns:
    #         LogicState: The output of the NAND gate.
    #     """
    #     and_output = self.get_and_gate_output(inputs)
    #     return self.invert_logic_state(and_output)

    # def get_or_gate_output(self, inputs):
    #     """
    #     Calculates the output of an OR gate based on its inputs.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the OR gate.

    #     Returns:
    #         LogicState: The output of the OR gate.
    #     """
    #     # If any input is ONE, the output is ONE
    #     if any(inp == LogicState.ONE for inp in inputs):
    #         return LogicState.ONE

    #     # If all inputs are ZERO, the output is ZERO
    #     elif all(inp == LogicState.ZERO for inp in inputs):
    #         return LogicState.ZERO

    #     # If any input is UNKNOWN, the output is UNKNOWN
    #     elif any(inp == LogicState.UNKNOWN for inp in inputs):
    #         return LogicState.UNKNOWN

    #     # If any input is HIGH_IMPEDANCE, the output is HIGH_IMPEDANCE
    #     elif any(inp == LogicState.HIGH_IMPEDANCE for inp in inputs):
    #         return LogicState.HIGH_IMPEDANCE

    #     # Default to UNKNOWN for any other unforeseen cases
    #     else:
    #         return LogicState.UNKNOWN

    # def get_nor_gate_output(self, inputs):
    #     """
    #     Calculates the output of a NOR gate based on its inputs.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the NOR gate.

    #     Returns:
    #         LogicState: The output of the NOR gate.
    #     """
    #     or_output = self.get_or_gate_output(inputs)
    #     return self.invert_logic_state(or_output)

    # def get_xor_gate_output(self, inputs):
    #     """
    #     Calculates the output of an XOR gate based on its inputs.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the XOR gate.

    #     Returns:
    #         LogicState: The output of the XOR gate.
    #     """
    #     count_one = sum(1 for inp in inputs if inp == LogicState.ONE)
    #     count_zero = sum(1 for inp in inputs if inp == LogicState.ZERO)
    #     count_unknown = sum(1 for inp in inputs if inp == LogicState.UNKNOWN)
    #     count_z = sum(1 for inp in inputs if inp == LogicState.HIGH_IMPEDANCE)

    #     # If any input is UNKNOWN, the output is UNKNOWN
    #     if count_unknown > 0:
    #         return LogicState.UNKNOWN

    #     # If any input is HIGH_IMPEDANCE and not all inputs are HIGH_IMPEDANCE, output is UNKNOWN
    #     if count_z > 0 and count_z != len(inputs):
    #         return LogicState.UNKNOWN

    #     # XOR is true if an odd number of inputs are ONE
    #     if count_one % 2 == 1:
    #         return LogicState.ONE
    #     else:
    #         return LogicState.ZERO

    # def get_xnor_gate_output(self, inputs):
    #     """
    #     Calculates the output of an XNOR gate based on its inputs.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the XNOR gate.

    #     Returns:
    #         LogicState: The output of the XNOR gate.
    #     """
    #     xor_output = self.get_xor_gate_output(inputs)
    #     return self.invert_logic_state(xor_output)

    # def get_not_gate_output(self, inputs):
    #     """
    #     Calculates the output of a NOT gate based on its input.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the NOT gate.

    #     Returns:
    #         LogicState: The output of the NOT gate.
    #     """
    #     if len(inputs) != 1:
    #         raise ValueError("NOT gate must have exactly one input.")

    #     inp = inputs[0]

    #     if inp == LogicState.ZERO:
    #         return LogicState.ONE
    #     elif inp == LogicState.ONE:
    #         return LogicState.ZERO
    #     elif inp == LogicState.UNKNOWN:
    #         return LogicState.UNKNOWN
    #     elif inp == LogicState.HIGH_IMPEDANCE:
    #         return LogicState.HIGH_IMPEDANCE
    #     else:
    #         return LogicState.UNKNOWN

    # def get_buf_gate_output(self, inputs):
    #     """
    #     Calculates the output of a BUF (Buffer) gate based on its input.

    #     Parameters:
    #         inputs (list of LogicState): The inputs to the BUF gate.

    #     Returns:
    #         LogicState: The output of the BUF gate.
    #     """
    #     if len(inputs) != 1:
    #         raise ValueError("BUF gate must have exactly one input.")

    #     inp = inputs[0]
    #     return inp  # Buffer simply outputs the input as-is

    # @staticmethod
    # def invert_logic_state(state):
        """
        Inverts the given LogicState.

        Parameters:
            state (LogicState): The LogicState to invert.

        Returns:
            LogicState: The inverted LogicState.
        """
        if state == LogicState.ZERO:
            return LogicState.ONE
        elif state == LogicState.ONE:
            return LogicState.ZERO
        elif state == LogicState.UNKNOWN:
            return LogicState.UNKNOWN
        elif state == LogicState.HIGH_IMPEDANCE:
            return LogicState.HIGH_IMPEDANCE
        else:
            return LogicState.UNKNOWN

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
    
    
    
    
    
    
        
        
    def update_output(self, time):
        inputs = []
        for input in self.input_connections:
            inputs.append(input.current_value)
        
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

            

