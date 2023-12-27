import sys

def map_range(range, x):
    assert isinstance(x, Range)
    dst, src, siz = range
    assert isinstance(dst, int)
    assert isinstance(src, int)
    assert isinstance(siz, int)
    cutter = Range(src, siz)
    delta = dst - src
    result = apply(x, cutter, delta)
    if not result[0].empty():
        print(f"Applying {cutter} to {x} (delta={delta})")
        print(f"Result is {result}")
    return result[0]

map_from = {}

with open("day5.txt", 'r') as f:
    lines = f.readlines()

frame = None
for line in lines:
    if line == "":
        break
    words = line.split(" ")
    if words[0] == 'seeds:':
        seeds = list(map(int, words[1:]))
        seeds = zip(seeds[::2], seeds[1::2])

    if 'to' in words[0]:
        src, tgt = words[0].split("-to-")
        frame = (src, tgt)
        map_from[src] = tgt
    if line[0].isdigit():
        r = list(map(int, words))
        assert frame
        if frame not in map_from:
            map_from[frame] = []
        map_from[frame] += [r]

class Range:
    def __init__(self, start, *args, length=None, end=None):
        if len(args) == 1:
            length = args[0]
        self.start = start
        if length is None and end is None:
            raise ValueError("Need length or end to make range")
        if length is not None and end is not None:
            raise ValueError("Need just length or just end to make range")
        self.length = length if length is not None else end-start
        assert self.start >= 0
        assert self.length >= 0
        
    @property
    def end(self):
        return self.start + self.length
    
    def has(self, x):
        return x >= self.start and x < self.end

    def __str__(self):
        return f"Range({self.start}, {self.length})"

    def __eq__(self, other):
        if not isinstance(other, Range):
            return False
        if self.length == 0 and other.length == 0:
            return True
        return self.start == other.start and self.length == other.length

    def __hash__(self):
        return self.start * self.length

    def __repr__(self):
        return str(self)
    
    def empty(self):
        return self.length == 0

    def move(self, delta):
        assert self.start + delta >= 0
        assert self.length >= 0
        return Range(self.start + delta, self.length)
        
    
def intersection(range1, range2):
    if range1.end <= range2.start:
        return Range(0, 0)
    if range2.end <= range1.start:
        return Range(0, 0)
    start = max(range1.start, range2.start)
    return Range(start, min(range1.end, range2.end) - start)

def pair_up(xs):
    return list(zip(xs[::2], xs[1::2]))

def subtract(range1, range2):
    result = []
    if range1.start < range2.start:
        result.append(Range(range1.start, end=min(range2.start, range1.end)))
    if range2.end < range1.end:
        result.append(Range(max(range1.start, range2.end), end=range1.end))

    return {r for r in result if not r.empty()}
    ## if range2.end <= range1.start or range2.start >= range1.end:
    ##     return {range1}
    ## if range2.end < range1.end and range2.start >= range1.start:
    ##     return {Range(range1.start, end=range2.start),
    ##                 Range(range2.end, end=range1.end)}
    ## if range2.end >= range1.end and range2.start <= range1.start:
    ##     return {}
    ## if range2.start < range1.start:
    ##     return {Range(range2.end, end=range1.end)}
    ## else:  # range2.end >= range1.end
    ##     return {Range(range1.start, end=range2.start)}

    
def slice(range1, cutter):
    
    overlap = intersection(range1, cutter)
    return (overlap, subtract(range1, cutter))

    cuts = sorted([range1.start, cutter.start, range1.end, cutter.end])
    results = [o for o in [overlap] if not o.empty()]
    lefties = [x for x in cuts if x <= overlap.start]
    righties = [x for x in cuts if x >= overlap.end]

    assert len(lefties) % 2 == 0
    assert len(righties) % 2 == 0
    return (overlap, set([Range(s, e-s) for s, e in pair_up(lefties) if e > s] + 
                             [Range(s, e-s) for s, e in pair_up(righties) if e > s]))
    
