import os

# Definitions for constants used in the ShakuNotator application


dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)


# AUDIO OPTIONS :

MIDI_INSTRUMENT_NUMBER = 73

PLAYBACK_TEMPO = 65

SAVE_TEMPO = 65

DEFAULT_VOLUME = 100

DEFAULT_TEMPO = 65



#VISUAL DETAILS :
#(use rgb format for colors)

GRID_COLOR = (0, 0, 0)

NOTE_FONT = os.path.join(parent, "./graphics/ShakuNotator.ttf")

TEXT_FONT = os.path.join(parent, "./graphics/askai9.ttc")

TEXT_COLOR = (0, 0, 0)

NOTE_COLOR = (0, 0, 0)



# POSITIONS, SIZES, SCALES :
# The following constants pertaining to positioning / sizes on sheet are in scale used by UI preview
#    -> scaled *4 in exported PDF/SVG
# Sizes and scales are in some cases related to application functionality
# so in case of any change test thoroughly.

MAIN_WINDOW_SIZE = "860x1000" # format accepted by tkinter Tk.geometry

SHEET_SIZE = (620, 877) # 1/4 of export size

EXPORT_SHEET_SIZE = (2480, 3508) # A4 paper

NOTE_ROW_SPACING = 20

PARTS_Y_START = 80

MEASURE_SKIP_LENGHT = 14

NOTE_Y_SPACING = 12

GRID_LINE_WIDHT = 1

RHYTHM_NOTATION_WIDHT = 2

RHYTHM_NOTATION_WIDHT_EXPORT = 3

COMPOSER_POSITION = (40, 30)

NAME_POSITION = (580, 30)

TEXT_FONT_SIZE = 20

GRID_Y = (70, 840) #grid min and max y dimensions (however actual grid widht depends on spacing)

GRID_X = (62, 600) #grid min and max x dimensions (however actual grid widht depends on spacing)

SHEET_NOTE_SIZE = 16 # has no effect on tkinter at the momente!!!

BUTTON_NOTE_SIZE = 20

VERTICAL_SPACE_PER_FOURTH_NOTE = 55 # THSI SHOULD NOT EXISTS SINCE WE HAVE NOTE_Y_SPACING

EXPORT_NOTE_FONT_SIZE_INCREMENT = 20

EXPORT_NOTE_CORRECTION_ON_X_AXIS = -10

NOTE_TO_RHYTM_SPACING = 16

RHYTM_LINE2_TO_LINE1_SPACING = 4

RHYTM_VERTICAL_LINE_LENGHT = 12

RHTM_VERTICAL_LINE_START_TO_NOTE_Y = 1

NOTATION_APPENDIX_X_FROM_NOTE = 11

NOTATION_APPENDIX_Y_FROM_NOTE = -9

NOTE_BUTTON_SIZE = 30



# FILING & UPLOAD OPTIONS :

AWS_S3_BUCKET = "shakunotator"



# SHAKUHACHI MUSIC OPTIONS & DETAILS :

MODE = "Tozan"

NOTES = {-4: os.path.join(parent, "graphics/" + str(-4) + ".png"),
-8: os.path.join(parent, "graphics/" + str(-8) + ".png")
}
for i in range(-2, 13):
    NOTES[i] = os.path.join(parent, "graphics/" + str(i) + ".png")
for i in range(13, 30):
    NOTES[i] = os.path.join(parent, "graphics/" + str(i - 13) + ".png")
for i in range(29, 41):
    NOTES[i] = os.path.join(parent, "graphics/" + str(i - 24) + ".png")

OCTAVES = {"Otsu": os.path.join(parent, "graphics/otsu.png"),
"Kan": os.path.join(parent, "graphics/kan.png"),
"Daikan": os.path.join(parent, "graphics/daikan.png")
}

MAX_PARTS = 10

LENGHTS = {2: "16th", 4: "8th", 8: "4th", 16: "half"}

MEASURE_LENGHT = 2

NOTE_TEXT_CODES = {-2: ".", -1: ",", 0: "Q", 1: "W", 2: "E", 3: "R",
4: "T", 5: "Y", 6: "U", 7: "I", 8: "O", 9: "P", 10: "A", 11: "S", 12: "D",
13: "W", 14: "E", 15: "R", 16: "T", 17: "Y", 18: "U", 19: "I", 20: "O",
21: "P", 22: "A", 23: "S", 24: "D", 25: "F", 26: "G", 27: "H", 28: "J",
29: "Y", 30: "U", 31: "I", 32: "O", 33: "P", 34: "A", 35: "S", 36: "D",
37: "F", 38: "G", 39: "H", 40: "J"
}

OCTAVE_TEXT_CODES = {"Otsu": "B", "Kan": "N", "Daikan": "M"}



# ALERT / ERROR MESSAGES :

MESSAGE_PADDING = (50, 40)

MESSAGE_FULL_SHEET = """
Sheet full, current version does not support multiple pages.\n
Save sheet and create new one\nfor any additional pages."""

MESSAGE_PART_ROOM = """
Sheet has no more room for additional parts,\n
and current version does not support multiple pages."""

MESSAGE_NO_ACCESS_TO_AWS = f"""
You have not configured credentials to the AWS S3 -bucket : {AWS_S3_BUCKET}\n
If necessary, please request access from admin,\n
or configure a different bucket as guided in documentation."""

MESSAGE_NO_NAME_TO_AWS = "You have to add a name to your composition to upload."

MESSAGE_OVERWRITE_ALERT = """
Detected unsaved changes in your current sheet.
\nPress cancel on loading screen if you want to save first."""

MESSAGE_LONG_NAME_COMPOSER = "Name & Composer combination too long"

MESSAGE_INCORRECT_FILE = "Not a valid .shaku file or data corrupted"

MESSAGE_UNDER_DEVELOPMENT = "The feature associated with the button you pressed\nis currently still under development"

MESSAGE_SUCCESFUL_UPLOAD = f"You have succesfully uploaded the composition to the AWS S3 -bucket : {AWS_S3_BUCKET}"