import random
from itertools import combinations

filename = 'model2.cvc'
STATE_BITNUM = 7
VALUE_BITNUM = 10
LINEAR_BITNUM = 2


def KEY_SUM1(sum_r, sum_ak):
    res = 'ASSERT(BVLE(BVPLUS(10'
    for r in range(sum_r):
        for i in range(sum_ak):
            res += ',0bin000000000@subkey_any_%s_%s' % (str(i), str(r))
    res += '), 0bin0000000000 ));\n'

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def define_var(name, d, num_r, bitnum):
    result = '{}_{}_{} : BITVECTOR({});\n'.format(name, d, num_r, bitnum)
    return result


def limitation_var_k(name, d, r):
    result = ''
    zero = '0' * VALUE_BITNUM
    result += 'ASSERT({0}_{1}_{2}[0:0] = 0bin1 => {0}_k_{1}_{2} /= 0bin{3});\n'.format(name, str(d), str(r), zero)
    result += 'ASSERT({0}_{1}_{2}[0:0] = 0bin0 => {0}_k_{1}_{2} = 0bin{3});\n'.format(name, str(d), str(r), zero)
    return result


def limitation_var_linear(name, d, r):
    result = ''
    result += 'ASSERT({0}_{1}_{2}[1:1] = 0bin1 => {0}_{1}_{2}[0:0] = 0bin1);\n'.format(name, str(d), str(r))
    result += 'ASSERT({0}_{1}_{2}[0:0] = 0bin0 => {0}_{1}_{2}[1:1] = 0bin0);\n'.format(name, str(d), str(r))
    return result


def equal_connect(name1, d1, r1, name2, d2, r2):
    result = ''
    result += 'ASSERT({}_{}_{} = {}_{}_{});\n'.format(name1, str(d1), str(r1), name2, str(d2), str(r2))
    result += 'ASSERT({}_k_{}_{} = {}_k_{}_{});\n'.format(name1, str(d1), str(r1), name2, str(d2), str(r2))

    return result


def equal_connect_linear(name1, d1, r1, name2, d2, r2):
    result = ''
    result += 'ASSERT({}_{}_{} = {}_{}_{});\n'.format(name1, str(d1), str(r1), name2, str(d2), str(r2))

    return result


