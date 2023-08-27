import math

from Controller import *

SEGMENT_LENGTH = 50  # shorter segments means straighter lines


# TODO implement a get_xy() method

class Plotter():
    def __init__(self):
        self.x = None
        self.y = None
        self.l = None
        self.r = None
        self.w = None
        self.plotter_controller = PlotterController02()
       
        # Test pour la connection serial
        
        self.pen_down()
        time.sleep(0.5)
        self.pen_up()

    # Permettre au servo moteur de controller le moteur vers le haut
    def pen_up(self):
        self.plotter_controller.pen_up()

    # Permettre au servo moteur de controller le moteur vers le haut
    def pen_down(self):
        self.plotter_controller.pen_down()

    # Permettre de se deplacer vers l et r
    def move_to_st(self, l, r, verbose=True):
      
        self.move_by_st(l - self.l, r - self.l, verbose=verbose)

    def move_by_st(self, delta_s, delta_t, verbose=True):
  
        self.plotter_controller.move(delta_s, delta_t)
        self.s += delta_s
        self.t += delta_t
        
        if verbose:
            print(f"Moving: delta_s={delta_s}, delta_t={delta_t}, (s, t, w) = {self.get_stw_pos()}")

    def move_to_xy(self, x, y, verbose=True):
    
        s = int(math.sqrt(x ** 2 + y ** 2))
        t = int(math.sqrt((self.w - x) ** 2 + y ** 2))
        if verbose:
            print(f"Moving: x={x}, y={y}")
        self.move_to_st(s, t, verbose=verbose)
        self.x = x
        self.y = y

    # deplacement droit vers les coordonnees x et y 
    def move_straight_to_xy(self, x, y):
        if self.x is None:
            self.move_to_xy(x, y)
        else:
            delta_x = x - self.x
            delta_y = y - self.y
            segments_remaining = int(math.sqrt(delta_x**2 + delta_y**2) // SEGMENT_LENGTH)  # number of segments is line length / SEGMENT_LENGTH
            while segments_remaining > 0:
                delta_x = x - self.x
                delta_y = y - self.y
                self.move_to_xy(self.x + delta_x//segments_remaining, self.y + delta_y//segments_remaining)
                segments_remaining -= 1
            
            # move remaining distance
            self.move_to_xy(x, y)


    #Permet de dessine un carre
    def draw_square(self, side_length: int):

        # middle = self.w / 2
        middle = 3000 + side_length / 2  # Make (3000,3000) be the top corner
        half_side = side_length / 2

        # Haut a gauche
        self.move_to_xy(middle - half_side, middle - half_side)  # Top Left

        # le ploteur vers le bas
        self.pen_down()
        # vers la droite
        self.move_straight_to_xy(middle + half_side, middle - half_side)  # Top Right
        # vers le bas
        self.move_straight_to_xy(middle + half_side, middle + half_side)  # Bottom Right
        # vers la gauche
        self.move_straight_to_xy(middle - half_side, middle + half_side)  # Bottom Left
        # vers le hat
        self.move_straight_to_xy(middle - half_side, middle - half_side)  # Top Left
        #ploteur vers le haut
        self.pen_up()




if __name__ == '__main__':
    plotter = Plotter()
    plotter.draw_square(100)
