import sys

def map_range(range, x):
    dst, src, siz = range
    ## print(f"Checking ", *map(type, [dst, src, siz, x]))
    ## print(f"       = ", *[dst, src, siz, x])
    if x >= src and x < src + siz:
        print(f" {x:11} maps in   {src:11}:{src + siz:11} to {x - src + dst:11}")
        return x - src + dst
    else:
        return x

map_from = {}

with open("day5.txt", 'r') as f:
    lines = f.readlines()

frame = None
for line in lines:
    if line == "":
        break
    words = line.split(" ")
    if words[0] == 'seeds:':
        seeds = map(int, words[1:])
            
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

def f(r):
    a, b, c = r
    return b

if len(sys.argv) > 1:
    things = [sys.argv[1]]
else:
    things = seeds

things = map(int, things)

thing_type = 'seed'

def show_mapping(m, type):
    m = sorted(m, key=f)
    end = 0
    for dst, src, siz in m:
        if src != end:
            print(f"src - end = {src-end}")
        print(f"mapping {type}s from {src:11}-{src+siz:11}; delta {dst-src}")
        end = src+siz

while True:
    print()
    print(thing_type)
    if thing_type not in map_from:
        ## print(things)
        break
    to_type = map_from[thing_type]

    print("mapping", thing_type, "to", to_type)

    # show_mapping(map_from[(thing_type, to_type)], thing_type)
        
    new_things = []
    for thing in things:
        for r in map_from[(thing_type, to_type)]:
            thingx = map_range(r, int(thing))
            if thing != thingx:
                thing = thingx
                break
        new_things += [thing]
    things = new_things
    thing_type = to_type

things.sort()
print(f"final {thing_type}s:")
print("", *(f"{t:11}\n" for t in things))