def generate_F():
    F = list(range(2**VALUE_BITNUM))
    random.shuffle(F)
    # print(F)

    result = 'F: ARRAY BITVECTOR({0}) OF BITVECTOR({0});\n'.format(str(VALUE_BITNUM))
    for i in range(2**VALUE_BITNUM):
        result += 'ASSERT(F[0bin{}] = 0bin{});\n'.format(bin(i)[2:].zfill(VALUE_BITNUM),bin(F[i])[2:].zfill(VALUE_BITNUM))

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def generate_round_state(num_r, num_branch, name):
    result = ''
    if name != 'linear':
        for d in range(num_branch):
            result += define_var('x' + name, d, num_r, STATE_BITNUM)
            result += define_var('y' + name, d, num_r, STATE_BITNUM)
            result += define_var('x' + name + '_k', d, num_r, VALUE_BITNUM)
            result += define_var('y' + name + '_k', d, num_r, VALUE_BITNUM)
            result += limitation_var_k('x' + name, d, num_r)
            result += limitation_var_k('y' + name, d, num_r)
    else:
        for d in range(num_branch):
            result += define_var('x' + name, d, num_r, LINEAR_BITNUM)
            result += define_var('y' + name, d, num_r, LINEAR_BITNUM)
            result += limitation_var_linear('x' + name, d, num_r)
            result += limitation_var_linear('y' + name, d, num_r)

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def initial_var():
    result = ''
    result += 'end : BITVECTOR(1);\n'
    result += 'ASSERT(end = 0bin1);\n'
    result += 'period_value1 : BITVECTOR(%s);\n' % str(VALUE_BITNUM)
    result += 'period_value2 : BITVECTOR(%s);\n' % str(VALUE_BITNUM)
    result += 'ASSERT(period_value1 /= period_value2);\n'

    generate_F()

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def link_round_state(num_branch, head_pr, head_r, middle_r, linear_r):
    result = ''
    result += 'ASSERT(BVPLUS(10'
    for d in range(num_branch):
        result += ',0bin000000000@xhead_{}_0[0:0]'.format(str(d))
    result += ') = 0bin{});\n'.format(bin(head_pr)[2:].zfill(10))

    for d in range(num_branch):
        result += 'ASSERT(x_%s_%s[6:5] = 0bin00);\n' % (str(d), str(head_r))
        result += 'ASSERT(x_%s_%s[4:4] = 0bin1 => period_value1 = 0bin%s);\n' % (str(d), str(head_r), bin(0)[2:].zfill(VALUE_BITNUM))
        result += 'ASSERT(x_%s_%s[2:2] = 0bin1 => period_value2 = 0bin%s);\n' % (str(d), str(head_r), bin(0)[2:].zfill(VALUE_BITNUM))

    tmp = ''
    for d in range(num_branch - 1):
        tmp += '(x_{0}_{1}[1:1]| x_{0}_{1}[2:2] | x_{0}_{1}[3:3] | x_{0}_{1}[4:4] = 0bin1) OR  '.format(str(d), str(head_r))
    tmp += '(x_{0}_{1}[1:1] | x_{0}_{1}[2:2] | x_{0}_{1}[3:3] | x_{0}_{1}[4:4] = 0bin1)'.format(str(num_branch - 1), str(head_r))
    result += 'ASSERT(' + tmp + ');\n'

    for d in range(num_branch):
        result += 'ASSERT(xhead_{0}_{1} = x_{0}_{1});\n'.format(str(d), str(head_r))
        result += 'ASSERT(xhead_k_{0}_{1} = x_k_{0}_{1});\n'.format(str(d), str(head_r))

    if linear_r > 0:
        for d in range(num_branch):
            result += '%s_%s_%s : BITVECTOR(1);\n' % ("xlinearfirstmask", str(d), str(head_r + middle_r))

        result += "MASKSUM: BITVECTOR(6);\n"
        result += "ASSERT(MASKSUM = 0bin000001);\n"
        result += 'ASSERT(MASKSUM = BVPLUS(6, '
        for d in range(num_branch - 1):
            result += '0bin00000@%s_%s_%s, ' % ("xlinearfirstmask", str(d), str(head_r + middle_r))
        result += '0bin00000@%s_%s_%s));\n' % ("xlinearfirstmask", str(num_branch - 1), str(head_r + middle_r))

        for d in range(num_branch):
            result += 'ASSERT((NOT(x_{0}_{1}[6:5] = 0bin01 AND x_{0}_{1}[4:4] = x_{0}_{1}[2:2]) AND NOT(x_{0}_{1}[4:4] = 0bin1 AND x_{0}_{1}[2:2] = 0bin1 AND x_{0}_{1}[6:6] = 0bin0) AND NOT(x_{0}_{1}[6:6] = 0bin0 AND x_{0}_{1}[4:4] = 0bin1 AND period_value1 /= 0bin{2}) AND NOT(x_{0}_{1}[6:6] = 0bin0 AND x_{0}_{1}[2:2] = 0bin1 AND period_value2 /= 0bin{2})) => xlinearfirstmask_{0}_{1} = 0bin0);\n'.format(d, head_r + middle_r ,'0'*VALUE_BITNUM)

        for d in range(num_branch):
            result += "ASSERT(xlinearfirstmask_{0}_{1} = 0bin1) => (xlinear_{0}_{1}[0:0] = 0bin1);\n".format(d, head_r + middle_r)

    with open(filename, 'a') as f:
        f.write(result)


