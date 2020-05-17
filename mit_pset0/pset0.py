import math
import numpy

question3 = 23 ** 5

# 34*x^2 + 68*x - 510
discriminant = (68 ** 2) - (4 * 34 * -510)
positive_root = ((-68) + discriminant ** (1 / 2)) / (2 * 34)
print(str(positive_root))


question5 = math.cos(3.4)**2 + math.sin(3.4)**2
print(str(question5))


x = input("Enter number x: ")
y = input("Enter number y: ")
x_raised_to_y = int(x)**int(y)
print(str(x_raised_to_y))
log_x = numpy.log2(int(x))
print(str(log_x))

