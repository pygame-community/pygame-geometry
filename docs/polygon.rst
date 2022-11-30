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

    **You cannot create a polygon with less than 3 vertices.**
Polygon Attributes
------
    The `Polygon` class has both virtual and non-virtual attributes. Non-virtual attributes
    are attributes that are stored in the `Polygon` object itself. Virtual attributes are the
    result of calculations that utilize the Polygon's non-virtual attributes.

    Here is the list of all the attributes of the `Polygon` class:

    .. attribute:: num_verts
        | :sl:`the number of vertices of the polygon`
        | :sg:`num_verts -> int (>=3)`

        The number of vertices of the `Polygon`. It is always >= 3 as a triangle is the
        smallest `Polygon` you can have. The attribute is read-only, so it cannot be
        reassigned. If you want to change the number of vertices, you have to reassign
        the 'vertices' attribute or use either of 'add_vertex', 'remove_vertex' or 'pop_vertex'.

    .. attribute:: vertices
        | :sl:`the vertices of the polygon`
        | :sg:`vertices -> List[Tuple[float, float]]`

        It's a List of Tuples representing the coordinates of the vertices. You can
        change the vertices of the `Polygon` by reassigning this attribute
        directly (e.g. 'polygon.vertices = [(0, 0), (1, 1), (2, 2)]') or by indexing
        the `Polygon` (e.g. 'polygon[0] = (0, 0)'). The former will change all the
        vertices while the latter will only change the selected vertex. If you just want
        to add a single vertex, you can use the 'add_vertex' method.

        .. note::
            If you want to change a vertex at a specific index the correct way to do it
            is 'polygon[index] = (x, y)'.
            The code 'polygon.vertices[index] = (x, y)' is not correct as you will not
            change the vertex at the specified index.
            Just as an example by doing 'polygon.vertices[0] = (0, 0)' you will not change
            the first vertex of the actual polygon but rather the first element of the list
            of vertices.

    .. attribute:: center
        | :sl:`the center of the polygon`
        | :sg:`center -> (float, float)`

        It's a Tuple representing the coordinates of the center of the `Polygon`.
        It is calculated as the average of all the vertices. It can be reassigned to
        move the `Polygon`. If reassigned, the `Polygon`'s vertices will be moved to
        create a `Polygon` with matching center.

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

