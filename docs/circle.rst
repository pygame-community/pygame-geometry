==================
:mod:`pygame_geometry.Circle`
==================

.. currentmodule:: pygame_geometry

.. class:: Circle

    | :sl:`pygame object for representing a circle`
    | :sg:`Circle((x, y), radius) -> Circle`
    | :sg:`Circle(x, y, radius) -> Circle`

    The `Circle` class provides many useful methods for collision / transform and intersection.
    A `Circle` can be created from a combination of a pair of coordinates that represent
    the center of the circle and a radius. Circles can also be created from python objects that
    are already a `Circle` or have an attribute named "circle".

    Specifically, to construct a circle you can pass the x, y, and radius values as separate
    arguments or inside a sequence(list or tuple).

    Functions that require a `Circle` argument may also accept these values as Circles:
    ::
        ((x, y), radius)
        (x, y, radius)

    It is important to note that you cannot create degenerate circles, which are circles with
    a radius of 0 or less. If you try to create such a circle, the `Circle` object will not be
    created and an error will be raised. This is because a circle with a radius of 0 or
    less is not a valid geometric object.
Circle Attributes
------
    The `Circle` class has both virtual and non-virtual attributes. Non-virtual attributes
    are attributes that are stored in the `Circle` object itself. Virtual attributes are the
    result of calculations that utilize the Circle's non-virtual attributes.

    Here is the list of all the attributes of the Circle class:

    .. attribute:: x
        | :sl:`x coordinate of the center of the circle`
        | :sg:`x -> float`

        The `x` coordinate of the center of the circle. It can be reassigned to move the circle.
        Reassigning the `x` attribute will move the circle to the new `x` coordinate.
        The `y` and `r` attributes will not be affected.

    .. attribute:: y
        | :sl:`y coordinate of the center of the circle`
        | :sg:`y -> float`

        The `y` coordinate of the center of the circle. It can be reassigned to move the circle.
        Reassigning the `y` attribute will move the circle to the new `y` coordinate.
        The `x` and `r` attributes will not be affected.

    .. attribute:: r
        | :sl:`radius of the circle`
        | :sg:`r -> float`

        It is not possible to set the radius to a negative value. It can be reassigned.
        If reassigned it will only change the radius of the circle.
        The circle will not be moved from its original position.

    .. attribute:: r_sqr
        | :sl:`radius of the circle squared`
        | :sg:`r_sqr -> float`

        It's equivalent to `r*r`. It can be reassigned. If reassigned, the radius
        of the circle will be changed to the square root of the new value.
        The circle will not be moved from its original position.

    .. attribute:: center
        | :sl:`x and y coordinates of the center of the circle`
        | :sg:`center -> (float, float)`

        It's a tuple containing the `x` and `y` coordinates that represent the center
        of the circle. It can be reassigned. If reassigned, the circle will be moved
        to the new position. The radius will not be affected.

    .. attribute:: diameter, d
        | :sl:`diameter of the circle`
        | :sg:`diameter -> float`

        It's calculated using the `d=2*r` formula. It can be reassigned. If reassigned
        the radius will be changed to half the diameter.
        The circle will not be moved from its original position.

    .. attribute:: area
        | :sl:`area of the circle`
        | :sg:`area -> float`

        It's calculated using the `area=pi*r*r` formula. It can be reassigned.
        If reassigned the circle radius will be changed to produce a circle with matching
        area. The circle will not be moved from its original position.

    .. attribute:: circumference
        | :sl:`circumference of the circle`
        | :sg:`circumference -> float`

        It's calculated using the `circumference=2*pi*r` formula. It can be reassigned.
        If reassigned the circle radius will be changed to produce a circle with matching
        circumference. The circle will not be moved from its original position.

    .. attribute:: top
        | :sl:`top coordinate of the circle`
        | :sg:`top -> (float, float)`

        It's a tuple containing the `x` and `y` coordinates that represent the top
        of the circle. It can be reassigned. If reassigned, the circle will be moved
        to the new position. The radius will not be affected.

    .. attribute:: bottom
        | :sl:`bottom coordinate of the circle`
        | :sg:`bottom -> (float, float)`

        It's a tuple containing the `x` and `y` coordinates that represent the bottom
        of the circle. It can be reassigned. If reassigned, the circle will be moved
        to the new position. The radius will not be affected.

    .. attribute:: left
        | :sl:`left coordinate of the circle`
        | :sg:`left -> (float, float)`

        It's a tuple containing the `x` and `y` coordinates that represent the left
        of the circle. It can be reassigned. If reassigned, the circle will be moved
        to the new position. The radius will not be affected.

    .. attribute:: right
        | :sl:`right coordinate of the circle`
        | :sg:`right -> (float, float)`

        It's a tuple containing the `x` and `y` coordinates that represent the right
        of the circle. It can be reassigned. If reassigned, the circle will be moved
        to the new position. The radius will not be affected.

