import pandas


def line_count(data):
    line = 0
    while True:
        temp = data.readline()
        if temp == '':
            data.seek(0, 0)
            return line
        line += 1


file = open('f3data.xls', 'r')
l = line_count(file)
f = []
for i in range(l):
    f.append(file.readline().split('\t'))
data_out = []
for i in range(8,15):
    t = f[i][3].split('×')
    s = float(t[0])/1000 * float(t[1])/1000
    m = 12.5*int(f[i][2])/s
    data_out.append(m)

print(data_out)