import re
from gate import Gate
from circuit import Circuit
from connection import Connection
from fanout import Fanout

def parse_iscas(file_path):
    """
    Parses a custom ISCAS netlist file and returns a Circuit object.

    Parameters:
        file_path (str): The path to the ISCAS netlist file.

    Returns:
        Circuit: An instance of the Circuit class containing gates, input_connections, output_connections, and fanouts.
    """
    gates = []
    gate_dict = {}
    signal_connections = {}  # Map signal names to Connection objects
    input_connections = []
    output_connections = []
    used_as_input_signals = set()
    current_gate = None

    connection_id_counter = 1  # To assign unique IDs to connections
    fanouts = []
    fanout_id_counter = 1  # To assign unique IDs to fanouts

    known_gate_types = {'and', 'nand', 'or', 'nor', 'not', 'xor', 'xnor', 'buff', 'inpt'}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('*'):
                continue

            # Split the line into parts
            parts = line.split()

            # Check if the line is a fanout definition line (when 'from' is in parts)
            if len(parts) >= 4 and 'from' in parts:
                from_index = parts.index('from')
                if from_index >= 2:
                    # It's a fanout definition line
                    fanout_index = parts[0]
                    fanout_signal_name = parts[1]
                    source_signal_name = parts[from_index + 1]
                    # Optional attributes
                    extra_info = parts[from_index + 2:]
                    # Handle '>sa1' or other attributes if necessary

                    # Get or create the Connection object for the source signal
                    if source_signal_name in signal_connections:
                        source_conn = signal_connections[source_signal_name]
                    else:
                        # Create a new Connection for the source signal
                        source_conn = Connection(
                            id=connection_id_counter,
                            name=source_signal_name,
                            source=None,  # Will be set when the source is defined
                            destination=None
                        )
                        connection_id_counter += 1
                        signal_connections[source_signal_name] = source_conn

                    # Create a Connection object for the fanout signal
                    fanout_conn = Connection(
                        id=connection_id_counter,
                        name=fanout_signal_name,
                        source=source_conn.source,  # Same source as source_conn
                        destination=None  # Will be set when the gate consuming it is parsed
                    )
                    connection_id_counter += 1
                    signal_connections[fanout_signal_name] = fanout_conn

                    # Create a Fanout object
                    fanout = Fanout(
                        id=fanout_index,
                        input_connection=source_conn,
                        output_connections=[fanout_conn]
                    )
                    fanouts.append(fanout)

                    # current_gate remains None
                    continue  # Move to the next line
                else:
                    raise ValueError(f"Invalid fanout definition line: {line}")

            # Check if the line is a gate definition line
            if len(parts) >= 3 and parts[2] in known_gate_types:
                gate_index = parts[0]
                signal_name = parts[1]
                gate_type = parts[2]
                # Handle possible extra columns
                extra_info = parts[3:]
                # Handle '>sa1' or other attributes if necessary

                # If gate_type == 'inpt', create a Connection (not a Gate)
                if gate_type == 'inpt':
                    # Create a Connection object for the input signal
                    conn = Connection(
                        id=connection_id_counter,
                        name=signal_name,
                        source=None,
                        destination=None  # Primary inputs have no destination
                    )
                    connection_id_counter += 1
                    signal_connections[signal_name] = conn
                    input_connections.append(conn)
                    # 'inpt' is not a gate, so current_gate remains None
                    current_gate = None
                else:
                    # Create a Gate object
                    gate = Gate(
                        id=gate_index,
                        input_connections=[],
                        output_connection=None,
                        gate_type=gate_type
                    )
                    gate_dict[signal_name] = gate

                    # Create a Connection object for the gate's output
                    output_conn = Connection(
                        id=connection_id_counter,
                        name=signal_name,
                        source=gate,
                        destination=None  # Will be set if this signal is used as input elsewhere
                    )
                    connection_id_counter += 1
                    signal_connections[signal_name] = output_conn
                    gate.output_connection = output_conn

                    # Add gate to the list
                    gates.append(gate)

                    # Store current gate to associate inputs in subsequent lines
                    current_gate = gate
                continue  # Move to the next line

            # If current_gate is not None, this line specifies inputs for the current gate
            if current_gate:
                input_signals = parts
                for input_signal in input_signals:
                    # Mark signal as used as input
                    used_as_input_signals.add(input_signal)

                    # Get or create the Connection object for the input signal
                    if input_signal in signal_connections:
                        conn = signal_connections[input_signal]
                    else:
                        # Create a new Connection object for undefined signals
                        conn = Connection(
                            id=connection_id_counter,
                            name=input_signal,
                            source=None,  # Will be set when the source is defined
                            destination=None
                        )
                        connection_id_counter += 1
                        signal_connections[input_signal] = conn

                    # Set the destination of the connection to the current gate
                    if conn.destination is None:
                        conn.destination = current_gate
                    else:
                        # Handle multiple destinations (fanout)
                        # Create a Fanout object if necessary
                        # Since we now have multiple destinations, we need to handle fanouts
                        fanout_conn = Connection(
                            id=connection_id_counter,
                            name=f"{conn.name}_fanout{fanout_id_counter}",
                            source=conn.source,
                            destination=current_gate
                        )
                        connection_id_counter += 1

                        # Update the signal_connections with the new connection
                        signal_connections[fanout_conn.name] = fanout_conn

                        # Add the new connection to the current gate's inputs
                        current_gate.input_connections.append(fanout_conn)

                        # Create a Fanout object
                        fanout = Fanout(
                            id=fanout_id_counter,
                            input_connection=conn,
                            output_connections=[fanout_conn]
                        )
                        fanout_id_counter += 1
                        fanouts.append(fanout)

                        continue  # Skip adding the original connection

                    # Add the connection to the gate's inputs
                    current_gate.input_connections.append(conn)
            else:
                raise ValueError(f"Unexpected line format without current gate: {line}")

        # Identify output connections (signals not used as inputs)
        for conn_name, conn in signal_connections.items():
            if conn_name not in used_as_input_signals and conn_name not in [c.name for c in input_connections]:
                # This is an output connection
                output_connections.append(conn)

    # Create the Circuit object with fanouts
    circuit = Circuit(
        gates=gates,
        input_connections=input_connections,
        output_connections=output_connections,
        fanouts=fanouts
    )

    return circuit
