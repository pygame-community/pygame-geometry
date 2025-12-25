==================
:mod:`geometry module`
==================

.. currentmodule:: geometry

The geometry module contains classes and functions for working with 2D geometric
objects such as Lines, Circles, and Polygons. Each object has a set of methods
for performing transformations, collisions, and other operations. The module
also contains a suite of standalone functions for performing operations such as
raycasting and other.

Classes
=======

Circle
------
The circle class represents a circle with a center point and radius. It has methods for
performing transformations and checking for collisions with other objects.

**Here is the full list of attributes:**
::
    x: The x coordinate of the center of the circle.

    y: The y coordinate of the center of the circle.

    center: The center point of the circle.

    r: The radius of the circle.

    diameter, d: The diameter of the circle.

    r_sqr: The radius squared of the circle.

    area: The area of the circle.

    circumference: The circumference of the circle.

    top: The top point of the circle.

    bottom: The bottom point of the circle.

    left: The left point of the circle.

    right: The right point of the circle.

**Here is the full list of methods:**
::
    move: Moves the circle by the given amount.

    move_ip: Moves the circle by the given amount in place.

    update: Updates the circle's attributes.

    copy: Returns a copy of the circle.

    collidepoint: Checks if the circle collides with the given point.

    collidecircle: Checks if the circle collides with the given circle.

    collideline: Checks if the circle collides with the given line.

    colliderect: Checks if the circle collides with the given rectangle.

    collidepolygon: Checks if the circle collides with the given polygon.

    collide: Checks if the circle collides with the given object.

    collidelist: Checks if the circle collides with any of the given objects.

    collidelistall: Checks if the circle collides with all of the given objects.

    contains: Checks if the circle fully contains the given object.

    rotate: Rotates the circle by the given amount.

    rotate_ip: Rotates the circle by the given amount in place.

    as_rect: Returns the smallest rectangle that contains the circle.

    intersect: Finds intersections between the circle and another shape.

Additionally to these, the circle shape can also be used as a collider for the ``geometry.raycast`` function.

Line
----
The line class represents a line segment with a start and end point. It has methods for
performing transformations such as movement, rotation, scaling and checking for collisions with
other objects.

**Here is the full list of attributes:**
::
    xa: The x coordinate of the start point of the line.

    ya: The y coordinate of the start point of the line.

    xb: The x coordinate of the end point of the line.

    yb: The y coordinate of the end point of the line.

    a: The start point of the line.

    b: The end point of the line.

    length: The length of the line.

    angle: The angle of the line.

    center: The center of the line.

    centerx: The x coordinate of the center of the line.

    centery: The y coordinate of the center of the line.

    slope: The slope of the line.

**Here is the full list of methods:**
::
    move: Moves the line by the given amount.

    move_ip: Moves the line by the given amount in place.

    rotate: Rotates the line by the given amount.

    rotate_ip: Rotates the line by the given amount in place.

    scale: Scales the line by the given amount.

    scale_ip: Scales the line by the given amount in place.

    flip_ab: Switches the endpoints of the line.

    flip_ab_ip: Switches the endpoints of the line in place.

    update: Updates the line's attributes.

    copy: Returns a copy of the line.

    collidepoint: Checks if the line collides with the given point.

    collidecircle: Checks if the line collides with the given circle.

    collideline: Checks if the line collides with the given line.

    colliderect: Checks if the line collides with the given rectangle.

    collidepolygon: Checks if the line collides with the given polygon.

    collide: Checks if the line collides with the given object.

    as_circle: Returns a circle which fully encloses the line.

    as_rect: Returns the smallest rectangle that contains the line.

    is_parallel: Checks if the line is parallel to the given line.

    is_perpendicular: Checks if the line is perpendicular to the given line.

    at: Returns the point at the given position along the line based on a factor.

    as_segments: returns the line as a list of segments.

    as_points: returns the line as a list of points.

    rotate: Rotates the line by the given amount.

    rotate_ip: Rotates the line by the given amount in place.

Additionally to these, the line shape can also be used as a collider for the ``geometry.raycast`` function.

Polygon
-------
The polygon class represents a polygon with a list of vertices. It has methods for
performing transformations such as movement, rotation, scaling and checking for collisions with
other objects.

**Here is the full list of attributes:**
::
    vertices: The list of vertices of the polygon.

    verts_num: The number of vertices of the polygon.

    center: The center point of the polygon.

    centerx: The x coordinate of the center of the polygon.

    centery: The y coordinate of the center of the polygon.

    perimeter: The perimeter of the polygon.

    area: The area of the polygon.

**Here is the full list of methods:**
::
    move: Moves the polygon by the given amount.

    move_ip: Moves the polygon by the given amount in place.

    copy: Returns a copy of the polygon.

    collidepoint: Checks if the polygon collides with the given point.

    collideline: Checks if the polygon collides with the given line.

    collidecircle: Checks if the polygon collides with the given circle.

    insert_vertex: Adds a vertex to the polygon.

    remove_vertex: Removes a vertex from the polygon.

    pop_vertex: Removes and returns a vertex from the polygon.

    is_convex: Checks if the polygon is convex.

    scale: Scales the polygon by the given amount.

    scale_ip: Scales the polygon by the given amount in place.

    as_rect: Returns the smallest rectangle that contains the polygon.

    as_segments: Returns a list of lines that make up the polygon.

    rotate: Rotates the polygon by the given amount.

    rotate_ip: Rotates the polygon by the given amount in place.

