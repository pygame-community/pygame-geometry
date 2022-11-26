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

    collideswith: Checks if the circle collides with the given object.

    contains: Checks if the circle contains the given object.

    as_rect: Returns the smallest rectangle that contains the circle.

Additionally to these, the circle shape can also be used as a collider for the ``geometry.raycast`` function.

Line
----
The line class represents a line segment with a start and end point. It has methods for
performing transformations such as movement, rotation, scaling and checking for collisions with
other objects.

**Here is the full list of attributes:**
::
    x1: The x coordinate of the start point of the line.

    y1: The y coordinate of the start point of the line.

    x2: The x coordinate of the end point of the line.

    y2: The y coordinate of the end point of the line.

    a: The start point of the line.

    b: The end point of the line.

    length: The length of the line.

    angle: The angle of the line.

    midpoint: The midpoint of the line.

    midpoint_x: The x coordinate of the midpoint of the line.

    midpoint_y: The y coordinate of the midpoint of the line.

    slope: The slope of the line.

**Here is the full list of methods:**
::
    move: Moves the line by the given amount.

    move_ip: Moves the line by the given amount in place.

    rotate: Rotates the line by the given amount.

    rotate_ip: Rotates the line by the given amount in place.

    scale: Scales the line by the given amount.

    scale_ip: Scales the line by the given amount in place.

    update: Updates the line's attributes.

    copy: Returns a copy of the line.

    collidepoint: Checks if the line collides with the given point.

    collidecircle: Checks if the line collides with the given circle.

    collideline: Checks if the line collides with the given line.

    colliderect: Checks if the line collides with the given rectangle.

    collideswith: Checks if the line collides with the given object.

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

    c_x: The x coordinate of the center of the polygon.

    c_y: The y coordinate of the center of the polygon.

    perimeter: The perimeter of the polygon.

**Here is the full list of methods:**
::
    move: Moves the polygon by the given amount.

    move_ip: Moves the polygon by the given amount in place.

    copy: Returns a copy of the polygon.

    collidepoint: Checks if the polygon collides with the given point.

    insert_vertex: Adds a vertex to the polygon.

    remove_vertex: Removes a vertex from the polygon.

    pop_vertex: Removes and returns a vertex from the polygon.

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