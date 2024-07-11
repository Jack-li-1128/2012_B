import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.optimize import curve_fit

compare_name = ['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6','B7','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11']
compare_power = [215,325,200,270,245,295,265,320,210,240,280,295,250,100,58,100,90,100,4,48,12,12,50,]


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


def polynomial_fit(x, y, degree, num_points=500):
    # Fit the polynomial
    p = np.polyfit(x, y, degree)
    poly = np.poly1d(p)

    # Generate a smooth range of x values
    x_smooth = np.linspace(x.min(), x.max(), num_points)
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
        plt.scatter(x, y, label='Data points')
        plt.plot(x_smooth, fitted_y_smooth, label=f'Polynomial fit (degree={degree})', color='red')
        plt.legend()
        plt.show()
        s += integral_simps
    return s


def year_sum_sin(et):
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
        # 数据点
        # x = np.array([8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
        # y = np.array([11.11, 94.44, 202.78, 266.67, 341.67, 386.11, 269.44, 175.00, 75.00, 5.56])
        # 定义从0到π的半周期正弦函数，且c=0
        def half_period_sin_fixed_c(x, a, phi):
            return a * np.sin(x + phi)
        # 将X转换到0到π的范围
        X_transformed = (x - min(x)) * (np.pi / (max(x) - min(x)))
        # 初始参数猜测
        initial_guess_fixed_c = [200, 0]
        # 拟合曲线
        params_fixed_c, params_covariance_fixed_c = curve_fit(half_period_sin_fixed_c, X_transformed, y,p0=initial_guess_fixed_c)
        # 生成拟合曲线的数据
        X_fit = np.linspace(min(x), max(x), 500)
        X_fit_transformed = (X_fit - min(x)) * (np.pi / (max(x) - min(x)))
        Y_fit_fixed_c = half_period_sin_fixed_c(X_fit_transformed, *params_fixed_c)
        # 获取 x 点的 y 值
        x_transformed = [(x[i] - min(x)) * (np.pi / (max(x) - min(x))) for i in range(len(x))]
        y_transformed = [half_period_sin_fixed_c(x_transformed[i], *params_fixed_c) for i in range(len(x))]
        y1 = [(y[i]-y_transformed[i])/2 for i in range(len(x))]
        '''
        X_9_transformed = (9 - min(X)) * (np.pi / (max(X) - min(X)))
        Y_9 = half_period_sin_fixed_c(X_9_transformed, *params_fixed_c)
        print("The fitted y value at x = 9 is:", Y_9)
        '''
        degree = len(r[0][i]) // 3 * 2
        poly, x_smooth, fitted_y_smooth = polynomial_fit(x, y1, degree, num_points=500)
        fitted_y_smooth = [fitted_y_smooth[i]+Y_fit_fixed_c[i] for i in range(len(fitted_y_smooth))]
        integral_simps = simps(fitted_y_smooth, x_smooth)
        plt.scatter(x, y, label='Data points')
        plt.plot(x_smooth, fitted_y_smooth, label=f'Polynomial fit (degree={degree})', color='red')
        plt.plot(x_smooth, Y_fit_fixed_c, label=f'sin Fit ', color='blue')
        plt.legend()
        plt.show()
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
        plt.scatter(x, y, label='Data points')
        plt.plot(x_smooth, fitted_y_smooth, label=f'Polynomial fit (degree={degree})', color='red')
        plt.legend()
        plt.show()
        s += integral_simps
    return s


def plant_w_year(trans_classes: list, et):
    # trans_classes = [[trans_name,[classes],ef]....]
    # bord_classes = [[bord_name, bord_area, ef]....]
    # 计算总辐射量
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

    def one_sys_w_year(bord_classes: list, sys_num):
        s_in = 0
        for i in range(len(r[0])):
            x = np.array(r[0][i])
            y = np.array(r[1][i])
            degree = len(r[0][i]) // 3 * 2
            poly, x_smooth, fitted_y_smooth = polynomial_fit(x, y, degree)
            one_sys_sum = np.zeros(len(fitted_y_smooth))
            for j in range(len(fitted_y_smooth)):
                for k in bord_classes:
                    if k[0] == 'A':
                        if fitted_y_smooth[j] >= 200:
                            one_sys_sum[j] += fitted_y_smooth[j] * k[2] * k[1]
                        else:
                            if fitted_y_smooth[j] >= 80:
                                one_sys_sum[j] += fitted_y_smooth[j] * k[2] * 0.05
                            else:
                                one_sys_sum[j] += 0
                    elif k[0] == 'C':
                        if fitted_y_smooth[j] >= 200:
                            one_sys_sum[j] += fitted_y_smooth[j] * k[2] * k[1]
                        else:
                            if fitted_y_smooth[j] >= 30:
                                one_sys_sum[j] += fitted_y_smooth[j] * k[2] * k[1] * 1.01
                            else:
                                one_sys_sum[j] += 0
                    elif k[0] == 'B':
                        if fitted_y_smooth[j] >= 80:
                            one_sys_sum[j] += fitted_y_smooth[j] * k[2] * k[1]
                        else:
                            one_sys_sum[j] += 0
                    else:
                        return TypeError
            integral_simps = simps(one_sys_sum, x_smooth)
            integral_simps *= trans_classes[h][2]
            s_in += integral_simps
        return s_in
    s = 0
    for h in range(len(trans_classes)):
        t = one_sys_w_year(trans_classes[h][1], h)
        s += t
    return s

