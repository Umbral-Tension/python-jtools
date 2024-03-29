import math
import itertools

class JPrime():
    """
    Class that stores a list of primes and extends it using Erotasthenes' Sieve.
    """

    def __init__(self):
        self.primes = [2, 3]
        self._multiples = {}
        self._greatest_checked_val = 3
        
    def clear_primes(self):
        self.primes = [2, 3]
        self._multiples = {}
        self._greatest_checked_val = 3

    def isprime(self, num):
        # trivial non-prime check
        if num != 2 and (num % 2 == 0 or num < 2):
            return False
        self._extend_primes(num)
        return num in self.primes

    def get_prime_range(self, upperbound, lowerbound = 2):
        """return a list of all primes from lowerbound to upperbound, inclusive."""
        self._extend_primes(upperbound)
        return list(itertools.filterfalse(lambda x: x < lowerbound or x > upperbound, self.primes))
        

    def _extend_primes(self, upperbound):
        """extend the class object's list of primes by doing a sieve on the values that haven't been checked previously."""
        if self._greatest_checked_val < upperbound - 1:
            extension = list(range(self._greatest_checked_val + 2, upperbound + 1, 2))
            extension = self._sieve(extension)
            self.primes.extend(extension)
            self.primes = list(set(self.primes)) # remove duplicates. Have not yet figured out a way to stop them from being produced in the first place.

    def _sieve(self, num_range):
        """Erotasthenes' Sieve

        A "base" is selected. The multiples of that base are calculated and removed from num_range.
        The base is incremented and the process repeats. The remaining values in num_range are primes.
        
        @param num_range: ordered list of all odd integers in some arbitary range. 
        
        Notes:
            Erotasthenes' sieve for the range 0-x only requires checking multiples of numbers less than sqrt(x), so
            base is only incremented up to sqrt(x).

            An updateable sieve with no need to store a full list of checked multiples was desired. For this, the
            dictionary _multiples is used. The keys of _multiples represent bases. The values represent the largest multiple
            of that base that has been calculated and crossed-off to date. Only as many as sqrt(biggest_range_ever_checked) KV pairs 
            have to be stored in _multiples.

            For any K, the multiplier which produced its current V is obtained like: m = K/V. From there, this sieve can pick up where
            the last sieve left off by incrementing m and crossing off (m*K) until that product exceeds the biggest number in num_range.

            Any multiple of an even will be even (not prime). Thus: base += 2 to avoid checking them.
        """
        range_max = num_range[-1]
        root = math.ceil(math.sqrt(range_max))
        for base in range(3, root+1, 2):
            if base not in self._multiples.keys():
                # multiplying by (base-2) ensures that the first m for a new base is base. So that you don't get redunant checks like base=5, m=3. That was already checked when base=m, m=5
                self._multiples[base] = base*(base-2) 

            m = int((self._multiples[base] / base)) + 2
            while True:
                multiple = base * m
                if multiple > range_max:
                    break
                if multiple > self._greatest_checked_val:
                    self._greatest_checked_val = multiple 
                try:
                    num_range.remove(multiple)
                except ValueError:
                    pass
                m += 2
            self._multiples[base] = base * (m - 2)
        return num_range



if __name__ == '__main__':
    from time import time

    upperbounds = [100, 1000, 10000, 30000, 50000, 100000, 500000]
    
    
    for upperbound in upperbounds:
        print('=====================')
        print(f'Time comparison for getting primes in range 2-{upperbound}')
        p1 = JPrime()
        p2 = JPrime()


        # direct approach
        start = time()
        p2.get_prime_range(upperbound)
        direct_time = time() - start
        print('directly:\n\t', direct_time)

        #incremental approach
        increments = int(math.ceil(.0005 * upperbound))
        start = time()
        for x in range(1, increments+1):
            p1.get_prime_range(upperbound//increments*x)
        incremental_time = time() - start
        print(f'in increments({increments}):\n\t{incremental_time}')


        print('ratio direct/incremental:', direct_time/incremental_time)
        print('=====================\n\n')