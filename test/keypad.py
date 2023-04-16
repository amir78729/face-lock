
import RPi.GPIO as GPIO
import time

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

secretCode = '123'

class Keypad:

    # The GPIO pin of the column of the key that is currently
    # being held down or -1 if no key is pressed
    keypad_pressed = -1

    input = ""
    
    def keypad_callback(self, channel):
        if self.keypad_pressed == -1:
            self.keypad_pressed = channel
    
    def __init__(self):

        # Setup GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(L1, GPIO.OUT)
        GPIO.setup(L2, GPIO.OUT)
        GPIO.setup(L3, GPIO.OUT)
        GPIO.setup(L4, GPIO.OUT)
        
        # Use the internal pull-down resistors
        GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Detect the rising edges on the column lines of the
        # keypad. This way, we can detect if the user presses
        # a button when we send a pulse.
        GPIO.add_event_detect(C1, GPIO.RISING, callback=self.keypad_callback)
        GPIO.add_event_detect(C2, GPIO.RISING, callback=self.keypad_callback)
        GPIO.add_event_detect(C3, GPIO.RISING, callback=self.keypad_callback)
        GPIO.add_event_detect(C4, GPIO.RISING, callback=self.keypad_callback)

    # Sets all lines to a specific state. This is a helper
    # for detecting when the user releases a button
    def set_all_lines(self, state):
        GPIO.output(L1, state)
        GPIO.output(L2, state)
        GPIO.output(L3, state)
        GPIO.output(L4, state)
    
    def check_special_keys(self):
        pressed = False
    
        GPIO.output(L3, GPIO.HIGH)
    
        if GPIO.input(C4) == 1:
            print("Input reset!")
            pressed = True
    
        GPIO.output(L3, GPIO.LOW)
        GPIO.output(L1, GPIO.HIGH)
    
        if not pressed and GPIO.input(C4) == 1:
            if self.input == secretCode:
                print("Code correct!")
            else:
                print("Incorrect code!")
            pressed = True
    
        GPIO.output(L3, GPIO.LOW)
    
        if pressed:
            self.input = ""
    
        return pressed
    
    # reads the columns and appends the value, that corresponds
    # to the button, to a variable
    def read_line(self, line, characters):
        # We have to send a pulse on each line to
        # detect button presses
        GPIO.output(line, GPIO.HIGH)
        x = None
        if (GPIO.input(C1) == 1):
            # self.input = self.input + characters[0]
            x = characters[0]
        if (GPIO.input(C2) == 1):
            # self.input = self.input + characters[1]
            x = characters[1]
        if (GPIO.input(C3) == 1):
            # self.input = self.input + characters[2]
            x = characters[2]
        if (GPIO.input(C4) == 1):
            # self.input = self.input + characters[3]
            x = characters[3]
        GPIO.output(line, GPIO.LOW)
        return x

    def get_character(self):
        for L, buttons in zip([L1, L2, L3, L4], [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"]
        ]):
            i = self.read_line(L, buttons)
            if i:
                return i
        return None


if __name__ == '__main__':
    keypad = Keypad()
    keypad.main()
    