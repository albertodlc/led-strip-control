import utils as Utils

# Format of the MESSSAGES
FIRST_HEX = "56"
FINAL_HEX = "00F0AA"
TURN_ON = "CC2333"
TURN_OFF = "CC2433"

def on_message():
    return bytearray.fromhex(TURN_ON)

def off_message():
    return bytearray.fromhex(TURN_OFF)

def color_message(R,G,B):
    return bytearray.fromhex(FIRST_HEX + Utils.rgb_to_hex(R, G, B) + FINAL_HEX)
