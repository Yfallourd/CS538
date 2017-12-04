# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:46:20 2017
@author: Anaïs Bonnet (A20411100) Yohann Fallourd (A20409789)
"""
import sys

#==============================================================================
#Method that return the total cost of a given set "selected_set"
#cost [in]: List where the ith element is the cost of the (i+1)th set
#selected_set [in]: List of the number of the selected set
#[out]: Total cost of "selected_set"
#==============================================================================
def total_cost(cost, selected_set):
    total_cost = 0
    for x in selected_set:
        total_cost = total_cost + cost[x - 1]
    return total_cost

#==============================================================================
#Method that return true if the solution entered is feasible 
#   and returns false otherwise
#p [in]: Integer that represent the minimal coverage requirement
#requirement [in]: List where the ith element is the required minimum
#   coverage for the (i+1)th set
#list_set [in]: List where the ith element is a list of all the numbers 
#   in the (i+1)th set
#selected_set [in]: List of the number of the selected set
#[out]: Boolean true if the solution is feasible or false if it isn't
#==============================================================================
def is_feasible(p, requirement, list_set, selected_set):
    list_coverage = [0] * len(requirement)

    for x in selected_set:
        for y in list_set[x - 1]:
            list_coverage[y - 1] = list_coverage[y - 1] + 1

    vertex_coverage = 0
    for x in range(0, len(requirement)):
        if list_coverage[x] >= requirement[x]:
            vertex_coverage = vertex_coverage + 1

    if vertex_coverage >= p:
        return True
    else:
        return False

#==============================================================================
#Method that return true if the instance is valid and returns false otherwise
#informations [in]: Array where the first element is the number of elements
#    of the instance and the second is the number of sets
#requirement [in]: List where the ith element is the required minimum
#   coverage for the (i+1)th set
#list_set [in]: List where the ith element is a list of all the numbers 
#   in the (i+1)th set
#cost [in]: List where the ith element is the cost of the (i+1)th set
#[out]: Boolean true if the instance is valid or false if it isn't
#==============================================================================
def is_instance_valid(informations, requirement, list_set, cost):
    if informations[0] == len(requirement) and informations[1] == len(list_set) and informations[1] == len(cost):
        return True
    else:
        return False


final_sentence = "This output "
file_instance_name = sys.argv[1]
file_solution_name = sys.argv[2]
file_instance = open(file_instance_name, "r")
file_solution = open(file_solution_name, "r")
instance = list(map(lambda s: s.strip(), file_instance.readlines()))
list_solution = [int(s) for s in file_solution.read().strip().split(' ')]
final_cost = list_solution[1]
list_selected_set = list_solution[2:]
informations = [int(s) for s in instance[0].split(' ')]
p = informations[2]
requirement = [int(s) for s in instance[1].split(' ')]
cost = [int(s) for s in instance[2].split(' ')]
list_set = [None] * (len(instance) - 3)
for x in range(3, len(instance)):
    list_set[x - 3] = [int(s) for s in instance[x].split(' ')]

is_minimal = True
list_sub_set = [None]
for x in list_selected_set:
    del list_sub_set[:]
    for y in list_selected_set:
        if x != y:
            list_sub_set.append(y)
    if is_feasible(p, requirement, list_set, list_sub_set):
        is_minimal = False

if is_feasible(p, requirement, list_set, list_selected_set):
    final_sentence = final_sentence + "is feasible, "
else:
    final_sentence = final_sentence + "isn't feasible, "

if total_cost(cost, list_selected_set) == final_cost:
    final_sentence = final_sentence + "has the correct cost and "
else:
    final_sentence = final_sentence + "hasn't the correct cost and "

if is_minimal:
    final_sentence = final_sentence + "is minimal"
else:
    final_sentence = final_sentence + "isn't minimal"

if not is_instance_valid(informations, requirement, list_set, cost):
    print("The instance entered as input isn't valid ")

print(final_sentence)
