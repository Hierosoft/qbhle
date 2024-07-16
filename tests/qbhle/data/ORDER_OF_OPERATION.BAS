PRINT "Started"
s = 7
t = 4 + s
x = 3 + 42 * (s - t)
REM Should be 0:
PRINT x + 165
' Should be -165:
PRINT x

t = s + 4
x = 3 + 42 * (s - t)
' Should be -165:
PRINT x

x = 3 + 42 * (t - s)
' Should be 171:
PRINT x

x = 3 + 42 * (t - s ^ 2)
' Should be -1593:
PRINT x

x = 3 + 42 - (t - s ^ 2)
' Should be 83:
PRINT x

x = 3 + 42 * (t - s ^ 2)
' Should be -1593:
PRINT x

x = 3 - 42 * (t - s ^ 2)
' Should be 1599:
PRINT x

x = .5 + .2
' Should be .7:
PRINT x

'DEFSTR': r'$',
'DEFINT': r'%',
'DEFLNG': r'&',
'DEFSNG': r'!',
'DEFDBL': r'#',

a$ = "1"
b% = 2
' ^ defaults to int32 so is mixed type since b% is int16 and
'   it should raise a type mismatch (?)
b% = 2%
c& = 3
c& = 3&
' float32 isn't quite .4 thanks to Intel, LOL
' (should be 0.4000000059604645):
d! = .4
d! = 0.4
d! = 0.4!
e# = .5
e# = 0.5
e# = 0.5#
' ID: r'[a-zA-Z_][a-zA-Z0-9_]*[$%&!\#]*'

f = d! + e#
' Should be .9 (It is even exact when using float32):
PRINT f

PRINT "Done"
