def setup():
    size(600, 600)  # canvas size
    no_loop()  # draw once, unless the mouse is clicked
    no_stroke() # no outlines
    
def draw():
    background(240)  # light gray background
    tile_size = 50  # size of each tile
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # randomly choose between a square or a circle
            if random(1) < 0.5:
                draw_square(x, y, tile_size)
            else:
                draw_circle(x, y, tile_size)

def draw_square(x, y, size):
    fill(random(255), random(255), random(255))  # random fill color
    rect(x, y, size, size)

def draw_circle(x, y, size):
    fill(random(255), random(255), random(255))  # random fill color
    ellipse(x + size / 2, y + size / 2, size, size)

def mouse_clicked():
    redraw()  # redraw the composition when the mouse is clicked

run_sketch()