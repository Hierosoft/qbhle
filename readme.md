# qbhle
QBHLE High-Level Emulator (formerly BluffBASIC) is for running QBASIC programs like console emulators run games:

Project status: planning
- I've done a lot of work on parsers, and learned I should be using an existing lexer and/or parser system instead to avoid repeating work
  - or ANTLR or Lark, but in this case, YACC since there is a pure Python implementation which prevents cross-platform maintenance issues. See <https://github.com/Hierosoft/qbhle/issues/1>.

High-level emulation means improving the quality or convenience of the program while avoiding overhead & complexity of emulating low-level operations. In practice:
- Use a modern sound library when the BASIC code calls a DOS one.
- Use a modern Impulse Tracker parser when the program calls a DOS one.
- Use the mouse position from a game engine when DOS mouse position memory address is read (There is some kind of multiplication necessary on one axis, so the output should be divided by 2 before returned to the program).
- ...You get the idea.

Targets:
- QBasic 1.1 subset
  - baseline: my games
- QuickBASIC 4.5 subset
  - baseline: DarkDread games
