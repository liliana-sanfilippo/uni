from itertools import combinations



def all_splits(o):
    counter = 0
    n = len(o)
    for r in range(1, n):
        for j_idx in combinations(range(n), r):
            j = [o[i] for i in j_idx]
            k = [o[i] for i in range(n) if i not in j_idx]
            counter = counter + 1
            yield (j, k)
    print("ITERATIONS: " + str(counter))



def get_dij(i,j):
    return mat[i][j]

def alpha_jk(j, k, mat):
    if len(j) == 0 or len(k) == 0:
        return None

    minimum = 100000 #could start with a none value or the value infinity
    for i in j:
        for jj in j:
            for kk in k:
                for l in k:
                    sum1 = mat[i][jj] + mat[kk][l]
                    sum2 = mat[i][kk] + mat[jj][l]
                    sum3 = mat[i][l] + mat[jj][kk]
                    value = max(sum1, sum2, sum3) - mat[i][jj] - mat[kk][l]
                    #print("Value: " + str(value))
                    if(value < minimum):
                        minimum = value

    return 0.5 * minimum


def delta_jk(i,jj, j, k):
    if((i in k and jj in k) or (i in j and jj in j)):
        return 0
    else:
        return 1


def d_1(object_set):
    n = len(object_set)
    d1 = [[0.0 for _ in range(n)] for _ in range(n)]
    for ii in object_set:
        for jj in object_set:
            d1[ii][jj] = d_1_ij(object_set, ii, jj)
    return d1

def d_1_ij(object_set, ii, jj):
    for split in all_splits(object_set):
        return alpha_jk(split[0],split[1], mat) * delta_jk(ii, jj, split[0], split[1])


def main(object_set, matrix):
    splits = all_splits(object_set)
    for elem in splits:
        print(str(elem[0]) + " & " + str(elem[1]))
        print("alpha: "+ str(alpha_jk(elem[0], elem[1], matrix)))
        #for ii in object_set:
         #   for jj in object_set:
                #print("delta("+ zuordnung[ii] + ","+ zuordnung[jj] +"): " + str(delta_jk(ii, jj, elem[0], elem[1])))
    print(str(d_1(object_set)))

mat = [
    [0,9,13,12,13],
    [9,0,12,7,15],
    [13,12,0,6,10],
    [12,7,6,0,12],
    [13,15,10,12,0]
]

mat_weg = [
    [0,6,8,5,10],
    [6,0,5,8,10],
    [8,5,0,4,8],
    [5,8,4,0,7],
    [10,10,8,7,0]
]

#main([["A"], ["B"], ["C"], ["D"], ["E"]])

zuordnung = ["A", "B", "C", "D", "E", "F"]

main([0, 1, 2, 3, 4], mat)



#main(["A", "B", "C", "D", "E"], mat)
