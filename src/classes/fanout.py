class Fanout:
    def __init__(self, id, input_connection, output_connections):
        self.id = id
        self.input_connection = input_connection
        self.output_connections = output_connections