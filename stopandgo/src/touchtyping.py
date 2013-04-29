# TODO:
#  - pop lowest balloon first
#  - score increasing with every hit

import font, mouse, pygame, random, sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
assert isinstance(screen, pygame.Surface)
safe = (0x75, 0xbb, 0xfd)
dead = (0x00, 0x00, 0x00)

font48 = font.Font(font.get_default_font(), 48, bold=True)

mouse.set_visible(False)

def blit_at(surface, loc):
    rect = surface.get_rect()
    rect.center = loc
    screen.blit(surface.convert_alpha(screen), rect)
    
class Letter(object):
    FEATHER = pygame.image.load("../resources/feather.png")
    BALL = pygame.image.load("../resources/ball.gif")
    ANVIL = pygame.image.load("../resources/anvil.png")
    LETTERS = tuple(
                    #u"aoeu"
                    u"aoeuhtns"
                    #u"abcdefghijklmnopqrstuvwxyz',.-"
                    )
    SURFACE = { l: font48.render(l, True, (0, 0, 0)) for l in LETTERS }
    
    def __init__(self, average_velocity=2.5):
        self.velocity = (0, random.uniform(0.8, 1.2) * average_velocity)
        if self.velocity[1] < 1.8:
            self.image = Letter.FEATHER
        elif self.velocity[1] < 3:
            self.image = Letter.BALL
        else:
            self.image = Letter.ANVIL
        self.hwidth = self.image.get_rect().width / 2
        self.hheight = self.image.get_rect().height / 2
        self.letter = random.choice(Letter.LETTERS)
        self.surface = Letter.SURFACE.get(self.letter)
        self.pos = (random.randrange(self.hwidth, width - self.hwidth), -self.hheight)
        
    def draw(self):
        blit_at(self.image, self.pos)
        blit_at(self.surface, self.pos)
    
    def move(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
    
    @property
    def is_popped(self):
        return self.pos[1] + self.hheight >= height
    
    def matches(self, keyevent):
        return keyevent.mod == 0 and keyevent.unicode == self.letter
        

letters = []
velocity =    [1.5,   2,   2, 2.5, 2.5,   3,   3, 3.5, 3.5,   4]
num_letters = [  1,   1,   2,   3,   3,   4,   5,   5,   6,   7]
pain =        [  1, 1.2, 1.4, 1.6, 1.8,   2, 2.5,   3,   4,   5]
transitions = [ 12,  20,  30,  42,  56,  72,  90, 110, 132, None]

chain = 0
hit = 0
lost = 0
mistypes = 0
max_health = 10
health = max_health
level = 1

screen.fill((0, 0, 0))
pygame.display.set_caption("FeatherTyper")
coverimage = pygame.image.load("../resources/coverscreen.gif")
blit_at(coverimage, (width/2, height/2))
pygame.display.flip()

not_started = True
while not_started:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.mod == 1024 and event.unicode == u'q':
                pygame.quit()
                sys.exit()
            if event.mod == 0 and event.unicode == u' ':
                not_started = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.mod == 1024 and event.unicode == u'q':
                pygame.quit()
                sys.exit()
            elif event.unicode != u'':
                i = next((i for i,l in enumerate(letters) if l.matches(event)), None)
                if i is not None:
                    del letters[i]
                    hit += 1
                    chain += 1
                    health = min(max_health, health + 1)
                    if chain == transitions[0]:
                        velocity.pop(0)
                        num_letters.pop(0)
                        transitions.pop(0)
                        pain.pop(0)
                        chain = 0
                        level += 1
                else:
                    print event
                    mistypes += 1
                    health -= pain[0]
                    chain = 0

    while len(letters) < num_letters[0]:
        letters.append(Letter(velocity[0]))
    for letter in letters:
        letter.move()
    lost_this_time = sum(1 for l in letters if l.is_popped)
    if lost_this_time > 0:
        lost += lost_this_time
        health -= lost_this_time * pain[0]
        health = max(health, 0)
        chain = 0
    screen.fill(tuple(d + (s - d) * health / max_health for s,d in zip(safe, dead)))
    for letter in reversed(letters):
        letter.draw()
    if transitions[0] is None:
        caption = "Level %d (final!)" % level
    else:
        caption = "Level %d (%d keys)" % (level, transitions[0] - chain)
    pygame.display.set_caption(caption)
    pygame.display.flip()
    letters = [l for l in letters if not l.is_popped]
    if health <= 0:
        print "Final score:"
        print "Hits:", hit
        print "Lost:", lost
        print "Mistypes:", mistypes
        pygame.quit()
        sys.exit()
