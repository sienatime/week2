# Write a function that takes an iterable (something you can loop through, ie: string, list, or tuple) and produces a dictionary with all distinct elements as the keys, and the number of each element as the value
def count_unique(some_iterable):
    #insert into dictionary with key as thing in list and increment the count 

    d = {}
    for item in some_iterable:
        d[item] = d.get(item, 0) + 1

    return d

# Given two lists, (without using the keyword 'in' or the method 'index') return a list of all common items shared between both lists
def common_items(list1, list2):
    common = []

    i = 0
    j = 0

    while i < len(list1):
        j = 0
        while j < len(list2):
            if list1[i] == list2[j]:
                common.append(list1[i])
                break
            j += 1
        i += 1

    return common

# Given two lists, (without using the keyword 'in' or the method 'index') return a list of all common items shared between both lists. This time, use a dictionary as part of your solution.
def common_items2(list1, list2):
    #get the common items between the two lists
    common1 = common_items(list1,list2)
    #insert that into dictionary with distinct elements as keys
    d = count_unique(common1)

    #the keys are the common items, but printed only once
    return d.keys()


list1 = [1,2,3,4,5,1,2,3]
list2 = [3,4,5,6,7,1,2,3]
list3 = [5,5,5,6,7]

print common_items(list1, list2)
print common_items(list2, list3)

print common_items2(list1, list2)
print common_items2(list2, list3)