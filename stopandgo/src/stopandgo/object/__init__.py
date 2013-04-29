import inspect
from decorator import decorator
from greenlet import greenlet
from stopandgo import graphics, scheduler

class Constructor(object):
    """
    Factory method for constructing arbitrary objects.
    """
    def __init__(self, objtype, args):
        self.objtype = objtype
        assert isinstance(self.objtype, type)
        self.args = dict(args)
    
    def construct(self):
        return self.objtype(self.args)
    
    def asCode(self, imports=()):
        typename = "%s.%s" % (self.objtype.__module__, self.objtype.__name__)
        shortesttypename = typename
        for importstr in imports:
            if typename.startswith(importstr + "."):
                shorttypename = typename.replace(importstr + ".", "", 1)
                if len(shorttypename) < len(shortesttypename):
                    shortesttypename = shorttypename
        argstr = ",".join("%s=%s" % e for e in self.args.iteritems())
        return "%s(%s)" % (shortesttypename, argstr)

class ReconstructibleType(type):
    """
    Metaclass that stores the arguments passed to the init method, allowing
    the object to be reconstructed afresh. The data is stored as a Constructor
    object in the __constructor__ attribute.
    """
    def __new__(self, name, parents, attr):
        @decorator
        def decoratedInit(init, *args, **kwargs):
            self = args[0]
            if '__constructor__' not in self.__dict__:
                argnames, _, _, defaults = inspect.getargspec(init)
                defaults = () if defaults is None else defaults
                numwithoutdefaults = len(argnames) - 1 - len(defaults)
                nodefault = object()
                extdefaults = (nodefault,) * numwithoutdefaults + defaults
                argdict = {}
                for name, value, default in zip(argnames[1:], args[1:], extdefaults):
                    if value is not default:
                        argdict[name] = value
                for name, value in kwargs:
                    argdict[name] = value
                self.__constructor__ = Constructor(type(self), argdict)
            init(*args, **kwargs)
        def __init__(self): pass
        init = attr.get('__init__', __init__)
        newAttr = dict(attr)
        newAttr['__init__'] = decoratedInit(init)
        return type.__new__(self, name, parents, newAttr)

class GameObject(object):
    __metaclass__ = ReconstructibleType
    
    def __init__(self, sprite, loc = (0,0)):
        self.sprite = sprite
        self.loc = loc
        self.greenlet = greenlet(self.ai)
    
    def __repr__(self):
        return self.__constructor__.asCode(imports=[GameObject.__module__])
    
    def switch(self):
        self.greenlet.switch()
        
    def wait(self):
        greenlet.getcurrent().parent.switch()
    
    def display(self):
        rect = self.sprite.get_rect()
        rect.center = self.loc
        graphics.screen.blit(self.sprite, rect)
    
    def ai(self):
        while True:
            self.wait()
