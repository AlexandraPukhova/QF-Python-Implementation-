import mmh3

class Cell:
    
    def __init__(self, occupied=0, continuation=0, shifted=0, value = None):
        self.value = value
        self.is_occupied = occupied # pertains to the slot occupacy, not the remainder contained in the slot, so it does not get affected as we shift a slot's remainder 
        self.is_continuation = continuation
        self.is_shifted = shifted

class QuotientFilter:
    
    # Initializing the table     
    def __init__(self, r, p, function):        
    
        self.num_hash_bits = p # p-bit fingerprints, will use 32-bit MMH3
        self.num_rbits = r
        self.num_qbits = p - r
        self.functions = function
        
        self.size = self.num_slots(self.num_qbits) # size of the array
        self.array = [Cell() for _ in range(self.size)] # create an array and populate it with cells of class Cell
        
    def num_slots(self, q):
        m = 2**(self.num_qbits)
        return int(m)
    
    def convertto_bits(self, n):
        return [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part 
    
    def get_index(self, key, function):
        hashed_key = abs(function.hash(str(key))) # convert key to str, because MMH3 only takes strings
        quotient = self.convertto_bits(hashed_key)
        int_quotient = int("".join(str(i) for i in (quotient)),2)
        return int_quotient%self.size
    
    def get_remainder(self, key, function):
        hashed_key = abs(function.hash(str(key)))
        remainder = self.convertto_bits(hashed_key)
        int_remainder = int("".join(str(i) for i in (remainder)),2)
        return int_remainder
    
    def is_slot_empty(self, key, function): # checks if the slot is empty
        index = self.get_index(key, function)
        if self.array[index].is_occupied == 0 and self.array[index].is_continuation == 0 and self.array[index].is_shifted == 0: 
            return True
    
    def findCluster(self, key, function): 
        index = self.get_index(key, function)
        # each cluster starts with 1 0 0, and all runs will have is_shifted = 1
        # the cluster is the only run that will have is_shifted = 0
        while self.array[index].is_shifted != 0:
            index -=1 # scan left
        return index # return the index where the cluster starts
    
    def findRun(self, key, function):
        start_of_cluster = self.findCluster(key, function) # index of the start of the cluster
        current_index = start_of_cluster # Scan right from the start of the cluster to find a run
        for index in range(start_of_cluster+1, self.get_index(key, function)):
            if self.array[current_index].is_continuation !=0:
                current_index += 1
        return current_index # the index of the start of the run 

    def next_run(self, new_index): # gives the index of the next run
        for index in range(new_index, self.size):
            if self.array[index].is_continuation != 0:
                index += 1
        return index
    
    def contains(self, key, function):
        if self.is_slot_empty(key, function): 
            return False, '%r is definitely not in the filter'%key
        
        # from the index to the beginning of the cluster, moving to the left, find the number of runs before the quotient's run
        runs_count = [] # get the number of the key's quotient's run, e.g. it is the third run in a cluster
        
        # if the key's quotient is the beginning of a cluster
        if self.get_index(key, function) == self.findCluster(key, function):
            runs_count = 1
        
        else:
            for index in range(self.get_index(key, function), self.findCluster(key, function), -1):
                if self.array[index].is_occupied == 1:
                    runs_count += 1
        
        # scan right to find the beginning of the quotient's run
        runs_passed = 0
        startof_quotient_run = -1 # set sentinel value
        for index in range(self.findCluster(key, function), self.size): # should stop as soon as runs_passed reaches runs_count
            if self.array[index].is_continuation == 0:
                runs_passed += 1
            if runs_passed == runs_count:
                startof_quotient_run = index # the index of the start of the quotient's run
        
        # check each value in the quotient's run, i.e. the run that starts with the index found in the previous for loop
        for index in range(startof_quotient_run, self.next_run(startof_quotient_run)-1):
            if self.array[index].value == self.array[self.get_index(key, function)].value:
                return True, '%r is probably in the filter'%key
    
    def insert(self, key, function):

        if self.contains(key, function)[0]:
            return '%r probably already exists in the filter.' %key

        index = self.get_index(key, function)

        if self.is_slot_empty(key, function):
            self.array[index].value = self.get_remainder(key, function)
            self.array[index].is_occupied = 1
            return
        
        elif self.array[index].is_occupied == 1:
            i = 1
            while self.array[index + i].is_occupied == 1: # get to the first unoccupied cell 
                i+=1
            # might have to account for when it reaches the end of table
            
            # Assuming the old key's remainder < the new key's remainder, so the new key's remainder is shifted into the next slot
            # to fix: account for when it is not, so that the values are stored in sorted order to enable merging later
            
            while i > 0:
                # shift the value that is in that slot
                self.array[index+i].value = self.array[index + i - 1].value
                self.array[index+i].is_occupied == 1
                
                # there might be a case when it does not become a continuation, did not account for this
                self.array[index+i].is_continuation == 1
                self.array[index+i].is_shifted == 1
                i -=1
                
            # push in the new value
            self.array[index].value = get_remainder(key, function)
            self.array[index].is_occupied == 1
            self.array[index].is_continuation == 1
            return
        
# More operations that QF can support:
# The following operations are also, theoretically, supported by QF.
     
#     def fp_prob()
#     # FP(False Positives) probability rate function that is is based on q, r and number of added keys

#     def remove(self, key):
#     # Lack of theoretical material regarding this operation
#     # Did not complete
    
#     def merge(qf1, qf2)
#     # Steps:
#     # 1. reconstruct all the fingerprints, the resulting list of integers will be in sorted order
#     # 2. convert both filers into such lists
#     # 3. merge two lists 
#     # 4. populate a larger QF with this list
