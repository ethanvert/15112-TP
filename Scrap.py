import math
from cmu_112_graphics import *
from dataclasses import make_dataclass

def ct1(n):
    print(1+2*n-3*4, n//4, n/4, (n%4)**3)
    x = (n+2)%n
    y = (n-2)%n
    return 10*x + y
print(ct1(10)) # prints 5 total values (on 2 lines)


def ct2(x, y):
    x *= 2
    print(float(y), pow(min(x, int(x)), abs(y-8)), bool(x/y), bool(1//y))
print(ct2(2.8, 5)) # prints 5 total values (on 2 lines)


# h(x,y) is used by ct3()
def h(x, y):
    if (y > x):
        if (x < 5):
            return 2
        elif (x >= 3) and (y < 10):
            return 4
    else:
        return 6
    return x

def ct3(x):
    y = 10*h(x,10) + h(3,x)
    z = 10*h(x,5) + h(x, x+1)
    return y + z/100
print(ct3(5))

def integerSquareRoot(v):
    if type(v) != int or v < 0:
        return None
    else:
        return int(math.sqrt(v))

assert(integerSquareRoot(0) == 0)
assert(integerSquareRoot(1) == 1)
assert(integerSquareRoot(2) == 1)
assert(integerSquareRoot(3) == 1)
assert(integerSquareRoot(4) == 2)
assert(integerSquareRoot(5) == 2)
assert(integerSquareRoot(99) == 9)
assert(integerSquareRoot(123**2) == 123)
assert(integerSquareRoot(123**2 - 1) == 122)
assert(integerSquareRoot(2.4) == None)
assert(integerSquareRoot(-5) == None)
assert(integerSquareRoot('Do not crash here!') == None)

def alternatesEvenOdd(n):
    dig1 = n % 10
    dig10 = n % 100 // 10
    dig100 = n // 100

    if(dig1 % 2 == dig10 %2 or dig10 % 2 == dig100 % 2):
        return False
    else:
        return True

assert(alternatesEvenOdd(147) == True)
assert(alternatesEvenOdd(478) == True)
assert(alternatesEvenOdd(124) == False)
assert(alternatesEvenOdd(235) == False)
assert(alternatesEvenOdd(777) == False)
assert(alternatesEvenOdd(222) == False)
assert(alternatesEvenOdd(787) == True)
assert(alternatesEvenOdd(878) == True)
assert(alternatesEvenOdd(943) == True)
assert(alternatesEvenOdd(652) == True)
assert(alternatesEvenOdd(692) == True)

def ct1(x, y, z):
  x *= z
  z = y ** z
  return (10 * y + z) % x

print(ct1(4, 3, 2))

def ct2():
  print(42, end='')
  # no return statement!

print(ct2())

# f(x,y) is used by ct3

def f(x, y):
  y += 1
  return x - x // y

def ct3(x, y):
  x = f(x, y - 1)
  return x / (y - 1)

print(ct3(7, 3))

# h(x,y) is used by ct4

def h(x, y):
  if (x > y):
    if (x > 2 * y):
      return 3
  elif (x < 2 * y):
    return 5
  else:
    return 7
  return 9

def ct4():
  w = h(8, 4)
  x = h(4, 8)
  y = h(8, 3)
  z = w + 10 * x + 100 * y
  print(z)

ct4()

def fasterIsPrime(n):
  if n < 2:
    return False
  if n == 2:
    return True
  if n % 2 == 0:
    return False
  maxFactor = int(n**0.5)

  for factor in range(3, maxFactor+1,2):
    if n % factor == 0:
      return False
    return True

print(fasterIsPrime(1237))

def ct1(x, y):
    for i in range(x):
        for j in range(i, y):
            if (i + j) % 3 == 0:
               print(j)
        print(f"i + j = {i + j}")
        if i < 2:
            print(112)
            if (i + j > 4):
                print("here")
                break

ct1(3, 5)

def ct2(a, b, c):
    n = 0
    while n < 1234:
        print(n)
        n += c
        n *= a
        b, c = c, b
    return n
print(ct2(10, 7, 2)) 

def isPrime(n):
  if n < 2:
    return False
  if n == 2:
    return True
  if n % 2 == 0:
    return False
  
  maxFactor = int(n**0.5)
  for x in range(3, maxFactor+1, 2):
    if n % x == 0:
      return False
  return True

def isSnarf(n):
  if n < 10:
    return False
  prevDig = -1

  while n > 0:
    currDig = n % 10
    if prevDig > 0 and currDig % 2 == prevDig % 2:
      return False
    prevDig = currDig
    n //= 10
  return True

def nthSnarfPrime(n):
  guess = 0
  found = 0

  while found <= n:
    guess += 1

    if isPrime(guess) and isSnarf(guess):
      found += 1

  return guess

def testNthSnarfPrime():
    print('Testing nthSnarfPrime()...', end='')
    assert(nthSnarfPrime(0) == 23)
    assert(nthSnarfPrime(1) == 29)
    assert(nthSnarfPrime(5) == 61)
    assert(nthSnarfPrime(9) == 101)
    print('Passed!')

testNthSnarfPrime()

def ct1(x, y):
  while (x > y):
    x -= y
    y -= 1
  r = 0
  for z in range(y):
    r += z
  return 100*x + r

print(ct1(20, 7))

def ct2(a, b, c):
  r = 0
  for x in range(a, b, c):
    for y in range(x):
      r = 10*r + y
  return r

print(ct2(0, 5, 2))

def isPrime(n):
  if n < 2:
    return False
  if n == 2:
    return True
  if n % 2 == 0:
    return False
  maxFactor = int(n**0.5)

  for factor in range(3, maxFactor+1, 2):
    if n % factor == 0:
      return False
  return True

def isLeftTruncatable(n):
  if n < 0 or not isPrime(n):
    return False
  
  

def nthLeftTruncatablePrime(n):
  guess = 0
  found = 0

def isSummish(n):
  if n < 1000:
    return False
  while n >= 100:
    onesDig = n % 10
    tensDig = n % 100 // 10
    hundsDig = n % 1000 // 100

    if onesDig != tensDig + hundsDig:
      return False
    n //= 10
  return True

def nthSummishNumber(n):
  guess = 1000
  found = 0

  while found <= n:
    guess += 1

    if isSummish(guess):
      found += 1
  return guess

def testNthSummishNumber():
  print('Testing nthSummishNumber()...', end='')
  assert(nthSummishNumber(0) == 1011)
  assert(nthSummishNumber(1) == 1123)
  assert(nthSummishNumber(2) == 1235)
  assert(nthSummishNumber(3) == 1347)
  print('Passed!')

testNthSummishNumber()


import sys
print(f'sudo "{sys.executable}" -m pip install pillow')
print(f'sudo "{sys.executable}" -m pip install requests')



# def redrawAll(app, canvas):
#     (cx, cy, r) = (app.width/2, app.height/2, min(app.width, app.height)/3)
#     canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="yellow")
#     r *= 0.85 # make smaller so time labels lie inside clock face
#     for hour in range(12):
#         hourAngle = math.pi/2 - (2*math.pi)*(hour/12)
#         hourX = cx + r * math.cos(hourAngle)
#         hourY = cy - r * math.sin(hourAngle)
#         label = str(hour if (hour > 0) else 12)
#         canvas.create_text(hourX, hourY, text=label, font="Arial 16 bold")

# runApp(width=400, height=400)

print("\n".isspace())

def ct1(s):
    t = s.upper()
    s += 'z'
    t *= len(s+t)
    return f's+t{s+t}'
print(ct1('a'))

def ct2(r, s):
    t = ''
    for i in range(0, len(r), 2):
        t += str(s.find(r[i]))

    result = f'{t}=={eval(t)}'
    return result
print(ct2('amazing', 'zambia'))

def ct1(s):
  t = ''
  u = t
  n = 0
  s = s[1:]
  for c in s:
    if c.isspace():
      n += 1
    elif c.islower():
      t += c.upper() * n
    elif c.isalpha():
      u += c
  return f'{t}-{u}-{n}'

print(ct1('Ab! Cd?\teF?'))

# s

# def redrawAll(canvas, width, height):
#   for x in range(0, width+1, 50):
#     canvas.create_line(0 + width, 0, width - x, height, fill = "black") # <-- Fill in this line

# runApp(width=400, height=200)

def ct1(L):
 M = L[:]
 for i in range(len(L)):
  if M[i] % 2 == 0: # <-- the fourth line
    print("here with ", M[i])
    print(L.pop() - i, M.append("a"))
  else:
    print("here")
    M.extend(["hey"])
 print(M)
 print(L)
L = [345, 12, 9, 20, 50]
ct1(L)

def ct42(K):
 I = copy.copy(K)
 M = [ ] + I
 C = K
 C += [ ] # Is this the same as C = C + [ ]?
 H = [K[0], K[-1], K[2], K[-2]]
 E = K
 E = E[::-1]
 print(E[-1])
 print(K.pop(-1), end=", ")
 print(I.pop(1), end=", ")
 print(C.pop(-2), end=", ")
 print(H.pop(2))
 print(K)
 print(I)
 print(M)
 print(C)
 print(H)
 print(E, E)
ct42([15, 112, 42, 50])


def removeRepeats(L, k):
  index = len(L) - 1
  while index >= 0:
    if L[index] == k and L.count(k) > 1:
      L.pop(index)
      index = len(L) -1
    else:
      index -= 1

def removeCountNotK(L, k):
  index = 0

  while index < len(L):
    if L.count(L[index]) != k:
      removeRepeats(L, L[index])
      L.pop(index)
    else:
      removeRepeats(L, L[index])
      index += 1

L = [1, 5, 1, 1, 2, 4, 2, 6, 4]
assert(removeCountNotK(L, 0) == None)
assert(L == []) # no elements in list L appear 0 times
L = [1, 5, 1, 1, 2, 4, 2, 6, 4]
assert(removeCountNotK(L, 1) == None)
assert(L == [5, 6]) # 5 and 6 are the elements that appear once in L
L = [1, 5, 1, 1, 2, 4, 2, 6, 4]
assert(removeCountNotK(L, 3) == None)
assert(L == [1]) # 1 is the only element that appears three times in L

print("... passed!")



def ct4():
 Cookie = make_dataclass('Cookie', ['name', 'tasty'])
 chocoCookie = Cookie(name='Chocolate Chip', tasty=10)
 print(isinstance(chocoCookie.name, Cookie))
 lastCookie, otherCookie = chocoCookie, copy.copy(chocoCookie)
 lastCookie.name = 'Cilantro'
 print(f"I like {otherCookie.name} cookies...")
 print(f"But I like {chocoCookie.name} cookies more!")
 print([lastCookie == c for c in (otherCookie, chocoCookie)])
ct4()



def isJespr(n):
  if n < 1000:
    return False
  
  biggestFour = 0

  while n > 1000:
    print('here')
    currFour = n % 10000

    if currFour > biggestFour:
      biggestFour = currFour

    n //= 10
    print(n)

  return isPrime(biggestFour)
    
def nthJespr(n):
  guess = 0
  count = 0

  while count <= n:
    guess += 1

    if isJespr(guess):
      count += 1
  print(guess)
  return guess

# assert(nthJespr(0) == 1009) # 1009 is prime
# assert(nthJespr(1234) == 11039) # 1103 is prime
#assert(nthJespr(2000) == 17433) # 7433 is prime
# assert(nthJespr(4242) == 36553) # 6553 is prime
# assert(nthJespr(12345) == 108087) # 8087 is prime
# assert(nthJespr(15112) == 131192) # 3119 is prime
# assert(nthJespr(66666) == 578807) # 8807 is prime
# assert(nthJespr(100000) == 883179) # 8831 is prime

def getNumMinesInDirection(L, row, col, drow, dcol):
  newRow = row + drow
  newCol = col + dcol

  if L[newRow][newCol] == 1:
    return 1
  else:
    return 0

def getNumMines(L, row, col, rows, cols):
  l, r, u, d = False, False, False, False
  se, sw, ne, nw = False, False ,False, False
  count = 0

  if row-1 >= 0:
    u = True
  if row+1 < rows:
    d = True
  if col-1 >= 0:
    l = True
  if col+1 < cols:
    r = True
  if l and u:
    nw = True
  if l and d:
    sw = True
  if r and u:
    ne = True
  if r and d:
    se = True

  if l:
    count += getNumMinesInDirection(L, row, col, 0, -1)
  if r:
    count += getNumMinesInDirection(L, row, col, 0, +1)
  if u:
    count += getNumMinesInDirection(L, row, col, -1, 0)
  if d:
    count += getNumMinesInDirection(L, row, col, +1, 0)
  if ne:
    count += getNumMinesInDirection(L, row, col, -1, +1)
  if se:
    count += getNumMinesInDirection(L, row, col, +1, +1)
  if nw:
    count += getNumMinesInDirection(L, row, col, -1, -1)
  if sw:
    count += getNumMinesInDirection(L, row, col, +1, -1)
  return count

def mineSweeper(L):
  rows = len(L)
  cols = len(L[0])
  newBoard = [[] for _ in range(rows)]

  for i in range(rows):
    for j in range(cols):
      if L[i][j] == 1:
        newBoard[i].append("X")
      else:
        newBoard[i].append(getNumMines(L, i, j, rows, cols))

  print(newBoard)
  return newBoard

L = [[0, 1, 1, 0],
     [0, 1, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 0]]

assert(mineSweeper(L) == [[2, "X", "X", 1],
[3, "X", 4 , 1],
[2, "X", 2 , 0],
[1, 1 , 1 , 0]])

L = [[1, 1, 1, 1],
     [0, 1, 0, 0],
     [0, 1, 0, 0],
     [0, 1, 0, 1]]

assert(mineSweeper(L) == [["X", "X", "X", "X"],
                          [4, "X", 5, 2],
                          [3, "X", 4, 1],
                          [2, "X", 3, "X"]])

def appStarted(app):
  app.cx = app.width/2


import copy
def ct1(n):
 w = set([])
 b = {1, 9}
 while n > 0:
  w.add(n % 10)
  b.add(n % 100 // 10 + 2)
  n //= 100
 l, o = w, copy.copy(b)
 for item in b:
  if (item - 1) % 5 != 4:
    o.remove(item)
  else:
    for i in range(-4, 3, 2):
      l.add(item + i)
  for quiz in (b, o, w, l):
    print(sorted(quiz))
print(ct1(37135))


def f1(L):
  if L == [ ]: 
    print("here")
    return 0
  if f1(L[1:]) > 0:
    return f1(L[1:]) - L[0]
  else:
    return f1(L[1:]) + L[0]

f1([2,3,5,9])

def ct1Helper(L, depth):
  print("+" * depth, L)
  if len(L) <= depth:
    result = set()

  else:
    mid = len(L) // 2
    front, back = L[:mid], L[mid:]

    if L[mid] % 2 == 1:
      result = ct1Helper(back, depth-1) 
      result.add(max(front))
    else:
      result = ct1Helper(front, depth+2)
      result.add(min(back))
  print("*" * depth, sorted(result))
  return result

def ct1(L):
  ct1Helper(L, 2)

print(ct1([4, 3, 1, 2, 0]))

def ctQS(L, d=1):
  if len(L) < 2:
    result = L
  else:
    p = L[0]
    a = [e for e in L if e < p]
    b = [e for e in L if e == p]
    c = [e for e in L if e > p]
    result = ctQS(a, d+1) + b + ctQS(c, d+1)
  print("!" * d, result)
  return result

print(ctQS([1, 5, 1, 1, 2]))

def ct1(n):
    if (n <= 0):
        return [ ]
    elif (n%10 >= 5):
        return [n] + ct1(n//2)
    else:
        return ct1(n-2) + [-n]
print(ct1(15))


def getBottomUpColumn(M, col):
  if col<0 or (len(M)>0 and col>len(M[0])-1) or len(M) == 0:
    return None
  return gBCUHelper(M, col)

def gBCUHelper(M, col, row = float("inf")):
  if row == float("inf"):
    row = len(M)-1
  if row < 0:
    return [ ]
  else:
    print(col)
    return [M[row][col]] + gBCUHelper(M, col, row-1)

def testGetBottomUpColumn():   
    print('Testing getBottomUpColumn()...', end='')
    print(getBottomUpColumn([[1,2,3],[4,5,6]], 0))
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 0) == [4, 1])
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 1) == [5, 2])  
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 2) == [6, 3])
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 3) == None)  
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], -1) == None) 
    print('Passed!')
    print('Note: We may grade your code with additional test cases')


