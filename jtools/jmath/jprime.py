import math
import itertools

class JPrime():

    def __init__(self):
        self.primes = [2, 3]
        self._multiples = {}
        self.curr_max_prime = 3
        self._greatest_checked_value = 3

    def isprime(self, num):
        if self._trivial_nonprime(num):
            return False
        self._extend_list(num)
        return num in self.primes

    def _trivial_nonprime(self, num):
        return num != 2 and (num % 2 == 0 or num < 2)

    def _extend_list(self, num):
        if self._greatest_checked_value < num:
            extension = list(range(self._greatest_checked_value + 2, num + 1, 2))
            extension = self._sieve(extension)
            self.primes.extend(extension)

    def _sieve(self, numberlist):
        """Erotasthenes' Sieve

        A minimum "base" is selected. The multiples of that base are calculated and removed from the numberlist.
        The base is incremented and the process repeats. The remaining values in numberlist are primes."""
        # Note:
        #   Erotasthenes' sieve for the range 0-X only requires checking multiples of numbers less than sqrt(X), so
        #   base is only incremented up to sqrt(x).
        # Note:
        #   An updateable sieve w/ no need to store the FULL list of multiples was desired. For this, _multiples is
        #   used. _multiples is a dictionary wherein the keys represent bases. The values represent the largest multiple
        #   of that base that has been calculated and crossed-off to date. For any K, the multiplier which produced its
        #   current V is obtained like: m = K/V. From there, this sieve can pick up where the last sieve left off by
        #   incrementing m and crossing off (m*K) until that product exceeds the biggest number in numberlist.
        # Note:
        #   Any multiple of an even will be even. Thus: base += 2 to avoid checking them.
        greatest_num = max(numberlist)
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
                    numberlist.remove(result)
                except ValueError:
                    pass
                m += 2
            self._multiples[base] = base * (m - 2)
        return numberlist

    def get_prime_range(self, upperbound, lowerbound = 2):
        self._extend_list(upperbound)
        return [item for item in itertools.filterfalse(lambda x: x < lowerbound or x > upperbound, self.primes)]














