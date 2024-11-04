from iscas_parser import parse_iscas
def simulation(circuit_path, inputs_path, test_vecotors_path):
    circuit = parse_iscas(circuit_path)
    for gate in circuit.gates:
        print (gate.gate_type, gate.inputs, gate.output)