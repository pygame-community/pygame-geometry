#include "include/pygame.h"
#include "simd_collisions.h"
#include <string.h>

#if defined(_MSC_VER)
#include <intrin.h>
#include <malloc.h>
#endif

#if defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H)
#include <immintrin.h>
#endif /* defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H) */

PG_FORCEINLINE static int
pg_HasAVX2(void)
{
    // The check is cached.
    static int has_avx2 = -1;
    if (has_avx2 != -1)
        return has_avx2;

#if AVX2_IS_SUPPORTED
#if defined(__GNUC__)
    // Reference:
    // https://gcc.gnu.org/onlinedocs/gcc-4.8.2/gcc/X86-Built-in-Functions.html
    has_avx2 = __builtin_cpu_supports("avx2");
#elif defined(_MSC_VER)
    // Reference:
    // https://learn.microsoft.com/en-us/cpp/intrinsics/cpuid-cpuidex?view=msvc-170

    int cpu_info[4];
    __cpuid(cpu_info, 0);

    int info_n = cpu_info[0];
    int *data = (int *)_alloca(sizeof(int) * info_n * 4);
    // int data[info_n][4];

    for (int i = 0; i <= info_n; i++) {
        __cpuidex(cpu_info, i, 0);

        // memcpy(&data[i], cpu_info, sizeof(int) * 4);
        memcpy(data + i * 4, cpu_info, sizeof(int) * 4);
    }

    // has_avx2 = data[7][1] >> 5 & 1;
    has_avx2 = data[7 * 4 + 1] >> 5 & 1;
#else
    has_avx2 = 0;
#endif
#else
    has_avx2 = 0;
#endif /* ~__AVX2__ */

    return has_avx2;
}

#if AVX2_IS_SUPPORTED
PG_FORCEINLINE static int
pgIntersection_LineRect_avx2(pgLineBase *line, SDL_Rect *rect, double *X,
                             double *Y, double *T)
{
    double Rx = (double)rect->x;
    double Ry = (double)rect->y;
    double Rw = (double)rect->w;
    double Rh = (double)rect->h;

    // here we start to setup the variables
    __m256d x1_256d = _mm256_set1_pd(line->xa);
    __m256d y1_256d = _mm256_set1_pd(line->ya);
    __m256d x2_256d = _mm256_set1_pd(line->xb);
    __m256d y2_256d = _mm256_set1_pd(line->yb);
    __m256d x3_256d = _mm256_set_pd(Rx, Rx, Rx, Rx + Rw);
    __m256d y3_256d = _mm256_set_pd(Ry, Ry, Ry + Rh, Ry);
    __m256d x4_256d = _mm256_set_pd(Rx + Rw, Rx, Rx + Rw, Rx + Rw);
    __m256d y4_256d = _mm256_set_pd(Ry, Ry + Rh, Ry + Rh, Ry + Rh);

    // here we calculate the differences between the the coords of the points
    __m256d x1_m_x2_256d = _mm256_sub_pd(x1_256d, x2_256d);
    __m256d y3_m_y4_256d = _mm256_sub_pd(y3_256d, y4_256d);
    __m256d y1_m_y2_256d = _mm256_sub_pd(y1_256d, y2_256d);
    __m256d x3_m_x4_256d = _mm256_sub_pd(x3_256d, x4_256d);

    // we calculate the denominator of the equations
    __m256d den_256d =
        _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y3_m_y4_256d),
                      _mm256_mul_pd(y1_m_y2_256d, x3_m_x4_256d));

    // if the denominator is 0 then the line is parallel to the other line
    // in this occasion this can't be true here as a line will never be
    // parallel to all four sides of a rectangle
    __m256d den_zero_256d =
        _mm256_cmp_pd(den_256d, _mm256_setzero_pd(), _CMP_EQ_OQ);

    // we dont want to cause any floating point errors by dividing by 0
    // so we set the ones that are equal to 0 to 1
    den_256d = _mm256_or_pd(den_zero_256d, den_256d);

    // we calculate the rest of the differences between the coords of the
    // points
    __m256d x1_m_x3_256d = _mm256_sub_pd(x1_256d, x3_256d);
    __m256d y1_m_y3_256d = _mm256_sub_pd(y1_256d, y3_256d);

    // calculate the t values
    __m256d t_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x3_256d, y3_m_y4_256d),
                                   _mm256_mul_pd(y1_m_y3_256d, x3_m_x4_256d));
    t_256d = _mm256_div_pd(t_256d, den_256d);

    // calculate the u values
    __m256d u_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y1_m_y3_256d),
                                   _mm256_mul_pd(y1_m_y2_256d, x1_m_x3_256d));
    u_256d =
        _mm256_mul_pd(_mm256_div_pd(u_256d, den_256d), _mm256_set1_pd(-1.0));

    // we check this condition t >= 0 && t <= 1 && u >= 0 && u <= 1
    __m256d ones_256d = _mm256_set1_pd(1.0);
    __m256d zeros_256d = _mm256_set1_pd(0.0);
    __m256d t_zero_256d = _mm256_cmp_pd(t_256d, zeros_256d, _CMP_GE_OQ);
    __m256d t_one_256d = _mm256_cmp_pd(t_256d, ones_256d, _CMP_LE_OQ);
    __m256d u_zero_256d = _mm256_cmp_pd(u_256d, zeros_256d, _CMP_GE_OQ);
    __m256d u_one_256d = _mm256_cmp_pd(u_256d, ones_256d, _CMP_LE_OQ);
    __m256d condition_256d =
        _mm256_and_pd(_mm256_and_pd(t_zero_256d, t_one_256d),
                      _mm256_and_pd(u_zero_256d, u_one_256d));

    // if no lines touch the rectangle then this will be true
    if (_mm256_movemask_pd(condition_256d) == 0x0) {
        return 0;
    }

    __m256d blended_256d =
        _mm256_blendv_pd(_mm256_set1_pd(DBL_MAX), t_256d, condition_256d);

    __m128d min_256d = _mm_min_pd(_mm256_extractf128_pd(blended_256d, 0),
                                  _mm256_extractf128_pd(blended_256d, 1));
    double *min_ptr = (double *)&min_256d;

    double t = min_ptr[0] < min_ptr[1] ? min_ptr[0] : min_ptr[1];

    // outputs
    if (T)
        *T = t;
    if (X)
        *X = line->xa + t * (line->xb - line->xa);
    if (Y)
        *Y = line->ya + t * (line->yb - line->ya);

    return 1;
}

