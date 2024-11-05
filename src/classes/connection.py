class Connection:
    def __init__(self, id, name, source, destination):
        self.id = id
        self.name = name
        self.source = source
        self.destination = destination
        self.delay = 0
        self.current_value = None
        self.history_of_values = []
        self.history_id = 1
        self.level = None
        
    def update_value(self, vaule, time):
        self.current_value = vaule
        history_entry = {"id": self.history_id, "time": time, "value": self.current_value}
        self.history_of_values.append(history_entry)
        print(f"updated conneciton:{self.name}, to value:{self.current_value}")
        self.history_id += 1
        if self.destination:
            self.destination.update_output(time)
            
    def print_output(self, time):
        print(f"output connection: {self.name}  value: {self.current_value}")

