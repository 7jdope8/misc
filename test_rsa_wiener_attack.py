#!/usr/bin/env python3
# RSA wiener attack
# https://github.com/orisano/owiener
# https://en.wikipedia.org/wiki/Continued_fraction
# Author Dario Clavijo 2020
# GPLv3

import gmpy2

def cont_frac(a,b):
  coef=[]
  i = a//b
  while b != 0:
    r = a//b
    i = r
    coef.append(i)
    f = a - i*b
    a = b
    b = f
  return coef

def convergents(e):
    n = [] # Nominators
    d = [] # Denominators

    for i in range(len(e)):
        if i == 0:
            ni = e[i]
            di = 1
        elif i == 1:
            ni = e[i]*e[i-1] + 1
            di = e[i]
        else: # i > 1
            ni = e[i]*n[i-1] + n[i-2]
            di = e[i]*d[i-1] + d[i-2]

        n.append(ni)
        d.append(di)
        yield (ni, di)

def quadratic_solve(a,b,c):
  disc = (b**2) - (4*a*c)
  if disc >0:
    a2 = (2*a)
    x0= (-b + gmpy2.isqrt(disc))//a2
    x1= (-b - gmpy2.isqrt(disc))//a2
    return x0,x1

def wiener(e,N):
  tmp = []
  for pk,pd in convergents(cont_frac(e,N)):
    if pk > 0:
      phi = (e*pd - 1)//pk
      b = N-phi+1 # (p-1)*(q-1) = (p*q)-(p-q)+1 = N-(p-q)+1 
      x = quadratic_solve(1,-b,N)
      if x != None:
        if N % x[0] == 0 or N % x[1] == 0:
          return x

tests = []
tests.append((649,200))
tests.append((2621,8927))
tests.append((17993,90581))
tests.append((6792605526025, 9449868410449))
tests.append((30749686305802061816334591167284030734478031427751495527922388099381921172620569310945418007467306454160014597828390709770861577479329793948103408489494025272834473555854835044153374978554414416305012267643957838998648651100705446875979573675767605387333733876537528353237076626094553367977134079292593746416875606876735717905892280664538346000950343671655257046364067221469807138232820446015769882472160551840052921930357988334306659120253114790638496480092361951536576427295789429197483597859657977832368912534761100269065509351345050758943674651053419982561094432258103614830448382949765459939698951824447818497599,109966163992903243770643456296093759130737510333736483352345488643432614201030629970207047930115652268531222079508230987041869779760776072105738457123387124961036111210544028669181361694095594938869077306417325203381820822917059651429857093388618818437282624857927551285811542685269229705594166370426152128895901914709902037365652575730201897361139518816164746228733410283595236405985958414491372301878718635708605256444921222945267625853091126691358833453283744166617463257821375566155675868452032401961727814314481343467702299949407935602389342183536222842556906657001984320973035314726867840698884052182976760066141))

def test(tests):
  for e,N in tests:
    x = wiener(e,N)
    if x != None:
      if N == x[0]*x[1]:
        print ("e = %d\nN = %d = %d * %d" % (e,N,x[0],x[1]))
test(tests)