def showYourTurn():
    for index2 in range(3):
        basic.clear_screen()
        basic.pause(500)
        basic.show_leds("""
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            """)
        basic.pause(500)
    basic.clear_screen()
    drawLed(numLeds)

def on_button_pressed_a():
    global selectedToRemove
    if not (loadingIDs):
        basic.clear_screen()
        if yourTurn:
            if selectedToRemove < 3:
                selectedToRemove += 1
            else:
                selectedToRemove = 1
            basic.show_number(selectedToRemove)
        else:
            basic.show_leds("""
                # . . . #
                . # . # .
                . . # . .
                . # . # .
                # . . . #
                """)
            basic.pause(500)
            basic.clear_screen()
            drawLed(numLeds)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_gesture_logo_up():
    if canClear:
        basic.clear_screen()
        drawLed(numLeds)
input.on_gesture(Gesture.LOGO_UP, on_gesture_logo_up)

def isInList(array: List[any], num: number):
    index = 0
    while index <= len(array):
        if array[index] == num:
            return True
        index += 1
    return False

def on_button_pressed_ab():
    global synchronizing, loadingIDs, IDList
    if loadingIDs and not (isAdmin):
        basic.show_icon(IconNames.SAD)
        while loadingIDs:
            radio.send_value("ID", playerID)
            basic.pause(randint(100, 500))
        basic.show_icon(IconNames.HAPPY)
    if loadingIDs and (isAdmin and synchronizing):
        synchronizing = False
        loadingIDs = False
        basic.clear_screen()
        drawLed(numLeds)
        radio.send_value("syncDone", numLeds)
        IDList = bubbleSort(IDList)
    if loadingIDs and (isAdmin and not (synchronizing)):
        synchronizing = True
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def bubbleSort(list2: List[number]):
    global y, savedValue, x
    while x <= len(list2):
        y = 0
        while y <= len(list2) - (x + 1):
            if list2[y] > list2[y + 1]:
                savedValue = list2[y]
                list2[y] = list2[y + 1]
                list2[y + 1] = savedValue
            y += 1
        x += 1
    return list2
def drawLed(leds: number):
    global row, index3
    row = 0
    if leds != 0:
        index3 = 0
        while index3 <= leds - 1:
            if index3 % 5 == 0 and index3 != 0:
                row += 1
            led.plot(index3 - row * 5, row)
            index3 += 1

def on_received_string(receivedString):
    if receivedString == "youLose":
        basic.show_icon(IconNames.SKULL)
radio.on_received_string(on_received_string)

def selectAdmin():
    global isAdmin
    basic.show_leds("""
        . . . . .
        . . . . .
        . . # . .
        . . . . .
        . . . . .
        """)
    while True:
        if input.button_is_pressed(Button.A):
            isAdmin = True
            basic.show_icon(IconNames.DIAMOND)
            break
        if input.button_is_pressed(Button.B):
            isAdmin = False
            basic.show_icon(IconNames.SQUARE)
            break
    basic.pause(1000)
    basic.clear_screen()

def on_button_pressed_b():
    global numLeds, yourTurn, playerPlaying, selectedToRemove
    if not (loadingIDs):
        basic.clear_screen()
        if yourTurn:
            numLeds = numLeds - selectedToRemove
            if numLeds <= 0:
                radio.send_string("youLose")
                basic.show_string("YOU WIN")
                basic.show_icon(IconNames.STICK_FIGURE)
            else:
                drawLed(numLeds)
                radio.send_value("next", numLeds)
                yourTurn = False
                if isAdmin:
                    playerPlaying = False
            selectedToRemove = 0
        else:
            basic.show_leds("""
                # . . . #
                . # . # .
                . . # . .
                . # . # .
                # . . . #
                """)
            basic.pause(500)
            basic.clear_screen()
            drawLed(numLeds)
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_received_value(name, value):
    global numLeds, playerPlaying, loadingIDs, yourTurn
    if isAdmin:
        if name == "ID":
            if not (isInList(IDList, value)):
                IDList.append(value)
                radio.send_value("Done", value)
        if name == "next":
            numLeds = value
            playerPlaying = False
            drawLed(numLeds)
    else:
        if name == "Done":
            if value == playerID:
                loadingIDs = False
        if name == "yourTurn":
            if value == playerID:
                yourTurn = True
                showYourTurn()
        if name == "next":
            basic.clear_screen()
            numLeds = value
            drawLed(numLeds)
        if name == "syncDone":
            numLeds = value
            basic.clear_screen()
            drawLed(numLeds)
radio.on_received_value(on_received_value)

index3 = 0
row = 0
savedValue = 0
y = 0
x = 0
synchronizing = False
numLeds = 0
canClear = False
playerPlaying = False
IDList: List[number] = []
yourTurn = False
playerID = 0
selectedToRemove = 0
isAdmin = False
loadingIDs = False
radio.set_group(179)
radio.send_number(0)
loadingIDs = True
isAdmin = False
selectedToRemove = 0
playerID = control.device_serial_number()
yourTurn = False
turnIndex = 0
IDList = [control.device_serial_number()]
playerPlaying = False
canClear = False
selectAdmin()
if isAdmin:
    numLeds = randint(10, 25)

def on_forever():
    global yourTurn, turnIndex, playerPlaying, canClear
    if isAdmin and synchronizing:
        basic.show_leds("""
            # . # . #
            . # . # .
            # . # . #
            . # . # .
            # . # . #
            """)
        basic.pause(500)
        basic.show_leds("""
            . # . # .
            # . # . #
            . # . # .
            # . # . #
            . # . # .
            """)
        basic.pause(500)
    if isAdmin and (not (loadingIDs) and not (playerPlaying)):
        radio.send_value("yourTurn", IDList[turnIndex])
        radio.send_value("next", numLeds)
        if IDList[turnIndex] == playerID:
            yourTurn = True
            showYourTurn()
        turnIndex += 1
        playerPlaying = True
        if turnIndex >= len(IDList):
            turnIndex = 0
    if yourTurn:
        canClear = True
    else:
        canClear = False
basic.forever(on_forever)