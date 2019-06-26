# MICROSOFT DRM CURVE VALUES
_p = 785963102379428822376694789446897396207498568951
_a = 317689081251325503476317476413827693272746955927
_b = 79052896607878758718120572025718535432100651934
_x = 771507216262649826170648268565579889907769254176
_y = 390157510246556628525279459266514995562533196655

import random

def ext_euclid(a, b):                # Extended Euclid algorithm function for finding modular inverses
    if not b:
        return (a, 1, 0)
    d1, x1, y1 = ext_euclid(b, a%b)
    return (d1, y1, x1-(a//b)*y1)

class elcurve:                       # Modular elliptic curve object class
    def __init__(self, p, a, b):
        self.p = p                              ### Prime modulo
        self.a = a                              ### Curve coefficients
        self.b = b
        self.gen = None
    
    def inv(self, n):                           ### To find modular inverse in the context of the curve
        return (ext_euclid(n, self.p)[1])%self.p
    
    ##### TODO: Generator finder
    
    def pchk(self, point):                      ### To check whether a point belongs to the curve
        if point == (-1, -1):
            return True
        x, y = point
        if not ((y*y)%self.p-(x*x+self.a)%self.p*x-self.b)%self.p:
            return True
        return False
    
    def padd(self, point1, point2):             ### To add two points on the curve
        x1, y1 = point1
        x2, y2 = point2
        if x1 == x2:
            return (-1, -1)
        elif x1 < 0:
            return p2
        elif x2 < 0:
            return p1
        g = ((y2-y1)*self.inv((x2-x1)%self.p))%self.p
        x3 = ((g*g)%self.p-x1-x2)%self.p
        y3 = (g*(x1-x3)-y1)%self.p
        return (x3, y3)
    
    def pdbl(self, point):                      ### To double a point on the curve
        x1, y1 = point
        if x1 < 0 or y1 == 0:
            return (-1, -1)
        g = (((3*x1*x1)%self.p+self.a)%self.p*self.inv((2*y1)%self.p))%self.p
        x2 = ((g*g)%self.p-2*x1)%self.p
        y2 = ((g*(x1-x2))%self.p-y1)%self.p
        return (x2, y2)
    
    def pscmul(self, n, point):                 ### To multiply point by a constant
        if n:
            res = point
            exp = []
            f = 1
            while f <= n:
                exp.append(bool(f&n))
                f <<= 1
            exp.reverse()
            for f in exp[1:]:
                res = self.pdbl(res)
                if f:
                    res = self.padd(res, point)
            return res
        else:
            return (-1, -1)
    
    def keygen(self, dot = None, point = None): ### To generate key points
        if not point:
            point = self.gen
        if not dot:
            dot = random.randint(3, self.p-1)
        return self.pscmul(dot, point)
            

# MICROSOFT DRM CURVE AND GENERATOR
_mdrmc = elcurve(_p, _a, _b)
_mdrmg = (_x, _y)
