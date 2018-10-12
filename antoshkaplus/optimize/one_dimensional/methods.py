

def greedy_sample_branching(func, segment, sample_count, x_eps=.1**3):
    a, b = segment
    if b - a < x_eps: return (b - a) / 2, func((b - a) / 2)

    unit_dist = (b - a) / sample_count

    c_best = None
    p_best = None
    v_best = None
    # TODO use limit points !!!
    for i in range(sample_count):
        p = (i + 0.5) * unit_dist
        v = func(p)
        if v_best is None or v_best > v:
            p_best = p
            v_best = v
            c_best = 1
        elif v_best == v:
            c_best += 1

    if c_best > 1:
        return p_best, v_best

    return greedy_sample_branching(func, (p_best - unit_dist/2., p_best + unit_dist/2.), sample_count, x_eps)