PG_FORCEINLINE static int
pgCollision_RectLine_avx2(SDL_Rect *rect, pgLineBase *line)
{
    double Rx = (double)rect->x;
    double Ry = (double)rect->y;
    double Rw = (double)rect->w;
    double Rh = (double)rect->h;

    // here we start to setup the variables
    __m256d x1_256d = _mm256_set1_pd(line->xa);
    __m256d y1_256d = _mm256_set1_pd(line->ya);
    __m256d x2_256d = _mm256_set1_pd(line->xb);
    __m256d y2_256d = _mm256_set1_pd(line->yb);
    __m256d x3_256d = _mm256_set_pd(Rx, Rx, Rx, Rx + Rw);
    __m256d y3_256d = _mm256_set_pd(Ry, Ry, Ry + Rh, Ry);
    __m256d x4_256d = _mm256_set_pd(Rx + Rw, Rx, Rx + Rw, Rx + Rw);
    __m256d y4_256d = _mm256_set_pd(Ry, Ry + Rh, Ry + Rh, Ry + Rh);

    // here we calculate the differences between the the coords of the points
    __m256d x1_m_x2_256d = _mm256_sub_pd(x1_256d, x2_256d);
    __m256d y3_m_y4_256d = _mm256_sub_pd(y3_256d, y4_256d);
    __m256d y1_m_y2_256d = _mm256_sub_pd(y1_256d, y2_256d);
    __m256d x3_m_x4_256d = _mm256_sub_pd(x3_256d, x4_256d);

    // we calculate the denominator of the equations
    __m256d den_256d =
        _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y3_m_y4_256d),
                      _mm256_mul_pd(y1_m_y2_256d, x3_m_x4_256d));

    // if the denominator is 0 then the line is parallel to the other line
    // in this occasion this can't be true here as a line will never be
    // parallel to all four sides of a rectangle
    __m256d den_zero_256d =
        _mm256_cmp_pd(den_256d, _mm256_setzero_pd(), _CMP_EQ_OQ);

    // we dont want to cause any floating point errors by dividing by 0
    // so we set the ones that are equal to 0 to 1
    den_256d = _mm256_or_pd(den_zero_256d, den_256d);

    // we calculate the rest of the differences between the coords of the
    // points
    __m256d x1_m_x3_256d = _mm256_sub_pd(x1_256d, x3_256d);
    __m256d y1_m_y3_256d = _mm256_sub_pd(y1_256d, y3_256d);

    // calculate the t values
    __m256d t_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x3_256d, y3_m_y4_256d),
                                   _mm256_mul_pd(y1_m_y3_256d, x3_m_x4_256d));
    t_256d = _mm256_div_pd(t_256d, den_256d);

    // calculate the u values
    __m256d u_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y1_m_y3_256d),
                                   _mm256_mul_pd(y1_m_y2_256d, x1_m_x3_256d));
    u_256d =
        _mm256_mul_pd(_mm256_div_pd(u_256d, den_256d), _mm256_set1_pd(-1.0));

    // we check this condition t >= 0 && t <= 1 && u >= 0 && u <= 1
    __m256d ones_256d = _mm256_set1_pd(1.0);
    __m256d zeros_256d = _mm256_set1_pd(0.0);
    __m256d t_zero_256d = _mm256_cmp_pd(t_256d, zeros_256d, _CMP_GE_OQ);
    __m256d t_one_256d = _mm256_cmp_pd(t_256d, ones_256d, _CMP_LE_OQ);
    __m256d u_zero_256d = _mm256_cmp_pd(u_256d, zeros_256d, _CMP_GE_OQ);
    __m256d u_one_256d = _mm256_cmp_pd(u_256d, ones_256d, _CMP_LE_OQ);
    __m256d t_u_256d = _mm256_and_pd(_mm256_and_pd(t_zero_256d, t_one_256d),
                                     _mm256_and_pd(u_zero_256d, u_one_256d));

    // if no lines touch the rectangle then this will be false
    return _mm256_movemask_pd(t_u_256d) != 0x0;
}

