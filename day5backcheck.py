import sys

def map_range(range, x):
    dst, src, siz = range
    if x >= src and x < src + siz:
        print(f"item {x} maps in range {src}-{src + siz} to {x - src + dst}")
        return x - src + dst
    else:
        return x

def unmap_range(range, x):
    dst, src, siz = range
    if x >= dst and x < dst + siz:
        print(f"item {x} maps in range {dst}-{dst + siz} to {x - dst + src}")
        return x - dst + src
    else:
        return x

mappings = {}
map_from = {}
map_to = {}

with open("day5.txt", 'r') as f:
    lines = f.readlines()

frame = None
for line in lines:
    if line == "":
        break
    words = line.split(" ")
    if words[0] == 'seeds:':
        seeds = words[1:]
    if 'to' in words[0]:
        src, tgt = words[0].split("-to-")
        frame = (src, tgt)
        map_from[src] = tgt
        map_to[tgt] = src
    if line[0].isdigit():
        r = list(map(int, words))
        if frame not in mappings:
            mappings[frame] = []
        mappings[frame] += [r]

things = [sys.argv[1]]
thing_type = 'location'
while True:
    print(thing_type)
    if thing_type not in map_to:
        ## print(things)
        break
    from_type = map_to[thing_type]
    new_things = []
    for thing in things:
        for r in mappings[(from_type, thing_type)]:
            thing = unmap_range(r, int(thing))
        new_things += [thing]
    things = new_things
    thing_type = from_type
