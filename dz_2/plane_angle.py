import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __sub__(self, no):
        return Point(
            self.x - no.x,
            self.y - no.y,
            self.z - no.z
        )
    
    def dot(self, no):
        return self.x * no.x + self.y * no.y + self.z * no.z
    
    def cross(self, no):
        return Point(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )
    
    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(a, b, c, d):
    AB = b - a
    BC = c - b 
    CD = d - c
    
    X = AB.cross(BC)
    Y = BC.cross(CD) 

    dot_product = X.dot(Y)
    
    magnitudes = X.absolute() * Y.absolute()
    
    if magnitudes == 0:
        return 0.0
    
    cos_phi = dot_product / magnitudes
    
    cos_phi = max(-1.0, min(1.0, cos_phi))
    
    angle_rad = math.acos(cos_phi)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

if __name__ == '__main__':
    a = Point(1, 2, 3)
    b = Point(5, 5, 6)
    c = Point(7, 8, 9)
    d = Point(1, 11, 2)
    angle = plane_angle(a, b, c, d)
    print(f"{angle:.2f}")