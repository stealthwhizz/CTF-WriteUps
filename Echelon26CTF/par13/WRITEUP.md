# Operation Maya - Challenge 13 Writeup

## Challenge Description

The final artifact recovered from Operation Maya appears ordinary. It conforms perfectly to expectations, until examined more closely. The illusion holds only if you accept a single truth. This last clue will unveil the entire operation.

## Initial Analysis

We are given a file `13.zip` which contains a PNG image called `challenge.png`.

### File Information
- **File**: challenge.png
- **Type**: PNG image
- **Size**: 1005 bytes
- **Dimensions**: 256 x 256 pixels
- **Color Mode**: RGB

## Investigation Process

### Step 1: Basic File Inspection

First, I examined the file structure and confirmed it was a valid PNG image:

```bash
file 13/challenge.png
# Output: PNG image data, 256 x 256, 8-bit/color RGB, non-interlaced
```

The file appeared to be a standard PNG with no obvious appended data after the IEND chunk.

### Step 2: Visual Analysis

Opening the image reveals what appears to be a uniform gray (128, 128, 128) square - completely ordinary and unremarkable.

### Step 3: Steganography Check

I checked for LSB (Least Significant Bit) steganography, but all LSBs were 0, ruling out this method.

### Step 4: Pixel Analysis - The Breakthrough

The key clue was **"the illusion holds only if you accept a single truth"**. This suggested looking deeper at what appears to be a uniform image.

Using Python and PIL, I analyzed the unique colors in the image:

```python
from PIL import Image
import numpy as np

img = Image.open("13/challenge.png")
pixels = np.array(img)
unique_colors = np.unique(pixels.reshape(-1, 3), axis=0)
```

**Results:**
```
Number of unique colors: 6

Unique colors (R, G, B) -> As ASCII:
( 99, 111, 114) -> R:  c G:  o B:  r
(102, 108,  97) -> R:  f G:  l B:  a
(103, 123, 115) -> R:  g G:  { B:  s
(110, 125, 128) -> R:  n G:  } B:  ?
(112, 105, 111) -> R:  p G:  i B:  o
(128, 128, 128) -> R:  ? G:  ? B:  ? (background - 65,531 pixels)
```

## The Solution

The "illusion" was hiding in plain sight! The image is **not** uniform - it contains 5 special pixels (among 65,536 total) whose RGB values, when interpreted as ASCII characters, spell out the flag.

These 5 pixels are located at:
- Row 16, Columns 19-23

### Decoding Process

Each pixel's RGB values correspond to ASCII characters:

| Position | RGB Values | Characters | Contribution |
|----------|------------|------------|--------------|
| (16, 19) | (102, 108, 97) | f, l, a | **fla** |
| (16, 20) | (103, 123, 115) | g, {, s | **g{s** |
| (16, 21) | (99, 111, 114) | c, o, r | **cor** |
| (16, 22) | (112, 105, 111) | p, i, o | **pio** |
| (16, 23) | (110, 125, 128) | n, } | **n}** |

Reading these in positional order from left to right:
**fla + g{s + cor + pio + n} = flag{scorpion}**

## Flag

```
flag{scorpion}
```

## Key Insights

1. **Visual Deception**: The image appears completely uniform gray to the naked eye
2. **Minimal Alteration**: Only 5 out of 65,536 pixels were modified
3. **RGB-to-ASCII Encoding**: Each color channel (R, G, B) stores one ASCII character
4. **Positional Reading**: The pixels must be read in their spatial order to reconstruct the message
5. **The "Single Truth"**: The clue about "accepting a single truth" refers to the fact that we need to look at individual pixel values as ASCII, not accept the visual appearance

## Tools Used

- Python 3
- PIL (Python Imaging Library)
- NumPy
- Basic file analysis tools (file, hexdump)

## Lessons Learned

This challenge demonstrates that:
- Data can be hidden in extremely subtle ways
- Even "uniform" images may contain hidden information
- RGB values can encode multiple characters per pixel (3 channels = 3 characters)
- Context and clues are crucial for identifying the steganography method
- Visual analysis alone is insufficient - programmatic pixel inspection is necessary

---

**Challenge Category**: Steganography  
**Difficulty**: Medium  
**Solved**: January 17, 2026
