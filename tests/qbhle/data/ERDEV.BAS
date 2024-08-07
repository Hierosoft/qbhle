' Error handling example from
' https://www.qbasic.net/en/reference/qb11/Statement/ON-ERROR.htm
'Illustrates ERDEV, ERDEV$, ERL, ERR, ERROR, ON ERROR, and RESUME.
   ON ERROR GOTO Handler
10 CHDIR "a:\"                'Causes ERR 71 "Disk not ready"
                              'if no disk in Drive A.
20 y% = 0
30 x% = 5 / y%                'ERR 11 "Division by zero."
40 PRINT "x% ="; x%
50 ERROR 57                   'ERR 57 "Device I/O error."

Handler:
  PRINT
  PRINT "Error "; ERR; " on line "; ERL
  SELECT CASE ERR
    CASE 71
      PRINT "Using device "; ERDEV$; " device error code = "; ERDEV
      RESUME NEXT
    CASE 11
      INPUT "What value do you want to divide by"; y%
      RESUME                  'Retry line 30 with new value of y%.
    CASE ELSE
      PRINT "Unexpected error, ending program."
      END
  END SELECT