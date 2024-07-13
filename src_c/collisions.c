#include "include/collisions.h"
#include "simd_collisions.h"
#include <stdio.h>

#if defined(__GNUC__) && \
    (__GNUC__ > 2 || (__GNUC__ == 2 && (__GNUC_MINOR__ > 95)))
#define LIKELY(x) __builtin_expect(!!(x), 1)
#define UNLIKELY(x) __builtin_expect(!!(x), 0)
#else
#define LIKELY(x) (x)
#define UNLIKELY(x) (x)
#endif

static int
pgCollision_LineLine(pgLineBase *A, pgLineBase *B)
{
    double x1_m_x2 = A->xa - A->xb;
    double y3_m_y4 = B->ya - B->yb;
    double y1_m_y2 = A->ya - A->yb;
    double x3_m_x4 = B->xa - B->xb;

    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    double x1_m_x3 = A->xa - B->xa;
    double y1_m_y3 = A->ya - B->ya;

    double t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    double t = t1 / den;

    double u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    double u = -(u1 / den);

    return t >= 0 && t <= 1 && u >= 0 && u <= 1;
}

static int
pgIntersection_LineLine(pgLineBase *A, pgLineBase *B, double *X, double *Y,
                        double *T)
{
    double xa = A->xa;
    double ya = A->ya;
    double xb = A->xb;
    double yb = A->yb;
    double x3 = B->xa;
    double y3 = B->ya;
    double x4 = B->xb;
    double y4 = B->yb;

    double x1_m_x2 = xa - xb;
    double y3_m_y4 = y3 - y4;
    double y1_m_y2 = ya - yb;
    double x3_m_x4 = x3 - x4;

    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    double x1_m_x3 = xa - x3;
    double y1_m_y3 = ya - y3;

    double t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    double t = t1 / den;

    double u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    double u = -(u1 / den);

    if (t >= 0 && t <= 1 && u >= 0 && u <= 1) {
        if (X)
            *X = xa + t * (xb - xa);
        if (Y)
            *Y = ya + t * (yb - ya);
        if (T)
            *T = t;
        return 1;
    }
    return 0;
}

static int
pgCollision_LinePoint(pgLineBase *line, double Cx, double Cy)
{
    double dx = line->xa - Cx;
    double dy = line->ya - Cy;
    double dx2 = line->xb - Cx;
    double dy2 = line->yb - Cy;
    double dx3 = line->xa - line->xb;
    double dy3 = line->ya - line->yb;

    double d = sqrt(dx * dx + dy * dy) + sqrt(dx2 * dx2 + dy2 * dy2);
    double d3 = sqrt(dx3 * dx3 + dy3 * dy3);

    double width = 0.000001;
    return d >= d3 - width && d <= d3 + width;
}

static int
pgCollision_CirclePoint(pgCircleBase *circle, double Cx, double Cy)
{
    double dx = circle->x - Cx;
    double dy = circle->y - Cy;
    return dx * dx + dy * dy <= circle->r * circle->r;
}

static int
pgIntersection_LineCircle(pgLineBase *line, pgCircleBase *circle, double *X,
                          double *Y, double *T)
{
    double xa = line->xa;
    double ya = line->ya;
    double xb = line->xb;
    double yb = line->yb;
    double xc = circle->x;
    double yc = circle->y;
    double rsq = circle->r * circle->r;

    double x1_m_xc = xa - xc;
    double y1_m_yc = ya - yc;

    double dx = xb - xa;
    double dy = yb - ya;
    double A = dx * dx + dy * dy;
    double B = 2 * (dx * x1_m_xc + dy * y1_m_yc);
    double C = x1_m_xc * x1_m_xc + y1_m_yc * y1_m_yc - rsq;
    double discriminant = B * B - 4 * A * C;
    if (discriminant < 0) {
        return 0;
    }
    double sqrt_d = sqrt(discriminant);
    double t = (-B - sqrt_d) / (2 * A);
    if (t < 0 || t > 1) {
        t = (-B + sqrt_d) / (2 * A);
        if (t < 0 || t > 1) {
            return 0;
        }
    }

    if (X)
        *X = xa + t * dx;
    if (Y)
        *Y = ya + t * dy;
    if (T)
        *T = t;
    return 1;
}

