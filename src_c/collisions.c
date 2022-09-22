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
    double x1_m_x2 = A->x1 - A->x2;
    double y3_m_y4 = B->y1 - B->y2;
    double y1_m_y2 = A->y1 - A->y2;
    double x3_m_x4 = B->x1 - B->x2;

    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    double x1_m_x3 = A->x1 - B->x1;
    double y1_m_y3 = A->y1 - B->y1;

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
    double x1 = A->x1;
    double y1 = A->y1;
    double x2 = A->x2;
    double y2 = A->y2;
    double x3 = B->x1;
    double y3 = B->y1;
    double x4 = B->x2;
    double y4 = B->y2;

    double x1_m_x2 = x1 - x2;
    double y3_m_y4 = y3 - y4;
    double y1_m_y2 = y1 - y2;
    double x3_m_x4 = x3 - x4;

    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    double x1_m_x3 = x1 - x3;
    double y1_m_y3 = y1 - y3;

    double t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    double t = t1 / den;

    double u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    double u = -(u1 / den);

    if (t >= 0 && t <= 1 && u >= 0 && u <= 1) {
        if (X)
            *X = x1 + t * (x2 - x1);
        if (Y)
            *Y = y1 + t * (y2 - y1);
        if (T)
            *T = t;
        return 1;
    }
    return 0;
}

static int
pgCollision_LinePoint(pgLineBase *line, double Cx, double Cy)
{
    double Ax = line->x1;
    double Ay = line->y1;
    double Bx = line->x2;
    double By = line->y2;

    /* https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection */
    return (Bx - Ax) * (Cy - Ay) == (Cx - Ax) * (By - Ay) &&
           ((Ax != Bx) ? (Ax <= Cx && Cx <= Bx) || (Bx <= Cx && Cx <= Ax)
                       : (Ay <= Cy && Cy <= By) || (By <= Cy && Cy <= Ay));
}

static int
pgCollision_CirclePoint(pgCircleBase *circle, double Cx, double Cy)
{
    double dx = circle->x - Cx;
    double dy = circle->y - Cy;
    return dx * dx + dy * dy <= circle->r_sqr;
}

static int
pgIntersection_LineCircle(pgLineBase *line, pgCircleBase *circle, double *X,
                          double *Y, double *T)
{
    double x1 = line->x1;
    double y1 = line->y1;
    double x2 = line->x2;
    double y2 = line->y2;
    double xc = circle->x;
    double yc = circle->y;
    double r = circle->r;
    double rsq = circle->r_sqr;

    double dx = x2 - x1;
    double dy = y2 - y1;
    double A = dx * dx + dy * dy;
    double B = 2 * (dx * (x1 - xc) + dy * (y1 - yc));
    double C = (x1 - xc) * (x1 - xc) + (y1 - yc) * (y1 - yc) - rsq;
    double descriminant = B * B - 4 * A * C;
    if (descriminant < 0) {
        return 0;
    }
    double t = (-B - sqrt(descriminant)) / (2 * A);
    if (t < 0 || t > 1) {
        t = (-B + sqrt(descriminant)) / (2 * A);
        if (t < 0 || t > 1) {
            return 0;
        }
    }

    if (X)
        *X = x1 + t * dx;
    if (Y)
        *Y = y1 + t * dy;
    if (T)
        *T = t;
    return 1;
}

static int
pgCollision_LineCircle(pgLineBase *line, pgCircleBase *circle)
{
    double x1 = line->x1;
    double y1 = line->y1;
    double x2 = line->x2;
    double y2 = line->y2;
    double cx = circle->x;
    double cy = circle->y;
    double r = circle->r;

    if (pgCollision_CirclePoint(circle, x1, y1) ||
        pgCollision_CirclePoint(circle, x2, y2))
        return 1;

    double dx = x1 - x2;
    double dy = y1 - y2;
    double len = sqrt((dx * dx) + (dy * dy));

    double dot =
        (((cx - x1) * (x2 - x1)) + ((cy - y1) * (y2 - y1))) / (len * len);

    double closest_x = x1 + (dot * (x2 - x1));
    double closest_y = y1 + (dot * (y2 - y1));

    pgLineBase line2 = {x1, y1, x2, y2};
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
    return pgIntersection_LineRect_avx2(line, rect, X, Y, T);
#else
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
            *X = line->x1 + final_t * (line->x2 - line->x1);
        if (Y)
            *Y = line->y1 + final_t * (line->y2 - line->y1);
        if (T)
            *T = final_t;
    }

    return ret;
#endif /* ~__AVX2__ */
}

