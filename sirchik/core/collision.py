import pygame

class Collision:
    @staticmethod
    def aabb(x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 < x2+w2 and x1+w1 > x2 and y1 < y2+h2 and y1+h1 > y2
    
    @staticmethod
    def circle(x1, y1, r1, x2, y2, r2):
        dx, dy = x1-x2, y1-y2
        return (dx*dx + dy*dy)**0.5 < r1+r2
    
    @staticmethod
    def point_in_rect(px, py, x, y, w, h):
        return x <= px <= x+w and y <= py <= y+h
    
    @staticmethod
    def resolve_aabb(x, y, w, h, vx, vy, bx, by, bw, bh):
        new_x, new_y = x, y
        new_vx, new_vy = vx, vy
        
        if vx > 0 and x+w > bx and x < bx:
            new_x = bx - w
            new_vx = 0
        elif vx < 0 and x < bx+bw and x+w > bx+bw:
            new_x = bx + bw
            new_vx = 0
        
        if vy > 0 and y+h > by and y < by:
            new_y = by - h
            new_vy = 0
        elif vy < 0 and y < by+bh and y+h > by+bh:
            new_y = by + bh
            new_vy = 0
        
        return new_x, new_y, new_vx, new_vy
    
    @staticmethod
    def check_and_resolve(x, y, w, h, vx, vy, blocks):
        new_x, new_y = x, y
        new_vx, new_vy = vx, vy
        
        for block in blocks:
            if isinstance(block, pygame.Rect):
                bx, by, bw, bh = block.x, block.y, block.w, block.h
            else:
                bx, by, bw, bh = block[0], block[1], block[2], block[3]
            
            if Collision.aabb(new_x, new_y, w, h, bx, by, bw, bh):
                new_x, new_y, new_vx, new_vy = Collision.resolve_aabb(
                    new_x, new_y, w, h, new_vx, new_vy, bx, by, bw, bh)
        
        return new_x, new_y, new_vx, new_vy