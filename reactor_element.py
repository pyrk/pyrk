#/usr/bin/env python
    

class ReactorElement:
    def __init__(self, position):
        self._posiiton=position
        
    def add_element(self, m, material, overwrite=True):
        for i, mat, ve in m:
            coord = m.mesh.getVtxCoords(ve)
            if self.in_element(coord):
                if overwrite == True or m.mats[i] == None :
                    m.mats[i] = material 

    def in_element(self, coord):
        raise NotImplementedError


class Sphere(ReactorElement):
    def __init__(self, radius, position):
        self._radius = radius
        self._position = position

    def in_element(self, coord):
        return self.in_sphere(coord, self._radius, self._position)
    
    def in_sphere(self, coord, radius, position):
        x0, y0, z0 = position
        rsq = (coord[0]-x0)**2 + (coord[1]-y0)**2 + (coord[2]-z0)**2
        if (rsq <= radius**2):
            return True
        else:
            return False


class Cylinder(ReactorElement):
    def __init__(self, radius, height, position):
        self._radius = radius
        self._height = height
        self._position = position

    def in_element(self, coord):
        return self.in_cylinder(coord, self._radius, self._height, self._position)
     
    def in_cylinder(self, coord, radius, height, position):
        x0, y0, z0 = position
        z_max = height/2. + z0
        z_min = height/2. - z0
        rsq = (coord[0]-x0)**2 + (coord[1]-y0)**2
        if (rsq <= radius**2 and z_min <= z <= z_max):
            return True
        else:
            return False


class Cone(ReactorElement):
    def __init__(self, r_top, r_bot, height, position):
        self._r_top = r_top
        self._r_bot = r_bot
        self._height = height
        self._position = position

    def in_element(self, coord):
        x0, y0, z0 = self._position
        z_max = self._height/2. + z0
        z_min = self._height/2. - z0
        rsq = (coord[0]-x0)**2 + (coord[1]-y0)**2
        if rsq <= self.r(z)**2 :
            return True
        else : 
            return False

    def r(r_top, r_bot, height, position, z):
        x0, y0, z0 = position
        if r_top == r_bot:
            ret = r_top
        else :
            slope = height/(r_top-r_bot) 
            ret = slope*(z-z0-height/2.) 
        return ret

    def r(self, z):
        return r(self._r_top, 
            self._r_bot,
            self._height,
            self._position,
            z)





        


