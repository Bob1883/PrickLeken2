def on_button_pressed_a():
    global selectedToRemove
    basic.clear_screen()
    if selectedToRemove < 3:
        selectedToRemove += 1
    else:
        selectedToRemove = 1
    basic.show_number(selectedToRemove)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_gesture_logo_up():
    basic.clear_screen()
    drawLed(numLeds)
input.on_gesture(Gesture.LOGO_UP, on_gesture_logo_up)

def drawLed(leds: number):
    global row
    row = 0
    if leds != 0:
        index = 0
        while index <= leds - 1:
            if index % 5 == 0 and index != 0:
                row += 1
            led.plot(index - row * 5, row)
            index += 1

def on_button_pressed_b():
    global numLeds, selectedToRemove
    basic.clear_screen()
    numLeds = numLeds - selectedToRemove
    if numLeds <= 0:
        basic.show_string("YOU WIN")
    else:
        drawLed(numLeds)
    selectedToRemove = 0
input.on_button_pressed(Button.B, on_button_pressed_b)

row = 0
selectedToRemove = 0
numLeds = 0
numLeds = randint(10, 25)
selectedToRemove = 0
drawLed(numLeds)