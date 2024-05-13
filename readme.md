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
  - Probably (the GDM parser part only) should be rewritten in Python and then use high-level calls to play samples.
    - Or just convert everything to ogg manually and use such files if present...HLE at its finest.
- [PC-BASIC](https://github.com/robhagemans/pcbasic) (Python!) "interpreter for GW-BASIC, Advanced BASIC (BASICA), PCjr Cartridge Basic and Tandy 1000 GWBASIC. It interprets these BASIC dialects with a high degree of accuracy, aiming for bug-for-bug compatibility" using pysdl2
  - Uses a custom parser
  - "runs plain-text, tokenised and protected .BAS files"
  - "implements floating-point arithmetic in the Microsoft Binary Format (MBF) and can therefore read and write binary data files created by GW-BASIC"
- QB64: Very good modern QBasic compiler, but requires slight changes to programs since behavior slightly varies from QBasic 1.1:
  - `CHAIN` (switching to another BAS file) doesn't work
  - Runs `SOUND` commands asynchronously (my programs requires sync calls since sounds are sometimes used as precise delays)


## Roadmap
- [ ] 0.1 lex & parse BASIC
  - See https://github.com/Hierosoft/qbhle/issues/1 for details and status.
- [ ] 0.9 QBasic 1.1 subset
  - baseline: https://github.com/Hierosoft/qjak
- [ ] 1.0 QuickBASIC 4.5 subset
  - baseline: DarkDread games

### Other ideas:
- See [Issues](https://github.com/Hierosoft/qbhle/issues) tagged with "enhancement"
