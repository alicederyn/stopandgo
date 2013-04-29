world = []

def importLevel(module):
    world[:] = (o for o in module.__dict__.itervalues()
                if isinstance(o, object.GameObject))
