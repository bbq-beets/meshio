import numpy

num_nodes_per_cell = {
    "vertex": 1,
    "line": 2,
    "triangle": 3,
    "quad": 4,
    "quad8": 8,
    "tetra": 4,
    "hexahedron": 8,
    "hexahedron20": 20,
    "wedge": 6,
    "pyramid": 5,
    #
    "line3": 3,
    "triangle6": 6,
    "quad9": 9,
    "tetra10": 10,
    "hexahedron27": 27,
    "wedge15": 15,
    "wedge18": 18,
    "pyramid13": 13,
    "pyramid14": 14,
    #
    "line4": 4,
    "triangle10": 10,
    "quad16": 16,
    "tetra20": 20,
    "wedge40": 40,
    "hexahedron64": 64,
    #
    "line5": 5,
    "triangle15": 15,
    "quad25": 25,
    "tetra35": 35,
    "wedge75": 75,
    "hexahedron125": 125,
    #
    "line6": 6,
    "triangle21": 21,
    "quad36": 36,
    "tetra56": 56,
    "wedge126": 126,
    "hexahedron216": 216,
    #
    "line7": 7,
    "triangle28": 28,
    "quad49": 49,
    "tetra84": 84,
    "wedge196": 196,
    "hexahedron343": 343,
    #
    "line8": 8,
    "triangle36": 36,
    "quad64": 64,
    "tetra120": 120,
    "wedge288": 288,
    "hexahedron512": 512,
    #
    "line9": 9,
    "triangle45": 45,
    "quad81": 81,
    "tetra165": 165,
    "wedge405": 405,
    "hexahedron729": 729,
    #
    "line10": 10,
    "triangle55": 55,
    "quad100": 100,
    "tetra220": 220,
    "wedge550": 550,
    "hexahedron1000": 1000,
    #
    "line11": 11,
    "triangle66": 66,
    "quad121": 121,
    "tetra286": 286,
}


def cell_data_from_raw(cells, cell_data_raw):
    cell_data = {k: {} for k in cells}
    for key in cell_data_raw:
        d = cell_data_raw[key]
        r = 0
        for k in cells:
            cell_data[k][key] = d[r : r + len(cells[k])]
            r += len(cells[k])
    return cell_data


def raw_from_cell_data(cell_data):
    # merge cell data
    cell_data_raw = {}
    for d in cell_data.values():
        for name, values in d.items():
            if name in cell_data_raw:
                cell_data_raw[name].append(values)
            else:
                cell_data_raw[name] = [values]
    for name in cell_data_raw:
        cell_data_raw[name] = numpy.concatenate(cell_data_raw[name])

    return cell_data_raw


def write_xml(filename, root, pretty_print=False):
    from lxml import etree as ET

    tree = ET.ElementTree(root)
    tree.write(filename, pretty_print=pretty_print)


# https://www.vtk.org/doc/nightly/html/vtkCellType_8h_source.html
vtk_to_meshio_type = {
    0: "empty",
    1: "vertex",
    # 2: 'poly_vertex',
    3: "line",
    # 4: 'poly_line',
    5: "triangle",
    # 6: 'triangle_strip',
    7: "polygon",
    # 8: 'pixel',
    9: "quad",
    10: "tetra",
    # 11: 'voxel',
    12: "hexahedron",
    13: "wedge",
    14: "pyramid",
    15: "penta_prism",
    16: "hexa_prism",
    21: "line3",
    22: "triangle6",
    23: "quad8",
    24: "tetra10",
    25: "hexahedron20",
    26: "wedge15",
    27: "pyramid13",
    28: "quad9",
    29: "hexahedron27",
    30: "quad6",
    31: "wedge12",
    32: "wedge18",
    33: "hexahedron24",
    34: "triangle7",
    35: "line4",
    #
    # 60: VTK_HIGHER_ORDER_EDGE,
    # 61: VTK_HIGHER_ORDER_TRIANGLE,
    # 62: VTK_HIGHER_ORDER_QUAD,
    # 63: VTK_HIGHER_ORDER_POLYGON,
    # 64: VTK_HIGHER_ORDER_TETRAHEDRON,
    # 65: VTK_HIGHER_ORDER_WEDGE,
    # 66: VTK_HIGHER_ORDER_PYRAMID,
    # 67: VTK_HIGHER_ORDER_HEXAHEDRON,
}
meshio_to_vtk_type = {v: k for k, v in vtk_to_meshio_type.items()}
