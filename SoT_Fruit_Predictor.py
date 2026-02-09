########################################################################################
### Code to Predict Average Food Distribution Obtained from Islands in Sea of Thieves
########################################################################################
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path
from PIL import Image
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


fruit_probs = [0.5, 0.3, 0.15, 0.04, 0.01]  # must sum to 1
n = 10  # amount of fruit per island
p = 5  # number of fruit in pocket
I = 5000  # number of islands visited


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
    fruit_to_num = {'banana': 0, 'coconut': 1, 'pomegranate': 2, 'mango': 3, 'pineapple': 4}
    num_to_fruit = {0: 'banana', 1: 'coconut', 2: 'pomegranate', 3: 'mango', 4: 'pineapple'}
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
percents = [count / len(haul) for count in counts]

### Plotting
plt.style.use('seaborn-darkgrid')
labels = ['bananas', 'coconuts', 'pomegranates', 'mangos', 'pineapples']
colors = ['#FFC300', '#8B5A2B', '#C70039', '#FF7F50', '#98FB98']

assets = {
    'bananas': Path('assets/Banana.webp'),
    'coconuts': Path('assets/Coconut.webp'),
    'pomegranates': Path('assets/Pomegranate.webp'),
    'mangos': Path('assets/Mango.webp'),
    'pineapples': Path('assets/Pineapple.webp'),
}

fig = plt.figure(constrained_layout=True, figsize=(10, 10), dpi=120)
gs = fig.add_gridspec(2, 1, height_ratios=[4, 1.0], hspace=0.02)
ax = fig.add_subplot(gs[0])
bars = ax.bar(labels, percents, color=colors, edgecolor='black')
ax.set_ylabel('Percent of haul')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
ax.set_ylim(0, max(percents) * 1.15)
ax.set_title(f'Average Fruit Distribution After {I} Islands')
for bar, pct in zip(bars, percents):
    height = bar.get_height()
    ax.annotate(f'{pct*100:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6),
                textcoords='offset points',
                ha='center', va='bottom', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels([''] * len(labels))
icon_ax = fig.add_subplot(gs[1], sharex=ax)
icon_ax.set_xlim(ax.get_xlim())
icon_ax.axis('off')
ICON_SCALE = 0.61
ICON_Y_OFFSET = 0.17
imgs = []
for fruit in ['bananas', 'coconuts', 'pomegranates', 'mangos', 'pineapples']:
    img_path = assets[fruit]
    try:
        img = Image.open(img_path).convert('RGBA')
        arr = np.asarray(img)
        imgs.append((arr, img.size[0], img.size[1]))
    except Exception:
        imgs.append(None)
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
icon_ax.set_ylim(0, 1)
for info, bar in zip(imgs, bars):
    if info is None:
        continue
    arr, iw, ih = info
    x = bar.get_x()
    w = bar.get_width()
    x0_disp = ax.transData.transform((x, 0))[0]
    x1_disp = ax.transData.transform((x + w, 0))[0]
    bar_width_px = max(1.0, abs(x1_disp - x0_disp))
    icon_bbox = icon_ax.get_window_extent(renderer)
    max_h_px = max(1.0, icon_bbox.height * 0.95)
    zoom_w = bar_width_px / float(iw)
    zoom_h = max_h_px / float(ih)
    zoom = min(zoom_w, zoom_h) * ICON_SCALE
    im = OffsetImage(arr, zoom=zoom, interpolation='bilinear')
    x_center = x + w / 2.0
    ab = AnnotationBbox(im, (x_center, ICON_Y_OFFSET), frameon=False, box_alignment=(0.5, 0.0), xycoords=icon_ax.transData)
    ab.set_clip_path(icon_ax.patch)
    icon_ax.add_artist(ab)
plt.show()
