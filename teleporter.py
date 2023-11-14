import sys
sys.setrecursionlimit(100000)
class Teleporter:
    _cache = {}
    _reg7 = 0

    def dec(self, v:int) -> int:
        return v - 1
    
    def add(self, v1:int, v2:int) -> int:
        return (v1+v2) % 32768
    
    def ackermann(self, reg0:int, reg1:int) -> int:
        key = (reg0, reg1)
        if key in self._cache:
            return self._cache[key]
        
        if key[0] == 0:
            out = self.add(reg1,1)
        elif key[1] == 0:
            out = self.ackermann(self.dec(reg0), self._reg7)
        else:
            out = self.ackermann(self.dec(reg0), self.ackermann(reg0, self.dec(reg1)))
        
        self._cache[key] = out
        return out
    
    def solve(self, verbose:bool=False) -> int:
        self._reg7 = 25700 # hack a short search 
        while (True):
            self._reg7 += 1
            if verbose:
                print(f"Trying {self._reg7} ... ");
            self._cache.clear()

            result = self.ackermann(4,1)
            if result == 6:
                if verbose:
                    print(f"Ok!")
                return self._reg7
            
            if verbose:
                print("Nope...")
    
if __name__ == "__main__":
    t = Teleporter()
    result = t.solve()
    print(f"Result: {result}")