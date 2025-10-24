# SmartHash Manager - Linear Probing Implementation

## Overview

This implementation adds **linear probing** collision resolution and **advanced search capabilities** to the SmartHash Manager hashtable backend, while maintaining the existing UI design.

## Key Features Implemented

### 1. Linear Probing Collision Resolution

- **Algorithm**: When a collision occurs (hash index already occupied), the algorithm probes forward linearly: `(h(k) + i) mod m`
- **Wraparound**: Probing wraps around to index 0 when reaching the end of the table
- **Most Recent Shifts Forward**: When multiple entries hash to the same index, the most recently inserted entry is shifted to the next available slot
- **Rehashing on Removal**: When an entry is removed, subsequent entries in the probe chain are rehashed to maintain integrity

**Example from Test Output:**
```
Inserted: ID=8, Name=Item A, Hash=8, Slot=8
Inserted: ID=19, Name=Item B, Hash=8, Slot=9  (probed 1 slot)
Inserted: ID=30, Name=Item C, Hash=8, Slot=10 (probed 2 slots)
```

### 2. Search Functionality

Three search methods are now available:

#### a) Search by ID
```python
result = hash_table.search_by_id(102)
```
- Searches for exact ID match
- Returns single `Record` or `None`
- Uses linear probing to find the record

#### b) Search by Name
```python
results = hash_table.search_by_name("Apple")
```
- Case-insensitive partial matching
- Returns list of all matching `Record` objects
- Example: Searching "Apple" finds "Apple iPhone", "Apple MacBook", "Apple Watch"

#### c) Search by Hash Number
```python
results = hash_table.search_by_hash(5)
```
- Finds all records that originally hashed to the given index
- Returns list of `Record` objects
- Includes records that may have been probed to different slots
- **Use case**: See all collisions for a specific hash value

**Example from Test Output:**
```
Records with original hash 5: Found 3 results
  - ID=5, Original Hash=5, Final Slot=5, Inserted At=1
  - ID=16, Original Hash=5, Final Slot=6, Inserted At=2  (probed)
  - ID=27, Original Hash=5, Final Slot=7, Inserted At=3  (probed)
```

### 3. Insertion Order Tracking

- Each record now has an `inserted_at` field
- Tracks the order of insertion with an auto-incrementing counter
- Helps determine which entry is "most recent" in collision scenarios
- Preserved across table resizing operations

### 4. Hashtable Size Monitoring

- **Method**: `get_hashtable_size()` returns number of occupied slots
- **UI Display**: Shows size, capacity, and load factor
- **Format**: "Hashtable Size: 3/11 (Load: 27.27%)"

### 5. Enhanced Data Model

The `Record` dataclass now includes:

```python
@dataclass
class Record:
    mode: str                      # "Product" or "Item"
    id: int                        # Unique identifier
    name: str                      # Display name
    price: Optional[float]         # For Product mode
    description: Optional[str]     # For Item mode
    key: Optional[int]             # Internal use (hidden from UI)
    hash_index: Optional[int]      # Final slot index after probing
    inserted_at: Optional[int]     # Insertion order
```

## UI Changes (Maintaining Layout)

The following changes were made to integrate the new features **without altering the UI layout or styling**:

### Table Columns Updated
- **Before**: Mode, ID, Name, Price/Desc, Key, Hash
- **After**: Mode, ID, Name, Price/Desc, Slot Index, Inserted At

Changes:
- Removed: "Key" column (now hidden)
- Removed: "Hash" column 
- Added: "Slot Index" (final position after probing)
- Added: "Inserted At" (insertion order)

### Search Bar Enhanced
- Added dropdown to select search type: **ID**, **Name**, or **Hash Number**
- Added dedicated "Search" button
- Search box supports Enter key to trigger search
- Clear button to reset search

### Size Display
- New label showing hashtable statistics above the form
- Format: "Hashtable Size: N/Capacity (Load: X.XX%)"
- Updates automatically after insert/remove operations

## Technical Implementation Details

### Hash Function
```python
def _hash(self, k: int) -> int:
    return k % self._capacity
```

### Linear Probing Algorithm
```python
def _find_slot(self, key: int, for_insertion: bool = False):
    initial_idx = self._hash(key)
    idx = initial_idx
    probes = 0
    
    while probes < self._capacity:
        current_record = self._buckets[idx]
        
        if current_record is None:
            return idx if for_insertion else None
        
        if current_record.id == key:
            return idx
        
        # Collision: probe forward
        idx = (idx + 1) % self._capacity
        probes += 1
    
    return None
```

### Collision Example

**Scenario**: Table capacity = 11