Circle Methods
------
    The `Circle` functions which modify the position or size return a new copy of the
    `Circle` with the affected changes. The original `Circle` is not modified.
    Some methods have an alternate "in-place" version that returns None but affects the
    original `Circle`. These "in-place" methods are denoted with the "ip" suffix.

    Here is the list of all the methods of the Circle class:

    .. method:: move

        | :sl:`moves the circle by a given amount`
        | :sg:`move((x, y)) -> Circle`
        | :sg:`move(x, y) -> Circle`
        | :sg:`move(Vector2) -> Circle`

        The `move` method allows you to create a new `Circle` object that is moved by a given
        offset from the original `Circle`. This is useful if you want to move a `Circle` without
        modifying the original. The move method takes either a tuple of (x, y) coordinates,
        two separate x and y coordinates, or a `Vector2` object as its argument, and returns
        a new `Circle` object with the updated position.

        .. note::
            This method is equivalent(behaviour wise) to the following code:
            ::
                Circle((circle.x + x, circle.y + y), circle.r)

      .. ## Circle.move ##

    .. method:: move_ip

        | :sl:`moves the circle by a given amount, in place`
        | :sg:`move_ip((x, y)) -> None`
        | :sg:`move_ip(x, y) -> None`
        | :sg:`move_ip(Vector2) -> None`

        The `move_ip` method is similar to the move method, but it moves the `Circle` in place,
        modifying the original `Circle` object. This method takes the same types of arguments
        as move, and it always returns None.

        .. note::
            This method is equivalent(behaviour wise) to the following code:
            ::
                circle.x += x
                circle.y += y

      .. ## Circle.move_ip ##

    .. method:: update

        | :sl:`updates the circle position and radius`
        | :sg:`update((x, y), radius) -> None`
        | :sg:`update(x, y, radius) -> None`

        The `update` method allows you to set the position and radius of a `Circle` object in
        place. This method takes either a tuple of (x, y) coordinates, two separate x and
        y coordinates, and a radius as its arguments, and it always returns `None`.

        .. note::
            This method is equivalent(behaviour wise) to the following code:
            ::
                circle.x = x
                circle.y = y
                circle.r = radius

      .. ## Circle.update ##

    .. method:: as_rect

        | :sl:`returns the smallest pygame.Rect object that contains the circle`
        | :sg:`as_rect() -> Rect`

        The `as_rect` method returns a `pygame.Rect` object that represents the smallest
        rectangle that completely contains the `Circle` object. This means that the `Rect`
        object returned by as_rect will have dimensions such that it completely encloses
        the `Circle`, with no part of the `Circle` extending outside of the `Rect`.

        .. note::
            This method is equivalent(behaviour wise) to the following code:
            ::
                Rect(circle.x - circle.r, circle.y - circle.r, circle.r * 2, circle.r * 2)

      .. ## Circle.as_rect ##

    .. method:: collidepoint

        | :sl:`test if a point is inside the circle`
        | :sg:`collidepoint((x, y)) -> bool`
        | :sg:`collidepoint(x, y) -> bool`
        | :sg:`collidepoint(Vector2) -> bool`

        The `collidepoint` method tests whether a given point is inside the `Circle`
        (including the edge of the `Circle`). It takes a tuple of (x, y) coordinates, two
        separate x and y coordinates, or a `Vector2` object as its argument, and returns
        `True` if the point is inside the `Circle`, `False` otherwise.

      .. ## Circle.collidepoint ##

    .. method:: collidecircle

        | :sl:`test if two circles collide`
        | :sg:`collidecircle(Circle) -> bool`
        | :sg:`collidecircle(x, y, radius) -> bool`
        | :sg:`collidecircle((x, y), radius) -> bool`

        The `collidecircle` method tests whether two `Circle` objects overlap. It takes either
        a `Circle` object, a tuple of (x, y) coordinates and a radius, or separate x and y
        coordinates and a radius as its argument, and returns `True` if any portion of the two
        `Circle` objects overlap, `False` otherwise.

        .. note::
            If this method is called with a `Circle` object that is the same as the `Circle`
            it is called on, it will always return `True`.

      .. ## Circle.collidecircle ##

    .. method:: collideline

        | :sl:`test if a line collides with the circle`
        | :sg:`collideline(Line) -> bool`
        | :sg:`collideline((xa, ya), (xb, yb)) -> bool`
        | :sg:`collideline(xa, ya, xb, yb) -> bool`

        The `collideline` method tests whether a given line intersects the `Circle`. It takes
        either a `Line` object, a tuple of two (x, y) coordinate pairs representing the
        endpoints of the line, or four separate x and y coordinates as its argument.
        Returns `True` if any portion of the line overlaps with the `Circle`, `False` otherwise.

      .. ## Circle.collideline ##

    .. method:: colliderect

        | :sl:`checks if a rectangle intersects the circle`
        | :sg:`colliderect(Rect) -> bool`
        | :sg:`colliderect((x, y, width, height)) -> bool`
        | :sg:`colliderect(x, y, width, height) -> bool`
        | :sg:`colliderect((x, y), (width, height)) -> bool`

        The `colliderect` method tests whether a given rectangle intersects the `Circle`. It
        takes either a `Rect` object, a tuple of (x, y, width, height) coordinates, or separate
        x, y coordinates and width, height as its argument. Returns `True` if any portion
        of the rectangle overlaps with the `Circle`, `False` otherwise.

      .. ## Circle.colliderect ##

    .. method:: collidepolygon

        | :sl:`checks if a polygon intersects the circle`
        | :sg:`collidepolygon(Polygon, only_edges=False) -> bool`
        | :sg:`collidepolygon((xa, ya), (xb, yb), ..., only_edges=False) -> bool`
        | :sg:`collidepolygon((xa, ya), (xb, yb), ..., only_edges=False) -> bool`

        Tests whether a given `Polygon` collides with the `Circle`.
        It takes either a `Polygon` or Polygon-like object as an argument and it returns
        `True` if the polygon collides with the `Circle`, `False` otherwise.

        The optional `only_edges` argument can be set to `True` to only test whether the
        edges of the polygon intersect the `Circle`. This means that a Polygon that is
        completely inscribed in, or circumscribed by the `Circle` will not be considered colliding.
        This can be useful for performance reasons if you only care about the edges of the
        polygon.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to calculate the collision.

      .. ## Circle.collidepolygon ##

    .. method:: collide

        | :sl:`test if a shape or point and the circle collide`
        | :sg:`collide(Line) -> bool`
        | :sg:`collide(Circle) -> bool`
        | :sg:`collide(Rect) -> bool`
        | :sg:`collide(Polygon) -> bool`
        | :sg:`collide((x, y)) -> bool`
        | :sg:`contains(Vector2) -> bool`

        The `collide` method tests whether a given shape or point collides (overlaps)
        with a `Circle` object. The function takes in a single argument, which can be a
        `Line`, `Circle`, `Rect`, `Polygon`, tuple or list containing the x and y coordinates
        of a point, or a `Vector2` object. The function returns a boolean value of `True`
        if there is any overlap between the shape or point and the `Circle` object, or
        `False` if there is no overlap.

        .. note::
            It is important to note that the shape must be an actual shape object, such as
            a `Line`, `Circle`, `Polygon`, or `Rect` instance. It is not possible to pass a tuple
            or list of coordinates representing the shape as an argument(except for a point),
            because the type of shape represented by the coordinates cannot be determined.
            For example, a tuple with the format (a, b, c, d) could represent either a `Line`
            or a Rect object, and there is no way to determine which is which without explicitly
            passing a `Line` or `Rect` object as an argument.

         .. note::
            Collisions with a `Polygon` object are evaluated the same way the :meth:`collidepolygon`
            method does by default, meaning with only_edges set to `False`.

      .. ## Circle.collide ##

    .. method:: collidelist

            | :sl:`test if a list of objects collide with the circle`
            | :sg:`collidelist(colliders) -> int`

            The `collidelist` method tests whether a given list of shapes or points collides
            (overlaps) with this `Circle` object. The function takes in a single argument, which
            must be a list of `Line`, `Circle`, `Rect`, `Polygon`, tuple or list containing the
            x and y coordinates of a point, or `Vector2` objects. The function returns the index
            of the first shape or point in the list that collides with the `Circle` object, or
            -1 if there is no collision.

            .. note::
                It is important to note that the shapes must be actual shape objects, such as
                `Line`, `Circle`, `Polygon`, or `Rect` instances. It is not possible to pass a tuple
                or list of coordinates representing the shape as an argument(except for a point),
                because the type of shape represented by the coordinates cannot be determined.
                For example, a tuple with the format (a, b, c, d) could represent either a `Line`
                or a `Rect` object, and there is no way to determine which is which without
                explicitly passing a `Line` or `Rect` object as an argument.

        .. ## Circle.collidelist ##

    .. method:: collidelistall

            | :sl:`test if all objects in a list collide with the circle`
            | :sg:`collidelistall(colliders) -> list`

            The `collidelistall` method tests whether a given list of shapes or points collides
            (overlaps) with this `Circle` object. The function takes in a single argument, which
            must be a list of `Line`, `Circle`, `Rect`, `Polygon`, tuple or list containing the
            x and y coordinates of a point, or `Vector2` objects. The function returns a list
            containing the indices of all the shapes or points in the list that collide with
            the `Circle` object, or an empty list if there is no collision.

            .. note::
                It is important to note that the shapes must be actual shape objects, such as
                `Line`, `Circle`, `Polygon`, or `Rect` instances. It is not possible to pass a tuple
                or list of coordinates representing the shape as an argument(except for a point),
                because the type of shape represented by the coordinates cannot be determined.
                For example, a tuple with the format (a, b, c, d) could represent either a `Line`
                or a `Rect` object, and there is no way to determine which is which without
                explicitly passing a `Line` or `Rect` object as an argument.

        .. ## Circle.collidelistall ##

    .. method:: contains

        | :sl:`test if a shape or point is inside the circle`
        | :sg:`contains(Line) -> bool`
        | :sg:`contains(Circle) -> bool`
        | :sg:`contains(Rect) -> bool`
        | :sg:`contains(Polygon) -> bool`
        | :sg:`contains((x, y)) -> bool`
        | :sg:`contains(Vector2) -> bool`

        The `contains` method tests whether a given shape or point is completely contained
        within a `Circle` object. The function takes in a single argument, which can be a
        `Line`, `Circle`, `Rect`, `Polygon`, tuple or list containing the x and y coordinates
        of a point, or a `Vector2` object. The function returns a boolean value of `True`
        if the shape or point is completely contained within the `Circle` object, `False`
        otherwise.

        .. note::
            It is important to note that the shape must be an actual shape object, such as
            a `Line`, `Circle`, `Rect`, or `Polygon` instance. It is not possible to pass a tuple
            or list of coordinates representing the shape as an argument(except for a point),
            because the type of shape represented by the coordinates cannot be determined.
            For example, a tuple with the format (a, b, c, d) could represent either a `Line`
            or a `Rect` object, and there is no way to determine which is which without
            explicitly passing a `Line` or `Rect` object as an argument.

      .. ## Circle.contains ##

    .. method:: rotate
        | :sl:`rotates the circle`
        | :sg:`rotate(angle, rotation_point=Circle.center) -> None`

        Returns a new `Circle` that is rotated by the specified angle around a point.
        A positive angle rotates the circle clockwise, while a negative angle rotates it counter-clockwise.
        The rotation point can be a `tuple`, `list`, or `Vector2`.
        If no rotation point is given, the circle will be rotated around its center.

      .. ## Circle.rotate ##

    .. method:: rotate_ip
        | :sl:`rotates the circle in place`
        | :sg:`rotate_ip(angle, rotation_point=Circle.center) -> None`

        This method rotates the circle by a specified angle around a point.
        A positive angle rotates the circle clockwise, while a negative angle rotates it counter-clockwise.
        The rotation point can be a `tuple`, `list`, or `Vector2`.

        If no rotation point is given, the circle will be rotated around its center.

      .. ## Circle.rotate_ip ##

    .. method:: copy

        | :sl:`returns a copy of the circle`
        | :sg:`copy() -> Circle`

        The `copy` method returns a new `Circle` object having the same position and radius
        as the original `Circle` object. The function takes no arguments and returns the
        new `Circle` object.

      .. ## Circle.copy ##

    .. method:: intersect

        | :sl:`finds intersections between the circle and another shape`
        | :sg:`intersect(Circle) -> list[Tuple[float, float]]`

        Returns a list of intersection points between the circle and another shape.
        The other shape must be a `Circle` object.
        If the circle does not intersect or has infinite intersections, an empty list is returned.

        .. note::
            The shape argument must be an instance of the `Circle` class.
            Passing a tuple or list of coordinates representing the shape is not supported,
            as the type of shape cannot be determined from coordinates alone.

      .. ## Circle.intersect ##