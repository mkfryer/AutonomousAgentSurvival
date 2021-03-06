"""
Created on Thu May 16 19:42:21 2019
@author: Adam
"""
from World import World
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":

    print("You are in main")



    #ratios = np.array([[0,0],[10,0],[0,10],[5,5]])
    ratios = np.array([[100,0]])

    results = []
    for test in ratios:
        world = World(good=test[0],bad=test[1],people=100)
        for i in range(1,8):
            world.each_day()
        results.append(world.get_data)
    results = np.array(results)
    #print(results)



    fig, ax = plt.subplots(3,1,figsize=(10,10),sharex='all')

    for i in range(len(results)):
        ax[0].plot(results[i][:,0])
        ax[1].plot(range(len(results[i])),results[i][:,1])
        ax[2].scatter(range(len(results[i])),np.argmax(results[i][:,2:].astype(int),axis=1),label=str(i))

    plt.xlabel('Day')
    plt.ylabel('Population')
    plt.legend()
    ax[0].set_title('Population')
    ax[1].set_title('% Correct')
    ax[2].set_title('Majority Well')
    plt.show()