def XOR(num_r, num_xor, head_r, middle_r):
    result = ''

    if num_r < head_r + middle_r:
        result += define_var('XOR_IN1', num_xor, num_r, STATE_BITNUM)
        result += define_var('XOR_IN2', num_xor, num_r, STATE_BITNUM)
        result += define_var('XOR_OUT', num_xor, num_r, STATE_BITNUM)
        result += define_var('XOR_IN1_k', num_xor, num_r, VALUE_BITNUM)
        result += define_var('XOR_IN2_k', num_xor, num_r, VALUE_BITNUM)
        result += define_var('XOR_OUT_k', num_xor, num_r, VALUE_BITNUM)
        result += limitation_var_k('XOR_IN1', num_xor, num_r)
        result += limitation_var_k('XOR_IN2', num_xor, num_r)
        result += limitation_var_k('XOR_OUT', num_xor, num_r)

        result += 'ASSERT(XOR_OUT_{0}_{1}[6:6] = XOR_IN1_{0}_{1}[6:6] | XOR_IN2_{0}_{1}[6:6]);\n'.format(str(num_xor), str(num_r))

        result += 'ASSERT(XOR_OUT_{0}_{1}[5:5] = XOR_IN1_{0}_{1}[5:5] | XOR_IN2_{0}_{1}[5:5]);\n'.format(str(num_xor), str(num_r))

        result += 'ASSERT(XOR_OUT_{0}_{1}[4:4] = BVXOR(XOR_IN1_{0}_{1}[4:4] , XOR_IN2_{0}_{1}[4:4]));\n'.format(str(num_xor), str(num_r))

        result += 'ASSERT(XOR_OUT_{0}_{1}[3:3] = XOR_IN1_{0}_{1}[3:3] | XOR_IN2_{0}_{1}[3:3]);\n'.format(str(num_xor), str(num_r))

        result += 'ASSERT(XOR_OUT_{0}_{1}[2:2] = BVXOR(XOR_IN1_{0}_{1}[2:2] , XOR_IN2_{0}_{1}[2:2]));\n'.format(str(num_xor), str(num_r))

        result += 'ASSERT(XOR_OUT_{0}_{1}[1:1] = BVXOR(XOR_IN1_{0}_{1}[1:1] , XOR_IN2_{0}_{1}[1:1]));\n'.format(str(num_xor), str(num_r))

        result += 'ASSERT(NOT(XOR_IN1_k_{0}_{1} = XOR_IN2_k_{0}_{1}) => XOR_OUT_{0}_{1}[0:0] = XOR_IN1_{0}_{1}[0:0] | XOR_IN2_{0}_{1}[0:0]);\n'.format(str(num_xor), str(num_r))
        result += 'ASSERT((XOR_IN1_k_{0}_{1} = XOR_IN2_k_{0}_{1}) => XOR_OUT_{0}_{1}[0:0] = BVXOR(XOR_IN1_{0}_{1}[0:0], XOR_IN2_{0}_{1}[0:0]));\n'.format(str(num_xor), str(num_r))

        result += 'ASSERT(XOR_OUT_k_{0}_{1} = BVXOR(XOR_IN1_k_{0}_{1}, XOR_IN2_k_{0}_{1}));\n'.format(str(num_xor), str(num_r))

    else:
        result += define_var('XOR_IN1', num_xor, num_r, LINEAR_BITNUM)
        result += define_var('XOR_IN2', num_xor, num_r, LINEAR_BITNUM)
        result += define_var('XOR_OUT', num_xor, num_r, LINEAR_BITNUM)
        result += limitation_var_linear('XOR_IN1', num_xor, num_r)
        result += limitation_var_linear('XOR_IN2', num_xor, num_r)
        result += limitation_var_linear('XOR_OUT', num_xor, num_r)

        result += 'ASSERT(XOR_OUT_%s_%s[0:0] = (XOR_IN1_%s_%s[0:0] & XOR_IN2_%s_%s[0:0]));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))
        result += 'ASSERT(XOR_OUT_%s_%s[1:1] = (XOR_IN1_%s_%s[1:1] & XOR_IN2_%s_%s[1:1]));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def F(num_r, num_f, head_r, middle_r):
    result = ''
    if num_r < head_r:
        result += define_var('F_IN', num_f, num_r, STATE_BITNUM)
        result += define_var('F_OUT', num_f, num_r, STATE_BITNUM)
        result += define_var('F_IN_k', num_f, num_r, VALUE_BITNUM)
        result += define_var('F_OUT_k', num_f, num_r, VALUE_BITNUM)
        result += limitation_var_k('F_IN', num_f, num_r)
        result += limitation_var_k('F_OUT', num_f, num_r)
        result += 'ASSERT((F_IN_{0}_{1}[0:0] | F_IN_{0}_{1}[5:5] | F_IN_{0}_{1}[4:4] | F_IN_{0}_{1}[6:6] = 0bin1) => (end = 0bin0));\n'.format(str(num_f), str(num_r))
        result += 'ASSERT((F_IN_{0}_{1}[4:4] = 0bin1 AND period_value1 /= 0bin{2}) OR (F_IN_{0}_{1}[2:2] = 0bin1 AND period_value2 /= 0bin{2}) => end = 0bin0);\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))
        result += 'ASSERT(IF (F_IN_{0}_{1} = 0bin0000000) THEN (F_OUT_{0}_{1} = 0bin0000000) ELSE (F_OUT_{0}_{1} = 0bin0001000) ENDIF);\n'.format(str(num_f), str(num_r))

    elif num_r < head_r + middle_r:
        result += define_var('F_IN', num_f, num_r, STATE_BITNUM)
        result += define_var('F_OUT', num_f, num_r, STATE_BITNUM)
        result += define_var('F_IN_k', num_f, num_r, VALUE_BITNUM)
        result += define_var('F_OUT_k', num_f, num_r, VALUE_BITNUM)
        result += limitation_var_k('F_IN', num_f, num_r)
        result += limitation_var_k('F_OUT', num_f, num_r)

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000000) => (F_OUT_{0}_{1} = 0bin0000000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000001) => (F_OUT_{0}_{1} = 0bin0000001));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000010) => (F_OUT_{0}_{1} = 0bin0001000 AND period_value1 /= 0b{2} AND period_value2 /= 0b{2}) OR (F_OUT_{0}_{1} = 0bin0010000 AND period_value1 = 0b{2}) OR (F_OUT_{0}_{1} = 0bin0000100 AND period_value2 = 0b{2}));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))

        if num_r == 0:
            result += 'ASSERT((F_IN_{0}_{1} = 0bin0000100 AND period_value2 = 0b{2}) => (F_OUT_{0}_{1} = 0bin0000100));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))
            result += 'ASSERT((F_IN_{0}_{1} = 0bin0010000 AND period_value1 = 0b{2}) => (F_OUT_{0}_{1} = 0bin0010000));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))

        else:
            result += 'ASSERT((F_IN_{0}_{1} = 0bin0000100 AND period_value2 = 0b{2}) => (F_OUT_{0}_{1} = 0bin0001000));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))
            result += 'ASSERT((F_IN_{0}_{1} = 0bin0010000 AND period_value1 = 0b{2}) => (F_OUT_{0}_{1} = 0bin0001000));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0001000) => (F_OUT_{0}_{1} = 0bin0001000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0100000) => (F_OUT_{0}_{1} = 0bin0100000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000011 AND F_IN_k_{0}_{1} = period_value1) => (F_OUT_{0}_{1} = 0bin0010000));\n'.format(str(num_f), str(num_r))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000011 AND F_IN_k_{0}_{1} = period_value2) => (F_OUT_{0}_{1} = 0bin0000100));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000011 AND F_IN_k_{0}_{1} /= period_value1 AND F_IN_k_{0}_{1} /= period_value2 ) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0001001) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0010001) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000101) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0100001) => (F_OUT_{0}_{1} = 0bin0100000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0001010) => (F_OUT_{0}_{1} = 0bin0001000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0010010) => (F_OUT_{0}_{1} = 0bin1000000 AND period_value1 /= 0b{2}) OR (F_OUT_{0}_{1} = 0bin0001000 AND period_value1 = 0b{2}));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000110) => (F_OUT_{0}_{1} = 0bin1000000 AND period_value2 /= 0b{2}) OR (F_OUT_{0}_{1} = 0bin0001000 AND period_value2 = 0b{2}));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0100010) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0011000) => (F_OUT_{0}_{1} = 0bin1000000 AND period_value1 /= 0b{2}) OR (F_OUT_{0}_{1} = 0bin0001000 AND period_value1 = 0b{2}));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0001100) => (F_OUT_{0}_{1} = 0bin1000000 AND period_value2 /= 0b{2}) OR (F_OUT_{0}_{1} = 0bin0001000 AND period_value2 = 0b{2}));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0010100) => (F_OUT_{0}_{1} = 0bin0100000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0100100) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0110000) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0101000) => (F_OUT_{0}_{1} = 0bin1000000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0011010) => (F_OUT_{0}_{1} = 0bin1000000 AND period_value1 /= 0b{2}) OR (F_OUT_{0}_{1} = 0bin0001000 AND period_value1 = 0b{2}));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0001110) => (F_OUT_{0}_{1} = 0bin1000000 AND period_value2 /= 0b{2}) OR (F_OUT_{0}_{1} = 0bin0001000 AND period_value2 = 0b{2}));\n'.format(str(num_f), str(num_r), bin(0)[2:].zfill(VALUE_BITNUM))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0010101) => (F_OUT_{0}_{1} = 0bin0100000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0110100) => (F_OUT_{0}_{1} = 0bin0100000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0110101) => (F_OUT_{0}_{1} = 0bin0100000));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1}[6:6] = 0bin1) => (F_OUT_{0}_{1}[6:6] = 0bin1));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT((F_IN_{0}_{1} = 0bin0000111 OR F_IN_{0}_{1} = 0bin0001011 OR F_IN_{0}_{1} = 0bin0010011 OR F_IN_{0}_{1} = 0bin0100011 OR F_IN_{0}_{1} = 0bin0001101 OR F_IN_{0}_{1} = 0bin0100101 OR F_IN_{0}_{1} = 0bin0011001 OR F_IN_{0}_{1} = 0bin0101001 OR F_IN_{0}_{1} = 0bin0110001 OR F_IN_{0}_{1} = 0bin0010110 OR F_IN_{0}_{1} = 0bin0100110 OR F_IN_{0}_{1} = 0bin0011010 OR F_IN_{0}_{1} = 0bin0101010 OR F_IN_{0}_{1} = 0bin0110010 OR F_IN_{0}_{1} = 0bin0011100 OR F_IN_{0}_{1} = 0bin0101100 OR F_IN_{0}_{1} = 0bin0110100 OR F_IN_{0}_{1} = 0bin0111000) => (F_OUT_{0}_{1}[6:6] = 0bin1));\n'.format(str(num_f), str(num_r))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0001111 OR F_IN_{0}_{1} = 0bin0010111 OR F_IN_{0}_{1} = 0bin0100111 OR F_IN_{0}_{1} = 0bin0011011 OR F_IN_{0}_{1} = 0bin0101011 OR F_IN_{0}_{1} = 0bin0110011 OR F_IN_{0}_{1} = 0bin0011101 OR F_IN_{0}_{1} = 0bin0101101 OR F_IN_{0}_{1} = 0bin0110101 OR F_IN_{0}_{1} = 0bin0111001 OR F_IN_{0}_{1} = 0bin0011110 OR F_IN_{0}_{1} = 0bin0101110 OR F_IN_{0}_{1} = 0bin0110110 OR F_IN_{0}_{1} = 0bin0111010 OR F_IN_{0}_{1} = 0bin0111100) => (F_OUT_{0}_{1}[6:6] = 0bin1));\n'.format(str(num_f), str(num_r))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0011111 OR F_IN_{0}_{1} = 0bin0101111 OR F_IN_{0}_{1} = 0bin0110111 OR F_IN_{0}_{1} = 0bin0111011 OR F_IN_{0}_{1} = 0bin0111101 OR F_IN_{0}_{1} = 0bin0111110) => (F_OUT_{0}_{1}[6:6] = 0bin1));\n'.format(str(num_f), str(num_r))
        result += 'ASSERT((F_IN_{0}_{1} = 0bin0111111) => (F_OUT_{0}_{1}[6:6] = 0bin1));\n'.format(str(num_f), str(num_r))

        result += 'ASSERT(F_OUT_{0}_{1}[0:0] = 0bin1 => F_OUT_k_{0}_{1} = F[F_IN_k_{0}_{1}]);\n'.format(str(num_f), str(num_r))

    else:
        result += define_var('F_IN', num_f, num_r, LINEAR_BITNUM)
        result += define_var('F_OUT', num_f, num_r, LINEAR_BITNUM)
        result += limitation_var_linear('F_IN', num_f, num_r)
        result += limitation_var_linear('F_OUT', num_f, num_r)

        result += "ASSERT (F_IN_{0}_{1} = 0bin00) => ((F_OUT_{0}_{1} = 0bin00));\n".format(num_f, num_r)
        result += "ASSERT (F_IN_{0}_{1} = 0bin01) => ((F_OUT_{0}_{1} = 0bin00));\n".format(num_f, num_r)
        result += "ASSERT (F_IN_{0}_{1} = 0bin11) => ((F_OUT_{0}_{1} = 0bin11));\n".format(num_f, num_r)

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def AK(num_r, num_ak, head_r, middle_r):
    result = ''

    if num_r < head_r + middle_r:
        result += define_var('K_IN', num_ak, num_r, STATE_BITNUM)
        result += define_var('K_OUT', num_ak, num_r, STATE_BITNUM)
        result += define_var('K_IN_k', num_ak, num_r, VALUE_BITNUM)
        result += define_var('K_OUT_k', num_ak, num_r, VALUE_BITNUM)
        result += limitation_var_k('K_IN', num_ak, num_r)
        result += limitation_var_k('K_OUT', num_ak, num_r)

        if num_r < VALUE_BITNUM:
            bit_string = ['0' for i in range(VALUE_BITNUM)]
            bit_string[VALUE_BITNUM - 1 - num_r] = '1'
            bit_string[num_ak] = '1'
            subkey = ''.join(bit_string)
        elif VALUE_BITNUM <= num_r < 2 * VALUE_BITNUM:
            bit_string = ['1' for i in range(VALUE_BITNUM)]
            bit_string[VALUE_BITNUM - 1 - num_r] = '0'
            bit_string[num_ak] = '0'
            subkey = ''.join(bit_string)
        else:
            bit_string = [str(random.randint(0,1)) for i in range(VALUE_BITNUM)]
            subkey = ''.join(bit_string)
        # print(subkey)

        result += 'ASSERT(K_IN_k_{0}_{1} = {2} => (K_OUT_{0}_{1}[0:0] = 0bin0 AND K_OUT_{0}_{1}[6:1] = K_IN_{0}_{1}[6:1]));\n'.format(str(num_ak), str(num_r), '0bin'+subkey)
        result += 'ASSERT((K_IN_k_{0}_{1} /= {2}) => (K_OUT_k_{0}_{1} = BVXOR(K_IN_k_{0}_{1}, {2}) AND K_OUT_{0}_{1}[0:0] = 0bin1 AND K_OUT_{0}_{1}[6:1] = K_IN_{0}_{1}[6:1]));\n'.format(str(num_ak), str(num_r), '0bin'+subkey)

    else:
        result += define_var('K_IN', num_ak, num_r, LINEAR_BITNUM)
        result += define_var('K_OUT', num_ak, num_r, LINEAR_BITNUM)
        result += limitation_var_linear('K_IN', num_ak, num_r)
        result += limitation_var_linear('K_OUT', num_ak, num_r)

        result += "ASSERT (K_IN_{0}_{1} = 0bin00) => ((K_OUT_{0}_{1} = 0bin00));\n".format(num_ak, num_r)
        result += "ASSERT (K_IN_{0}_{1} = 0bin01) => ((K_OUT_{0}_{1} = 0bin01));\n".format(num_ak, num_r)
        result += "ASSERT (K_IN_{0}_{1} = 0bin11) => ((K_OUT_{0}_{1} = 0bin01));\n".format(num_ak, num_r)

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def AK_prob(num_r, num_ak, head_r, middle_r, subkey):
    result = ''

    if num_r < head_r + middle_r:
        result += define_var('K_IN', num_ak, num_r, STATE_BITNUM)
        result += define_var('K_OUT', num_ak, num_r, STATE_BITNUM)
        result += define_var('K_IN_k', num_ak, num_r, VALUE_BITNUM)
        result += define_var('K_OUT_k', num_ak, num_r, VALUE_BITNUM)
        result += define_var('subkey', num_ak, num_r, VALUE_BITNUM)
        result += define_var('subkey_any', num_ak, num_r, 1)
        result += limitation_var_k('K_IN', num_ak, num_r)
        result += limitation_var_k('K_OUT', num_ak, num_r)

        result += 'ASSERT(subkey_{0}_{1} = {2} OR subkey_any_{0}_{1} = 0bin1);\n'.format(str(num_ak),str(num_r),'0bin'+subkey)

        result += 'ASSERT(K_IN_k_{0}_{1} = subkey_{0}_{1} => (K_OUT_{0}_{1}[0:0] = 0bin0 AND K_OUT_{0}_{1}[6:1] = K_IN_{0}_{1}[6:1]));\n'.format(str(num_ak), str(num_r))
        result += 'ASSERT((K_IN_k_{0}_{1} /= subkey_{0}_{1}) => (K_OUT_k_{0}_{1} = BVXOR(K_IN_k_{0}_{1}, subkey_{0}_{1}) AND K_OUT_{0}_{1}[0:0] = 0bin1 AND K_OUT_{0}_{1}[6:1] = K_IN_{0}_{1}[6:1]));\n'.format(str(num_ak), str(num_r))

    else:
        result += define_var('K_IN', num_ak, num_r, LINEAR_BITNUM)
        result += define_var('K_OUT', num_ak, num_r, LINEAR_BITNUM)
        result += limitation_var_linear('K_IN', num_ak, num_r)
        result += limitation_var_linear('K_OUT', num_ak, num_r)

        result += "ASSERT (K_IN_{0}_{1} = 0bin00) => ((K_OUT_{0}_{1} = 0bin00));\n".format(num_ak, num_r)
        result += "ASSERT (K_IN_{0}_{1} = 0bin01) => ((K_OUT_{0}_{1} = 0bin01));\n".format(num_ak, num_r)
        result += "ASSERT (K_IN_{0}_{1} = 0bin11) => ((K_OUT_{0}_{1} = 0bin01));\n".format(num_ak, num_r)

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def COPY(num_r, num_copy, head_r, middle_r):
    result = ''
    if num_r < head_r + middle_r:
        result += define_var('COPY_IN', num_copy, num_r, STATE_BITNUM)
        result += define_var('COPY_OUT1', num_copy, num_r, STATE_BITNUM)
        result += define_var('COPY_OUT2', num_copy, num_r, STATE_BITNUM)
        result += define_var('COPY_IN_k', num_copy, num_r, VALUE_BITNUM)
        result += define_var('COPY_OUT1_k', num_copy, num_r, VALUE_BITNUM)
        result += define_var('COPY_OUT2_k', num_copy, num_r, VALUE_BITNUM)
        result += limitation_var_k('COPY_IN', num_copy, num_r)
        result += limitation_var_k('COPY_OUT1', num_copy, num_r)
        result += limitation_var_k('COPY_OUT2', num_copy, num_r)

        result += 'ASSERT(COPY_OUT1_%s_%s = COPY_IN_%s_%s);\n' % (str(num_copy), str(num_r), str(num_copy), str(num_r))
        result += 'ASSERT(COPY_OUT2_%s_%s = COPY_IN_%s_%s);\n' % (str(num_copy), str(num_r), str(num_copy), str(num_r))
        result += 'ASSERT(COPY_OUT1_k_%s_%s = COPY_IN_k_%s_%s);\n' % (str(num_copy), str(num_r), str(num_copy), str(num_r))
        result += 'ASSERT(COPY_OUT2_k_%s_%s = COPY_IN_k_%s_%s);\n' % (str(num_copy), str(num_r), str(num_copy), str(num_r))

    else:
        result += define_var('COPY_IN', num_copy, num_r, LINEAR_BITNUM)
        result += define_var('COPY_OUT1', num_copy, num_r, LINEAR_BITNUM)
        result += define_var('COPY_OUT2', num_copy, num_r, LINEAR_BITNUM)
        result += limitation_var_linear('COPY_IN', num_copy, num_r)
        result += limitation_var_linear('COPY_OUT1', num_copy, num_r)
        result += limitation_var_linear('COPY_OUT2', num_copy, num_r)

        result += "ASSERT COPY_OUT1_{0}_{1} = COPY_IN_{0}_{1};\n".format(num_copy, num_r)
        result += "ASSERT COPY_OUT2_{0}_{1} = COPY_IN_{0}_{1};\n".format(num_copy, num_r)

    with open(filename, 'a') as f:
        f.write(result)

    return 0


