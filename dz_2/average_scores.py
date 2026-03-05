def compute_average_scores(scores):
    final = [0 for _ in range(len(scores[0]))]
    ln_pr = len(scores)
    ln_st = len(scores[0])
    for pr in range(ln_pr):
        for stud in range(ln_st):
            final[stud] += scores[pr][stud] / ln_pr
    
    return final
if __name__ == '__main__':
    n,x = map(int, input().split())

    arr = [list(map(float,input().split()))[:n] for _ in range(x)]

    for i in range(n):
        print(f'{compute_average_scores(arr)[i]:.1f}')


