from memory_profiler import profile

precision = 10
fp = open('memory_profiler_even_mean.log', 'w+')

@profile(precision=precision, stream=fp)
def basic_mean(N=5):
    nbrs = [n for n in range(0, 10 ** N) if n % 2 == 0]
    total = sum(nbrs)
    mean = total / len(nbrs)
    return mean

@profile(precision=precision, stream=fp)
def basic_mean_with_gen(N=5):
    nbrs = (n for n in range(0, 10 ** N) if n % 2 == 0)
    total = 0
    count = 0
    for n in nbrs:
        total += n
        count += 1
    mean = total / count
    return mean

if __name__ == '__main__':
    basic_mean()
    basic_mean_with_gen()
