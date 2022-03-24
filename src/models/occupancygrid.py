import pygame
from src.resource_manager import ResourceManager

import os, csv

from math import *

# OccupancyManager: wraps two occupancy grids
class OccupancyManager():
    def __init__(self, nx, ny, level_file_good, level_file_evil, offset_good=(0,0), offset_evil=(400,0)):
        self.occ_good = OccupancyGrid('good', nx, ny, level_file_good, offset=offset_good, tilesize=32)
        self.occ_evil = OccupancyGrid('evil', nx, ny, level_file_evil, offset=offset_evil, tilesize=32)
    
    def HandleCollision(self, twin, x, y, dx, dy):
        if twin == 'good':
            (xnew, ynew) = self.occ_good.HandleCollision(x, y, dx, dy)
        elif twin == 'evil':
            (xnew, ynew) = self.occ_evil.HandleCollision(x, y, dx, dy)
        return (xnew, ynew)
    
    def DrawTest(self, screen):
        self.occ_good.DrawTest(screen)
        self.occ_evil.DrawTest(screen)

# OccupancyMap: implementation of occupancy grid
class OccupancyGrid():
    def __init__(self, type, nx, ny, level_file, offset=(0,0), tilesize=32):
        self.nx = nx
        self.ny = ny
        self.offset = offset
        self.tilesize = tilesize
        
        # Initialise occupancy
        self.occ = []
        for iy in range(self.ny):
            self.occ.append([])
            for ix in range(self.nx):
                self.occ[-1].append(False)
        
        self.set_occupancy(level_file)
        
        """
        self.occ[5][5] = True
        self.occ[6][5] = True
        if type == 'good':
            self.occ[6][6] = True
            self.occ[6][7] = True
            
            self.occ[8][8] = True
            self.occ[11][9] = True
            self.occ[12][9] = True
            self.occ[8][9] = True
            self.occ[10][9] = True
            self.occ[8][10] = True
            self.occ[10][10] = True
            
            self.occ[8][7] = True
            self.occ[9][7] = True
            self.occ[10][7] = True
            self.occ[11][7] = True
        """
    
    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                map.append(list(row))
        return map

    def set_occupancy(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if not tile == "-1":
                    self.occ[y][x] = True
                x += 1
            y += 1
    
    # GetTileIndex: return (column,row) of tile for a point
    def GetTileIndex(self, x, y):
        ix = int(x/self.tilesize)
        iy = int(y/self.tilesize)
        
        return (ix, iy)
    
    # CheckCollisionTileIndex:
    # return true if target tile index is on an occupied tile, false otherwise
    def CheckCollisionTileIndex(self, ind):
        (ix, iy) = ind
        if self.occ[iy][ix] == True:
            return True
        else:
            return False
    
    # HandleCollision: handles how to constrain an object trying to move from (x,y)
    # to (x+dx,y+dy) in occupancy map. Returns constrained (x, y)
    def HandleCollision(self, x, y, dx, dy):
        
        psize = 30 # player hitbox size
        
        x = x-self.offset[0]
        y = y-self.offset[1]
        
        # first fix any hitting game extents
        xlim = 32*12
        ylim = 32*18
        if x >= xlim - 16 - 1:
            x = xlim - 16 - 1
        if x <= 16 + 1:
            x = 16 + 1
        if y <= 16 + 1:
            y = 16 + 1
        if y >= ylim - 16 - 1:
            y = ylim - 16 - 1
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
        elif dx < 0 and dy == 0:
            if self.CheckCollisionTileIndex(ul_ind) or self.CheckCollisionTileIndex(ll_ind) or self.CheckCollisionTileIndex(l_ind):
                newx = self.tilesize*ul_ind[0] + 1 + int(psize/2) + self.tilesize
        elif dx == 0 and dy > 0:
            if self.CheckCollisionTileIndex(lr_ind) or self.CheckCollisionTileIndex(ll_ind) or self.CheckCollisionTileIndex(d_ind):
                newy = self.tilesize*ll_ind[1] - 1 - int(psize/2)
        elif dx == 0 and dy < 0:
            if self.CheckCollisionTileIndex(ul_ind) or self.CheckCollisionTileIndex(ur_ind) or self.CheckCollisionTileIndex(u_ind):
                newy = self.tilesize*ul_ind[1] + 1 + int(psize/2) + self.tilesize
        elif dx > 0 and dy < 0: # handle corner cases (it's real ugly :) .... )
            xref = self.tilesize*ur_ind[0] - 1 - int(psize/2)
            yref = self.tilesize*ur_ind[1] + 1 + int(psize/2) + self.tilesize
            if self.CheckCollisionTileIndex(ul_ind) and self.CheckCollisionTileIndex(lr_ind):
                newx = xref
                newy = yref
            elif self.CheckCollisionTileIndex(ul_ind):
                newy = yref
            elif self.CheckCollisionTileIndex(lr_ind):
                newx = xref
            elif self.CheckCollisionTileIndex(ur_ind):
                ind1 = (ur_ind[0],ur_ind[1]+1)
                if fabs(newx-xref) < fabs(newy-yref) or self.CheckCollisionTileIndex(ind1):
                    newx = xref
                else:
                    newy = yref
        elif dx > 0 and dy > 0:
            xref = self.tilesize*lr_ind[0] - 1 - int(psize/2)
            yref = self.tilesize*lr_ind[1] - 1 - int(psize/2)
            if self.CheckCollisionTileIndex(ll_ind) and self.CheckCollisionTileIndex(ur_ind):
                newx = xref
                newy = yref
            elif self.CheckCollisionTileIndex(ll_ind):
                newy = yref
            elif self.CheckCollisionTileIndex(ur_ind):
                newx = xref
            elif self.CheckCollisionTileIndex(lr_ind):
                ind1 = (lr_ind[0],lr_ind[1]-1)
                if fabs(newx-xref) < fabs(newy-yref) or self.CheckCollisionTileIndex(ind1):
                    newx = xref
                else:
                    newy = yref
        elif dx < 0 and dy > 0:
            xref = self.tilesize*ll_ind[0] + 1 + int(psize/2) + self.tilesize
            yref = self.tilesize*ll_ind[1] - 1 - int(psize/2)
            if self.CheckCollisionTileIndex(ul_ind) and self.CheckCollisionTileIndex(lr_ind):
                newx = xref
                newy = yref
            elif self.CheckCollisionTileIndex(lr_ind):
                newy = yref
            elif self.CheckCollisionTileIndex(ul_ind):
                newx = xref
            elif self.CheckCollisionTileIndex(ll_ind):
                ind1 = (ll_ind[0],ll_ind[1]-1)
                if fabs(newx-xref) < fabs(newy-yref) or self.CheckCollisionTileIndex(ind1):
                    newx = xref
                else:
                    newy = yref
        elif dx < 0 and dy < 0:
            xref = self.tilesize*ul_ind[0] + 1 + int(psize/2) + self.tilesize
            yref = self.tilesize*ul_ind[1] + 1 + int(psize/2) + self.tilesize
            if self.CheckCollisionTileIndex(ur_ind) and self.CheckCollisionTileIndex(ll_ind):
                newx = xref
                newy = yref
            elif self.CheckCollisionTileIndex(ur_ind):
                newy = yref
            elif self.CheckCollisionTileIndex(ll_ind):
                newx = xref
            elif self.CheckCollisionTileIndex(ul_ind):
                ind1 = (ul_ind[0],ul_ind[1]+1)
                if fabs(newx-xref) < fabs(newy-yref) or self.CheckCollisionTileIndex(ind1):
                    newx = xref
                else:
                    newy = yref        
        
        return (newx+self.offset[0], newy+self.offset[1])
    
    # DrawTest: just draws mock-up of occupancy using pygame.draw.rect
    def DrawTest(self, screen):
        for iy in range(self.ny):
            for ix in range(self.nx):
                pos = (self.tilesize*ix+self.offset[0],self.tilesize*iy+self.offset[1],self.tilesize,self.tilesize)
                if self.occ[iy][ix] == True:
                    pygame.draw.rect(screen,(255,0,0),pos)
                    
    
    