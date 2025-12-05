def dim(matrix):
  return(len(matrix), len(matrix[0]))
def canMult(m, n):
  return dim(m)[1] == dim(n)[0]
def entry(i, j, m, n):
  sum = 0
  for a in range(dim(m)[1]):
    sum += m[i][a] * n[a][j]
  return sum
def matrixMult(m,n):
    rows = dim(m)[0]
    cols = dim(n)[1]
    mat = [[entry(i,j,m,n) for j in range(cols)] for i in range(rows)]
    return mat
def transpose(m):
    rows = dim(m)[0]
    cols = dim(m)[1]    
    return [[m[i][j] for i in range(rows)] for j in range(cols)]
def printMatrix(m):
    rows = dim(m)[0]
    for i in range(rows):
        print(m[i])
    print("")
M = [[1,2],[0,-1],[3,4]]
N = [[1,2],[1,2]]

print(dim(M))
print(dim(N))
print(canMult(M,N))
print(canMult(N,M))
#printMatrix(matrixMult(M,N))
printMatrix(M)
printMatrix(transpose(M))