| Step | Action | ID | Hash | Slot | Notes |
|------|--------|----|----|------|-------|
| 1 | Insert | 8 | 8 | 8 | Direct placement |
| 2 | Insert | 19 | 8 | 9 | Collision! Probed to 9 |
| 3 | Insert | 30 | 8 | 10 | Collision! Probed to 10 |

### Dynamic Resizing

- Triggers when load factor exceeds 0.75 (75%)
- Resizes to next prime number ≈ 2× current capacity
- All records are rehashed with preserved `inserted_at` values
- Example: 11 → 23 → 47 → 97 → 197...

### Error Handling

**Full Table**: When the table reaches capacity and cannot resize:
```python
raise RuntimeError("Hash table is full - cannot insert")
```

**Invalid Input**: Clear error messages for:
- Non-numeric ID in search
- Non-numeric hash number in search
- Empty required fields

## Files Modified/Created

1. **hash_table.py** ✅ 
   - Refactored from separate chaining to linear probing
   - Added search methods
   - Added insertion tracking
   - Added size management

2. **ui_main.py** ✅
   - Added search UI controls (dropdown + button)
   - Updated table columns
   - Added size label display
   - Integrated search functionality
   - Maintained existing layout and styling

3. **storage_manager.py** ✅
   - Updated CSV export to include new fields
   - Maintained backward compatibility

4. **main.py** ✅
   - Minor update for resource path handling
   - No functional changes

## Testing

Run the comprehensive test suite:

```bash
python3 test_hashtable.py
```

### Test Coverage

1. ✅ Linear probing with collisions
2. ✅ Search by ID
3. ✅ Search by name (partial match)
4. ✅ Search by hash number
5. ✅ Insertion order tracking
6. ✅ Full table error handling
7. ✅ Removal and rehashing

All tests pass successfully with expected output.

## Usage Examples

### Example 1: Searching by Hash Number

```python
# Find all items that hash to index 5
results = hash_table.search_by_hash(5)
for rec in results:
    print(f"ID: {rec.id}, Name: {rec.name}, Slot: {rec.hash_index}")
```

**Output:**
```
ID: 5, Name: Item at hash 5, Slot: 5
ID: 16, Name: Item hash 16->5, Slot: 6  (probed)
ID: 27, Name: Item hash 27->5, Slot: 7  (probed)
```

### Example 2: Name Search

```python
# Search for all Apple products
results = hash_table.search_by_name("Apple")
# Returns: Apple iPhone, Apple MacBook, Apple Watch
```

### Example 3: Monitoring Size

```python
size = hash_table.get_hashtable_size()  # Number of occupied slots
capacity = hash_table.capacity          # Total capacity
load = hash_table.load_factor           # size/capacity
```

## Edge Cases Handled

1. **Table Full**: Clear error message when insertion fails
2. **Wraparound**: Probing wraps from end to beginning
3. **Removal Rehashing**: Maintains probe chain integrity
4. **Empty Search**: Shows all records when search is cleared
5. **No Results**: Informative message when search finds nothing
6. **Import Errors**: Graceful handling of import failures when table is full

## Performance Characteristics

- **Best Case Insert**: O(1) - no collision
- **Worst Case Insert**: O(n) - all slots must be probed
- **Average Case Insert**: O(1/(1-α)) where α is load factor
- **Search**: Same as insert (uses linear probing)
- **Space Complexity**: O(n) where n is capacity

## Comparison: Before vs After

| Feature | Before (Separate Chaining) | After (Linear Probing) |
|---------|---------------------------|------------------------|
| Collision Resolution | Linked lists in buckets | Linear probing forward |
| Space Overhead | Higher (pointers) | Lower (contiguous array) |
| Cache Performance | Poor (scattered) | Better (sequential) |
| Search by Hash | Not available | ✅ Available |
| Insertion Tracking | Not available | ✅ Available |
| Size Monitoring | Basic | ✅ Enhanced |

## Requirements Met

✅ Search by ID, Name, or Hash Number  
✅ Linear probing collision resolution  
✅ Most recent duplicate shifts forward  
✅ Hide Key field from UI  
✅ Display hashtable size  
✅ Show ID and Name in lookups  
✅ Insertion order tracking  
✅ Slot index display  
✅ No UI layout changes  
✅ No stylesheet modifications  
✅ Error handling for full table  
✅ Wraparound probing  
✅ Deterministic tie-breaking (insertion order)  

## Notes

- The `key` field is maintained internally but **hidden from UI**
- All original UI styling and layout preserved
- Backward compatible with existing CSV files
- Autosave format updated to support new fields
- Dynamic resizing ensures table rarely fills up
