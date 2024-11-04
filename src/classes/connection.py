class Connection:
    def __init__(self, id, name, source, destination):
        self.id = id
        self.name = name
        self.source = source
        self.destination = destination
        self.delay = 0