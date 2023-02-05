import math
class Circle:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
    def collideRect(self,rect):
        """ Detect collision between a rectangle and circle. """
        rleft = rect.x
        rtop = rect.y
        width = rect.w
        height = rect.h

        center_x = round(self.x)
        center_y = round(self.y)
        radius = round(self.r)
        # complete boundbox of the rectangle
        rright, rbottom = rleft + width, rtop + height

        # bounding box of the circle
        cleft, ctop     = center_x-radius, center_y-radius
        cright, cbottom = center_x+radius, center_y+radius

        # trivial reject if bounding boxes do not intersect
        if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
            return False  # no collision possible

        # check whether any point of rectangle is inside circle's radius
        for x in (rleft, rleft+width):
            for y in (rtop, rtop+height):
                # compare distance between circle's center point and each point of
                # the rectangle with the circle's radius
                if math.hypot(x-center_x, y-center_y) <= radius:
                    return True  # collision detected

        # check if center of circle is inside rectangle
        if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
            return True  # overlaid
        
        eps = 5

        # checks for every pixel at the top of the rectangle, weather the pixel
        # (and any pixel within "eps" distance) is also part of the circumference
        y = rtop
        for x in range(rleft,rright+1):
            if ((x-center_x)**2 + (y-center_y)**2)-eps <= radius**2 and ((x-center_x)**2 + (y-center_y)**2)+eps >= radius**2:
                return True

        # checks for every pixel at the bottom of the rectangle, weather the pixel
        # (and any pixel within "eps" distance) is also part of the circumference
        y = rbottom
        for x in range(rleft,rright+1):
            if ((x-center_x)**2 + (y-center_y)**2)-eps <= radius**2 and ((x-center_x)**2 + (y-center_y)**2)+eps >= radius**2:
                return True

        # checks for every pixel at the left of the rectangle, weather the pixel
        # (and any pixel within "eps" distance) is also part of the circumference
        x = rleft
        for y in range(rtop,rbottom+1):
            if ((x-center_x)**2 + (y-center_y)**2)-eps <= radius**2 and ((x-center_x)**2 + (y-center_y)**2)+eps >= radius**2:
                return True
        
        # checks for every pixel at the right of the rectangle, weather the pixel
        # (and any pixel within "eps" distance) is also part of the circumference
        x = rright
        for y in range(rtop,rbottom+1):
            if ((x-center_x)**2 + (y-center_y)**2)-eps <= radius**2 and ((x-center_x)**2 + (y-center_y)**2)+eps >= radius**2:
                return True

        return False  # no collision detected