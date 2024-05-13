
from http://web.ukonline.co.uk/sinclair.zx81/chap05.html 8/8/2007

In some dialects of BASIC you must always enclose the arguments of a function on brackets. This is not the case in ZX81 8K BASIC. 

SGN 	The sign function (sometimes called signum to avoid confusion with SIN). The result is -1, 0 or +1 according as the argument is negative, zero or positive.
ABS 	The absolute value, or modulus. The result is the argument made positive, so that

       ABS -3.2 = ABS 3.2 = 3.2 
SIN 	*
COS 	*
TAN 	*
ASN 	arcsin *
ACS 	arccos *
ATN 	arctan *
LN 	natural logarithm (to base 2.718281828459045..., alias e)
EXP 	exponential function
SQR 	square root
INT 	integer part. This always rounds down, so INT 3.9 = 3 & INT -3.9 = -4. (An integer is a whole number, possibly negative.)
PI 	= 3.1415265358979..., the girth in cubits of a circle one cubit across. PI has no argument. (Only ten digits of this are actually stored in the computer, & only eight will be displayed.)
RND 	Neither has RND an argument. It yields a random number between 0 (which value it can take) & 1 (which it cannot).
