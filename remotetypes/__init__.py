"""Package for the remoteset distribution."""

import os

import Ice

try:
    slice_path = os.path.join(
        os.path.dirname(__file__),
        "remotetypes.ice",
    )

    Ice.loadSlice(slice_path)
    import remotetypes # noqa: F401

except ImportError:
    slice_path = os.path.join(
        os.path.dirname(__file__),
        "remotetypes.ice",
    )

    Ice.loadSlice(slice_path)
    import remotetypes  # noqa: F401
