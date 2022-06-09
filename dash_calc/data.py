from typing import Callable
import numpy as np
from attrs import define


data = {str(i): x for i, x in enumerate(np.random.random((2,10,10,10)))}

@define
class Operation:
    operation: Callable
    symbol: str

operations = {
    'add': Operation(np.add, '+'),
    'subtract': Operation(np.subtract, '-'),
    'multiply': Operation(np.multiply, '*'),
    'divide': Operation(np.divide, '/'),
}
