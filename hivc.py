def driveSquare(sideLength):
  for _ in range(4):
    controller.move("forward", sideLength)
    controller.turn(left, 90)
driveTime = 10
driveSquare(driveTime)
moveTime = 5
controller.move("backward", moveTime)
driveSquare(moveTime)
