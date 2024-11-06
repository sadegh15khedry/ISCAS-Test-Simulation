class Connection:
    def __init__(self, id, name, source, destination):
        self.id = id
        self.name = name
        self.source = source
        self.destination = destination
        self.current_value = 'X'
        self.value_time = 0
        self.history_of_values = []
        self.history_of_times = []
        self.history_id = 1
        self.level = None
        
    def update_value(self, value, time):
        # print(type(time))
        # time = int(time)
        self.current_value = value
        self.value_time = time
        self.history_of_values.append(self.current_value)
        self.history_of_times.append(self.value_time)
        
        # print(f"updated conneciton:{self.name}, to value:{self.current_value}")
        self.history_id += 1

            
    def print_output(self, time):
        print(f"output connection: {self.name}  value: {self.current_value}")
        
        
    def set_level(self, value):
        self.level = value
        # print (f"circuit input: {self.name} level: {self.level}") 
        if self.destination:
            self.destination.set_level()
            

        

