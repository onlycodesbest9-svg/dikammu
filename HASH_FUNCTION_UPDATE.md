# Hash Function Update

## Problem

Previously, Hash Number could equal ID, causing confusion:
- ID=8 → Hash Number = 8 % 11 = 8 ✗ (same!)
- ID=5 → Hash Number = 5 % 11 = 5 ✗ (same!)

This made searching ambiguous - searching for ID=8 or Hash=8 would seem like the same thing.

## Solution

**New Hash Function**: `(ID + 1) % capacity`

This ensures Hash Number is always different from ID.

## Examples

| ID | Old Hash (ID % 11) | New Hash ((ID+1) % 11) | Different? |
|----|--------------------|------------------------|------------|
| 0  | 0                  | 1                      | ✅ Yes     |
| 1  | 1                  | 2                      | ✅ Yes     |
| 5  | 5                  | 6                      | ✅ Yes     |
| 8  | 8                  | 9                      | ✅ Yes     |
| 10 | 10                 | 0                      | ✅ Yes     |
| 19 | 8                  | 9                      | ✅ Yes     |
| 30 | 8                  | 9                      | ✅ Yes     |
| 102| 3                  | 4                      | ✅ Yes     |

## Search Behavior

### Search by ID
Returns records where **ID exactly matches** the search value.

**Example:**
```
Search by ID = 8
→ Returns: Records with ID=8 only
```

### Search by Hash Number
Returns all records whose **calculated hash** matches the search value.

**Example:**
```
Search by Hash Number = 9
→ Returns: Records with ID=8 (hash=9) and ID=19 (hash=9)
```

## No More Duplication

✅ **Search by ID=5**: Returns only ID=5 records  
✅ **Search by Hash=5**: Returns records where (ID+1)%11 = 5 (e.g., ID=4, ID=15, ID=26...)  
✅ **Completely different results** - no duplication!

## Table Display

The table now shows:

| ID | Name | Hash Number | Notes |
|----|------|-------------|-------|
| 5  | Mouse | 6 | Hash = (5+1) % 11 = 6 |
| 10 | Keyboard | 0 | Hash = (10+1) % 11 = 0 |
| 20 | Monitor | 10 | Hash = (20+1) % 11 = 10 |

**Key Point**: Hash Number column is always different from ID column!

## Implementation

### hash_table.py
```python
def _hash(self, k: int) -> int:
    """
    Compute initial hash index.
    Formula: (k + 1) % capacity
    This ensures Hash Number is different from ID.
    """
    return (k + 1) % self._capacity
```

### ui_main.py
```python
# Calculate hash number (original hash before probing)
# Using same formula as hashtable: (ID + 1) % capacity
hash_number = (rec.id + 1) % self.hash_table.capacity
```

## Benefits

1. **Clear Distinction**: ID and Hash Number are visually different
2. **No Search Confusion**: Searching by ID vs Hash gives different results
3. **Better Understanding**: Users can see how hashing transforms IDs
4. **Avoids Duplicates**: ID=5 and Hash=5 are now completely different things

## Migration Note

If you have existing data, the hash values will be recalculated automatically when you load the data. The records will be re-inserted into the hashtable using the new hash function.