testGetBottomUpColumn()


def evenRangeSum(lo, hi):
  if lo>hi:
    return 0
  else:
    if lo % 2 == 1:
      lo+=1
    return lo + evenRangeSum(lo+2, hi)

def testEvenRangeSum():
  print("Testing evenRangeSum()...", end = '')
  assert(evenRangeSum(2,6) == 12)
  assert(evenRangeSum(0,10) == 30)
  print(evenRangeSum(1,11))
  assert(evenRangeSum(1,11) == 30)
  assert(evenRangeSum(10,0) == 0)
  print("Passed")

testEvenRangeSum()


class Cookie(object):
  def __init__(self, flavor):
    self.flavor, self.toppings = flavor, []
  def addTopping(self, topping):
    self.toppings.append(topping)
  def __repr__(self):
    return f'{self.flavor} cookie with {len(self.toppings)} toppings'
  def __eq__(self, other):
    return isinstance(other, Cookie) and repr(self) == repr(other)

class SmolCookie(Cookie):
  def addTopping(self, topping):
    if len(self.toppings) == 2: self.toppings.pop(0)
    super().addTopping(topping)

def ct1():
 c1 = Cookie('Chocolate')
 c2 = SmolCookie('Chocolate')
 print(c1)
 c1.addTopping('garlic')
 c2.addTopping('cheese')
 print(c1 == c2, c2 == c1)
 for i in range(10):
  c2.addTopping('mayo')
 print(c2.toppings)
