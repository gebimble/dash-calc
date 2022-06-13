from typing import Callable
from string import ascii_letters

import numpy as np
import xarray as xr

from attrs import define

length = 10
x = y = z = np.arange(length)

data = [
    xr.Dataset(
        data_vars={''.join(np.random.choice([x for x in ascii_letters], 10)): (['x', 'y', 'z'], d)},
        coords={'x': x, 'y': y, 'z': z}
        ) for d in np.random.random((2,10,10,10))
    ]

data = {str(i): d for i, d in enumerate(data, 1)}

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
