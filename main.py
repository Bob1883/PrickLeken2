def showYourTurn():
    for index2 in range(3):
        basic.clear_screen()
        basic.pause(100)
        basic.show_leds("""
            . . # . .
            . . # . .
            . . # . .
            . . . . .
            . . # . .
            """)
        basic.pause(100)
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
    global index3, index
    index3 = 0
    while index <= len(array):
        if array[index] == num:
            return True
        index += 1
    return False
def restartGame():
    global restartVar, selectedToRemove, playerPlaying, loadingIDs, turnIndex, synchronizing, canClear, numLeds, yourTurn
    restartVar = False
    selectedToRemove = 0
    playerPlaying = False
    loadingIDs = False
    turnIndex = 0
    synchronizing = False
    canClear = False
    basic.clear_screen()
    if isAdmin:
        numLeds = randint(10, 25)
        radio.send_value("restartGame", numLeds)
        basic.pause(500)
        radio.send_value("yourTurn", IDList[turnIndex])
        yourTurn = True
        drawLed(numLeds)
    else:
        yourTurn = False
        selectedToRemove = 0
        basic.show_icon(IconNames.HAPPY)

def on_button_pressed_ab():
    global synchronizing, loadingIDs, IDList
    if loadingIDs and (isAdmin and synchronizing):
        synchronizing = False
        loadingIDs = False
        basic.clear_screen()
        drawLed(numLeds)
        radio.send_value("syncDone", numLeds)
        IDList = IDList
    if restartVar:
        restartGame()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

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
    global restartVar, messageReceived, playerPlaying, nextMessageReceived
    if receivedString == "youLose":
        basic.show_icon(IconNames.SKULL)
        restartVar = True
    if receivedString == "messageReceived":
        messageReceived = True
    if receivedString == "donePlaying":
        if playerPlaying:
            playerPlaying = False
            drawLed(numLeds)
            radio.send_string("nextMessageReceived")
        else:
            radio.send_string("nextMessageReceived")
    if receivedString == "nextMessageReceived":
        nextMessageReceived = True
radio.on_received_string(on_received_string)

def selectAdmin():
    global isAdmin, synchronizing
    basic.show_leds("""
        . # . . .
        . # # . .
        . # # # .
        . # # . .
        . # . . .
        """)
    while loadingIDs:
        radio.send_value("ID", playerID)
        basic.pause(randint(50, 100))
        if input.button_is_pressed(Button.A):
            isAdmin = True
            basic.show_leds("""
                . # # # .
                . # . # .
                . # # # .
                . # . # .
                . # . # .
                """)
            basic.pause(500)
            synchronizing = True
            break
    if not (isAdmin):
        basic.show_icon(IconNames.YES)

def on_button_pressed_b():
    global numLeds, restartVar, yourTurn, playerPlaying, nextMessageReceived, selectedToRemove
    if not (loadingIDs):
        basic.clear_screen()
        if yourTurn:
            numLeds = numLeds - selectedToRemove
            if numLeds <= 0:
                for index22 in range(4):
                    radio.send_string("youLose")
                    basic.pause(200)
                basic.show_string("YOU WIN")
                basic.show_icon(IconNames.HAPPY)
                restartVar = True
            else:
                drawLed(numLeds)
                yourTurn = False
                playerPlaying = False
                radio.send_value("next", numLeds)
                basic.pause(100)
                if not (isAdmin):
                    nextMessageReceived = False
                    while not (nextMessageReceived):
                        radio.send_string("donePlaying")
                        basic.pause(200)
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
    global numLeds, loadingIDs, yourTurn
    if isAdmin:
        if name == "ID":
            IDList.append(value)
            radio.send_value("Done", value)
        if name == "next":
            if numLeds != value:
                numLeds = value
                drawLed(numLeds)
    else:
        if name == "Done":
            if value == playerID:
                loadingIDs = False
        if name == "yourTurn":
            if value == playerID and not (yourTurn):
                yourTurn = True
                radio.send_string("messageReceived")
                showYourTurn()
            if value == playerID and yourTurn:
                radio.send_string("messageReceived")
        if name == "next":
            basic.clear_screen()
            numLeds = value
            drawLed(numLeds)
        if name == "syncDone":
            numLeds = value
            basic.clear_screen()
            drawLed(numLeds)
radio.on_received_value(on_received_value)

nextMessageReceived = False
messageReceived = False
row = 0
synchronizing = False
turnIndex = 0
index = 0
index3 = 0
numLeds = 0
restartVar = False
canClear = False
playerPlaying = False
IDList: List[number] = []
yourTurn = False
playerID = 0
selectedToRemove = 0
isAdmin = False
loadingIDs = False
radio.set_group(121)
radio.send_number(0)
loadingIDs = True
isAdmin = False
selectedToRemove = 0
playerID = control.device_serial_number()
yourTurn = False
IDList = [control.device_serial_number()]
playerPlaying = False
canClear = False
restartVar = False
selectAdmin()
if isAdmin:
    numLeds = randint(10, 25)

def on_forever():
    global messageReceived, turnIndex, yourTurn, playerPlaying, canClear
    if isAdmin and synchronizing:
        basic.clear_screen()
        for row2 in range(5):
            for col in range(3):
                led.plot(col + 1, 4 - row2)
            basic.pause(200)
        basic.pause(200)
        basic.clear_screen()
    if isAdmin and (not (loadingIDs) and not (playerPlaying)):
        drawLed(numLeds)
        messageReceived = False
        turnIndex += 1
        if turnIndex >= len(IDList):
            turnIndex = 0
        if IDList[turnIndex] == playerID:
            yourTurn = True
            messageReceived = True
            showYourTurn()
        else:
            while not (messageReceived):
                radio.send_value("yourTurn", IDList[turnIndex])
                basic.pause(100)
        for index23 in range(4):
            basic.pause(100)
            radio.send_value("next", numLeds)
        playerPlaying = True
        basic.pause(100)
    if yourTurn:
        canClear = True
    else:
        canClear = False
basic.forever(on_forever)
