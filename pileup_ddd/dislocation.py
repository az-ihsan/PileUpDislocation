import attr 
from numpy import sqrt, linalg
from numpy import random
from numpy import pi, deg2rad

@attr.s
class SlipPlanes(object):
    id = attr.ib()
    x = attr.ib()
    y = attr.ib()
    angle = attr.ib(converter=lambda angle:deg2rad(angle))
    length = attr.ib()
    dislocation_id = attr.ib(factory=list)

@attr.s
class Dislocation(object):
    id = attr.ib() 
    x_loc = attr.ib()
    fx = attr.ib()
    b = attr.ib()
    sp_id = attr.ib()
    f_ext = attr.ib()

    def computeForce(self, cls, slip_system, D, stress_0):
        #accessing slip plane 
        sp_self = slip_system[self.sp_id]
        sp_cls = slip_system[cls.sp_id]
        dx = self.x_loc - cls.x_loc
        dy = sp_self.y - sp_cls.y
        ssq = dx**2 + dy**2
        dist = sqrt(ssq)
        ffx = stress_0 *self.b * cls.b * dx * (dx**2 - dy**2)/ssq**2
        self.fx = self.fx + ffx

        # add -f to sum of force on another dislocation
        cls.fx = cls.fx - ffx

    def imgForcePileUp(self, slip_system, stress_0):
        d = self.x_loc
        x = self.x_loc
        y = slip_system[self.sp_id].y
        first_term = (x + d) * ((x+d)**2 - y**2) / ((x+d)**2 + y**2)**2
#         second_term = (x - d) * ((x-d)**2 - y**2) / ((x-d)**2 + y**2)**2
        third_term = 2*d*((x-d)*(x+d)**3 - 6*x*(x+d)*y**2 + y**4) / ((x+d)**2 + y**2)**3
        stress_yx = stress_0*self.b*(first_term + third_term)
        ffx = self.b*stress_yx
        self.fx = self.fx + ffx

    def imgStressPileup(self, slip_system, stress_0, x):
        d = self.x_loc
        y = slip_system[self.sp_id].y
        first_term = (x + d) * ((x+d)**2 - y**2) / ((x+d)**2 + y**2)**2
        second_term = (x - d) * ((x-d)**2 - y**2) / ((x-d)**2 + y**2)**2
        third_term = 2*d*((x-d)*(x+d)**3 - 6*x*(x+d)*y**2 + y**4) / ((x+d)**2 + y**2)**3
        stress_yx = stress_0*self.b*(first_term  - second_term + third_term)

        
    def moveDislocation(self, D, B, dt):
        self.fx = self.fx + self.f_ext* self.b
        delta_x = (self.fx/B) * dt
        self.x_loc= self.x_loc + delta_x
        if self.x_loc > D: 
            self.x_loc = self.x_loc - D
        elif self.x_loc < 0:
            self.x_loc = self.x_loc + D 
            
  

    