static int
pgCollision_RectLine(SDL_Rect *rect, pgLineBase *line)
{
#if AVX2_IS_SUPPORTED
    return pgCollision_RectLine_avx2(rect, line);
#else
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
#endif /* ~__AVX2__ */
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

    return dx * dx + dy * dy <= circle->r_sqr;
    return 0;
}

static int
pgCollision_PolyPoly(pgPolygonBase *polygon_1, pgPolygonBase *polygon_2)
{
    pgPolygonBase *poly_1 = polygon_1;
    pgPolygonBase *poly_2 = polygon_2;

    int shape;
    for (shape = 0; shape < 2; shape++) {
        if (shape == 1) {
            poly_1 = polygon_2;
            poly_2 = polygon_1;
        }
        Py_ssize_t it_poly_1;
        for (it_poly_1 = 0 ; it_poly_1 < poly_1->verts_num; it_poly_1++) {
            double diag_start_x = poly_1->c_x;
            double diag_start_y = poly_1->c_y;

            double diag_end_x = poly_1->vertices[2 * it_poly_1];
            double diag_end_y = poly_1->vertices[2 * it_poly_1 + 1];

            Py_ssize_t it_poly_2;
            for (it_poly_2 = 0; it_poly_2 < poly_2->verts_num; it_poly_2++) {
                double segment_start_x = poly_2->vertices[it_poly_2 * 2];
                double segment_start_y = poly_2->vertices[it_poly_2 * 2 + 1];

                double segment_end_x = poly_2->vertices[((it_poly_2 + 1) % poly_2->verts_num) * 2];
                double segment_end_y = poly_2->vertices[((it_poly_2 + 1) % poly_2->verts_num) * 2 + 1];

                double h = (segment_end_x - segment_start_x) * (diag_start_y - diag_end_y) - (diag_start_x - diag_end_x) * (segment_end_y - segment_start_y);
                double t1 = ((segment_start_y - segment_end_y) * (diag_start_x - segment_start_x) + (segment_end_x - segment_start_x) * (diag_start_y - segment_start_y)) / h;
                double t2 = ((diag_start_y - diag_end_y) * (diag_start_x - segment_start_x) + (diag_end_x - diag_start_x) * (diag_start_y - segment_start_y)) / h;

                if (t1 >= 0.0f && t1 < 1.0f && t2 >= 0.0f && t2 < 1.0f) {
                    return 1;
                }
            }
        }
    }
    return 0;
}

static int
pgCollision_PolyLine(pgPolygonBase *polygon, pgLineBase *line)
{
    double line_start_x = line->x1;
    double line_start_y = line->y1;
    double line_end_x = line->x2;
    double line_end_y = line->y2;

    Py_ssize_t it_poly;
    for (it_poly = 0; it_poly < polygon->verts_num; it_poly++) {
        double segment_start_x = polygon->vertices[it_poly * 2];
        double segment_start_y = polygon->vertices[it_poly * 2 + 1];

        double segment_end_x = polygon->vertices[((it_poly + 1) % polygon->verts_num) * 2];
        double segment_end_y = polygon->vertices[((it_poly + 1) % polygon->verts_num) * 2 + 1];

        double h = (segment_end_x - segment_start_x) * (line_start_y - line_end_y) - (line_start_x - line_end_x) * (segment_end_y - segment_start_y);
        double t1 = ((segment_start_y - segment_end_y) * (line_start_x - segment_start_x) + (segment_end_x - segment_start_x) * (line_start_y - segment_start_y)) / h;
        double t2 = ((line_start_y - line_end_y) * (line_start_x - segment_start_x) + (line_end_x - line_start_x) * (line_start_y - segment_start_y)) / h;

        if (t1 >= 0.0f && t1 < 1.0f && t2 >= 0.0f && t2 < 1.0f) {
            return 1;
        }
    }
    return 0;
}

static int
pgCollision_PolyRect(pgPolygonBase *poly, SDL_Rect *rect)
{
    double r_x = (double)rect->x, r_y = (double)rect->y, r_w = (double)rect->w,
           r_h = (double)rect->h;
    double rect_vertices[8] = {
        r_x, r_y, r_x + r_w, r_y, r_x + r_w, r_y + r_h, r_x, r_y + r_h,
    };
    pgPolygonBase rect_poly;
    rect_poly.verts_num = 4;
    rect_poly.vertices = rect_vertices;
    rect_poly.c_x = r_x + r_w / 2;
    rect_poly.c_y = r_y + r_h / 2;
    return pgCollision_PolyPoly(poly, &rect_poly);
}

