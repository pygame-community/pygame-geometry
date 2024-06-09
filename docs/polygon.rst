
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
    separate arguments or inside a Sequence(list or tuple). Generators are also accepted.

    Functions that require a `Polygon` argument may also accept these values as Polygons:
    ::
        ((xa, ya), (xb, yb), (x3, y3), ...)
        [(xa, ya), (xb, yb), (x3, y3), ...]

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

        A list of tuples representing the coordinates of the polygon's vertices.
        You can modify the vertices in several ways:

        - Directly reassign the `vertices` attribute: ``polygon.vertices = [(0, 0), (1, 1), (0, 1)]``
        - Index the `Polygon`: ``polygon[0] = (0, 0)``
        - Use the `insert_vertex` method to add a single vertex

        .. note::
            Directly reassigning the `vertices` attribute will always recalculate the center
            of the `Polygon`. This means that even if you change the entire list to the same
            values except for one vertex, changing the entire vertices list is always more
            expensive than changing a single vertex.

            For example, if you have a polygon with vertices [(0, 0), (1, 1), (0, 1)] and
            you want to change the first vertex to (99, 99), you should use ``polygon[0] = (99, 99)``
            instead of ``polygon.vertices = [(99, 99), (1, 1), (0, 1)]``.

        .. note::
            To change a single vertex at an index, the correct method is ``polygon[index] = (x, y)``.
            Do not use ``polygon.vertices[index] = (x, y)`` as this will not change the vertex
            at the specified index but rather the element at the specified index of the
            newly created list of vertices.


    .. attribute:: center
        | :sl:`the center of the polygon`
        | :sg:`center -> (float, float)`

        It's a Tuple representing the coordinates of the center of the `Polygon`.
        It is calculated as the average of all the vertices. It can be reassigned to
        move the `Polygon`. If reassigned, the `Polygon`'s vertices will be moved to
        create a `Polygon` with matching center.

    .. attribute:: centerx
        | :sl:`the x coordinate of the center of the polygon`
        | :sg:`centerx -> float`

        It's the x coordinate of the center of the `Polygon`. It is calculated as the
        average of all the x coordinates of the vertices. It can be reassigned to move
        the `Polygon`. If reassigned, the polygon's vertices will be moved to
        create a `Polygon` with matching center.

    .. attribute:: centery
        | :sl:`the y coordinate of the center of the polygon`
        | :sg:`centery -> float`

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

    .. method:: collideline

        | :sl:`tests if a line intersects the polygon`
        | :sg:`collideline(Line, only_edges=False) -> bool`
        | :sg:`collideline((xa, ya), (xb, yb), only_edges=False) -> bool`
        | :sg:`collideline(xa, ya, xb, yb, only_edges=False) -> bool`

        Tests whether a given `Line` collides with the `Polygon`.
        It takes either a `Line` or Line-like object as an argument and it returns `True`
        if the `Line` collides with the `Polygon`, `False` otherwise.

        The optional `only_edges` argument can be set to `True` to only test whether the
        edges of the polygon intersect the `Line`. This means that a Line that is
        inscribed by the `Polygon` or completely outside of it will not be considered colliding.
        
      .. ## Polygon.collideline ##  

    .. method:: collidecircle

        | :sl:`tests if a circle is inside the polygon`
        | :sg:`collidecircle(Circle, only_edges=False) -> bool`
        | :sg:`collidecircle((x, y), radius, only_edges=False) -> bool`
        | :sg:`collidecircle(x, y, radius, only_edges=False) -> bool`

        Tests whether a given `Circle` collides with the `Polygon`.
        It takes either a `Circle` or Circle-like object as an argument and it returns
        `True` if the circle collides with the `Polygon`, `False` otherwise.

        The optional `only_edges` argument can be set to `True` to only test whether the
        edges of the polygon intersect the `Circle`. This means that a Polygon that is
        completely inscribed in, or circumscribed by the `Circle` will not be considered colliding.

        This can be useful for performance reasons if you only care about the edges of the
        polygon.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to calculate the collision.

      .. ## Polygon.collidecircle ##

    .. method:: as_segments

        | :sl:`returns the line segments of the polygon`
        | :sg:`as_segments() -> list[Line]`

        Returns a list of the line segments of the polygon given as self.

      .. ## Polygon.as_segments ##

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
        | :sg:`rotate(angle, rotation_point) -> Polygon`

        Returns a new Polygon that is rotated by the given angle (in degrees). The original
        Polygon is not modified. The rotation is done around the center of the `Polygon` by
        default but can be changed by passing a different rotation point.

        .. note::
            Rotating the polygon by positive angles will rotate it clockwise, while
            rotating it by negative angles will rotate it counter-clockwise.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to rotate it.

      .. ## Polygon.rotate ##

    .. method:: rotate_ip

        | :sl:`rotates the polygon by a given angle`
        | :sg:`rotate_ip(angle, rotation_point) -> None`

        Rotates the Polygon by the given angle (in degrees). The original Polygon
        is modified. Always returns None. The rotation is done around the center of the
        `Polygon` by default but can be changed by passing a different rotation point.

        .. note::
            Rotating the polygon by positive angles will rotate it clockwise, while
            rotating it by negative angles will rotate it counter-clockwise.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to rotate it.

      .. ## Polygon.rotate_ip ##

    .. method:: is_convex

        | :sl:`checks whether the polygon is convex or concave`
        | :sg:`is_convex() -> bool`

        Checks whether the polygon is convex or concave.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to check if it's convex.

      .. ## Polygon.is_convex ##

    .. method:: insert_vertex
        | :sl:`inserts a new vertex to the polygon`
        | :sg:`insert_vertex(index, (x, y)) -> None`
        | :sg:`insert_vertex(index, Vector2) -> None`

        Adds a new vertex to the `Polygon`'s vertices at the specified index. The method returns `None`.

        .. note::
            The `index` argument can be any positive or negative integer. If the `index` is
            negative, it is counted from the end of the list of vertices. For example, if
            the `index` is -1, the vertex will be inserted at the end of the list. If the
            `index` is positive and greater than the number of vertices, the vertex
            will always be inserted at the end of the list.

            Inserting a vertex at the end of the list:
            ```
            polygon = Polygon([(0,0), (1,0), (1,1)])
            polygon.insert_vertex(-1, (0,1)) # same will happen with 3 or more as index
            print(polygon.vertices)
            # Output: [(0,0), (1,0), (1,1), (0,1)]
            ```

        .. note::
            You can insert as many vertices as memory available, but keep in mind that a larger
            number of vertices will increase CPU usage for tasks such as calculating collisions,
            moving the `Polygon`, copying, etc. It is recommended to keep the number of
            vertices as low as possible.

      .. ## Polygon.insert_vertex ##


    .. method:: remove_vertex
        | :sl:`removes a vertex from the polygon`
        | :sg:`remove_vertex(index) -> None`

        Removes a vertex at the given `index` from the `Polygon`, but only if the `Polygon`
        has more than three vertices already. This method always returns `None`.

        .. note::
            The `index` must be less than the number of vertices in the `Polygon`.
            If `index` is 0, the first vertex will be removed. If `index` is the number
            of vertices in the `Polygon` minus one, the last vertex will be removed.
            If a negative `index` is given, it will be counted from the end of the list of vertices.
            For example, an `index` of -1 will remove the last vertex in the `Polygon`.

        .. note::
            The minimum number of vertices for a `Polygon` is 3 (a triangle), so you cannot
            remove a vertex if the `Polygon` only has 3 vertices.
            If you attempt to do so, the vertex will not be removed and an error will be raised.

      .. ## Polygon.remove_vertex ##

    .. method:: pop_vertex
        | :sl:`removes and returns a vertex from the polygon`
        | :sg:`pop_vertex(index) -> (x, y)`

        Removes and returns the vertex at the given index from the `Polygon`, but only if
        it has more than three vertices already. Returns the removed vertex as a tuple.

        .. note::
            The given index must be less than the number of vertices of the `Polygon`.
            If the index is 0, the first vertex will be removed. If the index is the number
            of vertices of the `Polygon` minus one, the last vertex will be removed.
            If a negative index is given, it will be counted from the end of the list of
            vertices.
        .. note::
            Since the minimum number of vertices for a `Polygon` is 3 (triangle), you
            cannot remove a vertex if the `Polygon` only has 3 vertices. If you try,
            the vertex will not be removed and an error will be raised.

      .. ## Polygon.pop_vertex ##

    .. method:: as_rect

        | :sl:`returns the bounding box of the polygon`
        | :sg:`as_rect() -> Rect`

        Returns a `pygame.Rect` object that contains the `Polygon`. The Rect object will
        be the smallest rectangle that contains the `Polygon`.

        .. note::
            In the case of a polygon with all vertices on a same line or all in the same
            point, the returned Rect will have a width and height of 1. This is because
            the Rect object cannot have a width or height of 0.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to calculate the bounding box.

      .. ## Polygon.as_rect ##

    .. method:: scale

        | :sl:`scales the polygon by a given factor`
        | :sg:`scale(factor) -> Polygon`

        Returns a new Polygon that is scaled by the given factor. The original Polygon is
        not modified. The scaling is done relative to the center of the `Polygon`.

        .. note::
            Using a `factor` greater than 1 will enlarge the `Polygon`.
            Using a `factor` less than 1 will shrink the `Polygon`.

        .. warning::
            Scaling a `Polygon` by a factor very close to 0 could make it disappear.
            This is because the vertices of the `Polygon` will be so close to each other
            that they will be considered to be in the same point. This is a limitation of
            the algorithm used to calculate the collisions and a general limitation of
            the floating point numbers used in computers.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to scale it.

      .. ## Polygon.scale ##

    .. method:: scale_ip

        | :sl:`scales the polygon by a given factor`
        | :sg:`scale_ip(factor) -> None`

        Scales the Polygon from its center by the given factor. The original Polygon is modified.
        Always returns None.

        .. note::
            Using a `factor` greater than 1 will enlarge the `Polygon`.
            Using a `factor` less than 1 will shrink the `Polygon`.

        .. warning::
            Repeatedly scaling a `Polygon` by a factor less than 1 will eventually make it
            disappear. This is because the vertices of the `Polygon` will be so close to
            each other that they will be considered to be in the same point. This is a
            limitation of the algorithm used to calculate the collisions and a general
            limitation of the floating point numbers used in computers.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to scale it.

      .. ## Polygon.scale_ip ##

    .. method:: flip

        | :sl:`flips the polygon`
        | :sg:`flip(x, y, flip_around) -> Polygon`

        Returns a new Polygon that is flipped horizontally and/or vertically. The original
        Polygon is not modified. The flipping is done relative to the given point.
        By default, the flipping is done relative to the center of the `Polygon`.

        .. note::
            If `x` is True, the Polygon will be flipped horizontally.
            If `y` is True, the Polygon will be flipped vertically.
            If `x` and `y` are both True, the Polygon will be flipped
            horizontally and vertically.

      .. ## Polygon.flip ##

    .. method:: flip_ip

        | :sl:`flips the polygon`
        | :sg:`flip_ip(x, y, flip_around) -> None`

        Flips the Polygon horizontally and/or vertically. The original Polygon is modified.
        The flipping is done relative to the given point. By default, the flipping is done
        relative to the center of the `Polygon`. Always returns None.

        .. note::
            If `x` is True, the Polygon will be flipped horizontally.
            If `y` is True, the Polygon will be flipped vertically.
            If `x` and `y` are both True, the Polygon will be flipped
            horizontally and vertically.

       .. ## Polygon.flip_ip ##