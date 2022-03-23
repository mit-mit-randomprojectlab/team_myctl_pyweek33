import pygame
from src.resource_manager import ResourceManager

# OccupancyMap: implementation of occupancy grid
class OccupancyGrid():
    def __init__(self, nx, ny, offset=(0,0), tilesize=32):
        self.nx = nx
        self.ny = ny
        self.offset = offset
        self.tilesize = tilesize
        
        # some test data for now, will load from level files ...
        self.occ = []
        for iy in range(self.ny):
            self.occ.append([])
            for ix in range(self.nx):
                self.occ[-1].append(False)
        
        self.occ[5][5] = True
        self.occ[6][5] = True
        self.occ[6][6] = True
        self.occ[6][7] = True
    
    # GetTileIndex: return (column,row) of tile for a point
    def GetTileIndex(self, x, y):
        ix = int((x-self.offset[0])/self.tilesize)
        iy = int((y-self.offset[1])/self.tilesize)
        return (ix, iy)
    
    # CheckCollisionPoint:
    # return true if target point (x,y) is on an occupied tile, false otherwise
    def CheckCollisionPoint(self, x, y):
        (ix, iy) = self.GetTileIndex(x, y)
        if self.occ[iy][ix] == True:
            return True
        else:
            return False
    
    def CheckCollisionTileIndex(self, ix, iy):
        if self.occ[iy][ix] == True:
            return True
        else:
            return False
    
    # HandleCollision: handles how to constrain an object trying to move from (x,y)
    # to (x+dx,y+dy) in occupancy map. Returns constrained (x, y)
    def HandleCollision(self, x, y, dx, dy):
        
        psize = 32 # player hitbox size
        
        newx = x
        newy = y
        
        # Work out collision points around (x,y)
        ul_ind = self.GetTileIndex(x-psize/2,y-psize/2) # corners
        ur_ind = self.GetTileIndex(x+psize/2,y-psize/2)
        ll_ind = self.GetTileIndex(x-psize/2,y+psize/2)
        lr_ind = self.GetTileIndex(x+psize/2,y+psize/2)
        
        u_ind = self.GetTileIndex(x,y-psize/2) # cardinal points
        d_ind = self.GetTileIndex(x,y+psize/2)
        l_ind = self.GetTileIndex(x-psize/2,y)
        r_ind = self.GetTileIndex(x+psize/2,y)
        
        # handle different cases:
        # first four: lateral/longitudinal collisions
        # next four: corner cases
        if dx > 0 and dy == 0: 
            if self.CheckCollisionTileIndex(ur_ind) or self.CheckCollisionTileIndex(lr_ind) or self.CheckCollisionTileIndex(r_ind):
                newx = self.tilesize*ur_ind[0] - 1 - int(psize/2)
        elif vx < 0 and vy == 0:
            if self.CheckCollisionTileIndex(ul_ind) or self.CheckCollisionTileIndex(ll_ind) or self.CheckCollisionTileIndex(l_ind):
                newx = self.tilesize*ul_ind[0] + 1 + int(psize/2) + self.tilesize
        elif vx == 0 and vy > 0:
            if self.CheckCollisionTileIndex(lr_ind) or self.CheckCollisionTileIndex(ll_ind) or self.CheckCollisionTileIndex(d_ind):
                newy = self.tilesize*ll_ind[1] - 1 - int(psize/2)
        elif vx == 0 and vy < 0:
            if self.CheckCollisionTileIndex(ul_ind) or self.CheckCollisionTileIndex(ur_ind) or self.CheckCollisionTileIndex(u_ind):
                newy = self.tilesize*ul_ind[1] + 1 + int(psize/2) + self.tilesize
        
        return (newx, newy)
    
    # DrawTest: just draws mock-up of occupancy using pygame.draw.rect
    def DrawTest(self, screen):
        for iy in range(self.ny):
            for ix in range(self.nx):
                pos = (self.tilesize*ix+self.offset[0],self.tilesize*iy+self.offset[1],self.tilesize,self.tilesize)
                if self.occ[iy][ix] == True:
                    pygame.draw.rect(screen,(255,255,255),pos)
                else:
                    pygame.draw.rect(screen,(0,0,0),pos)
    
    