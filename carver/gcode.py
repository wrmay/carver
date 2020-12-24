# it would be better to make this an object and not pollute the global namespace
GCODE_OUTPUT_FILE = None
GCODE_FEED_RATE = None
GCODE_PLUNGE_SPEED = None
GCODE_SPINDLE_SPEED = None


def open_output(filename):
    global GCODE_OUTPUT_FILE
    GCODE_OUTPUT_FILE = open(filename, 'w', newline='\r\n')


def setup(feed_rate, plunge_feed_rate, spindle_speed):
    global GCODE_FEED_RATE, GCODE_PLUNGE_SPEED, GCODE_SPINDLE_SPEED

    GCODE_FEED_RATE = feed_rate
    GCODE_PLUNGE_SPEED = plunge_feed_rate
    GCODE_SPINDLE_SPEED = spindle_speed

    print('G90', file=GCODE_OUTPUT_FILE)

    print('F{0} S{1}'.format(GCODE_FEED_RATE, GCODE_SPINDLE_SPEED), file=GCODE_OUTPUT_FILE)


def start_spindle_clockwise():
    print('M3', file=GCODE_OUTPUT_FILE)


def start_spindle_counterclockwise():
    print('M4', file=GCODE_OUTPUT_FILE)


def stop_spindle():
    print('M5', file=GCODE_OUTPUT_FILE)


def end():
    print('M2', file=GCODE_OUTPUT_FILE)
    GCODE_OUTPUT_FILE.close()


def goto_xy_fast(x, y):
    x = round(x, 3)
    y = round(y, 3)
    print('G0 X{0} Y{1}'.format(x, y), file=GCODE_OUTPUT_FILE)


def goto_z_fast(z):
    z = round(z, 3)
    print('G0 Z{0}'.format(z), file=GCODE_OUTPUT_FILE)


def goto_fast(x, y, z):
    x = round(x, 3)
    y = round(y, 3)
    z = round(z, 3)
    print('G0 X{0} Y{1} Z{2}'.format(x, y, z), file=GCODE_OUTPUT_FILE)


def goto(x, y, z):
    x = round(x, 3)
    y = round(y, 3)
    z = round(z, 3)
    print('G1 X{0} Y{1} Z{2}'.format(x, y, z), file=GCODE_OUTPUT_FILE)


def goto_x(x):
    x = round(x, 3)
    print('G1 X{0}'.format(x), file=GCODE_OUTPUT_FILE)


def goto_y(y):
    y = round(y, 3)
    print('G1 Y{0}'.format(y), file=GCODE_OUTPUT_FILE)


def goto_z(z):
    z = round(z, 3)
    print('G1 Z{0} F{1}'.format(z, GCODE_PLUNGE_SPEED), file=GCODE_OUTPUT_FILE)
    print('F{0}'.format(GCODE_FEED_RATE), file=GCODE_OUTPUT_FILE)


def goto_xy(x, y):
    x = round(x, 3)
    y = round(y, 3)
    print('G1 X{0} Y{1}'.format(x, y), file=GCODE_OUTPUT_FILE)


def clockwise_arc(to_x, to_y, center_offset_x, center_offset_y):
    to_x = round(to_x, 3)
    to_y = round(to_y, 3)
    center_offset_x = round(center_offset_x, 3)
    center_offset_y = round(center_offset_y, 3)
    print('G2 X{0} Y{1} I{2} J{3}'.format(to_x, to_y, center_offset_x, center_offset_y), file=GCODE_OUTPUT_FILE)
