#Christian Trivette, Student ID: 001307104

class chainingHashTable:
    def __init__(self):
        self.table = [[]]

    def insertPackage(self, item):
        # get the bucket list where this item will be placed -> time complexity = O(1)
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

        # insert the package into the bucket list
        bucket_list.append(item)

    # method to search for a package using the packageID
    def search(self, key):
        # get the bucket list and see where this package should be at -> time complexity = O(1)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            return bucket_list[bucket_list.index(key)]

    # method to remove a package from the hash table
    def remove(self, key):
        # get the bucket list and see where this package should be at -> time complexity = O(1)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)