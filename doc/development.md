# QBHLE Development Notes

## Tasks
(formerly 1.Notes.txt in qjak folder)

- make BKeyword object that stores info on the keyword (type, etc)
- create public string ReadWord() that gets the word and moves the cursor
- '%' sign at end of var denotes integer! '$' is string, '!' is SINGLE, '&' is LONG, none or '#' is DOUBLE.
- ';' at end of a PRINT line keeps it from wrapping! IMPORTANT when writing on last line else scrolling is applied to whole graphics buffer
- add LET statement (or delete all) - same with CALL
- add # to the end of everything that is not anything not declared as function/sub, nor has other suffix, nor is a statement, nor is in quotes (no multiline quotes allowed), nor is a comment
- allow X=9.987654321 : PRINT USING "#####.###"; X;
- debugger
- warn on:
  - duplicate names that have different or missing suffixes
  - use of unassigned variables
  - functions with void return (i.e. FunctionName=x never happens)
  - converting to boolean
  - argument modified by function (allowed, but can sometimes be a mistake)
  - mismatched for loop variables, or even detect decrement, step, etc.
- error on:
  - assignment of boolean used as a conditional
  - "+="-style operators
