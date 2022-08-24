#include "include/pygame.h"
#include "include/collisions.h"
#include <stdio.h>

#if (defined(__AVX2__) || defined(__SSE2__)) && defined(HAVE_IMMINTRIN_H)
#include <immintrin.h>
#endif

#if !defined(PG_ENABLE_ARM_NEON) && defined(__aarch64__)
// arm64 has neon optimisations enabled by default, even when fpu=neon is not
// passed
#define PG_ENABLE_ARM_NEON 1
#endif

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H)
#define AVX2_IS_SUPPORTED 1
#else
#define AVX2_IS_SUPPORTED 0
#endif /* ~defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H) */

#ifdef AVX2_IS_SUPPORTED
PG_FORCEINLINE static int
pgIntersection_LineRect_avx2(pgLineBase *line, SDL_Rect *rect, double *X, double *Y,
                        double *T);
PG_FORCEINLINE static int
pgCollision_RectLine_avx2(SDL_Rect *rect, pgLineBase *line);
#endif
