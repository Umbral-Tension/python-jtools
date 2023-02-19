import math
import itertools

class JPrime():

    def __init__(self):
        self.primes = [2, 3]
        self._multiples = {}
        self._greatest_checked_val = 3
        
    def isprime(self, num):
        if self._trivial_nonprime(num):
            return False
        self._extend_primes(num)
        return num in self.primes

    def get_prime_range(self, upperbound, lowerbound = 2):
        self._extend_primes(upperbound)
        selection_iterator = itertools.filterfalse(lambda x: x < lowerbound or x > upperbound, self.primes)
        return list(selection_iterator)

    def clear_primes(self):
        self.primes = [2, 3]
        self._multiples = {}

    def _trivial_nonprime(self, num):
        return num != 2 and (num % 2 == 0 or num < 2)

    def _extend_primes(self, num):
        if self._greatest_checked_val < num:
            extension = list(range(self._greatest_checked_val + 2, num + 1, 2))
            extension = self._sieve(extension)
            self.primes.extend(extension)

    def _sieve(self, num_range):
        """Erotasthenes' Sieve

        A minimum "base" is selected. The multiples of that base are calculated and removed from the numberlist.
        The base is incremented and the process repeats. The remaining values in numberlist are primes."""
        # Note:
        #   Erotasthenes' sieve for the range 0-X only requires checking multiples of numbers less than sqrt(X), so
        #   base is only incremented up to sqrt(x).
        #
        #   An updateable sieve w/ no need to store a full list of checked multiples was desired. For this, the
        #   dictionary _multiples is used. Only as many as sqrt(biggest_num_to_check) kv pairs are ever stored there.
        #   In _multiples the keys represent bases. The values represent the largest multiple
        #   of that base that has been calculated and crossed-off to date. For any K, the multiplier which produced its
        #   current V is obtained like: m = K/V. From there, this sieve can pick up where the last sieve left off by
        #   incrementing m and crossing off (m*K) until that product exceeds the biggest number in num_range.
        #
        #   Any multiple of an even will be even (not prime). Thus: base += 2 to avoid checking them.
        greatest_num = max(num_range)
        root = math.ceil(math.sqrt(greatest_num))
        for base in range(3, root+1, 2):
            if base not in self._multiples.keys():
                self._multiples[base] = base

            m = (self._multiples[base] / base) + 2
            while True:
                result = base * m
                if result > greatest_num:
                    break
                try:
                    num_range.remove(result)
                except ValueError:
                    pass
                m += 2
            self._multiples[base] = base * (m - 2)
        return num_range

