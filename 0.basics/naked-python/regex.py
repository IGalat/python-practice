import re

pattern = re.compile(r"\$\{[a-zA-Z1-9 ]+}")
text = "some ${tab} text${enter}, and ${shift down} more${shift up}"

text1 = text

# replace after all finds
for m in pattern.finditer(text1):
    print(m.start(), m.group())
    text1 = text1.replace(m.group(), "_")

print()

text2 = text

# replace on every find
while match := pattern.search(text2):
    print(match.start(), match.group())
    text2 = text2.replace(match.group(), "_")
