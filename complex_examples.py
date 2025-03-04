import gc
import sys
import time
import weakref
import memory_profiler
import tracemalloc
from typing import List, Dict

# Example 1: Basic Reference Counting
print("\nExample 1: Basic Reference Counting")


def demonstrate_ref_counting():
    # Create a list and check its reference count
    my_list = [1, 2, 3]
    print(f"Reference count: {sys.getrefcount(my_list)}")

    # Create another reference
    another_ref = my_list
    print(f"Reference count after new reference: {sys.getrefcount(my_list)}")

    # Remove reference
    del another_ref
    print(f"Reference count after deleting reference: {sys.getrefcount(my_list)}")


demonstrate_ref_counting()
#================================================================================

# Example 2: Memory Usage Tracking
print("\nExample 2: Memory Usage Tracking")


@memory_profiler.profile
def memory_growth():
    # Create a growing list to see memory increase
    big_list = []
    for i in range(100000):
        big_list.append(i)
    return big_list


d = memory_growth()
#================================================================

# Example 3: Circular Reference
print("\nExample 3: Circular Reference")


def create_circular_ref():
    class Node:
        def __init__(self):
            self.ref = None

    # Create circular reference
    node1 = Node()
    node2 = Node()
    node1.ref = node2
    node2.ref = node1

    # Get collector stats before
    print("Before collection:", gc.get_count())

    # Delete references and collect
    del node1, node2
    gc.collect()
    print("After collection:", gc.get_count())


create_circular_ref()
#=============================================================

# Example 4: Memory Leak Detection with tracemalloc
print("\nExample 4: Memory Leak Detection")


def memory_leak_example():
    tracemalloc.start()

    # Create a function that might leak
    cache = {}
    for i in range(10000):
        key = f"key_{i}"
        cache[key] = "some_data" * 100

    # Get memory snapshot
    snapshot = tracemalloc.take_snapshot()
    print("Top 3 memory allocations:")
    for stat in snapshot.statistics('lineno')[:3]:
        print(f"{stat.count} blocks: {stat.size / 1024:.1f} KiB")

    tracemalloc.stop()


memory_leak_example()
#============================================================================

# Example 5: Weak References
print("\nExample 5: Weak References")


def demonstrate_weak_ref():
    class DataHolder:
        def __init__(self, data):
            self.data = data

    # Create object and weak reference
    obj = DataHolder("important_data")
    weak_ref = weakref.ref(obj)

    print("Weak ref before deletion:", weak_ref())
    del obj
    print("Weak ref after deletion:", weak_ref())


demonstrate_weak_ref()
#=====================================================================

# Example 6: Custom Object with GC Monitoring
print("\nExample 6: Custom Object with GC Monitoring")


class GCMonitoredObject:
    def __init__(self, name):
        self.name = name
        print(f"Created {self.name}")

    def __del__(self):
        print(f"Destroying {self.name}")


def monitor_gc_behavior():
    # Create objects
    obj1 = GCMonitoredObject("Object 1")
    obj2 = GCMonitoredObject("Object 2")

    # Get GC counts before
    print("GC count before:", gc.get_count())

    # Delete and force collection
    del obj1, obj2
    gc.collect()
    print("GC count after:", gc.get_count())


monitor_gc_behavior()
#========================================================================

# Example 7: Memory Profile Decorator
print("\nExample 7: Memory Profile Decorator")


def track_memory(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_mem = tracemalloc.get_traced_memory()[0]

        result = func(*args, **kwargs)

        end_mem = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()
        print(f"Memory change: {(end_mem - start_mem) / 1024:.2f} KiB")
        return result

    return wrapper


@track_memory
def memory_intensive_function():
    return [i * i for i in range(10000)]


memory_intensive_function()
#==================================================================

# Example 8: Complex Memory Leak with Class
print("\nExample 8: Complex Memory Leak")


class LeakyClass:
    _cache = {}  # Class-level cache that can cause leaks

    def __init__(self, name):
        self.name = name
        LeakyClass._cache[name] = self

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()
        gc.collect()


@track_memory
def demonstrate_memory_leak():
    # Create many instances
    for i in range(1000):
        LeakyClass(f"object_{i}")

    print("Objects in cache:", len(LeakyClass._cache))
    LeakyClass.clear_cache()
    print("Objects after clear:", len(LeakyClass._cache))


demonstrate_memory_leak()
#=========================================================================

# Example 9: Generation-based GC
print("\nExample 9: Generation-based GC")


def show_gc_generations():
    # Get current GC thresholds
    print("GC thresholds:", gc.get_threshold())

    # Create some objects and check generations
    objects = []
    for i in range(3):
        objects.append([i * j for j in range(1000)])
        print(f"After creation {i + 1}:", gc.get_count())

    # Force collection for each generation
    for i in range(3):
        print(f"Collecting generation {i}")
        gc.collect(i)
        print("Counts after collection:", gc.get_count())


show_gc_generations()
#====================================================================
# Example 10: Advanced Memory Profiling
print("\nExample 10: Advanced Memory Profiling")


def complex_memory_operations():
    tracemalloc.start()
    initial_snapshot = tracemalloc.take_snapshot()

    # Perform various memory operations
    data_structures = []
    for i in range(100):
        data_structures.append({
            'list': [j * j for j in range(100)],
            'dict': {str(j): j for j in range(100)},
            'set': set(range(100))
        })

    final_snapshot = tracemalloc.take_snapshot()
    stats = final_snapshot.compare_to(initial_snapshot, 'lineno')

    print("\nTop 10 memory changes:")
    for stat in stats[:10]:
        print(f"{stat.size_diff / 1024:.1f} KiB: {stat.count_diff} blocks")

    tracemalloc.stop()

    # Clean up and show GC stats
    del data_structures
    gc.collect()
    print("\nFinal GC stats:", gc.get_stats())


complex_memory_operations()