def parse_iscas_netlist(file_path):
    """
    Parses an ISCAS netlist file and returns a dictionary representation of the circuit.

    Parameters:
        file_path (str): The path to the ISCAS netlist file.

    Returns:
        dict: A dictionary with keys 'inputs', 'outputs', and 'gates'. 'inputs' and 'outputs' are lists
              of signal names. 'gates' is a dictionary where each key is a gate name and each value is
              a dictionary with keys 'type' and 'inputs'.
    """
    import re

    inputs = []
    outputs = []
    gates = {}

    # Regular expressions for parsing
    input_re = re.compile(r'^INPUT\((\w+)\)')
    output_re = re.compile(r'^OUTPUT\((\w+)\)')
    gate_re = re.compile(r'^(\w+)\s*=\s*(\w+)\((.*)\)')

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Match INPUT declarations
            input_match = input_re.match(line)
            if input_match:
                input_name = input_match.group(1)
                inputs.append(input_name)
                continue

            # Match OUTPUT declarations
            output_match = output_re.match(line)
            if output_match:
                output_name = output_match.group(1)
                outputs.append(output_name)
                continue

            # Match gate definitions
            gate_match = gate_re.match(line)
            if gate_match:
                gate_name = gate_match.group(1)
                gate_type = gate_match.group(2)
                gate_inputs = [s.strip() for s in gate_match.group(3).split(',')]
                gates[gate_name] = {
                    'type': gate_type,
                    'inputs': gate_inputs
                }
                continue

            # Handle unrecognized lines
            raise ValueError(f"Unrecognized line format: {line}")

    return {
        'inputs': inputs,
        'outputs': outputs,
        'gates': gates
    }
