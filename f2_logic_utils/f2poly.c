#include "f2poly.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

F2Poly* f2poly_empty() {
    F2Poly* p = malloc(sizeof(F2Poly));
    p->num_terms = 0;
    p->capacity = 8;
    p->terms = malloc(sizeof(Monomial) * p->capacity);
    return p;
}

void f2poly_free(F2Poly* p) {
    free(p->terms);
    free(p);
}

void f2poly_add_term(F2Poly* p, Monomial m) {
    for (size_t i = 0; i < p->num_terms; ++i) {
        if (p->terms[i] == m) {
            memmove(&p->terms[i], &p->terms[i+1], sizeof(Monomial)*(p->num_terms - i - 1));
            p->num_terms--;
            return;
        }
    }
    if (p->num_terms == p->capacity) {
        p->capacity *= 2;
        p->terms = realloc(p->terms, sizeof(Monomial) * p->capacity);
    }
    p->terms[p->num_terms++] = m;
}

F2Poly* f2poly_add(F2Poly* a, F2Poly* b) {
    F2Poly* result = f2poly_empty();
    for (size_t i = 0; i < a->num_terms; ++i)
        f2poly_add_term(result, a->terms[i]);
    for (size_t i = 0; i < b->num_terms; ++i)
        f2poly_add_term(result, b->terms[i]);
    return result;
}

F2Poly* f2poly_mul(F2Poly* a, F2Poly* b) {
    F2Poly* result = f2poly_empty();
    for (size_t i = 0; i < a->num_terms; ++i) {
        for (size_t j = 0; j < b->num_terms; ++j) {
            Monomial m = a->terms[i] | b->terms[j];
            f2poly_add_term(result, m);
        }
    }
    return result;
}

uint8_t f2poly_eval(F2Poly* p, uint8_t* values) {
    uint8_t result = 0;
    for (size_t i = 0; i < p->num_terms; ++i) {
        Monomial m = p->terms[i];
        uint8_t val = 1;
        for (int b = 0; b < MAX_VARS; ++b) {
            if ((m >> b) & 1) val &= values[b];
        }
        result ^= val;
    }
    return result;
}

void f2poly_print(F2Poly* p) {
    if (p->num_terms == 0) {
        printf("0\n");
        return;
    }
    for (size_t i = 0; i < p->num_terms; ++i) {
        if (i > 0) printf(" + ");
        Monomial m = p->terms[i];
        if (m == 0) {
            printf("1");
            continue;
        }
        int first = 1;
        for (int b = 0; b < MAX_VARS; ++b) {
            if ((m >> b) & 1) {
                if (!first) printf("*");
                printf("x%d", b + 1);
                first = 0;
            }
        }
    }
    printf("\n");
}

// 辅助函数：跳过空格
static void skip_ws(const char** p) {
    while (isspace(**p)) (*p)++;
}

// 从字符串中提取一个 monomial
static Monomial parse_monomial(const char** p) {
    Monomial m = 0;
    skip_ws(p);
    if (**p == '1') {
        (*p)++;
        return 0;
    }

    while (**p == 'x') {
        (*p)++; // skip 'x'
        int var = 0;
        while (isdigit(**p)) {
            var = var * 10 + (**p - '0');
            (*p)++;
        }
        if (var <= 0 || var > MAX_VARS) {
            fprintf(stderr, "Variable x%d out of range\n", var);
            exit(1);
        }
        m |= (1 << (var - 1));
        skip_ws(p);
        if (**p == '*') {
            (*p)++;
            skip_ws(p);
        } else {
            break;
        }
    }
    return m;
}

// 从字符串创建多项式
F2Poly* f2poly_create(const char* str) {
    F2Poly* p = f2poly_empty();
    const char* ptr = str;
    while (*ptr) {
        skip_ws(&ptr);
        Monomial m = parse_monomial(&ptr);
        f2poly_add_term(p, m);
        skip_ws(&ptr);
        if (*ptr == '+') {
            ptr++;
        }
    }
    return p;
}