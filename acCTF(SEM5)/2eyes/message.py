from PIL import Image
import numpy as np

a = Image.open("").convert("L")
b = Image.open("").convert("L")
# threshold to binary (black=1/white=0)
A = (np.array(a) < 128).astype(np.uint8)
B = (np.array(b) < 128).astype(np.uint8)
stacked = np.logical_or(A, B).astype(np.uint8) * 255
Image.fromarray(stacked).save("stacked_result.png")