Polygon Methods
------
    The Polygon functions which modify the position, orientation or shape return a new
    copy of the `Polygon` with the affected changes. The original `Polygon` is not modified.
    Some methods have an alternate "in-place" version that returns `None` but affects the
    original `Polygon`. These "in-place" methods are denoted with the "ip" suffix.

    Here is the list of all the methods of the `Polygon` class:

    .. method:: move

        | :sl:`moves the polygon by a given amount`
        | :sg:`move((x, y)) -> Polygon`
        | :sg:`move(x, y) -> Polygon`

        Returns a new Polygon that is moved by the given offset. The original Polygon is
        not modified.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to move it.

      .. ## Polygon.move ##

    .. method:: move_ip

        | :sl:`moves the polygon by a given amount`
        | :sg:`move_ip((x, y)) -> None`
        | :sg:`move_ip(x, y) -> None`

        Moves the Polygon by the given offset. The original Polygon is modified.
        Always returns None.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to move it.

      .. ## Polygon.move_ip ##

    .. method:: collidepoint

        | :sl:`tests if a point is inside the polygon`
        | :sg:`collidepoint((x, y)) -> bool`
        | :sg:`collidepoint(x, y) -> bool`

        Returns True if the given point is inside the `Polygon`, False otherwise.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to calculate the collision.

      .. ## Polygon.collidepoint ##

    .. method:: copy

        | :sl:`returns a copy of the polygon`
        | :sg:`copy() -> Polygon`

        Returns a copy of the `Polygon`. The copy is a new `Polygon` object with the same
        vertices as the original `Polygon`.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to copy it.

      .. ## Polygon.copy ##

    .. method:: rotate

        | :sl:`rotates the polygon by a given angle`
        | :sg:`rotate(angle) -> Polygon`

        Returns a new Polygon that is rotated by the given angle (in degrees). The original
        Polygon is not modified. The rotation is done around the center of the `Polygon`.

        .. note::
            Rotating the polygon by positive angles will rotate it clockwise, while
            rotating it by negative angles will rotate it counter-clockwise.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to rotate it.

      .. ## Polygon.rotate ##

    .. method:: rotate_ip

        | :sl:`rotates the polygon by a given angle`
        | :sg:`rotate_ip(angle) -> None`

        Rotates the Polygon by the given angle (in degrees). The original Polygon
        is modified. Always returns None. The rotation is done around the center of the
        `Polygon`.

        .. note::
            Rotating the polygon by positive angles will rotate it clockwise, while
            rotating it by negative angles will rotate it counter-clockwise.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to rotate it.

      .. ## Polygon.rotate_ip ##

    .. method:: add_vertex <<NOT YET IMPLEMENTED>>

        | :sl:`adds a vertex to the polygon`
        | :sg:`add_vertex(index, (x, y)) -> None`
        | :sg:`add_vertex(index, Vector2) -> None`

        Adds a vertex at the given index to the `Polygon`. Always returns None.

        .. note::
            The given index must be between 0 and the number of vertices - 1.
            If the index is 0, the vertex will be added at the beginning of the list of
            vertices. If the index is the number of vertices of the `Polygon`, the vertex
            will be added at the end of the list of vertices.

        .. note::
            You can add as many vertices as you want, but keep in mind that the more
            vertices you have, the more CPU time it will take to calculate the collisions,
            move the `Polygon`, copying, etc. It is recommended to keep the number of vertices
            as low as possible and as close as the strict minimum as possible.

      .. ## Polygon.add_vertex ##

    .. method:: remove_vertex <<NOT YET IMPLEMENTED>>

        | :sl:`removes a vertex from the polygon`
        | :sg:`remove_vertex(index) -> None`

        Removes a vertex at the given index from the `Polygon`, but only if the `Polygon`
        has more than three vertices already. Always returns None.

        .. note::
            The given index must be between 0 and the number of vertices - 1.
            If the index is 0, the first vertex will be removed. If the index is the number
            of vertices of the `Polygon` minus one, the last vertex will be removed.
        .. note::
            Since the minimum number of vertices for a `Polygon` is 3 (triangle), you
            cannot remove a vertex if the `Polygon` only has 3 vertices. If you try,
            the vertex will not be removed and an error will be raised.

      .. ## Polygon.remove_vertex ##

    .. method:: pop_vertex <<NOT YET IMPLEMENTED>>

        | :sl:`removes and returns a vertex from the polygon`
        | :sg:`pop_vertex(index) -> (x, y)`

        Removes and returns vertex at the given index from the `Polygon`, but only if
        it has more than three vertices already. Returns the removed vertex as a tuple.

        .. note::
            The given index must be between 0 and the number of vertices - 1.
            If the index is 0, the first vertex will be removed. If the index is the number
            of vertices of the `Polygon` minus one, the last vertex will be removed.
        .. note::
            Since the minimum number of vertices for a `Polygon` is 3 (triangle), you
            cannot remove a vertex if the `Polygon` only has 3 vertices. If you try,
            the vertex will not be removed and an error will be raised.

      .. ## Polygon.pop_vertex ##

    .. method:: scale

        | :sl:`scales the polygon by a given factor`
        | :sg:`scale(factor) -> Polygon`

        Returns a new Polygon that is scaled by the given factor. The original Polygon is
        not modified. The scaling is done relative to the center of the `Polygon`.

        .. note::
            Scaling the polygon by a factor greater than 1 will make it bigger, while
            scaling it by a factor less than 1 but greater than 0 will make it smaller.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to scale it.

      .. ## Polygon.scale ##

    .. method:: scale_ip

        | :sl:`scales the polygon by a given factor`
        | :sg:`scale_ip(factor) -> None`

        Scales the Polygon by the given factor. The original Polygon is modified.
        Always returns None. The scaling is done relative to the center of the
        `Polygon`.

        .. note::
            Scaling the polygon by a factor greater than 1 will make it bigger, while
            scaling it by a factor less than 1 but greater than 0 will make it smaller.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to scale it.

      .. ## Polygon.scale_ip ##