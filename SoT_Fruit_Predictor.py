###############################################################################
### Code to Predict Average Food Distribution Obtained from Islands in Sea of Thieves
###############################################################################
import random
import matplotlib.pyplot as plt

fruit_probs = [0.5, 0.3, 0.15, 0.04, 0.01] # must sum to 1
n = 10 # amount of fruit per island
p = 5 # number of fruit in pocket
I = 5000 # number of islands visited

def select_fruit():
    rand = random.random()
    if rand < fruit_probs[0]:
        fruit = 'banana'
    elif rand < fruit_probs[0] + fruit_probs[1]:
        fruit = 'coconut'
    elif rand < fruit_probs[0] + fruit_probs[1] + fruit_probs[2]:
        fruit = 'pomegranate'
    elif rand < fruit_probs[0] + fruit_probs[1] + fruit_probs[2] + fruit_probs[3]:
        fruit = 'mango'
    else:
        fruit = 'pineapple'
    return fruit

def generate_island():
    fruits = [select_fruit() for x in range(n)]
    return fruits

def get_pocket():
    fruits = generate_island()
    fruit_to_num = {'banana' : 0, 'coconut' : 1, 'pomegranate' : 2, 'mango' : 3, 'pineapple' : 4}
    num_to_fruit = {0 : 'banana', 1 : 'coconut', 2 : 'pomegranate', 3 : 'mango', 4 : 'pineapple'}
    fruits = [fruit_to_num[fruit] for fruit in fruits]
    fruits = sorted(fruits)
    fruits = [num_to_fruit[fruit] for fruit in fruits]
    pocket = fruits[-p:]
    return pocket

def visit_islands():
    all_fruits = []
    for i in range(I):
        pocket = get_pocket()
        all_fruits = all_fruits + pocket
    return all_fruits

def count_fruits(haul):
    num_banana = haul.count('banana')
    num_coconut = haul.count('coconut')
    num_pomegranate = haul.count('pomegranate')
    num_mango = haul.count('mango')
    num_pineapple = haul.count('pineapple')
    counts = [num_banana, num_coconut, num_pomegranate, num_mango, num_pineapple]
    return counts

haul = visit_islands()
counts = count_fruits(haul)
percents = [count/len(haul) for count in counts]

fig = plt.figure()
labels = ['bananas', 'coconuts', 'pomegranates', 'mangos', 'pineapples']
plt.bar(labels, percents)
plt.show()













# end
