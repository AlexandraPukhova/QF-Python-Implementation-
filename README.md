# Quotient Filter Implementation for Python 2.7

##  What is Quotient Filter and why use it?

AMQ (Approximate Membership Query) data structures allow users to track whether an element is in the set. Bloom filter is one of the most well-known AMQ structures. Quotient filter (QF) is another probabilistic data structure that addresses some of the shortcomings of a Bloom filter: specifically, it allows for deletion of items, for resizing dynamically, and, potentially, for counting the number of occurrences of each item in an array (called a Counting Quotient Filter, which I am not extending my filer to). 

Fundamentally, a Quotient filter is a hash table, where a hash function generates a p-bit fingerprint. The r least significant bits is called the remainder while the q = p - r most significant bits is called the quotient (hence the name quotienting). The hash table has 2q slots. (Wikipedia, n.d.) The quotient filter uses slightly more space than a Bloom filter, but much less space than a counting Bloom filter: the size of a Quotient filter is usually 10-20% more than a bloom filter with same FP (False Probability) rate, but it usually is faster. It uses 3 metadata bits per slot. [1]

Like Bloom filer, QF can generate false positives, never deterministically stating that the eliment is in the set, i.e. it is always *probably* in the set. False negatives are not possible in the general case, unless Deletion is used in conjunction with a hash function that yields more that q+r bits. [2]

##  Supported Operations

This implementation introduces the following *main* operations (there are, in fact, more supporting opperations):

INSERT

CONTAINS

FINDCLUSTER

FINDRUN

Theoretically, QF is capable of supporting more operations. Namely, Deletion, Resize and Merge two filters (without having to re-hash the original keys).


##  Sample Code

Initialize the QF

Initialization of a QF is needed, before any of the supported operations can be performed.

```
new_filter = QuotientFilter(r=10, p=32, function=mmh3) # 32-bit MMH3
```

Insertion into QF

```
new_filter.insert('Hello',function=mmh3)
```

Proof of membership in QF

```
new_filter.contains('Hello',function=mmh3)
```

##  Hash function

MMH3 (MurmurHash3) is an open source non-cryptographic hash function suitable for general hash-based lookup. The MMH3 version that I used yields 32-bit hash values. MMH3 takes strings as input and produces integers, ensuring a good trade-off between uniformity and space.

##  Potential Applicaiton

A Quotient Filter, like most AMQ filers, can be used for database query optimization, as well as in networks, computational biology, storage systems, and many other fields. QF is beneficial, because duplicates can be tolerated efficiently and keys can be deleted, when necessary. [4]

##  Complexity 
- Time complexity: Lookups and inserts require locating the start and length of an entire cluster. If the hash function generates uniformly distributed fingerprints (which MMH3 does) then the length of most runs is O(1) and it is highly likely that all runs have length O(log m) where m is the number of slots in the table. [5]
- Space complexity: A quotient filter requires 10–20% more space than a comparable Bloom filter but is faster because each access requires evaluating only a single hash function. [5]

##  References

[1] https://blog.acolyer.org/2017/08/08/a-general-purpose-counting-filter-making-every-bit-count/

[2] https://github.com/Nomon/qf-go/blob/master/qf.go

[3] https://www3.cs.stonybrook.edu/~ppandey/files/p775-pandey.pdf

[4] https://dl.acm.org/citation.cfm?id=3035918.3035963

[5] https://en.m.wikipedia.org/wiki/Quotient_filter
