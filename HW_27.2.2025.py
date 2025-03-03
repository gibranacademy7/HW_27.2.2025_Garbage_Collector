# Question 1:
# "How can one determine how many strong references exist for an object?"

# Answer:
# In Python, you can use the sys.getrefcount() function from the sys module to determine the number of strong
# references to an object. However, note that sys.
# getrefcount(obj) returns a count that is typically one higher than the actual number of references,
# because the function itself temporarily creates an additional reference when it is called.

# Example:

import sys

class MyClass:
    pass

obj = MyClass()
print(sys.getrefcount(obj))  # Typically returns 2 (one for `obj`, one for the function argument)

#-------------------------------------------------------------------------------------------------------------

# Question 2:
# "What two components need to be measured to determine the size of a list in memory?"

# Answer:
# To determine the memory size of a list in Python, you need to measure two components:
#
# The list object itself – This includes the internal structure that holds metadata like size, capacity,
# and references to elements. You can measure this using sys.getsizeof(lst).
# The elements inside the list – Since a list stores references to objects rather than the objects themselves,
# you must also sum up the memory usage of each element using sys.getsizeof(item) for every item in the list.

# Example:

import sys

lst = [1, "hello", [3, 4]]

# Size of the list object itself
size_list = sys.getsizeof(lst)

# Size of elements inside the list
size_elements = sum(sys.getsizeof(item) for item in lst)

total_size = size_list + size_elements

print(f"List object size: {size_list} bytes")
print(f"Elements size: {size_elements} bytes")
print(f"Total size: {total_size} bytes")

#------------------------------------------------------------------------------------------------------------

# Question 3:

# "What does the function gc.get_count() provide? When is it advisable to use it?"

# Answer:
# The function gc.get_count() from the gc (garbage collection) module returns a tuple with three integers
# representing the number of objects in each generation of Python's garbage collector.

# Example:

import gc

print(gc.get_count())  # Example output: (552, 7, 0)

# Explaination:
# The tuple returned by gc.get_count() typically contains three values:
# The number of objects in the first generation.
# The number of objects in the second generation.
# The number of objects in the third generation.

# It is advisable to use gc.get_count() when you want to monitor

#----------------------------------------------------------------------------------------------------------

# Question 4:

# "What does the function gc.collect() do? When is it advisable to use it?"

# Answer:
# The function gc.collect() in Python manually triggers the garbage collector to free up memory
# by collecting and deleting unreachable objects, especially those involved in circular references.

# Example:

import gc

collected = gc.collect()  # Returns the number of objects collected
print(f"Collected {collected} unreachable objects")

# Explaination:

# When should you use gc.collect()?
# When dealing with circular references: Python’s default garbage collection may not immediately
# clean up objects that reference each other. If you suspect memory leaks due to such cases,
# gc.collect() can help.
# In memory-sensitive applications: If your program runs in a constrained environment (e.g., embedded systems), calling gc.collect() after processing large objects can help free memory earlier.
# During debugging: To check if objects are being properly garbage-collected, you can manually trigger collection and analyze what was removed.
# Before measuring memory usage: If profiling memory usage, calling gc.collect() ensures you're measuring only active objects.
# When NOT to use it:
# Avoid frequent calls in performance-critical code. Garbage collection can pause execution, so triggering it too often may degrade performance.
# Let Python's automatic garbage collector handle most cases. Manually forcing collection is usually unnecessary unless you detect a specific issue.

#--------------------------------------------------------------------------------------------------------------

# Question 5:

# "How can the garbage collector (GC) be disabled and re-enabled? When is it advisable to do so?"

# Answer:

# Disabling and Re-enabling the Garbage Collector
# Python allows you to disable the garbage collector using gc.disable() and re-enable it using gc.enable().

# Example:

import gc

gc.disable()  # Disable garbage collection
# Our code that should run without GC interruptions
gc.enable()   # Re-enable garbage collection

# Explaination:

# When Should You Disable GC?
# Performance Optimization:

# If your program creates many short-lived objects, garbage collection might run too frequently, causing performance slowdowns. Temporarily disabling it can improve efficiency.
# When Managing Large Objects:

# If you're processing large data structures (e.g., images, large lists, or machine learning models), GC interruptions can slow down execution. Disabling GC temporarily can prevent unnecessary pauses.
# When You Know No Cyclic References Exist:

# If you're confident your code doesn't create cyclic references
# (e.g., a function that only works with local variables), disabling GC can reduce overhead.
# When NOT to Disable GC:
# If your program runs for a long time without re-enabling GC, memory usage may increase, leading to leaks.
# If you're working with objects that reference each other cyclically, they might never be cleaned up.
# Best Practice: If you disable GC, make sure to re-enable it after the critical section and manually
# trigger gc.collect() if needed.
#----------------------------------------------------------------------------------------------------


# question 6:

# "What is the difference between a regular reference and a weak reference?
# How can a weak reference help solve the problem of circular references?"

# Answer:
# Difference Between a Regular and a Weak Reference
# Regular Reference: A standard reference in Python increases the reference count of an object,
# preventing it from being garbage collected as long as the reference exists.
# Weak Reference (weakref): A weak reference does not increase the reference count.
# This means the object can be garbage-collected even if a weak reference to it still exists.

# Example: Regular vs. Weak Reference:

import weakref

class MyClass:
    pass

obj = MyClass()           # Regular reference (strong)
weak_obj = weakref.ref(obj)  # Weak reference

print(weak_obj())  # Access the object (returns obj)

del obj  # Delete the original strong reference

print(weak_obj())  # Now returns None because obj is garbage collected

#------------------------------------------------------------------

# How Can a Weak Reference Solve Circular Reference Issues?
# A circular reference occurs when two or more objects reference each other,
# preventing their reference counts from reaching zero. Python's garbage collector can handle such cases,
# but weak references can prevent them from occurring in the first place.

# Example of Circular Reference Problem:

class A:
    def __init__(self, obj):
        self.obj = obj  # Strong reference

class B:
    def __init__(self, obj):
        self.obj = obj  # Strong reference

a = A(None)
b = B(a)
a.obj = b  # Circular reference

del a, b  # Objects won't be collected immediately due to circular reference

# Solution Using Weak References

import weakref

class A:
    def __init__(self, obj):
        self.obj = weakref.ref(obj) if obj is not None else None  # Handle None properly

class B:
    def __init__(self, obj):
        self.obj = obj  # Strong reference

a = A(None)  # This now works
b = B(a)
a.obj = weakref.ref(b)  # Works correctly

# Solution 2: Use Weak Reference Proxies
# Instead of storing a weak reference directly, you can use weakref.proxy()
# which raises an error if the referenced object no longer exists:

# Explaination:

# When to Use Weak References?
# For cache-like structures: Objects should not be kept alive longer than necessary.
# To avoid memory leaks caused by circular references: Especially in custom data structures
# (e.g., graphs, trees).
# For event listeners or callbacks: To prevent event subscribers from preventing object cleanup.

import weakref

class A:
    def __init__(self, obj):
        self.obj = weakref.proxy(obj) if obj is not None else None  # Use weak proxy

class B:
    def __init__(self, obj):
        self.obj = obj  # Strong reference

a = A(None)  # No error
b = B(a)
a.obj = weakref.proxy(b)  # Works correctly










#-----------------------------------------------------------------------
