==================
:mod:`pygame_geometry.Polygon`
==================

.. currentmodule:: pygame_geometry

.. class:: Polygon

    | :sl:`pygame object for representing a Polygon`
    | :sg:`Polygon(vertices) -> Polygon`
    | :sg:`Polygon(polygon) -> Polygon`

    The `Polygon` class provides many useful methods for collision, transform and intersection.
    A `Polygon` can be created from a Sequence of coordinates that represent the vertices
    of the `Polygon`. Polygons can also be created from python objects that are already a
    `Polygon` or have an attribute named "polygon".

    Specifically, to construct a `Polygon` you can pass the vertices' positions as
    separate arguments or inside a Sequence(list or tuple).

    Functions that require a `Polygon` argument may also accept these values as Polygons:
    ::
        ((x1, y1), (x2, y2), (x3, y3), ...)
        [(x1, y1), (x2, y2), (x3, y3), ...]

    The Polygon functions which modify the position, orientation or shape return a new
    copy of the `Polygon` with the affected changes. The original `Polygon` is not modified.
    Some methods have an alternate "in-place" version that returns `None` but affects the
    original `Polygon`. These "in-place" methods are denoted with the "ip" suffix.

    The `Polygon` class has both virtual and non-virtual attributes. Non-virtual attributes
    are attributes that are stored in the `Polygon` object itself. Virtual attributes are the
    result of calculations that utilize the Polygon's non-virtual attributes.

    Here is the list of all the attributes of the `Polygon` class:

    .. attribute:: num_verts
        | :sl:`the number of vertices of the polygon`
        | :sg:`num_verts -> int (>=3)`

        The number of vertices of the `Polygon`. It is always >= 3 as a triangle is the
        smallest `Polygon` you can get. The attribute is read-only. If you want to change
        the number of vertices, you have to reassign the 'vertices' attribute
        or use the 'add_vertex' method.

    .. attribute:: vertices
        | :sl:`the vertices of the polygon`
        | :sg:`vertices -> List[Tuple[float, float]]`

        It's a List of Tuples representing the coordinates of the vertices. You can
        change the vertices of the `Polygon` by reassigning this attribute
        directly (e.g. 'polygon.vertices = [(0, 0), (1, 1), (2, 2)]') or by indexing
        the `Polygon` (e.g. 'polygon[0] = (0, 0)'). The former will change all the vertices
        while the latter will only change the selected vertex. If you want to add a
        vertex, you can use the 'add_vertex' method.

    .. attribute:: center
        | :sl:`the center of the polygon`
        | :sg:`center -> (float, float)`

        It's a Tuple representing the coordinates of the center of the `Polygon`.
        It is calculated as the average of all the vertices. It can be reassigned to move the `Polygon`.
        If reassigned, the `Polygon`'s vertices will be moved to create a `Polygon` with matching center.

    .. attribute:: c_x
        | :sl:`the x coordinate of the center of the polygon`
        | :sg:`c_x -> float`

        It's the x coordinate of the center of the `Polygon`. It is calculated as the
        average of all the x coordinates of the vertices. It can be reassigned to move
        the `Polygon`. If reassigned, the polygon's vertices will be moved to
        create a `Polygon` with matching center.

    .. attribute:: c_y
        | :sl:`the y coordinate of the center of the polygon`
        | :sg:`c_y -> float`

        It's the y coordinate of the center of the `Polygon`. It is calculated as the
        average of all the y coordinates of the vertices. It can be reassigned to move
        the `Polygon`. If reassigned, the polygon's vertices will be moved to
        create a `Polygon` with matching center.

    .. attribute:: perimeter
        | :sl:`the perimeter of the polygon`
        | :sg:`perimeter -> float`

        It's the perimeter of the `Polygon`. It is calculated as the sum of the distances
        between all the vertices. This attribute is read-only, it cannot be reassigned.
