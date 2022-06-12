import math
import random
import matplotlib.pyplot as plt

DEFAULT_WORLD_FUNCTION = "4;(i+1)**2/16;(i+1)**2;i"


def compute_sinuzoids(domain, count, amplitude_expr, period_expr, phase_expr):
    """
    amplitude_expr * math.sin(x / period_expr - phase_expr)
    """
    functions = [
        (
            eval(amplitude_expr, globals(), locals()),
            eval(period_expr, globals(), locals()),
            eval(phase_expr, globals(), locals()),
        )
        for i in range(count)
    ]

    sinuzoids = [
        [
            amp * math.sin(x / per - pha)
            for amp, per, pha in (functions[i],)
            for x in range(domain)
        ] for i in range(count)
    ]

    return sinuzoids


def create_world(world_width, min_height, max_height, block_size, world_function):
    mid_height = (min_height + max_height) // 2 // block_size * block_size
    amplitude = (max_height - min_height) // 2
    count, *exprs = world_function.split(';')
    sinuzoids = compute_sinuzoids(world_width, int(count), *exprs)
    return [
        int(mid_height + sum(s) / int(count) * amplitude // block_size * block_size)
        for s in zip(*sinuzoids)
    ]



def main():
    count, amp_expr, per_expr, pha_expr = DEFAULT_WORLD_FUNCTION.split(';')

    while True:
        count = int(input(f"Count ({count}): ") or count)
        amp_expr = input(f"Amplitude ({amp_expr}): ") or amp_expr
        per_expr = input(f"Period ({per_expr}): ") or per_expr
        pha_expr = input(f"Phase ({pha_expr}): ") or pha_expr

        try:
            sinuzoids = compute_sinuzoids(500, count, amp_expr, per_expr, pha_expr)
        except Exception as exc:
            print("Error while computing the sinuzoids:", exc)
            continue

        fig, (ax1, ax2) = plt.subplots(2, 1)
        for s in sinuzoids:
            ax1.plot(s)
        ax2.plot([sum(s) / count for s in zip(*sinuzoids)])
        plt.ylim(-1, 1)
        plt.show()
        print("=======")

if __name__ == '__main__':
    main()