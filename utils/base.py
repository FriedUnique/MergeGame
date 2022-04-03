import math

class Vector2:    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x + other.x, self.y + self.y)
        return Vector2(self.x + other, self.y + other)
    
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x - other.x, self.y - self.y)
        return Vector2(self.x - other, self.y - other)
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x * other.x, self.y * self.y)
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x / other.x, self.y / self.y)
        return Vector2(self.x / other, self.y / other)

    def switch(self):
        x = self.x
        self.x = self.y
        self.y = x

    

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.x == other.y
        return self.x == other, self.y == other

    def __neg__(self):
        return -self.x, -self.y

    def __str__(self): # returns a value when this class is printed
        return f"(x: {self.x}, y: {self.y})"
    def __repr__(self):
        return f"Vector2(x: {self.x}, y: {self.y})"



    def Dot(vec1, vec2):
        return vec1.x * vec2.x + vec1.y * vec2.y

    def sqrLenght(vec):
        return vec.x**2 + vec.y**2

    def sqrDist(vec1, vec2):
        v = vec1 - vec2
        return v.x**2 + v.y**2

    def lenght(vec):
        return math.sqrt(vec.x**2 + vec.y**2)

    def distance(vec1, vec2):
        v = vec1 - vec2
        return math.sqrt(v.x**2 + v.y**2)

    def normalize(vec):
        vecLen = Vector2.lenght(vec)
        return Vector2(vec.x/vecLen, vec.y/vecLen)

    def negative(vec):
        return Vector2(-vec.x, -vec.y)

    def right(vec):
        return Vector2(-vec.y, vec.x)

    def angle_between_vec(vec1, vec2):
        return math.acos(Vector2.Dot(vec1, vec2))

def roundTupleValues(t: tuple):
    ts = list(t)
    for i in range(len(ts)):
        ts[i] = round(ts[i])

    return tuple(ts)

#! unused
def inputEval(s: str, d: dict):
    # inputEval(input(f"Select difficulty {tuple(levels.keys())}: "), levels)
    # "blue": Colors("blue", (93, 216, 228), (84, 194, 205), (233, 163, 49), (17, 24, 47))
    s = s.lower()
    lKeys = list(d.keys())

    if s.strip(" ") == "":
        print(f"No input! Using default: {lKeys[0]}")
        return lKeys[0]

    if s in lKeys:
        return s

    print(f"Bad input! Using default: {lKeys[0]}")
    return lKeys[0]