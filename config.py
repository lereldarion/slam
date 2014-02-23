import slam_util

# Config
class Pair (object):
    def __init__ (self, x = 0, y = 0): self.x, self.y = x, y
    def __add__ (self, other): return Pair (self.x + other.x, self.y + other.y)
    def __str__ (self): return "(%s,%s)" % (str (self.x), str (self.y))

class Config (object):
    def __init__ (self):
        self.output_by_name = dict ()
    
    def key (self):
        pass

# Entry point
if __name__ == "__main__":
    slam_util.compute_screen_positions ("blah")