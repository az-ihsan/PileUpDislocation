import matplotlib.pyplot as plt
import json
import numpy as np 
import sys
from pylab import cm

def imgStressPileup(d, b, stress_0, x, y):
    first_term = (x + d) * ((x+d)**2 - y**2) / ((x+d)**2 + y**2)**2
    second_term = (x - d) * ((x-d)**2 - y**2) / ((x-d)**2 + y**2)**2
    third_term = 2*d*((x-d)*(x+d)**3 - 6*x*(x+d)*y**2 + y**4) / ((x+d)**2 + y**2)**3
    stress_yx = stress_0*b*(first_term  - second_term + third_term)
    return stress_yx

def main():
    ## plot   
    data_path = sys.argv[1]
    save_img_path = sys.argv[2]
    with open(data_path) as f:
        data = json.load(f)
        data_dis = data['Dislocations']
        mat_pro = data['Material properties']

    # last_pos_positive = []

    # for dis in data_dis: 
    #     pos = dis['Position']
    #     last_pos_positive.append((pos[0], pos[1]))
        
    # last_positive = np.asanyarray(last_pos_positive)

    G = 1.0
    nu = mat_pro['Poissons ratio']['value']
    stress_0 = G/(2*np.pi*(1-nu))

    x = np.linspace(0, 80, 1000)
    y = np.linspace(-2, 2, 50)

    xx, yy = np.meshgrid(x, y)
    stress_xy = np.zeros_like(xx)

    for dislocation in data_dis:
        pos = dislocation['Position']
        b = dislocation['Burgers vector']['value']
        stress_xy = stress_xy + imgStressPileup(pos[0], b, stress_0, xx, yy)


    # fig, ax = plt.subplots(figsize=(10,1), dpi=100)
    # ax.set_title('Pile up dislocation')
    # ax.axhline(0, color='black',  alpha = 0.4)
    # ax.plot(last_positive.T[0], last_positive.T[1], 'r+', label="positive")

    fig, ax = plt.subplots(figsize=(10,2), dpi=300)
    ax.set_title('Stress Distribution')
    # ax.axhline(0, color='black', alpha = 0.4)
    ax.imshow(stress_xy,  cmap=cm.RdBu_r)
    fig.legend()
    fig.savefig(save_img_path)

if __name__ == "__main__":
    main()
