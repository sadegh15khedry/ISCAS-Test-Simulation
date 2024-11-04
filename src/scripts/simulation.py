from iscas_parser import parse_iscas
def simulation(circuit_path, inputs_path, test_vecotors_path):
    circuit = parse_iscas(circuit_path)
    for gate in circuit.gates:
        print (f"gate type: {gate.gate_type}")
        
    for fanout in circuit.fanouts:
        print(f"fanout: {fanout.input_connection.id} -> {len(fanout.output_connections)}")
        
    circuit.draw_circuit()