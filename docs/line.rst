==================
:mod:`pygame_geometry.Line`
==================

.. currentmodule:: pygame_geometry

.. class:: Line

    | :sl:`pygame object for representing a Line`
    | :sg:`Line(x1, y1, x2, y2) -> Line`
    | :sg:`Line(first, second) -> Line`
    | :sg:`Line(line) -> Line`


    The `Line` class provides many useful methods for collision, transform and intersection.
    A `Line` can be created from a pair of coordinates that represent the first and second
    point of the `Line`. Lines can also be created from python objects that are already a
    `Line` or have an attribute named "line".

    Specifically, to construct a `Line` you can pass the x1, y1, x2, y2 values as
    separate arguments or inside a sequence(list or tuple).

    Functions that require a `Line` argument may also accept these values as Lines:
    ::
        ((x1, y1), (x2, y2))
        (x1, y1, x2, y2)

    **You cannot create degenerate Lines(lines with the same start and end point). If you
    try, the `Line` will not be created and an error will be raised.**

Line Attributes
------
    The `Line` class has both virtual and non-virtual attributes. Non-virtual attributes
    are attributes that are stored in the `Line` object itself. Virtual attributes are the
    result of calculations that utilize the Line's non-virtual attributes.

    Here is the list of all the attributes of the `Line` class:

    .. attribute:: x1
        | :sl:`x coordinate of the first point of the line`
        | :sg:`x1 -> float`

        The `x` coordinate of the first point of the `Line`. It can be reassigned to
        move the `Line`. Reassigning the `x1` attribute will move x position of the first
        point to the new `x` coordinate. The `y1`, `x2`, `y2` attributes will not be affected.

    .. attribute:: y1
        | :sl:`y coordinate of the first point of the line`
        | :sg:`y1 -> float`

        The `y` coordinate of the first point of the `Line`. It can be reassigned to
        move the `Line`. Reassigning the `y1` attribute will move x position of the first
        point to the new `y` coordinate. The `x1`, `x2`, `y2` attributes will not be affected.

    .. attribute:: x2
        | :sl:`x coordinate of the second point of the line`
        | :sg:`x2 -> float`

        The `x` coordinate of the second point of the `Line`. It can be reassigned to
        move the `Line`. Reassigning the `x2` attribute will move x position of the first
        point to the new `x` coordinate. The `x1`, `y1`, `y2` attributes will not be affected.

    .. attribute:: y2
        | :sl:`y coordinate of the second point of the line`
        | :sg:`y2 -> float`

        The `y` coordinate of the second point of the `Line`. It can be reassigned to
        move the `Line`. Reassigning the `y2` attribute will move x position of the first
        point to the new y` coordinate. The `x1`, `y1`, `x2` attributes will not be affected.

    .. attribute:: a
        | :sl:`the first point of the line`
        | :sg:`a -> (float, float)`

        It's a tuple containing the `x1` and `y1` attributes representing the line's first point.
        It can be reassigned to move the `Line`. If reassigned the `x1` and `y1` attributes
        will be changed to produce a `Line` with matching first point position.
        The `x2` and `y2` attributes will not be affected.

    .. attribute:: b
        | :sl:`the second point of the line`
        | :sg:`b -> (float, float)`

        It's a tuple containing `x2` and `y2` attributes representing the line's second point.
        It can be reassigned to move the `Line`. If reassigned the `x2` and `y2` attributes
        will be changed to produce a `Line` with matching second point position.
        The `x1` and `y1` attributes will not be affected.

    .. attribute:: length
        | :sl:`the length of the line`
        | :sg:`length -> float`

        The length of the line. Calculated using the `sqrt((x2-x1)**2 + (y2-y1)**2)` formula.
        This attribute is read-only, it cannot be reassigned. To change the line's length
        use the `scale` method or change its `a` or `b` attributes.

    .. attribute:: angle
        | :sl:`the angle of the line`
        | :sg:`angle -> float`

        The angle of the line representing its orientation. Calculated using
        the `atan2(y2 - y1, x2 - x1)` formula. This attribute is read-only, it cannot
        be reassigned. To change the line's angle use the `rotate` method or change
        its `a` or `b` attributes.

    .. attribute:: slope
        | :sl:`the slope of the line`
        | :sg:`slope -> float`

        The slope of the line. Calculated using the `(y2 - y1) / (x2 - x1)` formula.
        This attribute is read-only, it cannot be reassigned. To change the line's slope
        use the `rotate` method or change its `a` or `b` attributes.

    .. attribute:: center
        | :sl:`the coordinate of the middle point of the line`
        | :sg:`center -> (float, float)`

        The center of the line. Calculated using the `((x1 + x2) / 2, (y1 + y2) / 2)` formula.
        It can be reassigned to move the `Line`. If reassigned the `x1`, `y1`, `x2`, `y2`
        attributes will be changed in order to produce a `Line` with matching center.

    .. attribute:: centerx
        | :sl:`the x coordinate of the middle point of the line`
        | :sg:`centerx -> float`

        The `x` coordinate of the center of the line, it's calculated using
        the `((x1 + x2) / 2)` formula. It can be reassigned to move the `Line`.
        If reassigned the `x1` and `x2` attributes will be changed in order to
        produce a `Line` with matching center. The `y1` and `y2` attributes will not
        be affected.

    .. attribute:: centery
        | :sl:`the y coordinate of the middle point of the line`
        | :sg:`centery -> float`

        The `y` coordinate of the center of the `Line`, it's calculated using
        the `((y1 + y2) / 2)` formula. It can be reassigned to move the `Line`.
        If reassigned the `y1` and `y2` attributes will be changed in order to
        produce a `Line` with matching center. The `x1` and `x2` attributes will not
        be affected.

Line Methods
------
    The Line functions which modify the position, orientation or size return a new copy of
    the `Line` with the affected changes. The original `Line` is not modified.
    Some methods have an alternate "in-place" version that returns `None` but affects the
    original `Line`. These "in-place" methods are denoted with the "ip" suffix.

    Here is the list of all the methods of the `Line` class:

    .. method:: move

        | :sl:`moves the line by a given amount`
        | :sg:`move((x, y)) -> Line`
        | :sg:`move(x, y) -> Line`

        Returns a new Line that is moved by the given offset. The original Line is
        not modified.

        .. note::
            This method is equivalent(behaviour wise) to the following code:
            ::
                Line(line.x1 + x, line.y1 + y, line.x2 + x, line.y2 + y)

      .. ## Line.move ##

    .. method:: move_ip

        | :sl:`moves the line by a given amount`
        | :sg:`move_ip((x, y)) -> None`
        | :sg:`move_ip(x, y) -> None`

        Moves the Line by the given offset. The original Line is modified. Always returns
        None.

        .. note::
            This method is equivalent(behaviour wise) to the following code:
            ::
                line.x1 += x
                line.y1 += y
                line.x2 += x
                line.y2 += y

      .. ## Line.move_ip ##


    .. method:: update

        | :sl:`updates the line's attributes`
        | :sg:`update((x1, y1), (x2, y2)) -> None`
        | :sg:`update(x1, y1, x2, y2) -> None`
        | :sg:`update(Line) -> None`

        Updates the `Line`'s attributes. The original Line is modified. Always returns None.

        .. note::
            This method is equivalent(behaviour wise) to the following code:
            ::
                line.x1 = x1
                line.y1 = y1
                line.x2 = x2
                line.y2 = y2

      .. ## Line.update ##

    .. method:: as_rect

        | :sl:`returns the line as a Rect`
        | :sg:`as_rect() -> Rect`

        Returns a `pygame.Rect` object that contains the Line. The Rect object will be
        the smallest rectangle that contains the Line.

      .. ## Line.as_rect ##

    .. method:: scale

        | :sl:`scales the line by the given factor from the given origin`
        | :sg:`scale(factor, origin) -> Line`
        | :sg:`scale(factor_and_origin) -> Line`

        Returns a new `Line` which is scaled by the given factor from the specified origin with 0.0 being
        the startpoint, 0.5 being the center and 1.0 being the end point.
        The original `Line` is not modified.

      .. ## Line.scale ##

    .. method:: scale_ip

        | :sl:`scales the line by the given factor from the given origin in place`
        | :sg:`scale_ip(factor, origin) -> None`
        | :sg:`scale_ip(factor_and_origin) -> None`

        Scales the `Line` by the given factor from the specified origin with 0.0 being
        the startpoint, 0.5 being the center and 1.0 being the end point.
        The original `Line` is modified.

      .. ## Line.scale_ip ##

    .. method:: flip_ab

        | :sl:`flips the line a and b points`
        | :sg:`flip_ab() -> Line`

        Returns a new `Line` that has the `a` and `b` points flipped.
        The original `Line` is not modified.

      .. ## Line.flip_ab ##

    .. method:: flip_ab_ip

        | :sl:`flips the line a and b points, in place`
        | :sg:`flip_ab_ip() -> None`

        Flips the `Line`'s `b` and `b` points. The original `Line` is modified.
        Always returns None.

      .. ## Line.flip_ab_ip ##

    .. method:: is_parallel

        | :sl:`test if the line is parallel to another line`
        | :sg:`is_parallel(Line) -> bool`

        Returns True if the `Line` is parallel to the given `Line`, False otherwise.

      .. ## Line.is_parallel ##

    .. method:: is_perpendicular

        | :sl:`test if the line is perpendicular to another line`
        | :sg:`is_perpendicular(Line) -> bool`

        Returns True if the `Line` is perpendicular to the given `Line`, False otherwise.

      .. ## Line.is_perpendicular ##


    .. method:: collidepoint

        | :sl:`test if a point is on the line`
        | :sg:`collidepoint((x, y)) -> bool`
        | :sg:`collidepoint(x, y) -> bool`
        | :sg:`collidepoint(Vector2) -> bool`

        Returns True if the given point is on the `Line`, False otherwise.

      .. ## Line.collidepoint ##

    .. method:: collideline

        | :sl:`test if a line intersects with another line`
        | :sg:`collideline(Line) -> bool`
        | :sg:`collideline((x1, y1), (x2, y2)) -> bool`
        | :sg:`collideline(x1, y1, x2, y2) -> bool`

        Returns True if the `Line` intersects with the given `Line`, False otherwise.

      .. ## Line.collideline ##

    .. method:: colliderect

        | :sl:`test if a line intersects with a rectangle`
        | :sg:`colliderect(Rect) -> bool`
        | :sg:`colliderect((x, y, w, h)) -> bool`
        | :sg:`colliderect(x, y, w, h) -> bool`

        Returns True if the `Line` intersects with the given `Rect`, False otherwise.

      .. ## Line.colliderect ##

    .. method:: collidecircle

        | :sl:`test if a line intersects with a circle`
        | :sg:`collidecircle(Circle) -> bool`
        | :sg:`collidecircle((x, y, r)) -> bool`
        | :sg:`collidecircle(x, y, r) -> bool`

        Returns True if the `Line` intersects with the given `Circle`, False otherwise.

      .. ## Line.collidecircle ##

    .. method:: collidepolygon

        | :sl:`test if a line intersects with a polygon`
        | :sg:`collidepolygon(Polygon, only_edges=False) -> bool`
        | :sg:`collidepolygon((x1, y1), (x2, y2), ..., only_edges=False) -> bool`
        | :sg:`collidepolygon(x1, y1, x2, y2, ..., only_edges=False) -> bool`

        Tests whether a given `Polygon` collides with the `Line`.
        It takes either a `Polygon` or Polygon-like object as an argument and it returns
        `True` if the polygon collides with the `Line`, `False` otherwise.

        The optional `only_edges` argument can be set to `True` to only test whether the
        edges of the polygon intersect the `Line`. This means that a Line that is
        inscribed by the `Polygon` or completely outside of it will not be considered colliding.
        This can be useful for performance reasons if you only care about the edges of the
        polygon.

        .. note::
            Keep in mind that the more vertices the polygon has, the more CPU time it will
            take to calculate the collision.

      .. ## Line.collidepolygon ##


    .. method:: collideswith

        | :sl:`test if a shape or point and the line collide`
        | :sg:`collideswith(Line) -> bool`
        | :sg:`collideswith(Circle) -> bool`
        | :sg:`collideswith(Rect) -> bool`
        | :sg:`collideswith(Polygon) -> bool`
        | :sg:`collideswith((x, y)) -> bool`
        | :sg:`contains(Vector2) -> bool`

        Returns `True` if any portion of the shape or point overlaps with the Line,
        `False` otherwise. This is a general alternative to the collision problem as it can
        be used to test for collisions with any shape or point. The shape can be a
        `Line`, `Circle`, `Polygon`, or `Rect`. The point can be a tuple or list containing the x and y
        coordinates of the point or a Vector2.

        .. note::
            If a shape is passed it must be an actual single shape object. It cannot be a
            tuple or list of coordinates that represent the shape. This is because there
            is no way to determine what type of shape the coordinates represent.

        .. note::
            Collisions with a `Polygon` object are evaluated the same way the :meth:`collidepolygon`
            method does by default, meaning with only_edges set to `False`.

      .. ## Line.collideswith ##


    .. method:: as_circle

        | :sl:`returns a circle that extends over the line`
        | :sg:`as_circle() -> Circle`

        Returns a `Circle` object, with the center point being the center point of the `Line`,
        and the diameter being the length of the `Line`.

      .. ## Line.as_circle ##


    .. method:: at

        | :sl:`returns the point at a given distance from the line's a point`
        | :sg:`at(fac) -> (x, y)`

        Returns the point at the given distance from the line's a point.
        The distance can be negative, in which case the point will be on the continuation of
        the line, but in the opposite direction.

      .. ## Line.at ##

    .. method:: copy

        | :sl:`returns a copy of the line`
        | :sg:`copy() -> Line`

        Returns a new `Line` having the same position and radius as the original.

      .. ## Line.copy ##

    .. method:: as_segments

        | :sl:`returns the line as a list of segments`
        | :sg:`as_segments(n_segments) -> [(x, y), (x, y)]`

        Segments the original line into N Lines of equal length and returns a list of
        them. The number of segments is determined by the `n_segments` parameter.

        .. note::
            The original line is not modified. The returned list of lines will always
            have the first line's `a` point at the same position as the original line's `a`
            point and the last line's `b` point at the same position as the original line's
            `b` point.


      .. ## Line.as_segments ##

    .. method:: as_points

        | :sl:`returns the line as a list of points`
        | :sg:`as_points(n_points) -> [(x, y), (x, y)]`

        Returns a list of points that represent the line. The first point in the list
        will be the line's `a` point and the last point will be the line's `b` point.
        The number of points is determined by the `n_points` parameter.

        .. note::
            The n_points parameter refers to the number of points that will created in
            between the line's `a` and `b` points. The number of points returned will
            always be n_points + 2. Because of this the n_points parameter must be at
            least 0.


      .. ## Line.as_points ##

    .. method:: rotate

        | :sl:`rotates the line around its center`
        | :sg:`rotate(angle, rotation_point) -> None`

        Returns a new `Line` that is rotated by the given angle around the given point.
        The angle can be positive or negative. If the angle is positive the line will be
        rotated clockwise and if it is negative the line will be rotated counter-clockwise.

        The rotation point can be a tuple, list, or Vector2. If no rotation point is
        specified the line will be rotated around its center point.

      .. ## Line.rotate ##

    .. method:: rotate_ip

        | :sl:`rotates the line around its center`
        | :sg:`rotate_ip(angle, rotation_point) -> None`

        Rotates the line by the given angle around the given point.
        The angle can be positive or negative. If the angle is positive the line will be
        rotated clockwise and if it is negative the line will be rotated counter-clockwise.

        The rotation point can be a tuple, list, or Vector2. If no rotation point is
        specified the line will be rotated around its center point.

      .. ## Line.rotate_ip ##