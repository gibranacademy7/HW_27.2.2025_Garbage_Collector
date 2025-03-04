# 1. Reference Counting (sys.getrefcount)

import sys

print('1' * 100)
a = []  # create an empty list
print("Reference count for a:", sys.getrefcount(a))  # Initial ref count
b = a  # Assign `a` to `b`, increasing ref count
print('id a = ', id(a))
print('id b = ', id(b))
print("Reference count for a:", sys.getrefcount(a))  # Increased ref count
del a  # Remove `a`, but `b` still holds a reference
print("Reference count for b:", sys.getrefcount(b))  # Still nonzero
#-----------------------------------------------------------------------------

# 2. Memory Size of Objects (sys.getsizeof)

print('2' * 100)
import sys

a = [1, 2, 3, 4, 5]
print("Size of a:", sys.getsizeof(a), "bytes")  # Size of list object itself (not elements)

a = [1, 2, 3, 4, [1] * 100000]
container_size = sys.getsizeof(a)  # Size of list (pointers)
elements_sizes = [sys.getsizeof(item) for item in a]  # Size of each element
total_elements_size = sum(elements_sizes)

print("Container size of 'a':", container_size, "bytes")
print("Sizes of individual elements:", elements_sizes)
print("Total size of all elements:", total_elements_size, "bytes")
print("Approximate total size:", container_size + total_elements_size, "bytes")
#------------------------------------------------------------------------------------

# 3. Checking Garbage Collector Counters (gc.get_count())

print('3' * 100)
import gc

print("Garbage Collector counts:", gc.get_count())  # Show objects in GC generations
gc.collect()  # Force garbage collection
print("Garbage Collector counts:", gc.get_count())  # Show updated counts
#--------------------------------------------------------------------------------------

# 4. Garbage Collector Collecting Cycles

print('4' * 100)
import gc

class A:
    pass

class B:
    pass

def fun1():
    a = A()
    b = B()
    a.next = a  # Self-reference
    b.next = b  # Self-reference

fun1()

print("Forcing garbage collection...")
unreachable = gc.collect()
print("Unreachable objects collected:", unreachable)
print("Garbage Collector counts after collection:", gc.get_count())
#----------------------------------------------------------------------------

# 5. Circular References

print('5' * 100)
import gc

class Node:
    def __init__(self, value):
        self.value = value
        self.other = None

a = Node(1)
b = Node(2)
a.other = b
b.other = a  # Circular reference

del a, b  # Remove external references

print("Forcing garbage collection on circular references...")
print("Garbage Collector counts before collection:", gc.get_count())
circlue = gc.collect()
print("Circular references collected:", circlue)
print("Garbage Collector counts after collection:", gc.get_count())
#=============================================================================

# 6. Weak References (weakref.ref())

print('6' * 100)
import weakref

class Node:
    def __init__(self, value):
        self.value = value
        self.other = None

a = Node(1)
b = Node(2)
a.other = weakref.ref(b)  # Use weak references
b.other = weakref.ref(a)

print("b via a.other:", a.other())
print("a via b.other:", b.other())
# ==========================================================

# 7. Simulating Memory Leaks

print('7' * 100)

leak_list = []

class Leaky:
    def __init__(self, value):
        self.value = value

def create_leak():
    for i in range(10000):
        leak_list.append(Leaky(i))  # Objects are never removed

print("Starting memory leak demonstration...")
create_leak()
print("Number of leaked objects:", len(leak_list))

print(len(gc.get_referents(leak_list)))
print(gc.get_count())
gc.collect()
print(gc.get_count())
print(len(gc.get_referents(leak_list)))
# ===============================================================

# 8. Profiling Memory Usage (memory_profiler)

print('8' * 100)
from memory_profiler import profile

@profile
def create_large_list():
    a = [i for i in range(1000)]
    print(4)
    return a

b = create_large_list()
#==========================================================

# 9. Object Graph Analysis (objgraph)

print('9' * 100)
import objgraph

a = [1, 2, 3]
b = {'key': [1]*1_000_00000}  # Large object
c = [a, 1]

objgraph.show_most_common_types(limit=10)
#=======================================================

# 10. GC Generations and Forced Collection

print('*' * 200)
import gc

gc.enable()

def create_cycle():
    x = {}
    x['self'] = x  # Circular reference
    return x

gc.collect()
print("After initial collection:", gc.get_count())

cycles = [create_cycle() for _ in range(10)]
print("After creating cycles:", gc.get_count())

gc.collect(0)  # Collect generation 0
print("After gen 0 collection:", gc.get_count())

more_cycles = [create_cycle() for _ in range(5)]
print("After creating more cycles:", gc.get_count())

full_collected = gc.collect()
print("After full collection:", gc.get_count(), "collected:", full_collected)
#==============================================================================