ct1()

def ct2(L):
  s = set(L)
  d1 = {}
  d2 = dict()
  for elem in s:
    d1[elem] = L.count(elem)
  print(d1)
  for key in d1:  
    if d1[key] in s:
      val = d1[key]
      d2[val] = d2.get(val, set())
      d2[val].add(key)
  return d2
print(ct2([1,1,1,2,4,4,5]))

[112]*-1

print([112]*-1)

def ct3(L, s=1, depth=1):
  if L == []:
    result = 0
  elif len(L) == 1:
    result = [L[0]] * s
  else:
    mid = len(L) // 2
    if mid % 2 == 0:
      newS = s
    else:
      newS = -s
    a = ct3(L[:mid], s, depth+1)
    b = ct3(L[mid:], newS, depth+1)
    result = a + b
  print('*' * depth, result)
  return result

L = [15, 112, 10]
print(ct3(L))

def vmc(L):
  s = set()
  for elem in L:
    if elem == L.count(elem):
      if elem not in s:
        s.add(elem)
  return s


def testVMC():
  print("Testing vmc...", end = '')
  assert(vmc([1,2,3,4,5]) == {1})
  assert(vmc([1,5,1,1,2]) == set())
  assert(vmc([5,2,5,2,5,6,5,1,5,0]) == {1,2,5})
  print("Passed!")
