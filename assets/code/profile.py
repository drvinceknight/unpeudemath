from memory_profiler import profile

precision = 10

fp = open('memory_profiler_basic_mean.log', 'w+')
@profile(precision=precision, stream=fp)
def basic_mean(N=5):
    nbrs = list(range(0, 10 ** N))
    total = sum(nbrs)
    mean = total / len(nbrs)
    return mean

fp = open('memory_profiler_basic_mean_with_gen.log', 'w+')
@profile(precision=precision, stream=fp)
def basic_mean_with_gen(N=5):
    nbrs = range(0, 10 ** N)
    total = sum(nbrs)
    mean = total / len(nbrs)
    return mean

if __name__ == '__main__':
    basic_mean()
    basic_mean_with_gen()