PG_FORCEINLINE static int
pgRaycast_LineRect_avx2(pgLineBase *line, SDL_Rect *rect, double max_t,
                        double *T)
{
    double Rx = (double)rect->x;
    double Ry = (double)rect->y;
    double Rw = (double)rect->w;
    double Rh = (double)rect->h;

    // here we start to setup the variables
    __m256d x1_256d = _mm256_set1_pd(line->xa);
    __m256d y1_256d = _mm256_set1_pd(line->ya);
    __m256d x2_256d = _mm256_set1_pd(line->xb);
    __m256d y2_256d = _mm256_set1_pd(line->yb);
    __m256d x3_256d = _mm256_set_pd(Rx, Rx, Rx, Rx + Rw);
    __m256d y3_256d = _mm256_set_pd(Ry, Ry, Ry + Rh, Ry);
    __m256d x4_256d = _mm256_set_pd(Rx + Rw, Rx, Rx + Rw, Rx + Rw);
    __m256d y4_256d = _mm256_set_pd(Ry, Ry + Rh, Ry + Rh, Ry + Rh);

    // here we calculate the differences between the the coords of the points
    __m256d x1_m_x2_256d = _mm256_sub_pd(x1_256d, x2_256d);
    __m256d y3_m_y4_256d = _mm256_sub_pd(y3_256d, y4_256d);
    __m256d y1_m_y2_256d = _mm256_sub_pd(y1_256d, y2_256d);
    __m256d x3_m_x4_256d = _mm256_sub_pd(x3_256d, x4_256d);

    // we calculate the denominator of the equations
    __m256d den_256d =
        _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y3_m_y4_256d),
                      _mm256_mul_pd(y1_m_y2_256d, x3_m_x4_256d));

    // if the denominator is 0 then the line is parallel to the other line
    // in this occasion this can't be true here as a line will never be
    // parallel to all four sides of a rectangle
    __m256d den_zero_256d =
        _mm256_cmp_pd(den_256d, _mm256_setzero_pd(), _CMP_EQ_OQ);

    // we dont want to cause any floating point errors by dividing by 0
    // so we set the ones that are equal to 0 to 1
    den_256d = _mm256_or_pd(den_zero_256d, den_256d);

    // we calculate the rest of the differences between the coords of the
    // points
    __m256d x1_m_x3_256d = _mm256_sub_pd(x1_256d, x3_256d);
    __m256d y1_m_y3_256d = _mm256_sub_pd(y1_256d, y3_256d);

    // calculate the t values
    __m256d t_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x3_256d, y3_m_y4_256d),
                                   _mm256_mul_pd(y1_m_y3_256d, x3_m_x4_256d));
    t_256d = _mm256_div_pd(t_256d, den_256d);

    // calculate the u values
    __m256d u_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y1_m_y3_256d),
                                   _mm256_mul_pd(y1_m_y2_256d, x1_m_x3_256d));
    u_256d =
        _mm256_mul_pd(_mm256_div_pd(u_256d, den_256d), _mm256_set1_pd(-1.0));

    // we check this condition t >= 0 && t <= max_t && u >= 0 && u <= 1
    __m256d ones_256d = _mm256_set1_pd(1.0);
    __m256d zeros_256d = _mm256_set1_pd(0.0);
    __m256d t_zero_256d = _mm256_cmp_pd(t_256d, zeros_256d, _CMP_GE_OQ);
    __m256d t_one_256d =
        _mm256_cmp_pd(t_256d, _mm256_set1_pd(max_t), _CMP_LE_OQ);
    __m256d u_zero_256d = _mm256_cmp_pd(u_256d, zeros_256d, _CMP_GE_OQ);
    __m256d u_one_256d = _mm256_cmp_pd(u_256d, ones_256d, _CMP_LE_OQ);
    __m256d condition_256d =
        _mm256_and_pd(_mm256_and_pd(t_zero_256d, t_one_256d),
                      _mm256_and_pd(u_zero_256d, u_one_256d));

    // if no lines touch the rectangle then this will be false
    if (_mm256_movemask_pd(condition_256d) == 0x0) {
        return 0;
    }

    __m256d blended_256d =
        _mm256_blendv_pd(_mm256_set1_pd(DBL_MAX), t_256d, condition_256d);

    __m128d min_256d = _mm_min_pd(_mm256_extractf128_pd(blended_256d, 0),
                                  _mm256_extractf128_pd(blended_256d, 1));
    double *min_ptr = (double *)&min_256d;

    *T = min_ptr[0] < min_ptr[1] ? min_ptr[0] : min_ptr[1];

    return 1;
}
#endif /* ~AVX2_IS_SUPPORTED */
