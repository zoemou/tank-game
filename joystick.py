import pygame


class Joystick():

    def __init__(self,tg):
        self.tg = tg
        pygame.joystick.init()
        self.count = 0

        self.numjoy = pygame.joystick.get_count()
        if self.numjoy > 0:
            self.tg.joyin = True
            for i in range(self.numjoy):
                self.joystick = pygame.joystick.Joystick(i)
                self.joystick.init()
                self.playerjoys = i

                self.numButtons = self.joystick.get_numbuttons()
                self.buttons = [i]*self.numButtons
                for i in range(self.numButtons):
                    self.buttons[i] = self.joystick.get_button(i)

                self.hats = self.joystick.get_numhats()
                self.hat = [i]*self.hats
                for i in range( self.hats ):
                    self.hat = self.joystick.get_hat(i)


                self.axes = self.joystick.get_numaxes()
                self.axis = [i]*self.axes
                for i in range(self.axes):
                    self.axis = self.joystick.get_axis(i)
        else:
            self.tg.joyin = False
            pygame.joystick.quit()





