# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 20:34:10 2019

@author: bmehl
"""
import random
from math import ceil
import time

def timed(method):
    def times(*args,**kw):
        ts = time.time()
        result = method(*args,**kw)
        te = time.time()
        print(method.__name__+' took',"{:.3}".format((te-ts)*1000),'milliseconds')
        return result
    return times

def save_file(pastList):
    with open("pastList.txt",'w+') as file:
        for person in pastList:
            file.write(person+"\n")

def open_file(filename):
    pastList = []
    with open(filename,'r') as file:
        pastList = file.readlines()
        
@timed
def cooking_scheduling(house_schedule, num_meals_person,weeks_away,STARTING_DAY=0,number_days=5):
    assert STARTING_DAY >= 0
    assert STARTING_DAY < 5
    NUMBER_MAP_DAY = {0:'S',1:'M',2:'T',3:'W',4:'Th'}
    num_meals_copy = num_meals_person.copy()
    print("The number of meals we are working with is "+str(sum(num_meals_person.values())))
    COOKING_DAYS = [0,1,2,3,4][:number_days] # sunday-thursday and number_days indicates the number we as a house choose to use
    if number_days == 4:
        COOKING_DAYS = [1,2,3,4]
    elif number_days == 3:
        COOKING_DAYS = [0,2,4]
    NUM_WEEKS = ceil(sum(num_meals_person.values())/len(COOKING_DAYS))
    print("This amounts to " +str(NUM_WEEKS)+" weeks of scheduling") #what day is the cook cycle starting on
    days_consideration = COOKING_DAYS[STARTING_DAY:]+COOKING_DAYS[:STARTING_DAY]
    current_planned_meals = 0
    counter = 0 # used as a last ditch termination if a solution is unable to be found
    num_meals = sum(num_meals_person.values())
    #originalPastList = open_file("pastList.txt")
    while current_planned_meals != num_meals and counter < 10**5:
        current_planned_meals = 0
        num_meals_person = num_meals_copy.copy()
        current_list = []
        past_list = ['Britta','Sean','Josiah','Tam','Shuta']# Changes this line Elizabeth
        meal_list = []
        for x in range(NUM_WEEKS):# this is the number of weeks we have to work with
            days_used = []
            cookingSchedule = {}
            if (num_meals-current_planned_meals)//len(COOKING_DAYS) > 0: # this if statement is used to force the first few days to be used and not a random assortment of days, try without it and you will see what i mean
                c = len(COOKING_DAYS)
            else:
                c = (num_meals%len(COOKING_DAYS))
            for y in days_consideration[:c]: # number of days in the week we are working with
                ones_list = []
                twos_list = []
                threes_list = []
                for z in house_schedule.keys():
                    if house_schedule[z][y] == 1:
                        ones_list.append(z)
                    elif house_schedule[z][y] == 2:
                        twos_list.append(z)
                    elif house_schedule[z][y] == 3:
                         threes_list.append(z)
                while True:
                    if len(ones_list) >= 1:
                        current_choice = random.choice(ones_list)
                        if num_meals_person[current_choice] >= 1 and current_choice not in current_list and current_choice not in past_list and current_choice not in weeks_away[x][y]:
                            current_list.append(current_choice)
                            num_meals_person[current_choice] -= 1
                            days_used.append(y)
                            break
                        else:
                            ones_list.remove(current_choice)
                    elif len(twos_list) >= 1:
                        current_choice = random.choice(twos_list)
                        #print(weeks_away[x][y])
                        if num_meals_person[current_choice] >= 1 and current_choice not in current_list and current_choice not in past_list and current_choice not in weeks_away[x][y]:
                            current_list.append(current_choice)
                            num_meals_person[current_choice] -= 1
                            days_used.append(y)
                            break
                        else:
                            twos_list.remove(current_choice)
##                    elif len(threes_list) >= 1:
##                        current_choice = random.choice(threes_list)
##                        if num_meals_person[current_choice] >= 1 and current_choice not in current_list: #and current_choice not in past_list and current_choice not in weeks_away[x][y]::
##                            current_list.append(current_choice)
##                            num_meals_person[current_choice] -= 1
##                            days_used.append(y)
##                            break
##                        else:
##                            threes_list.remove(current_choice)
                    else:
                        break
            if len(current_list) != number_days and x != NUM_WEEKS-1:
                break
            for i,x in enumerate(days_used):
                cookingSchedule[NUMBER_MAP_DAY[x]] = current_list[i]
            current_planned_meals += len(current_list)
            past_list = current_list
            #save_file(past_list)
            meal_list.append(cookingSchedule)
            cookingSchedule = {}
            current_list = []
            counter +=1
    if current_planned_meals != num_meals:
        print('Unable to be solved')
        for x in meal_list:
            print(x) 
        meal_list = []
    return meal_list
house_schedule = {'Frank':[3,3,5,4,1],#S,M,T,W,Th order Change these lists Elizabeth
                  'Jorge':[5,1,2,5,3],
                  'Harry':[2,1,2,4,2],
                  'Andy':[1,2,1,4,2],
                  'Shuta':[1,2,1,3,3],
                  'Brandon':[2,1,3,4,4],
                  'Sean':[4,4,1,1,3],
                  'Josiah':[4,5,1,5,1],
                  'Britta': [5,3,1,3,4],
                  'Elizabeth': [3,5,1,5,1],
                  'Noelle': [1,1,5,1,1],
                  'EmilyD':[5,5,3,1,1],
                  'Kai':[1,3,1,1,3],
                  } # this is the schedule for all of the people in the house whether they can cook on a day or not
                    # a 1 indicates yes, 2 is okay, 3 means fine, 4 and 5 mean no
num_meals_person = { 'Frank'           :1,# 
                                    'Jorge'             :1,# 
                                    'Harry'            :1,#
                                    'Andy'             :1,# 
                                    'Shuta'             :1,# 
                                    'Josiah'           :1,# 
                                    'Brandon'        :1,# 
                                    'Sean'              :1,#  
                                    'Britta'            :1,# 
                                    'Elizabeth'      :1,# 
                                    'Noelle'          :1,# 
                                    'EmilyD'         :1,#
                                    'Kai'               :1,# 
                    }
# this indicates the number of cooking spots the person needs to do
# weeks away is on a per week basis, for example the 1st week if you are
# starting on a tuesday, the first day of each row still corresponds to the sunday of that week
#["Noelle","Andy","Harry","EmilyD"],["Noelle","Andy","Harry","EmilyD"],["Noelle","Andy","Harry","EmilyD"],["Noelle","Andy","Harry","EmilyD"],["Noelle","Andy","Harry","EmilyD"]
weeks_away =[[[],[],[],[],[]],#23-27
                  [[],[],[],[],[]], #30-3
                  [[],[],[],[],[]],#
                  [[],[],[],[],[]],#22-26
                  [[],[],[],[],[]],#
                  [[],[],[],[],[]],
                  [[],[],[],[],[]]]#25-31
meal_list = cooking_scheduling(house_schedule, num_meals_person,weeks_away,STARTING_DAY=0,number_days=4)#elizabeth look here
for x in meal_list:
    print(x)       
