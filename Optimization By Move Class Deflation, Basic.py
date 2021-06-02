# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 21:21:33 2021

@author: amill
"""
#Note: this algorithm is basic at the moment as I am making the fundamental consituent parts but will become more complex over time 
#need to turn all of these into function if I can and expand it to 3d lattices if possible 
#at the moment its basically a MCM algorithm 
import time 
start = time.time()
import numpy as np 
import random as random 

#Optimization by Move Class Deflation, simple algo  
#this original is more of a place holder so we can see what the original spin system was 
#could use a random seed function to generate a bigger sequence of random ones and zeros. Look back at PNN CW for help on this. 
spin_glasses_original = [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1]
#below randomly selects a list of 1's and 0's which is k length long and the random seed makes sure this is permanent:
#hashing out random seed for now as not sure if it will effect the later code as well. 
#random.seed(41)
k= 200
spin_glasses_original = np.random.randint(2, size = k)
#converting it to a list which avoids the problems we might incur with numpy arrays 
spin_glasses_original = spin_glasses_original.tolist()
print('Our spin glass configuration for this algorithm is: ' + str(spin_glasses_original))
#this will just be a place holder variable for when we get higher energy 
spin_glasses_medium = spin_glasses_original.copy()
#deflation number 
d0 = len(spin_glasses_original)
#number of iterations, can get rid of this later 
iterations = 100000
#number of rejections before we lower d0
num_rejections_lower_d0 = 1000

#initial energy calculation of the system, very basic for now but can be updated with more complex equations 
initial_total_energy = 0
for i in range(len(spin_glasses_original)):
    if spin_glasses_original[i] != spin_glasses_original[i-1] and i!=0:
        initial_total_energy += 1
print('The initial total energy of the system is: ' + str(initial_total_energy))

#energy for the medium spin glass list 
medium_total_energy = 0
for i in range(len(spin_glasses_medium)):
    if spin_glasses_medium[i] != spin_glasses_medium[i-1] and i!=0:
        medium_total_energy += 1
print(medium_total_energy)

#counting the acceptance and rejection ratio of the system 
acceptance = 0
rejection = 0
number_rejections_this_round = 0 

#creating a list of indexes to randomly 
indexes = []
for t in range(len(spin_glasses_original)):
    indexes.append(t)

for i in range(iterations):
    #need to create an array of shuffle and no-shuffle indexes 
    shuffle_index = []
    #print('our initial value of d0 is ' + str(d0))
    #now I am picking d0 amount of indexes to shuffle and adding them to a list 
    for j in range(d0):
        #using random.choice to randomly pick an index from indexes 
        shuffle_element = random.choice(indexes)
        shuffle_index.append(shuffle_element)
        #I have to remove this element so that it cannot be chosen again 
        for k in indexes:
            if k==shuffle_element:
                indexes.remove(k)
    #print function was just to check the before and after shuffle to see if it worked
    #print('Before shuffle: ' + str(spin_glasses_medium))
    #creating a copy of the shuffle index list so I can shuffle it 
    shuffling_indexes = list(shuffle_index)
    #shuffling this new list 
    random.shuffle(shuffling_indexes)
    
    #swapping the indexes of the randomly chosen indexes and there shuffled indexes 
    for m in shuffle_index:
        for n in shuffling_indexes:
            spin_glasses_medium[m], spin_glasses_medium[n] = spin_glasses_medium[n], spin_glasses_medium[m]
    #These print functions were to make sure that the random swapping was working. 
    #print('After shuffle: ' + str(spin_glasses_medium))
    #print(shuffling_indexes, shuffle_index)

    #reassigning to calculate the newest energy 
    spin_glasses_newest = spin_glasses_medium
    #function to calculate new energy of the the system 
    def new_energy_calc(spin_glasses_newest):
        new_total_energy = 0
        for i in range(len(spin_glasses_newest)):
            if spin_glasses_newest[i] != spin_glasses_newest[i-1] and i!=0:
                new_total_energy += 1
        return new_total_energy
    
    
    print('The newest total energy of the system is: ' + str(new_energy_calc(spin_glasses_newest)))
    #functions says whether to accept (if lower) or reject (if higher) new system energy 
    if new_energy_calc(spin_glasses_newest) <= medium_total_energy:
        medium_total_energy = new_energy_calc(spin_glasses_newest)
        spin_glasses_medium = spin_glasses_newest
        acceptance += 1
        print('This energy has been Accepted! Woooooooo!')
    else: 
        print('Gonna have to reject this one, sorry bud.')
        rejection += 1
        number_rejections_this_round += 1
    
    #need to reset the indexes list so we can then again choose from them. 
    indexes = []
    for t in range(len(spin_glasses_original)):
        indexes.append(t)
    
    #this if statement changes the number of spins we want to change but at the moment it shortens the length of the new spin system instead
    #read documentation on random.sample() to finish this part 
    if number_rejections_this_round == num_rejections_lower_d0:
        d0 = d0 - 1
        print('To many rejections in a row, lets try lowering the number to see if that works. The new value of d0 is ' + str(d0))
        number_rejections_this_round = 0
        if d0 == 0:
            print('d0 will not go any lower mate, gonna have to stop here.')
            break 

#print(spin_glasses_medium)
print('The initial total energy of the system is: ' + str(initial_total_energy))
print('The final energy of this system is: ' + str(medium_total_energy))
print('The number of acceptances was ' + str(acceptance) + ' and the number of rejections was ' + str(rejection))
print('so our ratio of accepted to total number of attempted moves is ' + str(acceptance*100/(acceptance + rejection)) + '%')
#ok this is a start but I need the whole thing to iterate until a certain amount of rejections has been done and then decreases the deflation number
#I think the monte carlo metropolis algoirthm may help with this, worth having a look 
print('Our value of d0 is currently: ' + str(d0))
end = time.time()
print('This program took ' + str(end-start) + ' to run.')
