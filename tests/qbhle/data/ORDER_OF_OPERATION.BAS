s = 7
t = 11
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
