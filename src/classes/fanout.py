class Fanout:
    def __init__(self, id, input_connection, output_connections):
        self.id = id
        self.input_connection = input_connection
        self.output_connections = output_connections
        
        
    def draw(self):
        input_conn_name = f"{self.input_connection.name} (ID: {self.input_connection.id})"
        output_conn_names = [f"{conn.name} (ID: {conn.id})" for conn in self.output_connections]
        print(f"  Fanout ID: {self.id}")
        print(f"    Input: {input_conn_name}")
        print(f"    Outputs: {', '.join(output_conn_names)}\n")