import math
import unittest


def to_r_theta(x, y):
    theta = math.atan(y / x)
    r = math.sqrt(x ** 2 + y ** 2)
    return r, theta


def to_x_y(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def rotate_point(x, y, rad):
    r, theta = to_r_theta(x, y)
    theta += rad
    return to_x_y(r, theta)


class Circle:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def translate(self, x, y):
        self.center_x += x
        self.center_y += y

    def rotate(self, rads):
        self.center_x, self.center_y = rotate_point(self.center_x, self.center_y, rads)


class Line:

    @classmethod
    def from_2_points(cls, x1, y1, x2, y2):
        return Line(x1, y1, x2, y2)

    @classmethod
    def from_point_and_slope(cls, x, y, slope):
        return Line(x, y, x + 1, y + slope)

    @classmethod
    def vertical_with_x_intercept(cls, x_intercept):
        return Line(x_intercept, 0, x_intercept, 1)

    def __init__(self, x1, y1, x2, y2):
        """specify a line with two points.  Can also specify a line segment"""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def translate(self, x, y):
        self.x1 += x
        self.y1 += y
        self.x2 += x
        self.y2 += y

    def rotate(self, rad):
        self.x1, self.y1 = rotate_point(self.x1, self.y1, rad)
        self.x2, self.y2 = rotate_point(self.x2, self.y2, rad)

    def slope(self):
        if self.x1 == self.x2:
            return None
        else:
            return (self.y2 - self.y1)/(self.x2 - self.x1)

    def y_of(self, x):
        m = self.slope()
        if m is None:
            raise RuntimeError("Cannot find a unique y for a vertical line")

        y = self.y1 + m*(x - self.x1)
        return y


def line_line_intersect(line1, line2):
    m1 = line1.slope()
    m2 = line2.slope()

    # both lines are vertical
    if m1 is None and m2 is None:
        raise RuntimeError("Cannot find the intersection of 2 vertical lines.")

    # one line is vertical
    if m1 is None or m2 is None:
        if m1 is None:
            line1, line2 = line2, line1

        # line2 is vertical, line1 is not vertical
        x = line2.x1
        y = line1.y_of(x)
        return x, y

    # neither line is vertical
    x = ((m1 * line1.x1 - line1.y1) - (m2 * line2.x1 - line2.y1))/(m1 - m2)
    y = line1.y_of(x)

    return x, y


def line_circle_intersect(line, circle):
    """ returns a list of (x,y) tuples """
    results = []
    m = line.slope()

    # vertical line
    if m is None:
        M = line.x1
        C = M**2 - 2*M*circle.center_x + circle.center_x**2 + circle.center_y**2 - circle.radius ** 2
        if circle.center_y ** 2 - C < 0:
            pass
        elif circle.center_y ** 2 - C == 0:
            results.append((M, -1 * circle.center_y))
        else:
            D = math.sqrt(circle.center_y ** 2 - C)
            results.append((M, -1 * circle.center_y + D))
            results.append((M, -1 * circle.center_y - D))
    else:
        A = 1 + m ** 2
        b = line.y_of(0)
        B = 2 * m * (b - circle.center_y) -2 * circle.center_x
        C = circle.center_x ** 2 + (b - circle.center_y) ** 2 - circle.radius ** 2

        D = B ** 2 - 4 * A * C
        D = round(D, 6)
        if D == 0:
            x = (-1 * B) / (2 * A)
            results.append((x, line.y_of(x)))
        elif D > 0:
            x = (-1 * B + math.sqrt(D)) / (2 * A)
            results.append((x, line.y_of(x)))
            x = (-1 * B - math.sqrt(D)) / (2 * A)
            results.append((x, line.y_of(x)))

    return results


def circle_circle_intersect(circle1, circle2):
    if circle1.center_y == circle2.center_y:
        """the intersection points will lie on a vertical line"""
        x = (circle1.radius **2 - circle2.radius ** 2 + circle2.center_x ** 2 - circle1.center_x ** 2) / ( 2 * (circle2.center_x - circle1.center_x))
        line = Line.vertical_with_x_intercept(x)

    else:
        slope = (circle1.center_x - circle2.center_x) / (circle2.center_y - circle1.center_y)
        y_intercept = (circle1.radius ** 2 - circle2.radius ** 2 + circle2.center_x ** 2 - circle1.center_x ** 2 + circle2.center_y ** 2 - circle1.center_y **2) / ( 2 * (circle2.center_y - circle1.center_y))
        line = Line.from_point_and_slope(0, y_intercept, slope)

    return line_circle_intersect(line, circle1)


class Tests(unittest.TestCase):

    def test_line_line_01(self):
        line1 = Line.from_point_and_slope(0, 0, 0)
        line2 = Line.vertical_with_x_intercept(3)
        x, y = line_line_intersect(line1, line2)
        self.assertEqual(x,3)
        self.assertEqual(y,0)

    def test_line_circle_01(self):
        line = Line.from_point_and_slope(0, 0, 1)
        circle = Circle(0, 0, 1)
        expected_x = round(math.cos(math.pi / 4), 6)
        expected_y = round(math.sin(math.pi / 4), 6)
        solutions = [(round(x,6), round(y, 6)) for x, y in line_circle_intersect(line, circle)]
        self.assertIn((expected_x, expected_y), solutions)
        self.assertIn((-1 * expected_x, -1 * expected_y), solutions)

    def test_vertical_line_circle(self):
        line = Line.vertical_with_x_intercept(0)
        circle = Circle(0,0,2)
        solutions = line_circle_intersect(line, circle)
        self.assertIn((0,2), solutions)
        self.assertIn((0,-2), solutions)

    def test_circle_circle_1(self):
        circle1 = Circle(0, 0, 1)
        circle2 = Circle(2 * math.cos(math.pi / 4), 2 * math.sin(math.pi / 4), 1)
        solutions = circle_circle_intersect(circle1, circle2)
        rounded_solutions = [(round(x, 6), round(y, 6)) for x, y in solutions]
        self.assertEqual(1, len(rounded_solutions))
        self.assertIn(( round(math.cos(math.pi / 4),6), round(math.sin(math.pi / 4), 6)), rounded_solutions)

    def test_circle_circle_2(self):
        circle1 = Circle(0, 0, 1)
        circle2 = Circle(2, 0, 1)
        solutions = circle_circle_intersect(circle1, circle2)
        self.assertEqual(1, len(solutions))
        self.assertIn((1, 0), solutions)

    def test_circle_circle_3(self):
        circle1 = Circle(0, 0, 1)
        circle2 = Circle(0, 2, 1)
        solutions = circle_circle_intersect(circle1, circle2)
        self.assertEqual(1, len(solutions))
        self.assertIn((0, 1), solutions)

