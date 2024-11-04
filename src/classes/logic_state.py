from enum import Enum

class LogicState(Enum):
    ZERO = '0'
    ONE = '1'
    UNKNOWN = 'U'
    HIGH_IMPEDANCE = 'Z'

    def __str__(self):
        return self.value