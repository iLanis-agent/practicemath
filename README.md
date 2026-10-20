# Practice Math

Metronome ramp arithmetic. One stop of 8 measures at 60 BPM takes 32 seconds. The full ramp from 60 to 120 BPM in steps of 5 takes 4 minutes 50 seconds across 13 stops.

## What it computes

- **The stop truth** - how long one stop on the metronome takes: measures (1 to 64) times beats per measure (1 to 12) against the tempo (20 to 400 BPM).
- **The ramp truth** - the stops in a tempo ramp (start, end, step) and the total time across the whole ramp, noting when the steps never land on the end tempo.
- **The budget truth** - how far up the ramp a block of practice time (1 to 600 minutes) carries you, and what the next stop asks for.

## Boundary

Arithmetic only. The tempos, steps, measures and time budget are the owner's own entries, and it only counts beats. It has not heard anyone play and does not know the instrument, the level, the piece, or whether a tempo or a ramp is right, and it gives no verdict on playing or progress. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integer milliseconds, half-up per stop, exact sums).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/practicemath/
Repo: https://github.com/iLanis-agent/practicemath