assert intersection(Range(2, 5), Range(3, 5)) == Range(3, 4)
assert intersection(Range(4, 5), Range(3, 5)) == Range(4, 4)
assert intersection(Range(2, 5), Range(7, 5)) == Range(0, 0)
assert intersection(Range(5, 5), Range(0, 5)) == Range(0, 0)
assert intersection(Range(0, 10), Range(2, 5)) == Range(2, 5)
assert intersection(Range(3, 5), Range(0, 10)) == Range(3, 5)

def assert_equal(a, b):
    if a != b:
        print("Expected a == b:")
        print(f"  a = {a}:")
        print(f"  b = {b}:")
    assert a == b
    
print(slice(Range(2, 5), Range(3, 5)))
assert slice(Range(2, 5), Range(3, 5)) == (Range(3, 4), {Range(2, 1)})
assert slice(Range(4, 5), Range(3, 5)) == (Range(4, 4), {Range(8, 1)})
print(slice(Range(4, 5), Range(3, 6)))
assert slice(Range(4, 5), Range(3, 6)) == (Range(4, 5), set())
print( slice(Range(2, 5), Range(7, 5)) )
assert slice(Range(2, 5), Range(7, 5)) == (Range(0, 0), {Range(2, 5)})
assert slice(Range(5, 5), Range(0, 5)) == (Range(0, 0), {Range(5, 5)})
print( slice(Range(0, 10), Range(2, 5)))
assert slice(Range(0, 10), Range(2, 5)) == (Range(2, 5), {Range(0, 2), Range(7, 3)})
assert slice(Range(3, 5), Range(0, 10)) == (Range(3, 5), set())
assert_equal(slice(Range(3, 5), Range(4, 4)), (Range(4, 4), {Range(3,1)}))
assert_equal(slice(Range(3, 5), Range(3, 4)), (Range(3, 4), {Range(7,1)}))
assert slice(Range(3, 5), Range(3, 5)) == (Range(3, 5), set())

print("Tests OK")

def apply(obj, operator, delta):
    to_move, unaffected = slice(obj, operator)
    if to_move.empty():
        return (to_move, unaffected)
    return (to_move.move(delta), unaffected)

print(apply(Range(100, 75), Range(125, 25), 200))

def f(r):
    a, b, c = r
    return b

if len(sys.argv) > 1:
    things = [(sys.argv[1], sys.argv[2])]
else:
    things = seeds

things = [Range(int(s), int(l)) for s, l in things]

thing_type = 'seed'

def show_mapping(m, type):
    m = sorted(m, key=f)
    end = 0
    for dst, src, siz in m:
        if src != end:
            print(f"src - end = {src-end}")
        print(f"mapping {type}s from {src:11}-{src+siz:11}; delta {dst-src}")
        end = src+siz

print(things)
print()
print([(x, y) for x in things for y in things if x != y if not intersection(x, y).empty()])
    
while True:
    print()
    print(thing_type)
    if thing_type not in map_from:
        ## print(things)
        break
    to_type = map_from[thing_type]

    print("mapping", thing_type, "to", to_type)

    # show_mapping(map_from[(thing_type, to_type)], thing_type)
        
    new_things = set()
    print("num ranges:", len(things))
    print("set size:", sum(x.length for x in things))
    ##print(things)
    for thing in things:
        for r in map_from[(thing_type, to_type)]:
            # Problem is here: I can't include unmapped things in this result right now.
            # Need to just apply intersections right now, handle unmapped things at the end?
            x = map_range(r, thing)
            # things += ys
            new_things.update([x])
    things = {x for x in new_things if not x.empty()}
##    print(any(not intersection(x, y).empty() for x in things for y in things))
    print("Intersections")
    
    thing_type = to_type

##things.sort()
print(f"final {thing_type}s:")
##print("", *(f"{str(t):11}\n" for t in things))
print(things)
print(min(r.start for r in things))
