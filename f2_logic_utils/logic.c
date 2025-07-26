#include "logic.h"
#include <stdlib.h>

uint8_t rho(LogicOp op, Predicate* a, Predicate* b, uint8_t* values) {
    switch(op) {
        case PLAIN:
            return f2poly_eval(a->poly, values);
        case NOT: {
            uint8_t val = f2poly_eval(a->poly, values);
            return val ^ 1;
        }
        case AND: {
            uint8_t val1 = f2poly_eval(a->poly, values);
            uint8_t val2 = f2poly_eval(b->poly, values);
            return val1 & val2;
        }
        case OR: {
            uint8_t val1 = f2poly_eval(a->poly, values);
            uint8_t val2 = f2poly_eval(b->poly, values);
            return (val1 & val2) ^ val1 ^ val2;
        }
    }
    return 0;
}