hidden_mod_keys_string = """1 3 8 7 12
4 7 5 10 1
8 10 12 8 3
11 4 8 4 1
5 3 3 5 6
12 2 4 3 1
2 9 10 7 12
1 7 4 12 3
1 2 10 10 4
6 11 4 7 1
2 5 9 9 1
8 3 8 4 1
10 4 5 12 2
11 2 9 4 7
1 7 8 8 10
4 10 4 10 1
3 6 8 9 8
5 6 2 6 1
12 3 6 10 9
2 8 3 6 11
1 11 10 5 3
7 12 8 10 1
1 5 8 4 7
10 8 11 2 1
3 5 6 5 1
7 12 8 2 5
9 11 3 3 5
1 11 12 9 11
1 3 11 2 8
1 11 5 11 2
9 8 12 3 1
6 5 10 11 4
1 10 11 2 9
2 6 6 6 5
1 6 11 3 6
4 7 6 4 10"""

lines = hidden_mod_keys_string.split("\n")
keys = []
starters = []
finishers = []
combos = []


def match(key1: list[str], key2: list[str]) -> bool:
    return key1[3] == key2[0] and key1[4] == key2[1]


def combine(starter: list[str], middle: list[str], finisher: list[str]) -> None:
    starter_string = " ".join(starter)
    finisher_string = " ".join(finisher)
    combos.append(f"{starter_string} {middle[2]} {finisher_string}")


for line in lines:
    key = line.split()
    keys.append(key)
    if key[0] == "1":
        starters.append(key)
    if key[4] == "1":
        finishers.append(key)

for starter in starters:
    for middle in keys:
        if match(starter, middle):
            for finisher in finishers:
                if match(middle, finisher):
                    combine(starter, middle, finisher)

print(f"#combos {len(combos)}")
print("combos:\n" + "\n".join(combos))

print(f"#starters {len(starters)}, #finishers {len(finishers)}")
