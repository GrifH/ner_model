from annotations import all
counts = {}
for sen, ent in all:
    for entity in ent['entities']:
        if entity[2] in counts:
            counts[entity[2]]  = counts[entity[2]] + 1
        else:
            counts[entity[2]] = 1

print(counts)
