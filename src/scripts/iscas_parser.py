import re
from gate import Gate
from circuit import Circuit
from connection import Connection
from fanout import Fanout

def parse_iscas(file_path):
    gates = []
    gate_dict = {}
    signal_connections = {}  # Map signal names to Connection objects
    input_connections = []
    output_connections = []
    connections_used_as_inputs = set()
    current_gate = None

    connection_id_counter = 1  # To assign unique IDs to connections
    fanout_id_counter = 1      # To assign unique IDs to fanouts
    fanouts = []
    fanout_definitions = []    # Store fanout definitions to process after gates
    fanout_dict = {}           # Map input connection names to Fanout objects

    known_gate_types = {'and', 'nand', 'or', 'nor', 'not', 'xor', 'xnor', 'buff', 'inpt'}

    # Read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # First pass: process gate definitions and input gates
    for line in lines:
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('*'):
            continue

        # Split the line into parts
        parts = line.split()

        # Check if the line is a fanout definition (contains 'from')
        if 'from' in parts:
            # Store the fanout definition for later processing
            fanout_definitions.append(parts)
            continue

        # Check if the line is a gate definition line
        if len(parts) >= 3 and parts[2] in known_gate_types:
            gate_index = parts[0]
            gate_name = parts[1]
            gate_type = parts[2]
            # Handle possible extra columns
            extra_info = parts[3:]

            # If gate_type == 'inpt', create a Connection (not a Gate)
            if gate_type == 'inpt':
                # Create a Connection object for the input signal
                conn = Connection(
                    id=connection_id_counter,
                    name=gate_index,  # Use gate_index as signal name
                    source=None,
                    destination=None  # Primary inputs have no destination
                )
                connection_id_counter += 1
                # Map both gate_index and gate_name to the connection
                signal_connections[gate_index] = conn
                signal_connections[gate_name] = conn
                input_connections.append(conn)
                current_gate = None
            else:
                # Create a Gate object
                gate = Gate(
                    id=gate_index,
                    input_connections=[],
                    output_connection=None,
                    delay=None,  # Will be set when inputs are parsed
                    gate_type=gate_type
                )
                # Map both gate_index and gate_name to the gate
                gate_dict[gate_index] = gate
                gate_dict[gate_name] = gate

                # Create a Connection object for the gate's output
                output_conn = Connection(
                    id=connection_id_counter,
                    name=gate_index,  # Use gate_index as signal name
                    source=gate,
                    destination=None  # Will be set if this signal is used as input elsewhere
                )
                connection_id_counter += 1
                # Map both gate_index and gate_name to the connection
                signal_connections[gate_index] = output_conn
                signal_connections[gate_name] = output_conn
                gate.output_connection = output_conn

                # Add gate to the list
                gates.append(gate)

                # Store current gate to associate inputs in subsequent lines
                current_gate = gate
            continue  # Move to the next line

        # If current_gate is not None, this line specifies inputs for the current gate
        if current_gate:
            input_signals = parts
            delay = None

            # Handle the `NOT` gate specifically
            if current_gate.gate_type == 'not':
                # `NOT` gates have exactly one input signal
                if len(input_signals) != 1:
                    raise ValueError(f"NOT gate {current_gate.id} must have exactly one input, found: {input_signals}")
            else:
                # Check if the last item is a number (delay)
                if input_signals and re.match(r'^\d+$', input_signals[-1]):
                    delay = int(input_signals[-1])
                    input_signals = input_signals[:-1]  # Remove delay from input_signals
                    # Set the delay in current_gate
                    current_gate.delay = delay

            # Now process the input_signals
            for input_signal in input_signals:
                # Get the Connection object for the input signal
                conn = signal_connections.get(input_signal)
                if conn is None:
                    # Try to get connection using possible variations
                    possible_names = [
                        input_signal,
                        input_signal + 'gat',
                        input_signal + 'fan'
                    ]
                    for name in possible_names:
                        conn = signal_connections.get(name)
                        if conn:
                            break
                if conn is None:
                    # Create a new Connection object for undefined signals
                    conn = Connection(
                        id=connection_id_counter,
                        name=input_signal,
                        source=None,  # Will be set when the source is defined
                        destination=None
                    )
                    connection_id_counter += 1
                    signal_connections[input_signal] = conn

                # Add the connection to the list of connections used as inputs
                connections_used_as_inputs.add(conn)

                # Set the destination of the connection to the current gate
                if conn.destination is None:
                    conn.destination = current_gate

                # Add the connection to the gate's inputs
                current_gate.input_connections.append(conn)
        else:
            raise ValueError(f"Unexpected line format without current gate: {line}")

    # Second pass: process fanout definitions after gates have been processed
    for parts in fanout_definitions:
        from_index = parts.index('from')
        if from_index >= 2:
            # It's a fanout definition line
            fanout_index = parts[0]
            fanout_signal_name = parts[1]
            source_signal_name = parts[from_index + 1]
            # Optional attributes
            extra_info = parts[from_index + 2:]

            # Get the Connection object for the source signal
            source_conn = signal_connections.get(source_signal_name)
            if source_conn is None:
                raise ValueError(f"Source signal '{source_signal_name}' not found for fanout '{fanout_signal_name}'")

            # Create a Connection object for the fanout signal
            fanout_conn = Connection(
                id=connection_id_counter,
                name=fanout_index,  # Use fanout_index as signal name
                source=source_conn.source,  # Now source_conn.source should be set
                destination=None  # Will be set when the gate consuming it is parsed
            )
            connection_id_counter += 1
            # Map both fanout_index and fanout_signal_name to the fanout connection
            signal_connections[fanout_index] = fanout_conn
            signal_connections[fanout_signal_name] = fanout_conn

            # Add the source connection to the list of connections used as inputs
            connections_used_as_inputs.add(source_conn)

            # Group fanouts by input connection
            # Use source_conn.name as the key in fanout_dict
            fanout = fanout_dict.get(source_conn.name)
            if fanout:
                # Add the new output connection to the existing Fanout object
                fanout.output_connections.append(fanout_conn)
            else:
                # Create a new Fanout object
                fanout = Fanout(
                    id=fanout_id_counter,
                    input_connection=source_conn,
                    output_connections=[fanout_conn]
                )
                fanout_id_counter += 1
                fanouts.append(fanout)
                fanout_dict[source_conn.name] = fanout
        else:
            raise ValueError(f"Invalid fanout definition line: {parts}")

    # Update connections for gates that have inputs from fanouts
    for gate in gates:
        for i, conn in enumerate(gate.input_connections):
            # If the connection's source is None, try to update it from signal_connections
            if conn.source is None:
                updated_conn = signal_connections.get(conn.name)
                if updated_conn is not None:
                    gate.input_connections[i] = updated_conn
                    connections_used_as_inputs.add(updated_conn)

    # Identify output connections (connections that are outputs of gates and not used as inputs)
    for conn in signal_connections.values():
        if (
            isinstance(conn.source, Gate) and
            conn not in connections_used_as_inputs
        ):
            if conn not in output_connections:
                output_connections.append(conn)

    # Create the Circuit object with fanouts
    circuit = Circuit(
        gates=gates,
        input_connections=input_connections,
        output_connections=output_connections,
        fanouts=fanouts
    )

    return circuit






