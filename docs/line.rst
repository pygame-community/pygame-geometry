.. include:: common.txt

==================
:mod:`pygame.Line`
==================

.. currentmodule:: pygame

.. class:: Line

    | :sl:`pygame object for storing line coordinates`
    | :sg:`Line(x1, y1, x2, y2) -> Line`
    | :sg:`Line((x1, y1), (x2, y2)) -> Line`
    | :sg:`Line(object) -> Line`

    Pygame uses Line objects to represent lines using coordinates and provide
    useful methods to work with lines. A line can be created from a combination of
    x1, y1, x2 and y2 values. Lines can also be created from python objects that
    are already a Line or have an attribute named "line".

    Any pygame function that requires a Line argument also accepts any of these
    values to construct a Line. This makes it easier to create Lines on the fly
    as arguments to functions.

    The Line object is also iterable:

    ::

      line = Line(0, 1, 2, 3)
      x1, y1, x2, y2 = line


    .. method:: copy

        | :sl:`copy the line`
        | :sg:`copy() -> line`

        Returns a new Line having the same coordinates as the original

        .. ## Line.copy ##

    .. method:: raycast

        | :sl:`cast a ray against a list of shapes/colliders`
        | :sg:`raycast(List[Union[Line, Rect, Circle]]) -> Union[Tuple[float, float], None]`

        Performs a raycast against a list of supported shapes, and returns whether the line
        intersects with each of the shapes or not.
        Returns an x and y coordinate pair (tuple of float values) if there is an intersection
        found. Otherwise returns None if no intersection found.

        .. ## Line.raycast ##


    .. method:: collideline

        | :sl:`check if two lines intersect or not`
        | :sg:`collideline(Line) -> bool`
        | :sg:`collideline(LineLike) -> bool`

        Returns True if the two lines intersect. Otherwise returns False.

        .. ## Line.collideline ##

    .. method:: collidepoint

        | :sl:`check if a point is on a line or not`
        | :sg:`collidepoint(Point) -> bool`
        | :sg:`collidepoint(x, y) -> bool`
        | :sg:`collidepoint(PointLike) -> bool`

        Returns True if the point is on the line. Otherwise returns False.

        .. ## Line.collidepoint ##

    .. method:: collidecircle

        | :sl:`check if the line collides with the given circle or not`
        | :sg:`collidecircle(Circle) -> bool`

        Returns True if the line collides with the circle. Otherwise returns False.

        .. ## Line.collidecircle ##

    .. method:: colliderect

        | :sl:`check if the line collides with the rectangle or not`
        | :sg:`colliderect(Rect) -> bool`
        | :sg:`colliderect(RectLike) -> bool`

        Returns True if the line collides with the Rectangle. Otherwise returns False.

        .. ## Line.colliderect ##

    .. method:: as_rect

        | :sl:`returns the rectangle bounding the given line`
        | :sg:`as_rect() -> Rect`

        Returns a rectangle such that the given line is the diagonal of the rectangle.

        .. ## Line.as_rect ##

    .. method:: update

        | :sl:`update the current line with new values`
        | :sg:`update(Line) -> None`
        | :sg:`update(LineLike) -> None`

        Updates the current line values to the new values provided. Returns None.

        .. ## Line.update ##
