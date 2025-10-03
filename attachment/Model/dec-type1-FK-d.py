import operation_7bit_f_k
import os
import sys
import time

filename = operation_7bit_f_k.filename

if __name__ == '__main__':
    with open(filename, 'w') as f:
        f.write('')

    num_branch = 16
    start = time.time()

    if len(sys.argv) > 3:
        num_R_head = int(sys.argv[1])
        num_R_color = int(sys.argv[2])
        num_R_linear = int(sys.argv[3])
    else:
        num_R_head = num_branch - 1
        num_R_color = num_branch ** 2 - num_branch + 1
        num_R_linear = 1
    num_R_sum = num_R_head + num_R_color + num_R_linear

    num_pr = 0
    num_xor = 1
    num_roundfunc = 1

    # type1
    res = ''

    operation_7bit_f_k.initial_var()
    operation_7bit_f_k.generate_round_state(0, num_branch, 'head')
    operation_7bit_f_k.generate_round_state(num_R_head, num_branch, '')
    operation_7bit_f_k.generate_round_state(num_R_head + num_R_color, num_branch, 'linear')
    for r in range(num_R_sum):
        if r < num_R_head:
            operation_7bit_f_k.generate_round_state(r + 1, num_branch, 'head')

            operation_7bit_f_k.COPY(r, 0, num_R_head, num_R_color)
            operation_7bit_f_k.F(r, 0, num_R_head, num_R_color)
            operation_7bit_f_k.AK(r, 0, num_R_head, num_R_color)
            res += operation_7bit_f_k.equal_connect('yhead', 0, r, 'COPY_IN', 0, r)
            res += operation_7bit_f_k.equal_connect('COPY_OUT1', 0, r, 'F_IN', 0, r)
            res += operation_7bit_f_k.equal_connect('F_OUT', 0, r, 'K_IN', 0, r)
            res += operation_7bit_f_k.equal_connect('K_OUT', 0, r, 'XOR_IN1', 0, r)
            res += operation_7bit_f_k.equal_connect('COPY_OUT2', 0, r, 'xhead', num_branch-1, r)

            operation_7bit_f_k.XOR(r, 0, num_R_head, num_R_color)
            res += operation_7bit_f_k.equal_connect('yhead', 1, r, 'XOR_IN2', 0, r)
            res += operation_7bit_f_k.equal_connect('XOR_OUT', 0, r, 'xhead', 0, r)

            for i in range(2, num_branch):
                res += operation_7bit_f_k.equal_connect('yhead', i, r, 'xhead', i-1, r)

            for i in range(num_branch):
                res += operation_7bit_f_k.equal_connect('xhead', i, r + 1, 'yhead', i, r)

        elif r < num_R_head + num_R_color:
            operation_7bit_f_k.generate_round_state(r + 1, num_branch, '')

            operation_7bit_f_k.COPY(r, 0, num_R_head, num_R_color)
            operation_7bit_f_k.F(r, 0, num_R_head, num_R_color)
            operation_7bit_f_k.AK(r, 0, num_R_head, num_R_color)
            res += operation_7bit_f_k.equal_connect('x', num_branch-1, r, 'COPY_IN', 0, r)
            res += operation_7bit_f_k.equal_connect('COPY_OUT1', 0, r, 'F_IN', 0, r)
            res += operation_7bit_f_k.equal_connect('F_OUT', 0, r, 'K_IN', 0, r)
            res += operation_7bit_f_k.equal_connect('K_OUT', 0, r, 'XOR_IN1', 0, r)
            res += operation_7bit_f_k.equal_connect('COPY_OUT2', 0, r, 'y', 0, r)

            operation_7bit_f_k.XOR(r, 0, num_R_head, num_R_color)
            res += operation_7bit_f_k.equal_connect('x', 0, r, 'XOR_IN2', 0, r)
            res += operation_7bit_f_k.equal_connect('XOR_OUT', 0, r, 'y', 1, r)

            for i in range(2, num_branch):
                res += operation_7bit_f_k.equal_connect('y', i, r, 'x', i-1, r)

            for i in range(num_branch):
                res += operation_7bit_f_k.equal_connect('x', i, r + 1, 'y', i, r)

        else:
            operation_7bit_f_k.generate_round_state(r + 1, num_branch, 'linear')

            operation_7bit_f_k.COPY(r, 0, num_R_head, num_R_color)
            operation_7bit_f_k.F(r, 0, num_R_head, num_R_color)
            operation_7bit_f_k.AK(r, 0, num_R_head, num_R_color)
            res += operation_7bit_f_k.equal_connect_linear('ylinear', 0, r, 'COPY_IN', 0, r)
            res += operation_7bit_f_k.equal_connect_linear('COPY_OUT1', 0, r, 'F_IN', 0, r)
            res += operation_7bit_f_k.equal_connect_linear('F_OUT', 0, r, 'K_IN', 0, r)
            res += operation_7bit_f_k.equal_connect_linear('K_OUT', 0, r, 'XOR_IN1', 0, r)
            res += operation_7bit_f_k.equal_connect_linear('COPY_OUT2', 0, r, 'xlinear', num_branch-1, r)

            operation_7bit_f_k.XOR(r, 0, num_R_head, num_R_color)
            res += operation_7bit_f_k.equal_connect_linear('ylinear', 1, r, 'XOR_IN2', 0, r)
            res += operation_7bit_f_k.equal_connect_linear('XOR_OUT', 0, r, 'xlinear', 0, r)

            for i in range(2, num_branch):
                res += operation_7bit_f_k.equal_connect_linear('ylinear', i, r, 'xlinear', i-1, r)

            for i in range(num_branch):
                res += operation_7bit_f_k.equal_connect_linear('xlinear', i, r + 1, 'ylinear', i, r)

    operation_7bit_f_k.link_round_state(num_branch, num_pr, num_R_head, num_R_color, num_R_linear)

    with open(filename, 'a') as f:
        f.write(res)

    res = ''
    res += f'ASSERT(x_0_{num_branch-1} = 0bin0000100);\n'
    for i in range(1,num_branch-1):
        res += f'ASSERT(x_{i}_{num_branch-1} = 0bin0000001);\n'
    res += f'ASSERT(x_{num_branch-1}_{num_branch-1} = 0bin0000011);\n'
    res += f"ASSERT(BVXOR(period_value1, period_value2) = 0bin1000000001);\n"


    with open(filename, 'a') as f:
        f.write(res)

    operation_7bit_f_k.END(num_R_sum, num_branch, num_R_linear)

    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')