Functions
=========
The geometry module also contains a number of standalone functions for performing operations
such as raycasting and general utility functions.

    .. method:: raycast

        | :sl:`Returns the closest intersection point between a ray and a sequence of colliders`
        | :sg:`raycast(line, colliders) -> (x, y) | None`
        | :sg:`raycast(origin, angle, max_dist, colliders) -> (x, y) | None`
        | :sg:`raycast(origin, direction, max_dist, colliders) -> (x, y) | None`

        This function returns the closest intersection point between a ray and a sequence
        of colliders.
        A ray can be defined by a Line, an origin point and an angle, or an origin point
        and a direction.
        Apart from a Line, which has fixed length, the ray can have any length,
        including infinite length. To define an infinite ray, set the max_dist parameter
        to a negative value. The max_dist parameter cannot be set to 0.
        The colliders can be any sequence of objects Circle, Line, or Rect.

        The function returns a tuple containing the x and y coordinates of the closest intersection
        point, or None if no intersection was found.

      .. ## geometry.raycast ##

    .. method:: regular_polygon

        | :sl:`Returns a regular polygon with the given number of sides`
        | :sg:`regular_polygon(sides, center, radius, angle=0) -> Polygon`

        This function returns a regular polygon with the given number of sides.
        The polygon is centered at the given center point and has the given radius.
        The polygon can be rotated by the given angle through the optional
        `angle` parameter, defaulting to 0.

      .. ## geometry.regular_polygon ##

    .. method:: rect_to_polygon

        | :sl:`Returns a polygon that represents the given rectangle`
        | :sg:`rect_to_polygon(rect) -> Polygon`

        This function is used to convert a rectangle into a polygon.
        The resulting polygon will have four vertices, one for each corner of the
        rectangle. For example, if the input rectangle is specified as Rect(0, 0, 10, 10),
        the resulting polygon will have the following vertices:

        Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])

        which represent the top left, top right, bottom right, and bottom left corners
        of the rectangle, respectively.

      .. ## geometry.rect_to_polygon ##

    .. method:: is_line

        | :sl:`Checks if the given object is a geometry.Line`
        | :sg:`is_line(obj) -> bool`

        This function checks if the given object is a geometry.Line.
        It returns True if the object is a geometry.Line, and False otherwise.

        .. note::

            If the python object subclasses the geometry.Line class, this function will
            return False. Note that this function is equivalent to isinstance(obj, Line).
            Using that isinstance check is better for typechecking with mypy, and more
            explicit - so it’s recommended to use that instead of is_line.
            Utilizing is_line can save an unwanted Line import.

      .. ## geometry.is_line ##

    .. method:: is_circle

        | :sl:`Checks if the given object is a geometry.Circle`
        | :sg:`is_circle(obj) -> bool`

        This function checks if the given object is a geometry.Circle.
        It returns True if the object is a geometry.Circle, and False otherwise.

        .. note::

            If the python object subclasses the geometry.Circle class, this function will
            return False. Note that this function is equivalent to isinstance(obj, Circle).
            Using that isinstance check is better for typechecking with mypy, and more
            explicit - so it’s recommended to use that instead of is_circle.
            Utilizing is_circle can save an unwanted Circle import.

      .. ## geometry.is_circle ##

    .. method:: is_polygon

        | :sl:`Checks if the given object is a geometry.Polygon`
        | :sg:`is_polygon(obj) -> bool`

        This function checks if the given object is a geometry.Polygon.
        It returns True if the object is a geometry.Polygon, and False otherwise.

        .. note::

            If the python object subclasses the geometry.Polygon class, this function will
            return False. Note that this function is equivalent to isinstance(obj, Polygon).
            Using that isinstance check is better for typechecking with mypy, and more
            explicit - so it’s recommended to use that instead of is_polygon.
            Utilizing is_polygon can save an unwanted Polygon import.

      .. ## geometry.is_polygon ##

    .. method:: multiraycast

        | :sl:`Returns a list of intersection points between a sequence of rays and a sequence of colliders`
        | :sg:`multiraycast(rays, colliders) -> [(x, y) | None]`

        This function returns a list of intersection points between a sequence of
        rays and a sequence of colliders.
        The rays parameter is a sequence that can be composed of the following objects:

        - Line objects.
        - Tuples of: origin point, angle, max_dist.
        - Tuples of: origin point, direction, max_dist.
        - Tuples of: origin point, end point.

        Apart from Lines, which have fixed length, the rays can have any length,
        including infinite length. To define an infinite ray, set the max_dist parameter
        to a negative value. The max_dist parameter cannot be set to 0.
        The colliders can be any sequence of objects such as Circle, Line, or Rect.

        The function returns a list of tuples containing the closest intersection point to
        the ray's origin, or None if it couldn't find one.

     .. ## geometry.multiraycast ##
