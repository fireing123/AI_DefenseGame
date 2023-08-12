WHITE = (255, 255, 255)
BLACK = (000, 000, 000)
YELLOW = (255, 255, 000)
BLUE = (000, 000, 255)
RED = (255, 000, 000)

def darker(rgb, d):
    r, g, b = rgb
    return (r//d, g//d, b//2)