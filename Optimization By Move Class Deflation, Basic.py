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
import math as math 

#Optimization by Move Class Deflation, simple algo  
#this original is more of a place holder so we can see what the original spin system was 
#could use a random seed function to generate a bigger sequence of random ones and zeros. Look back at PNN CW for help on this. 
spin_glasses_original = [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1]
#this will just be a place holder variable for when we get higher energy 
spin_glasses_medium = spin_glasses_original.copy()
#deflation number 
d0 = len(spin_glasses_original)
#number of iterations, can get rid of this later 
iterations = 100000

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

for i in range(iterations):
    #doing the random swap function with the random sample instead. 
    spin_glasses_newest = random.sample(spin_glasses_medium, d0)
    
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
    
    #this if statement changes the number of spins we want to change but at the moment it shortens the length of the new spin system instead
    #read documentation on random.sample() to finish this part 
# =============================================================================
#     if number_rejections_this_round == 20:
#         d0 = d0 - 1
#         print('To many rejections in a row, lets try lowering the number to see if that works.')
#         number_rejections_this_round = 0
# =============================================================================

print(spin_glasses_medium)
print('The final energy of this system is: ' + str(medium_total_energy))
print('The number of acceptances was ' + str(acceptance) + ' and the number of rejections was ' + str(rejection))
print('so our ratio of accepted to total number of attempted moves is ' + str(acceptance*100/(acceptance + rejection)) + '%')
#ok this is a start but I need the whole thing to iterate until a certain amount of rejections has been done and then decreases the deflation number
#I think the monte carlo metropolis algoirthm may help with this, worth having a look 
end = time.time()
print('This program took ' + str(end-start) + ' to run.')