from Geometry.myPoint import myPoint
import math
class myLine:
    def __init__(self,start,end):
        self.start_point=start
        self.end_point=end
        self.mid_point=(self.start_point+self.end_point)/2