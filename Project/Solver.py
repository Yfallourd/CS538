import glpk
import sys


def createMatrixRow(S, e, Ssize, requirements):
    row = []
    for i in range(Ssize):
        row.append(1 if str(e) in S[i] else 0)  # if edge is not covered, don't count it

    for i in range(Esize):
        row.append(-requirements[i] if i == e-1 else 0)

    return row


# Initialize LP instance
lp = glpk.LPX()
lp.name = 'PSMC'
lp.obj.maximize = False

filename = sys.argv[1]
formatnumber = filename[8:10]

# Read instance
datafile = open(filename, 'r')
data = datafile.read().split("\n")
datafile.close()

matrix = []
Esize = int(data[0].split()[0])
Ssize = int(data[0].split()[1])
P = int(data.pop(0).split()[2])
requirements = map(int, data.pop(0).split())
costs = map(int, data.pop(0).split())

S = [each.split() for each in data]


lp.rows.add(Esize+1)
lp.cols.add(Ssize+Esize)


for row in range(len(lp.rows)):
    if row != Esize:
        lp.rows[row].bounds = 0, None
    else:
        lp.rows[row].bounds = P, None

for col in lp.cols:
    col.bounds = 0, 1

lp.obj[:] = costs+[0]*Esize  # The objective coefficients are the costs

for each in range(1, Esize+1):
    matrix += createMatrixRow(S, each, Ssize, requirements)  # Create a |E|x|E|+|S| matrix

matrix += [0]*Ssize
matrix += [1]*Esize  # Last row is to check that sum(y)>P

lp.matrix = matrix

lp.simplex()  # Have to find a relaxed solution

for col in lp.cols:
    col.kind = int  # Switch to integer program
lp.integer()

xsol = [col.value for col in lp.cols[:Ssize]]

ysol = [col.value for col in lp.cols[Ssize:]]


solB = [i+1 for i, j in enumerate(xsol) if j == 1]
solcost = int(lp.obj.value)

solstring = str(len(solB)) + " " + str(solcost) + " "
for each in solB:
    solstring += str(each) + " "


solfile = open("solution"+formatnumber+".txt", "w+")
solfile.truncate()
solfile.write(solstring)
solfile.close()
