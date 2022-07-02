import one  # a way to import more than one package - have to use one.foo.bar.func() after
from one.ein.hi import hi_german as german_hello
from one.uno import hi as spanish

print(german_hello())
print(spanish.hi_spanish())
print(one.ein.hi.hi_both())