static int
pgCollision_LineCircle(pgLineBase *line, pgCircleBase *circle)
{
    double xa = line->xa;
    double ya = line->ya;
    double xb = line->xb;
    double yb = line->yb;
    double cx = circle->x;
    double cy = circle->y;
    double r = circle->r;

    if (pgCollision_CirclePoint(circle, xa, ya) ||
        pgCollision_CirclePoint(circle, xb, yb))
        return 1;

    double dx = xa - xb;
    double dy = ya - yb;
    double len = sqrt((dx * dx) + (dy * dy));

    double dot =
        (((cx - xa) * (xb - xa)) + ((cy - ya) * (yb - ya))) / (len * len);

    double closest_x = xa + (dot * (xb - xa));
    double closest_y = ya + (dot * (yb - ya));

    pgLineBase line2 = {xa, ya, xb, yb};
    if (!pgCollision_LinePoint(&line2, closest_x, closest_y))
        return 0;

    dx = closest_x - cx;
    dy = closest_y - cy;
    double distance = sqrt((dx * dx) + (dy * dy));

    return distance <= r;
}

static int
pgCollision_CircleCircle(pgCircleBase *A, pgCircleBase *B)
{
    double dx, dy;
    double sum_radi;

    dx = A->x - B->x;
    dy = A->y - B->y;
    sum_radi = A->r + B->r;

    return dx * dx + dy * dy <= sum_radi * sum_radi;
}

