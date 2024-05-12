# QBHLE
QBHLE High-Level Emulator (formerly BluffBASIC)

Run QBasic programs using modern conventions.

High-level emulation (HLE) means avoiding overhead & complexity of emulating low-level operations, while potentially improving the quality. HLE is the way some console emulators run games and make them look better. Examples specific to QBHLE:
- Use a modern sound library when the BASIC code calls a DOS one.
- Use a modern Impulse Tracker parser and sound system when the program calls a DOS IT player.
- Use the mouse position from a modern game engine.
- Provide settings to enable various HLE behaviors such as:
  - Make shape commands (such as `CIRCLE`) draw vector or oversampled shapes.
- Underclocking! This makes programs work properly that otherwise could not. Making a DOSBOX just to underclock BASIC is overkill. So underclocking should be in the interpreter itself.


Related projects:
- https://github.com/Poikilos/bwsb

## Roadmap
0.1 BASIC lexer
   - See https://github.com/Hierosoft/qbhle/issues/1 for details and status.
0.9 QBasic 1.1 subset
   - baseline: my games
1.0 QuickBASIC 4.5 subset
   - baseline: DarkDread games
