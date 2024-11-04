import re
from gate import Gate
from circuit import Circuit

def parse_iscas(file_path):
    """
    Parses a custom ISCAS netlist file and returns a Circuit object.

    Parameters:
        file_path (str): The path to the ISCAS netlist file.

    Returns:
        Circuit: An instance of the Circuit class containing gates, inputs, and outputs.
    """
    inputs = []
    outputs = []
    gates = []
    gate_dict = {}
    current_gate = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('*'):
                continue

            # Check if the line starts with numbers (gate definition)
            if re.match(r'^\d+', line):
                parts = line.split()
                if len(parts) >= 3:
                    gate_index = parts[0]
                    gate_name = parts[1]
                    gate_type = parts[2]
                    # Handle possible extra columns
                    extra_info = parts[3:]

                    # Create a Gate object
                    gate = Gate(inputs=[], output=gate_name, gate_type=gate_type)
                    gate.delay = 0  # You can set delay if needed

                    # If gate is an input
                    if gate_type == 'inpt':
                        inputs.append(gate_name)

                    # Add gate to the list and dictionary
                    gates.append(gate)
                    gate_dict[gate_name] = gate

                    # Store current gate to associate inputs in subsequent lines
                    current_gate = gate
                else:
                    # This might be a line specifying inputs for the current gate
                    if current_gate:
                        input_gates = parts
                        current_gate.inputs.extend(input_gates)
                    else:
                        raise ValueError(f"Unexpected line format without current gate: {line}")
            else:
                # This line might be specifying inputs for the current gate
                parts = line.split()
                if current_gate:
                    input_gates = parts
                    current_gate.inputs.extend(input_gates)
                else:
                    raise ValueError(f"Unexpected line format without current gate: {line}")

    # Identify outputs (gates not used as inputs)
    all_inputs = set()
    for gate in gates:
        all_inputs.update(gate.inputs)

    outputs = [gate.output for gate in gates if gate.output not in all_inputs and gate.output not in inputs]

    # Create the Circuit object
    circuit = Circuit(gates=gates, inputs=inputs, outputs=outputs)

    return circuit