def END(end_r, num_branch, linear_r):
    result = ''
    if linear_r == 0:
        result += 'ASSERT('
        for d in range(num_branch-1):
            result += '(x_{0}_{1}[6:5] = 0bin01 AND x_{0}_{1}[4:4] = x_{0}_{1}[2:2]) OR (x_{0}_{1}[4:4] = 0bin1 AND x_{0}_{1}[2:2] = 0bin1 AND x_{0}_{1}[6:6] = 0bin0) OR (x_{0}_{1}[6:6] = 0bin0 AND x_{0}_{1}[4:4] = 0bin1 AND period_value1 /= 0bin{2}) OR (x_{0}_{1}[6:6] = 0bin0 AND x_{0}_{1}[2:2] = 0bin1 AND period_value2 /= 0bin{2})'.format(d, end_r, '0'*VALUE_BITNUM)
            result += ' OR '
        d = num_branch-1
        result += '(x_{0}_{1}[6:5] = 0bin01 AND x_{0}_{1}[4:4] = x_{0}_{1}[2:2]) OR (x_{0}_{1}[4:4] = 0bin1 AND x_{0}_{1}[2:2] = 0bin1 AND x_{0}_{1}[6:6] = 0bin0) OR (x_{0}_{1}[6:6] = 0bin0 AND x_{0}_{1}[4:4] = 0bin1 AND period_value1 /= 0bin{2}) OR (x_{0}_{1}[6:6] = 0bin0 AND x_{0}_{1}[2:2] = 0bin1 AND period_value2 /= 0bin{2}));\n'.format(d, end_r, '0'*VALUE_BITNUM)

    with open(filename, 'a') as f:
        f.write(result)

    return 0


if __name__ == '__main__':
    with open(filename,'w') as f:
        f.write('')
        generate_F()
        with open(filename, 'a') as f:
            f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')
    
    
    
