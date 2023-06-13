from collections.abc import Callable
from string import ascii_letters

import numpy as np
from scipy.stats import multivariate_normal
import xarray as xr

from attrs import define


length = 10

data = []
t = np.logspace(1, -1, 10)

for _ in range(2):
    x, y, z = (np.sort(np.random.uniform(-0.5, 0.5, length)) for _ in range(3))
    xx, yy, zz = np.meshgrid(x, y, z)
    data.append(
        xr.Dataset(
            data_vars={
                str(i)
                + "".join(np.random.choice([x for x in ascii_letters], 10)): (
                    ["x", "y", "z", "t"],
                    (
                        multivariate_normal.pdf(
                            np.column_stack([d.flat for d in (xx, yy, zz)]),
                            mean=[0, 0, 0],
                        )[..., np.newaxis]
                        * t
                    ).reshape((length, length, length, 10))
                    + np.random.uniform(0, 0.001, (length, length, length, 10)),
                )
                for i in range(2)
            },
            coords=dict(x=x, y=y, z=z, t=t),
        )
    )

data = {str(i): d for i, d in enumerate(data, 1)}


@define
class Operation:
    operation: Callable
    symbol: str


operations = {
    "add": Operation(np.add, "+"),
    "subtract": Operation(np.subtract, "-"),
    "multiply": Operation(np.multiply, "*"),
    "divide": Operation(np.divide, "/"),
}
