import struct

from .._exceptions import ReadError
from .._helpers import register
from . import _gmsh22, _gmsh40, _gmsh41

_readers = {"2": _gmsh22, "4": _gmsh40, "4.0": _gmsh40, "4.1": _gmsh41}
_writers = {"2": _gmsh22, "4": _gmsh41, "4.0": _gmsh40, "4.1": _gmsh41}


def read(filename):
    """Reads a Gmsh msh file.
    """
    with open(filename, "rb") as f:
        mesh = read_buffer(f)
    return mesh


def read_buffer(f):
    # The various versions of the format are specified at
    # <http://gmsh.info/doc/texinfo/gmsh.html#File-formats>.
    line = f.readline().decode("utf-8").strip()

    # skip any $Comments/$EndComments sections
    while line == "$Comments":
        while line != "$EndComments":
            line = f.readline().decode("utf-8").strip()
        line = f.readline().decode("utf-8").strip()

    if line != "$MeshFormat":
        raise ReadError()
    fmt_version, data_size, is_ascii = _read_header(f)

    try:
        reader = _readers[fmt_version]
    except KeyError:
        try:
            reader = _readers[fmt_version.split(".")[0]]
        except KeyError:
            raise ValueError(
                "Need mesh format in {} (got {})".format(
                    sorted(_readers.keys()), fmt_version
                )
            )
    return reader.read_buffer(f, is_ascii, data_size)


def _read_header(f):
    """Read the mesh format block

    specified as

     version(ASCII double; currently 4.1)
       file-type(ASCII int; 0 for ASCII mode, 1 for binary mode)
       data-size(ASCII int; sizeof(size_t))
     < int with value one; only in binary mode, to detect endianness >

    though here the version is left as str
    """

    # http://gmsh.info/doc/texinfo/gmsh.html#MSH-file-format

    line = f.readline().decode("utf-8")
    # Split the line
    # 4.1 0 8
    # into its components.
    str_list = list(filter(None, line.split()))
    fmt_version = str_list[0]
    if str_list[1] not in ["0", "1"]:
        raise ReadError()
    is_ascii = str_list[1] == "0"
    data_size = int(str_list[2])
    if not is_ascii:
        # The next line is the integer 1 in bytes. Useful for checking endianness.
        # Just assert that we get 1 here.
        one = f.read(struct.calcsize("i"))
        if struct.unpack("i", one)[0] != 1:
            raise ReadError()
    # Fast forward to $EndMeshFormat
    line = f.readline().decode("utf-8")
    while line.strip() != "$EndMeshFormat":
        line = f.readline().decode("utf-8")
    return fmt_version, data_size, is_ascii


def write(filename, mesh, fmt_version="4.1", binary=True):
    """Writes a Gmsh msh file.
    """
    try:
        writer = _writers[fmt_version]
    except KeyError:
        try:
            writer = _writers[fmt_version.split(".")[0]]
        except KeyError:
            raise ValueError(
                "Need mesh format in {} (got {})".format(
                    sorted(_writers.keys()), fmt_version
                )
            )

    writer.write(filename, mesh, binary=binary)


register(
    "gmsh",
    [".msh"],
    read,
    {
        "gmsh": lambda f, m, **kwargs: write(f, m, "4", **kwargs, binary=True),
        "gmsh2-ascii": lambda f, m, **kwargs: write(f, m, "2", **kwargs, binary=False),
        "gmsh2-binary": lambda f, m, **kwargs: write(f, m, "2", **kwargs, binary=True),
        "gmsh4-ascii": lambda f, m, **kwargs: write(f, m, "4", **kwargs, binary=False),
        "gmsh4-binary": lambda f, m, **kwargs: write(f, m, "4", **kwargs, binary=True),
    },
)