testVMC()

def ct2(d):
    s, t, u = set(), set(), set()
    for k in d:
        s.add(k)
        for v in d[k]:
            if v%2 == 0:
                t.add(v)
            else:
                u.add(v)
    return { min(s):t, max(s):u }
print(ct2({ 3:[1,2,4,1], 1:[5,5], 2:[0,5] }))

def ct3(n):
    if (n == 0):
        return (0, 1)
    else:
        x, y = ct3(n//10)
        if (n%2 == 0):
            return (x + (n%10), y)
        else:
            return (x, y * (n%10))
print(ct3(324508))

d = {1:{"he"}, 2:{"she", "it"}, 10:{"hehehehehe"}}
c = copy.deepcopy(d)
c[1010] = {"hoohwoehroewhro"}
print(c)

# This demos using modes (aka screens).

from cmu_112_graphics import *
import random

##########################################
# Splash Screen Mode
##########################################

def splashScreenMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='This demos a ModalApp!', font=font)
    canvas.create_text(app.width/2, 200, text='This is a modal splash screen!', font=font)
    canvas.create_text(app.width/2, 250, text='Press any key for the game!', font=font)

def splashScreenMode_keyPressed(app, event):
    app.mode = 'gameMode'

##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 20, text=f'Score: {app.score}', font=font)
    canvas.create_text(app.width/2, 60, text='Click on the dot!', font=font)
    canvas.create_text(app.width/2, 100, text='Press h for help screen!', font=font)
    canvas.create_text(app.width/2, 140, text='Press v for an MVC Violation!', font=font)
    canvas.create_oval(app.x-app.r, app.y-app.r, app.x+app.r, app.y+app.r,
                       fill=app.color)
    if app.makeAnMVCViolation:
        app.ohNo = 'This is an MVC Violation!'

