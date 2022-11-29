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

    **You cannot create degenerate circles(circles with a radius of 0 or less).
    If you try, the `Circle` will not be created and an error will be raised.**
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

        Returns a new Circle that is moved by the given offset. The original Circle is
        not modified.

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

        Moves the circle by the given offset. The original Circle is modified.
        Always returns None.

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

        Sets the position and radius of the circle, in place. The original Circle is
        modified. Always returns None.

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

        Returns a `pygame.Rect` object that contains the circle. The Rect object
        will be the smallest rectangle that contains the circle.

      .. ## Circle.as_rect ##

    .. method:: collidepoint

        | :sl:`test if a point is inside the circle`
        | :sg:`collidepoint((x, y)) -> bool`
        | :sg:`collidepoint(x, y) -> bool`
        | :sg:`collidepoint(Vector2) -> bool`

        Returns True if the point is inside the circle(edge included), False otherwise.

      .. ## Circle.collidepoint ##

    .. method:: collidecircle

        | :sl:`test if two circles collide`
        | :sg:`collidecircle(Circle) -> bool`
        | :sg:`collidecircle(x, y, radius) -> bool`
        | :sg:`collidecircle((x, y), radius) -> bool`

        Returns `True` if any portion of the two circles overlap, `False` otherwise.

        .. note::
            If collidecircle is called with a circle that is the same as the circle
            it is called on, it will always return True.

      .. ## Circle.collidecircle ##

    .. method:: collideline

        | :sl:`test if a line collides with the circle`
        | :sg:`collideline(Line) -> bool`
        | :sg:`collideline((x1, y1), (x2, y2)) -> bool`
        | :sg:`collideline(x1, y1, x2, y2) -> bool`

        Returns True if any portion of the line overlaps with the circle, False otherwise.

      .. ## Circle.collideline ##

    .. method:: colliderect

        | :sl:`checks if a rectangle intersects the circle`
        | :sg:`colliderect(Rect) -> bool`
        | :sg:`colliderect((x, y, width, height)) -> bool`
        | :sg:`colliderect(x, y, width, height) -> bool`
        | :sg:`colliderect((x, y), (width, height)) -> bool`

        Returns True if any portion of the rectangle overlaps with the circle, False otherwise.

      .. ## Circle.colliderect ##

    .. method:: collideswith

        | :sl:`test if a shape or point and the circle collide`
        | :sg:`collideswith(Line) -> bool`
        | :sg:`collideswith(Circle) -> bool`
        | :sg:`collideswith(Rect) -> bool`
        | :sg:`collideswith((x, y)) -> bool`
        | :sg:`contains(Vector2) -> bool`

        Returns `True` if any portion of the shape or point overlaps with the circle,
        `False` otherwise. This is a general alternative to the collision problem as it can
        be used to test for collisions with any shape or point. The shape can be a
        Line, Circle, or Rect. The point can be a tuple or list containing the x and y
        coordinates of the point or a Vector2.

        .. note::
            If a shape is passed it must be an actual single shape object. It cannot be a
            tuple or list of coordinates that represent the shape. This is because there
            is no way to determine what type of shape the coordinates represent.

      .. ## Circle.collideswith ##

    .. method:: contains

        | :sl:`test if a shape or point is inside the circle`
        | :sg:`contains(Line) -> bool`
        | :sg:`contains(Circle) -> bool`
        | :sg:`contains(Rect) -> bool`
        | :sg:`contains(Polygon) -> bool`
        | :sg:`contains((x, y)) -> bool`
        | :sg:`contains(Vector2) -> bool`

        Returns `True` if the shape or point is completely inside the circle, `False`
        otherwise. This is a general alternative to the containment problem as it can
        be used to test for containment of any shape or point. The shape can be a
        `Line`, `Circle`, `Rect` or `Polygon`. The point can be a tuple or list
        containing the `x` and `y` coordinates of the point or a Vector2.

        .. note::
            If a shape is passed it must be an actual single shape object. It cannot be a
            tuple or list of coordinates that represent the shape. This is because there
            is no way to determine what type of shape the coordinates represent.

      .. ## Circle.contains ##

    .. method:: copy

        | :sl:`returns a copy of the circle`
        | :sg:`copy() -> Circle`

        Returns a new `Circle` having the same position and radius as the original.

      .. ## Circle.copy ##