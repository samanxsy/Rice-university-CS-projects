# WordWrangler Game

# Written for python 2

# Saman Saybani

# Rice University - Computer Science

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(10)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists
def remove_duplicates(list1):
    '''
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    '''
    result = []
    if len(list1)> 0:
        result.append(list1[0])

        for elem in list1:
            if elem != result[-1]:
                result.append(elem)

    return result


def intersect(list1, list2):
    '''
    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    '''

    list1_replica = list(list1)
    lis2_replica = list(list2)

    result = []
    while (len(list1_replica) > 0) and (len(lis2_replica) > 0):
        if list1_replica[0] < lis2_replica[0]:
            list1_replica.pop(0)

        elif list1_replica[0] > lis2_replica[0]:
            lis2_replica.pop(0)

        else:
            result.append(list1_replica.pop(0))
            lis2_replica.pop(0)

    return result 


def merge(list1, list2):
    '''
    Merges two sorted lists.
    ''' 
    result = []
    list1_replica = list(list1)
    lis2_replica = list(list2)

    while (len(list1_replica) > 0) and (len(lis2_replica) > 0) :
        if list1_replica[0] < lis2_replica[0]:
            result.append(list1_replica.pop(0))
        else:
            result.append(lis2_replica.pop(0))

    if len(list1_replica) > 0:
        result.extend(list1_replica)
    else:
        result.extend(lis2_replica)

    return result    

                
def merge_sort(list1):
    '''
    Sorts the elements of list1.
    '''
    if len(list1) <= 1:
        return list1
    else:
        return merge(merge_sort(list1[:len(list1) / 2]), merge_sort(list1[len(list1) / 2:]))
                                                          

def gen_all_strings(word):
    '''
    Returns a list of all strings that can be formed from the letters
    in word.
    '''
    if word == "":
        return [""]

    else:
        first_item = word[0]
        other = word[1:]       
        rest_of_strings = gen_all_strings(other)
        plus_first_item = [first_item]

        for string in rest_of_strings:
            if len(string) > 0:
                for char in range(len(string)):
                    new_var = string[:char] + first_item + string[char:]
                    plus_first_item.append(new_var)

                plus_first_item.append(string + first_item)
     
        return plus_first_item + rest_of_strings
        

def load_words(filename):
    '''
    Loads word list from the file named filename.
    Returns a list of strings.
    '''
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)

    strings = []
    for line in netfile.readlines():
        strings.append(line[:-1])

    return strings


def run():
    '''
    Run game.
    '''
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, intersect, merge_sort, gen_all_strings)

    provided.run_game(wrangler)


run()
