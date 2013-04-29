from stopandgo import world

def step():
    for thing in world:
        thing.switch()

