from collections import deque
import operator

maze = [
    ["*", "8", "-", "1"],
    ["4", "*", "11","*"],
    ["+", "4", "-", "18"],
    ["22", "-", "9", "*"]
]

class PathState:
    x:int=0
    y:int=0
    path:list=['22']
    steps:int=0
    dir:str=''

    def __init__(self, x, y, path, steps, dir) -> None:
        self.x = x
        self.y = y
        self.path = path
        self.steps = steps
        self.dir = dir

    def is_solved(self) -> bool:
        return self.x == 3 and self.y == 0 and self.calc() == 30
    
    def calc(self) -> int:
        result = int(self.path[0])
        for i in range(1,len(self.path),2):
            result = eval(f"{result}{self.path[i]}{self.path[i+1]}")
        return result
    
    def neighbors(self) -> list:
        dirs = {
            'N': (0,-1),
            'S': (0,1),
            'E': (1,0),
            'W': (-1,0)
        }
        out = []
        for d,v in dirs.items():
            nx = self.x + v[0]
            ny = self.y + v[1]
            if 0 <= nx < 4 and 0 <= ny < 4:
                out.append(PathState(nx, ny, self.path + [maze[ny][nx]], self.steps + 1, self.dir+d))
        return out
    
    def __repr__(self) -> str:
        return f"<PathState ({self.x, self.y}), {self.path}, {self.steps}, {self.dir}>"

def search():
    start = PathState(0,3,["22"], 0, "")
    seen = {}
    q = deque([start])
    while q:
        current = q.pop()
        if current.is_solved():
            return current
        if hash(current) in seen:
            continue
        elif current.x == 3 and current.y == 0: 
            continue
        elif current.steps >= 13:
            continue 
        seen[hash(current)] = current
        if current.x == 0 and current.y == 3 and current.steps != 0:
            continue
        for n in current.neighbors():
            q.append(n) 
        
if __name__ == "__main__":
    print(search())