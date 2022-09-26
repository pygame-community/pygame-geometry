==================
:mod:`pygame_geometry.Circle`
==================

.. currentmodule:: pygame_geometry

.. class:: Circle

    | :sl:`pygame object for representing a circle`
    | :sg:`Circle((x, y), radius) -> Circle`
    | :sg:`Circle(x, y, radius) -> Circle`

    The `Circle` class provides many useful methods for collision / transform and intersection.
    A `Circle` can be created from a combination of a pair of coordinates (x, y) that represents
    the center of the circle and a radius. Circles can also be created from python objects that
    are already a `Circle` or have an attribute named "circle".

    Any function that requires a Circle argument also accepts any of these
    values as Circles, the following are all valid ways:
    ::
        ((x, y), radius)
        (x, y, radius)

    The Circle functions that change its position or size return a new copy of the
    Circle with the affected changes. The original Circle is not modified.
    Some methods have an alternate "in-place" version that returns None but affects the
    original Circle. These "in-place" methods are denoted with the "ip" suffix.

    The Circle object has both virtual and non-virtual attributes which can be used
    to move, measure or scale the Circle. The non-virtual attributes are attributes
    that are stored in the Circle object itself. Virtual attributes are the result
    of calculations that utilize the Circle's non-virtual attributes.

    Here is the list of all the attributes of the Circle class:

    .. attribute:: x
        | :sl:`x coordinate of the center of the circle`
        | :sg:`x -> int`
        | :sg:`x = float`

        The `x` coordinate of the center of the circle. It can be reassigned to move the circle.
        Reassigning the `x` attribute will move the circle to the new `x` coordinate.
        The `y` and `r` attributes will not be affected.

    .. attribute:: y
        | :sl:`y coordinate of the center of the circle`
        | :sg:`y -> int`
        | :sg:`y = float`

        The `y` coordinate of the center of the circle. It can be reassigned to move the circle.
        Reassigning the x attribute will move the circle to the new `y` coordinate.
        The `x` and `r` attributes will not be affected.

    .. attribute:: r
        | :sl:`radius of the circle`
        | :sg:`r -> float`
        | :sg:`r = float`

        It is not possible to set the radius to a negative value. It can be reassigned.
        If reassigned it will only change the radius of the circle.
        The circle will not be moved from its original position.

    .. attribute:: r_sqr
        | :sl:`radius of the circle squared`
        | :sg:`r_sqr -> float`

        It is the radius of the circle squared. It can be reassigned. If reassigned, the radius
        of the circle will be changed to the square root of the new value.
        The circle will not be moved from its original position.

    .. attribute:: center
        | :sl:`x and y coordinates of the center of the circle`
        | :sg:`center -> (x, y)`
        | :sg:`center = (x, y)`

        (Virtual attribute)
        It is a tuple of two floats representing the center of the circle. It can be reassigned.
        If reassigned, the circle will be moved to the new position. The radius will not be affected.

    .. attribute:: diameter, d
        | :sl:`diameter of the circle`
        | :sg:`diameter -> float`
        | :sg:`diameter = float`

        (Virtual attribute)
        It can be reassigned. If reassigned the radius will be changed to half the diameter.
        The circle will not be moved from its original position.

    .. attribute:: area
        | :sl:`area of the circle`
        | :sg:`area -> float`
        | :sg:`area = float`

        (Virtual attribute)
        It's calculated using the `area=pi*r*r` formula. It can be reassigned.
        If reassigned it will resize the circle radius to produce a circle with matching
        area. The circle will not be moved from its original position.

    .. attribute:: circumference
        | :sl:`circumference of the circle`
        | :sg:`circumference -> float`
        | :sg:`circumference = float`

        (Virtual attribute)
        It's calculated using the `circumference=2*pi*r` formula. It can be reassigned.
        If reassigned it will resize the circle radius to produce a circle with matching
        circumference. The circle will not be moved from its original position.