static int
pgCollision_PolyCircle(pgPolygonBase *poly, pgCircleBase *circle)
{
    double offset_x;
    double offset_y;
    Py_ssize_t it_poly;
    for (it_poly = 0; it_poly < poly->verts_num; it_poly++) {
        double segment_start_x = poly->vertices[it_poly * 2];
        double segment_start_y = poly->vertices[it_poly * 2 + 1];

        double segment_end_x = poly->vertices[((it_poly + 1) % poly->verts_num) * 2];
        double segment_end_y = poly->vertices[((it_poly + 1) % poly->verts_num) * 2 + 1];

        double radius_normal_x = segment_start_y - segment_end_y;
        double radius_normal_y = segment_end_x - segment_start_x;

        double radius_start_x = circle->x;
        double radius_start_y = circle->y;

        double radius_end_x = circle->x + radius_normal_x * circle->r;
        double radius_end_y = circle->y + radius_normal_y * circle->r;

        double h = (segment_end_x - segment_start_x) * (radius_start_y - radius_end_y) - (radius_start_x - radius_end_x) * (segment_end_y - segment_start_y);
        double t1 = ((segment_start_y - segment_end_y) * (radius_start_x - segment_start_x) + (segment_end_x - segment_start_x) * (radius_start_y - segment_start_y)) / h;
        double t2 = ((radius_start_y - radius_end_y) * (radius_start_x - segment_start_x) + (radius_end_x - radius_start_x) * (radius_start_y - segment_start_y)) / h;

        if (t1 >= 0.0f && t1 < 1.0f && t2 >= 0.0f && t2 < 1.0f) {
            //Check with the normal of radius perpendicular to line segment
            offset_x = (radius_end_x - radius_start_x) * t1;
            offset_y = (radius_end_y - radius_start_y) * t1;
            
            double offsetSMag = offset_x * offset_x + offset_y * offset_y;
            if (offsetSMag - circle->r * circle->r < 0.0f) {
                return 1;
            }
        }
        else {
            //check with the line to the selected vertex of the polygon
            offset_x = radius_start_x - segment_start_x;
            offset_y = radius_start_y - segment_start_y;

            double offsetSMag = offset_x * offset_x + offset_y * offset_y;
            if (offsetSMag - circle->r * circle->r < 0.0f) {
                return 1;
            }
        }
    }
    return 0;
}

static int
pgIntersection_PolyPoly(pgPolygonBase *polygon_1, pgPolygonBase *polygon_2)
{
    pgPolygonBase *poly_1 = polygon_1;
    pgPolygonBase *poly_2 = polygon_2;
    
    int shape;
    for (shape = 0; shape < 2; shape++)
    {
        if (shape == 1)
        {
            poly_1 = polygon_2;
            poly_2 = polygon_1;
        }
        Py_ssize_t it_poly_1;
        for (it_poly_1 = 0; it_poly_1 < poly_1->verts_num; it_poly_1++)
        {
            double diag_start_x = poly_1->c_x;
            double diag_start_y = poly_1->c_y;

            double diag_end_x = poly_1->vertices[2 * it_poly_1];
            double diag_end_y = poly_1->vertices[2 * it_poly_1 + 1];

            double offset_x = 0;
            double offset_y = 0;

            Py_ssize_t it_poly_2;
            for (it_poly_2 = 0; it_poly_2 < poly_2->verts_num;
                 it_poly_2++)
            {
                double segment_start_x = poly_2->vertices[it_poly_2 * 2];
                double segment_start_y = poly_2->vertices[it_poly_2 * 2 + 1];

                double segment_end_x = poly_2->vertices[((it_poly_2 + 1) % poly_2->verts_num) * 2];
                double segment_end_y = poly_2->vertices[((it_poly_2 + 1) % poly_2->verts_num) * 2 + 1];

                double h = (segment_end_x - segment_start_x) * (diag_start_y - diag_end_y) - (diag_start_x - diag_end_x) * (segment_end_y - segment_start_y);
                double t1 = ((segment_start_y - segment_end_y) * (diag_start_x - segment_start_x) + (segment_end_x - segment_start_x) * (diag_start_y - segment_start_y)) / h;
                double t2 = ((diag_start_y - diag_end_y) * (diag_start_x - segment_start_x) + (diag_end_x - diag_start_x) * (diag_start_y - segment_start_y)) / h;

                if (t1 >= 0 && t1 < 1 && t2 >= 0 && t2 < 1)
                {
                    offset_x += (diag_end_x - diag_start_x) * (1 - t1);
                    offset_y += (diag_end_y - diag_start_y) * (1 - t1);
                }
            }
            Py_ssize_t poly_1_it;
            for (poly_1_it = 0; poly_1_it < poly_1->verts_num; poly_1_it++)
            {
                poly_1->vertices[poly_1_it * 2] += offset_x;
                poly_1->vertices[poly_1_it * 2 + 1] += offset_y;
            }
            poly_1->c_x += offset_x;
            poly_2->c_y += offset_y;
        }
    }
    return 0;
}