def gameMode_timerFired(app):
    moveDot(app)

def gameMode_mousePressed(app, event):
    d = ((app.x - event.x)**2 + (app.y - event.y)**2)**0.5
    if (d <= app.r):
        app.score += 1
        randomizeDot(app)
    elif (app.score > 0):
        app.score -= 1

def gameMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
    elif (event.key == 'v'):
        app.makeAnMVCViolation = True

##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='This is the help screen!', font=font)
    canvas.create_text(app.width/2, 250, text='(Insert helpful message here)', font=font)
    canvas.create_text(app.width/2, 350, text='Press any key to return to the game!', font=font)

def helpMode_keyPressed(app, event):
    app.mode = 'gameMode'

##########################################
# Main App
##########################################

def appStarted(app):
    app.mode = 'splashScreenMode'
    app.score = 0
    app.timerDelay = 50
    app.makeAnMVCViolation = False
    randomizeDot(app)

def randomizeDot(app):
    app.x = random.randint(20, app.width-20)
    app.y = random.randint(20, app.height-20)
    app.r = random.randint(10, 20)
    app.color = random.choice(['red', 'orange', 'yellow', 'green', 'blue'])
    app.dx = random.choice([+1,-1])*random.randint(3,6)
    app.dy = random.choice([+1,-1])*random.randint(3,6)

