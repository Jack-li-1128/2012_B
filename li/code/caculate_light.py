import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps, trapz

def read_f_file():
    def line_count(data):
        line = 0
        while True:
            temp = data.readline()
            if temp == '':
                data.seek(0, 0)
                return line
            line += 1


    file = open('radiation.xls', 'r')
    l = line_count(file)
    f = []
    for i in range(l):
        f.append(file.readline().strip('\n').split('\t'))
    return f


def get_24hour(f,line):
    o = [[], []]
    tr = []
    tt = []
    for i in range(1, len(f)):
        if float(f[i][line]) != 0:
            tr.append(float(f[i][line]))
            tt.append(int(f[i][1]))
        if int(f[i][1]) == 23:
            o[0].append(tt[:])
            o[1].append(tr[:])
            tr.clear()
            tt.clear()
    return o


def polynomial_fit(x, y, degree):
    # Fit the polynomial
    p = np.polyfit(x, y, degree)
    poly = np.poly1d(p)

    # Generate a smooth range of x values
    x_smooth = np.linspace(x.min(), x.max(), 500)
    # Generate fitted y-values for the smooth x values
    fitted_y_smooth = poly(x_smooth)

    return poly, x_smooth, fitted_y_smooth


def year_sum(et):
    l = (et[0] ** 2 + et[1] ** 2 + et[2] ** 2) ** 0.5
    horizon = get_24hour(read_f_file(), 3)
    east = get_24hour(read_f_file(), 6)
    south = get_24hour(read_f_file(), 7)
    west = get_24hour(read_f_file(), 8)
    north = get_24hour(read_f_file(), 9)
    r = [[], []]
    for i in range(len(horizon[0])):
        rn = [horizon[0][i], [0 for _ in range(len(horizon[0][i]))]]
        for j in range(len(rn[0])):
            if et[2] >= 0 and rn[0][j] in horizon[0][i]:
                rn[1][j] += horizon[1][i][horizon[0][i].index(rn[0][j])] * et[2] / l
            if et[0] >= 0 and rn[0][j] in east[0][i]:
                rn[1][j] += east[1][i][east[0][i].index(rn[0][j])] * et[0] / l
            if et[0] <= 0 and rn[0][j] in west[0][i]:
                rn[1][j] += west[1][i][west[0][i].index(rn[0][j])] * abs(et[0]) / l
            if et[1] >= 0 and rn[0][j] in north[0][i]:
                rn[1][j] += north[1][i][north[0][i].index(rn[0][j])] * et[1] / l
            if et[1] <= 0 and rn[0][j] in south[0][i]:
                rn[1][j] += south[1][i][south[0][i].index(rn[0][j])] * abs(et[1]) / l
        r[0].append(rn[0])
        r[1].append(rn[1])
    s = 0
    for i in range(len(r[0])):
        x = np.array(r[0][i])
        y = np.array(r[1][i])
        degree = len(r[0][i]) // 3 * 2
        poly, x_smooth, fitted_y_smooth = polynomial_fit(x, y, degree)
        integral_simps = simps(fitted_y_smooth, x_smooth)
        s += integral_simps
    return s


def bord_w_year(ef, class_name, et):
    l = (et[0] ** 2 + et[1] ** 2 + et[2] ** 2) ** 0.5
    horizon = get_24hour(read_f_file(), 3)
    east = get_24hour(read_f_file(), 6)
    south = get_24hour(read_f_file(), 7)
    west = get_24hour(read_f_file(), 8)
    north = get_24hour(read_f_file(), 9)
    r = [[], []]
    for i in range(len(horizon[0])):
        rn = [horizon[0][i], [0 for _ in range(len(horizon[0][i]))]]
        for j in range(len(rn[0])):
            if et[2] >= 0 and rn[0][j] in horizon[0][i]:
                rn[1][j] += horizon[1][i][horizon[0][i].index(rn[0][j])] * et[2] / l
            if et[0] >= 0 and rn[0][j] in east[0][i]:
                rn[1][j] += east[1][i][east[0][i].index(rn[0][j])] * et[0] / l
            if et[0] <= 0 and rn[0][j] in west[0][i]:
                rn[1][j] += west[1][i][west[0][i].index(rn[0][j])] * abs(et[0]) / l
            if et[1] >= 0 and rn[0][j] in north[0][i]:
                rn[1][j] += north[1][i][north[0][i].index(rn[0][j])] * et[1] / l
            if et[1] <= 0 and rn[0][j] in south[0][i]:
                rn[1][j] += south[1][i][south[0][i].index(rn[0][j])] * abs(et[1]) / l
        r[0].append(rn[0])
        r[1].append(rn[1])
    s = 0
    for i in range(len(r[0])):
        x = np.array(r[0][i])
        y = np.array(r[1][i])
        degree = len(r[0][i]) // 3 * 2
        poly, x_smooth, fitted_y_smooth = polynomial_fit(x, y, degree)
        if class_name == 'A':
            for j in range(len(fitted_y_smooth)):
                if fitted_y_smooth[j] >= 200:
                    fitted_y_smooth[j] = fitted_y_smooth[j] * ef
                else:
                    fitted_y_smooth[j] = fitted_y_smooth[j] * ef * 0.05
        elif class_name == 'C':
            for j in range(len(fitted_y_smooth)):
                if fitted_y_smooth[j] >= 200:
                    fitted_y_smooth[j] = fitted_y_smooth[j] * ef
                else:
                    fitted_y_smooth[j] = fitted_y_smooth[j] * ef * 1.01
        elif class_name == 'B':
            for j in range(len(fitted_y_smooth)):
                fitted_y_smooth[j] = fitted_y_smooth[j] * ef
        integral_simps = simps(fitted_y_smooth, x_smooth)
        s += integral_simps
    return s


et = [0, -225, 1200]
for i in [16.84,16.64,18.7,16.5,14.98,15.11]:
    redi = year_sum(et)
    power = bord_w_year(i/100, 'A', et)
    profile = power/1000*43.5*0.5-1000*(i/100)*14.9
    print(round(profile,2))
    #n = power/redi
    #print(str('ef='+str(round(n*100,2))+'%,'+str(round(power,2))))
for i in [16.21,16.39,15.98,14.8,15.98,15.2,14.99]:
    redi = year_sum(et)
    power = bord_w_year(i/100, 'B', et)
    profile = power/1000*43.5*0.5 - 1000 * (i / 100) * 12.5
    print(round(profile,2))
    #n = power/redi
    #print(str('ef='+str(round(n*100,2))+'%,'+str(round(power,2))))
for i in [6.99,6.17,6.35,5.84,6.49,3.63,3.63,3.66,3.66,4.13,4.27]:
    redi = year_sum(et)
    power = bord_w_year(i/100, 'C', et)
    profile = power/1000*43.5*0.5 - 1000 * (i / 100) * 4.8
    print(round(profile,2))
    #n = power/redi
    #print(str('ef='+str(round(n*100,2))+'%,'+str(round(power,2))))



'''
r_h = get_24hour(read_f_file(), 3)
# Example usage:
x = np.array(r_h[0][0])
y = np.array(r_h[1][0])
degree = len(r_h[0][0])//2

poly, x_smooth, fitted_y_smooth = polynomial_fit(x, y, degree)

# Plotting the original data and the fitted polynomial
plt.scatter(x, y, label='Data points')
plt.plot(x_smooth, fitted_y_smooth, label=f'Polynomial fit (degree={degree})', color='red')
plt.legend()
plt.show()
# Integrate the fitted polynomial
integral_simps = simps(fitted_y_smooth, x_smooth)
'''