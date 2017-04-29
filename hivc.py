from RobotController import controller
def arcPath():
  loopNum = 0
  sideLength = 0
  import random
  i = 0
  sideLength = random.randInt(10)
  for _ in range(loopNum):
    controller.move("forward", sideLength)
    controller.turn(left, angle)
counter = 0
for _ in range(5):
  counter = counter