print(bord_w_year(18.7, 'A', [0,0,1]))

'''
result = plant_w_year([['SN15', [['C', 8.58, 0.0699], ['C', 9.9045, 0.0363]], 0.94]], (1, 0, 0))
print(result)
'''
'''
l = []
lx = []
ly = []
for i in range(10):
    for j in range(10):
        l.append(year_sum([round(i/100+0.35,2), round(-j/100-0.65,2), 1]))
        lx.append(round(i/100+0.35,2))
        ly.append(round(-j/100-0.65,2))

print(max(l))
print(lx[l.index(max(l))])
print(ly[l.index(max(l))])
'''
'''
for i in range(-10,0):
    print(year_sum([i/100-0.5,0,1]), i/100-0.5)
    '''
'''
et = [0.4, -0.7, 1]
for i in [16.84,16.64,18.7,16.5,14.98,15.11]:
    redi = year_sum(et)
    power = bord_w_year(i/100, 'A', et)
    profile = power/1000*31.5*0.5-1000*(i/100)*14.9
    #print(round(profile,2))
    n = power/redi
    print(str('ef='+str(round(n*100,2))+'%,'+str(round(power,2))))
for i in [16.21,16.39,15.98,14.8,15.98,15.2,14.99]:
    redi = year_sum(et)
    power = bord_w_year(i/100, 'B', et)
    profile = power/1000*31.5*0.5 - 1000 * (i / 100) * 12.5
    #print(round(profile,2))
    n = power/redi
    print(str('ef='+str(round(n*100,2))+'%,'+str(round(power,2))))
for i in [6.99,6.17,6.35,5.84,6.49,3.63,3.63,3.66,3.66,4.13,4.27]:
    redi = year_sum(et)
    power = bord_w_year(i/100, 'C', et)
    profile = power/1000*31.5*0.5 - 1000 * (i / 100) * 4.8
    #print(round(profile,2))
    n = power/redi
    print(str('ef='+str(round(n*100,2))+'%,'+str(round(power,2))))
'''

'''
plt.scatter(x, y, label='Data points')
plt.plot(x_smooth, fitted_y_smooth, label=f'Polynomial fit (degree={degree})', color='red')
plt.legend()
plt.show()
'''


# 南屋顶([['SN15', [['B', 39.24, 0.1621], ], 0.94],['SN15', [['C', 5.72, 0.0699], ['C', 6.6, 0.0363]], 0.94]], (0, -255, 1200))
# 西墙([['SN15', [['C', 20.02, 0.0699], ['C', 3.315, 0.0363]], 0.94]],(-1, 0, 0))
# 南墙([['SN15', [['C', 13.206, 0.0363], ], 0.94]], (0, -1, 0))
# 北屋顶([['SN15', [['C', 8.58, 0.0699], ['C', 2.201, 0.0363], ], 0.94]], (0, 2532, 1200))
# 东墙([['SN15', [['C', 8.58, 0.0699], ['C', 9.9045, 0.0363]], 0.94]], (1, 0, 0))

# 南屋顶([['SN15', [['B', 39.24, 0.1621], ], 0.94],['SN7', [['C', 5.72, 0.0699], ['C', 6.6, 0.0363]], 0.9]], (0, -255, 1200))
# 西墙([['SN7', [['C', 12.87, 0.0699], ['C', 7.7035, 0.0363]], 0.90]],(-1, 0, 0))
# 南墙([['SN3', [['C', 3.756924, 0.0617], ], 0.86],['SN2', [['C', 11.11505, 0.0363], ], 0.84]], (0, -1, 0))
# 北屋顶([['SN7', [['C', 10.01, 0.0699], ], 0.90],['SN1', [['C', 0.6603, 0.0363], ], 0.84]], (0, 2532, 1200))
# 东墙([['SN7', [['C', 7.15, 0.0699], ['C', 9.9045, 0.0363]], 0.9]], (1, 0, 0))