def moveDot(app):
    app.x += app.dx
    if (app.x < 0) or (app.x > app.width): app.dx = -app.dx
    app.y += app.dy
    if (app.y < 0) or (app.y > app.height): app.dy = -app.dy

runApp(width=600, height=500)

# This demos app.getUserInput(prompt) and app.showMessage(message)

from cmu_112_graphics import *

def appStarted(app):
    app.message = 'Click the mouse to enter your name!'

def mousePressed(app, event):
    name = app.getUserInput('What is your name?')
    if (name == None):
        app.message = 'You canceled!'
    else:
        app.showMessage('You entered: ' + name)
        app.message = f'Hi, {name}!'

def redrawAll(app, canvas):
    font = 'Arial 24 bold'
    canvas.create_text(app.width/2,  app.height/2,
                       text=app.message, font=font)

runApp(width=500, height=300)

hwAverage = 99.9         # This is the number you see in autolab
quizAverage = 89       # The number in autolab will change a tiny bit because of TP1/TP2
midtermAverage = 90.3    # This is the number you see in autolab
final = midtermAverage # Can replace with a hypothetical final exam score or keep as the midterm average
tp = 80                # Replace with a hypothetical TP score

grade = (0.3 * hwAverage) + (0.1 * quizAverage) + (0.2 * midtermAverage) + (0.2 * final) + (0.2 * tp)

if grade >= 89.5:
   print("A", grade)
elif grade >= 79.5:
   print("B", grade)
elif grade >= 69.5:
   print("C", grade)
elif grade >= 59.5:
   print("D", grade)
else:
   print("R", grade)