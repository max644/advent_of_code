from collections import Counter

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT

with open("8.txt", "r") as file:
    content = file.read()

layers = [content[x:x+LAYER_SIZE] for x in range(0, len(content), LAYER_SIZE)]
minZeroLayer = min(layers, key=lambda layer: Counter(layer)['0'])

counts = Counter(minZeroLayer)
print("Step 1 : %d" % (counts['1'] * counts['2']))

image = ["?"] * LAYER_SIZE
pixels = {"0": " ", "1": "X"}

for layer in layers:
    for pixelIdx in range(LAYER_SIZE):
        if image[pixelIdx] == "?" and (layer[pixelIdx] == "0" or layer[pixelIdx] == "1"):
            image[pixelIdx] = pixels[layer[pixelIdx]]

print("Step 2 : ")
print("\n".join([" ".join(image[idx:idx+WIDTH]) for idx in range(0, LAYER_SIZE, WIDTH)]))