import itertools
coins = [2,3,5,7,9]
for p in itertools.permutations(coins):
    if p[0]+ p[1] * pow(p[2],2) + pow(p[3],3) - p[4] == 399:
        print(p)
        break

# blue, red, shiny, concave, corroded