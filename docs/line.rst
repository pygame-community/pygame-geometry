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

    The Line functions which modify the position, orientation or size return a new copy of
    the `Line` with the affected changes. The original `Line` is not modified.
    Some methods have an alternate "in-place" version that returns `None` but affects the
    original `Line`. These "in-place" methods are denoted with the "ip" suffix.

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

    .. attribute:: midpoint
        | :sl:`the coordinate of the middle point of the line`
        | :sg:`midpoint -> (float, float)`

        The midpoint of the line. Calculated using the `((x1 + x2) / 2, (y1 + y2) / 2)` formula.
        It can be reassigned to move the `Line`. If reassigned the `x1`, `y1`, `x2`, `y2`
        attributes will be changed in order to produce a `Line` with matching midpoint.

    .. attribute:: midpoint_x
        | :sl:`the x coordinate of the middle point of the line`
        | :sg:`midpoint_x -> float`

        The `x` coordinate of the midpoint of the line, it's calculated using
        the `((x1 + x2) / 2)` formula. It can be reassigned to move the `Line`.
        If reassigned the `x1` and `x2` attributes will be changed in order to
        produce a `Line` with matching midpoint. The `y1` and `y2` attributes will not
        be affected.

    .. attribute:: midpoint_y
        | :sl:`the y coordinate of the middle point of the line`
        | :sg:`midpoint_y -> float`

        The `y` coordinate of the midpoint of the `Line`, it's calculated using
        the `((y1 + y2) / 2)` formula. It can be reassigned to move the `Line`.
        If reassigned the `y1` and `y2` attributes will be changed in order to
        produce a `Line` with matching midpoint. The `x1` and `x2` attributes will not
        be affected.