static int
pgIntersection_PolyLine(pgPolygonBase *polygon, pgLineBase *line)
{
    
}

static int
pgIntersection_PolyRect(pgPolygonBase *polygon, SDL_Rect *rect)
{
    int result;
    double r_x = (double)rect->x, r_y = (double)rect->y, r_w = (double)rect->w,
           r_h = (double)rect->h;
    double rect_vertices[8] = {
        r_x, r_y, r_x + r_w, r_y, r_x + r_w, r_y + r_h, r_x, r_y + r_h,
    };
    pgPolygonBase rect_poly;
    rect_poly.verts_num = 4;
    rect_poly.vertices = rect_vertices;
    rect_poly.c_x = r_x + r_w / 2;
    rect_poly.c_y = r_y + r_h / 2;
    result = pgIntersection_PolyPoly(polygon, &rect_poly);
    if (rect_poly.c_x != r_x + r_w / 2 || rect_poly.c_y != r_y + r_h / 2)
    {
        rect->x += rect_poly.c_x - (r_x + r_w / 2);
        rect->y += rect_poly.c_y - (r_y + r_h / 2);
    }
    return result;
}

static int
pgIntersection_PolyCircle(pgPolygonBase *polygon, pgCircleBase *circle)
{
    double offset_x;
    double offset_y;
    Py_ssize_t it_poly;
    for (it_poly = 0; it_poly < polygon->verts_num; it_poly++)
    {
        double segment_start_x = polygon->vertices[it_poly * 2];
        double segment_start_y = polygon->vertices[it_poly * 2 + 1];

        double segment_end_x =
            polygon->vertices[((it_poly + 1) % polygon->verts_num) * 2];
        double segment_end_y =
            polygon->vertices[((it_poly + 1) % polygon->verts_num) * 2 + 1];

        double radius_normal_x = segment_start_y - segment_end_y;
        double radius_normal_y = segment_end_x - segment_start_x;

        double radius_start_x = circle->x;
        double radius_start_y = circle->y;

        double radius_end_x = circle->x + radius_normal_x * circle->r;
        double radius_end_y = circle->y + radius_normal_y * circle->r;

        double h = (segment_end_x - segment_start_x) * (radius_start_y - radius_end_y) - (radius_start_x - radius_end_x) * (segment_end_y - segment_start_y);
        double t1 = ((segment_start_y - segment_end_y) * (radius_start_x - segment_start_x) + (segment_end_x - segment_start_x) * (radius_start_y - segment_start_y)) / h;
        double t2 = ((radius_start_y - radius_end_y) * (radius_start_x - segment_start_x) + (radius_end_x - radius_start_x) * (radius_start_y - segment_start_y)) / h;

        if (t1 >= 0.0f && t1 < 1.0f && t2 >= 0.0f && t2 < 1.0f)
        {
            // Check with the normal of radius perpendicular to line segment
            offset_x = (radius_end_x - radius_start_x) * t1;
            offset_y = (radius_end_y - radius_start_y) * t1;

            double offsetSMag = offset_x * offset_x + offset_y * offset_y;
            if (offsetSMag - circle->r * circle->r < 0.0f)
            {
                Py_ssize_t poly_it;
                for (poly_it = 0; poly_it < polygon->verts_num; poly_it++)
                {
                    polygon->vertices[poly_it * 2] += offset_x;
                    polygon->vertices[poly_it * 2 + 1] += offset_y;
                }
                polygon->c_x += offset_x;
                polygon->c_y += offset_y;
                return 1;
            }
        }
        else
        {
            // check with the line to the selected vertex of the polygon
            offset_x = radius_start_x - segment_start_x;
            offset_y = radius_start_y - segment_start_y;

            double offsetSMag = offset_x * offset_x + offset_y * offset_y;
            if (offsetSMag - circle->r * circle->r < 0.0f)
            {
                Py_ssize_t poly_it;
                for (poly_it = 0; poly_it < polygon->verts_num; poly_it++)
                {
                    polygon->vertices[poly_it * 2] += offset_x;
                    polygon->vertices[poly_it * 2 + 1] += offset_y;
                }
                polygon->c_x += offset_x;
                polygon->c_y += offset_y;
                return 1;
            }
        }
    }
    return 0;
}
