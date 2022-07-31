from typing import Optional, Tuple, Sequence, List

import math

def _calculate_segment_intersection(
    x1: float, y1: float, 
    x2: float, y2: float, 
    x3: float, y3: float, 
    x4: float, y4: float
) -> Optional[Tuple[float, float]]:
    
    x1_m_x2 = x1 - x2
    y3_m_y4 = y3 - y4
    y1_m_y2 = y1 - y2
    x3_m_x4 = x3 - x4
    
    dem = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4

    if dem == 0:
        return

    x1_m_x3 = x1 - x3
    y1_m_y3 = y1 - y3

    t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4
    t = t1 / dem

    u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3
    u = -(u1 / dem)

    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        return (
            x1 + t * (x2 - x1),
            y1 + t * (y2 - y1)
        )
    return

def convert_rect_to_lines(rect):
    return (
        (rect.left, rect.top, rect.right, rect.top),
        (rect.left, rect.bottom, rect.right, rect.bottom),
        (rect.left, rect.top, rect.left, rect.bottom),
        (rect.right, rect.top, rect.right, rect.bottom),
    )

def raycast(
    origin: Sequence[float, float],
    target: Sequence[float, float],
    lines: List[Sequence[Sequence[float, float], Sequence[float, float]]]
) -> Sequence[float, float]:
    # this is old code, might need some optimizations
    x1, y1 = origin
    x2, y2 = target
    line_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    highest_point = (x2, y2)
    highest_point_length = line_length
    for wall in lines:
        try:
            c = _calculate_segment_intersection(
                x1, y1, x2, y2, wall[0], wall[1], wall[2], wall[3]
            )
            c_length = math.sqrt((x1 - c[0]) ** 2 + (y1 - c[1]) ** 2)
            if highest_point_length > c_length:
                highest_point = c
                highest_point_length = c_length
        except:
            pass
    return highest_point