static int
pgIntersection_LineRect(pgLineBase *line, SDL_Rect *rect, double *X, double *Y,
                        double *T)
{
#if AVX2_IS_SUPPORTED
    if (pg_HasAVX2())
        return pgIntersection_LineRect_avx2(line, rect, X, Y, T);
#endif /* ~__AVX2__ */

    double x = (double)rect->x;
    double y = (double)rect->y;
    double w = (double)rect->w;
    double h = (double)rect->h;

    pgLineBase a = {x, y, x + w, y};
    pgLineBase b = {x, y, x, y + h};
    pgLineBase c = {x, y + h, x + w, y + h};
    pgLineBase d = {x + w, y, x + w, y + h};

    int ret = 0;

    double temp_t = DBL_MAX;
    double final_t = DBL_MAX;

    ret |= pgIntersection_LineLine(line, &a, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgIntersection_LineLine(line, &b, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgIntersection_LineLine(line, &c, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgIntersection_LineLine(line, &d, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);

    if (ret) {
        if (X)
            *X = line->xa + final_t * (line->xb - line->xa);
        if (Y)
            *Y = line->ya + final_t * (line->yb - line->ya);
        if (T)
            *T = final_t;
    }

    return ret;
}

static int
pgCollision_RectLine(SDL_Rect *rect, pgLineBase *line)
{
#if AVX2_IS_SUPPORTED
    if (pg_HasAVX2())
        return pgCollision_RectLine_avx2(rect, line);
#endif /* ~__AVX2__ */

    double x = (double)rect->x;
    double y = (double)rect->y;
    double w = (double)rect->w;
    double h = (double)rect->h;

    pgLineBase a = {x, y, x + w, y};
    pgLineBase b = {x, y, x, y + h};
    pgLineBase c = {x, y + h, x + w, y + h};
    pgLineBase d = {x + w, y, x + w, y + h};

    return pgCollision_LineLine(line, &a) || pgCollision_LineLine(line, &b) ||
           pgCollision_LineLine(line, &c) || pgCollision_LineLine(line, &d);
}

static int
pgCollision_RectCircle(SDL_Rect *rect, pgCircleBase *circle)
{
    double cx = circle->x, cy = circle->y;
    double rx = (double)rect->x, ry = (double)rect->y;
    double rw = (double)rect->w, rh = (double)rect->h;
    double r_bottom = ry + rh;
    double r_right = rx + rw;

    double test_x = cx;
    double test_y = cy;

    if (cx < rx) {
        test_x = rx;
    }
    else if (cx > r_right) {
        test_x = r_right;
    }

    if (cy < ry) {
        test_y = ry;
    }
    else if (cy > r_bottom) {
        test_y = r_bottom;
    }

    double dx = cx - test_x;
    double dy = cy - test_y;

    return dx * dx + dy * dy <= circle->r * circle->r;
}

static int
pgCollision_PolygonPoint(pgPolygonBase *poly, double x, double y)
{
    int collision = 0;
    Py_ssize_t i, j;

    for (i = 0, j = poly->verts_num - 1; i < poly->verts_num; j = i++) {
        double xi = poly->vertices[i * 2];
        double yi = poly->vertices[i * 2 + 1];

        if (x == xi && y == yi) {
            return 1;
        }

        double xj = poly->vertices[j * 2];
        double yj = poly->vertices[j * 2 + 1];

        if (((yi > y) != (yj > y)) &&
            (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) {
            collision = !collision;
        }
    }

    return collision;
}

static inline int
pgCollision_PolygonPoints(pgPolygonBase *poly, double xa, double ya, double xb,
                          double yb)
{
    int collision1 = 0, collision2 = 0;
    Py_ssize_t i, j;

    double *vertices = poly->vertices;

    for (i = 0, j = poly->verts_num - 1; i < poly->verts_num; j = i++) {
        double xi = vertices[i * 2];
        double yi = vertices[i * 2 + 1];
        double xj = vertices[j * 2];
        double yj = vertices[j * 2 + 1];

        double xj_xi = xj - xi;
        double yj_yi = yj - yi;

        if (((yi > ya) != (yj > ya)) &&
            (xa < xj_xi * (ya - yi) / yj_yi + xi)) {
            collision1 = !collision1;
        }

        if (((yi > yb) != (yj > yb)) &&
            (xb < xj_xi * (yb - yi) / yj_yi + xi)) {
            collision2 = !collision2;
        }
    }

    return collision1 || collision2;
}

static inline int
_pgCollision_line_polyedges(pgLineBase *line, pgPolygonBase *poly)
{
    Py_ssize_t i, j;
    double *vertices = poly->vertices;

    for (i = 0, j = poly->verts_num - 1; i < poly->verts_num; j = i++) {
        if (pgCollision_LineLine(
                line, &(pgLineBase){vertices[j * 2], vertices[j * 2 + 1],
                                    vertices[i * 2], vertices[i * 2 + 1]})) {
            return 1;
        }
    }

    return 0;
}

static inline int
pgCollision_PolygonLine(pgPolygonBase *poly, pgLineBase *line, int only_edges)
{
    int collision = _pgCollision_line_polyedges(line, poly);

    if (collision || only_edges) {
        return collision;
    }

    return pgCollision_PolygonPoints(poly, line->xa, line->ya, line->xb,
                                     line->yb);
}

static int
_pgCollision_PolygonPoint_opt(pgPolygonBase *poly, double x, double y)
{
    /* This is a faster version of pgCollision_PolygonPoint that assumes
     * that the point passed is not on one of the polygon's vertices. */
    int collision = 0;
    Py_ssize_t i, j;

    for (i = 0, j = poly->verts_num - 1; i < poly->verts_num; j = i++) {
        double xi = poly->vertices[i * 2];
        double yi = poly->vertices[i * 2 + 1];
        double xj = poly->vertices[j * 2];
        double yj = poly->vertices[j * 2 + 1];

        if (((yi > y) != (yj > y)) &&
            (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) {
            collision = !collision;
        }
    }

    return collision;
}

static int
pgCollision_CirclePolygon(pgCircleBase *circle, pgPolygonBase *poly,
                          int only_edges)
{
    Py_ssize_t i, j;
    double cx = circle->x;
    double cy = circle->y;
    double cr = circle->r;
    double cr_sqr = cr * cr;

    /* Check if the circle is colliding with any of the polygon's edges. */
    for (i = 0, j = poly->verts_num - 1; i < poly->verts_num; j = i++) {
        double xi = poly->vertices[i * 2];
        double yi = poly->vertices[i * 2 + 1];
        double xj = poly->vertices[j * 2];
        double yj = poly->vertices[j * 2 + 1];

        double dx = xj - xi;
        double dy = yj - yi;

        double xi_m_cx = xi - cx;
        double yi_m_cy = yi - cy;

        double at2 = 2 * (dx * dx + dy * dy);
        double b = 2 * (dx * xi_m_cx + dy * yi_m_cy);
        double c = xi_m_cx * xi_m_cx + yi_m_cy * yi_m_cy - cr_sqr;

        double bb4ac = b * b - 2 * at2 * c;

        if (bb4ac < 0) {
            continue;
        }

        double sqrt_bb4ac = sqrt(bb4ac);
        double mu1 = (-b + sqrt_bb4ac) / at2;
        double mu2 = (-b - sqrt_bb4ac) / at2;

        if ((0 <= mu1 && mu1 <= 1) || (0 <= mu2 && mu2 <= 1)) {
            return 1;
        }
    }

    /* Circle is not colliding with any of the polygon's edges. If we only
     * care for edge collision, return now. */
    if (only_edges) {
        return 0;
    }

    int center_inside = _pgCollision_PolygonPoint_opt(poly, cx, cy);

    if (center_inside) {
        return 1;
    }

    /* Check if any of the polygon's vertices are inside the circle */
    for (i = 0; i < poly->verts_num; i++) {
        double dx = poly->vertices[i * 2] - cx;
        double dy = poly->vertices[i * 2 + 1] - cy;

        if (dx * dx + dy * dy <= cr_sqr) {
            return 1;
        }
    }

    return 0;
}

static int
pgRaycast_LineLine(pgLineBase *A, pgLineBase *B, double max_t, double *T)
{
    double xa = A->xa;
    double ya = A->ya;
    double xb = A->xb;
    double yb = A->yb;
    double x3 = B->xa;
    double y3 = B->ya;
    double x4 = B->xb;
    double y4 = B->yb;

    double x1_m_x2 = xa - xb;
    double y3_m_y4 = y3 - y4;
    double y1_m_y2 = ya - yb;
    double x3_m_x4 = x3 - x4;

    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    double x1_m_x3 = xa - x3;
    double y1_m_y3 = ya - y3;

    double t = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    t /= den;

    double u = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    u /= -den;

    if (t >= 0 && u >= 0 && u <= 1 && t <= max_t) {
        *T = t;
        return 1;
    }
    return 0;
}

static int
pgRaycast_LineRect(pgLineBase *line, SDL_Rect *rect, double max_t, double *T)
{
#if AVX2_IS_SUPPORTED
    if (pg_HasAVX2())
        return pgRaycast_LineRect_avx2(line, rect, max_t, T);
#endif /* ~__AVX2__ */

    double x = (double)rect->x;
    double y = (double)rect->y;
    double w = (double)rect->w;
    double h = (double)rect->h;

    pgLineBase a = {x, y, x + w, y};
    pgLineBase b = {x, y, x, y + h};
    pgLineBase c = {x, y + h, x + w, y + h};
    pgLineBase d = {x + w, y, x + w, y + h};

    int ret = 0;

    double temp_t = DBL_MAX;
    double final_t = DBL_MAX;

    ret |= pgRaycast_LineLine(line, &a, max_t, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgRaycast_LineLine(line, &b, max_t, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgRaycast_LineLine(line, &c, max_t, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgRaycast_LineLine(line, &d, max_t, &temp_t);
    final_t = MIN(temp_t, final_t);

    if (ret && final_t <= max_t) {
        *T = final_t;
    }

    return ret;
}

static int
pgRaycast_LineCircle(pgLineBase *line, pgCircleBase *circle, double max_t,
                     double *T)
{
    double xa = line->xa;
    double ya = line->ya;
    double xb = line->xb;
    double yb = line->yb;
    double xc = circle->x;
    double yc = circle->y;

    double x1_m_xc = xa - xc;
    double y1_m_yc = ya - yc;

    double dx = xb - xa;
    double dy = yb - ya;
    double A = dx * dx + dy * dy;
    double B = 2 * (dx * x1_m_xc + dy * y1_m_yc);
    double C = x1_m_xc * x1_m_xc + y1_m_yc * y1_m_yc - circle->r * circle->r;

    double discriminant = B * B - 4 * A * C;
    if (discriminant < 0) {
        return 0;
    }
    double sqrt_d = sqrt(discriminant);
    double t = (-B - sqrt_d) / (2 * A);
    if (t < 0) {
        t = (-B + sqrt_d) / (2 * A);
        if (t < 0) {
            return 0;
        }
    }

    if (t <= max_t)
        *T = t;

    return 1;
}

static int
pgIntersection_CircleCircle(pgCircleBase *A, pgCircleBase *B,
                            double *intersections)
{
    double dx = B->x - A->x;
    double dy = B->y - A->y;
    double d2 = dx * dx + dy * dy;
    double r_sum = A->r + B->r;
    double r_diff = A->r - B->r;
    double r_sum2 = r_sum * r_sum;
    double r_diff2 = r_diff * r_diff;

    if (d2 > r_sum2 || d2 < r_diff2) {
        return 0;
    }

    if (d2 == 0 && A->r == B->r) {
        return 0;
    }

    double d = sqrt(d2);
    double a = (d2 + A->r * A->r - B->r * B->r) / (2 * d);
    double h = sqrt(A->r * A->r - a * a);

    double xm = A->x + a * (dx / d);
    double ym = A->y + a * (dy / d);

    double xs1 = xm + h * (dy / d);
    double ys1 = ym - h * (dx / d);
    double xs2 = xm - h * (dy / d);
    double ys2 = ym + h * (dx / d);

    if (d2 == r_sum2 || d2 == r_diff2) {
        intersections[0] = xs1;
        intersections[1] = ys1;
        return 1;
    }

    intersections[0] = xs1;
    intersections[1] = ys1;
    intersections[2] = xs2;
    intersections[3] = ys2;
    return 2;
}
