# Practice Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from fractions import Fraction

BPM = "each tempo must be a whole number from 20 to 400 BPM"
STEP = "the step must be a whole number from 1 to 100 BPM"
BEATS = "the beats per measure must be a whole number from 1 to 12"
MEAS = "the measures per stop must be a whole number from 1 to 64"
BUDGET = "the time budget must be a whole number from 1 to 600 minutes"

def p(t, err, lo, hi):
    t = t.strip()
    if not t.isdigit() or len(t) > 4:
        raise ValueError(err)
    v = int(t)
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def ms(bpm, beats, meas):
    return int(hu(Fraction(60000) * beats * meas, bpm))

def time_s(msv):
    s = hu(msv, 1000); m, r = s // 60, s % 60
    if m == 0: return str(r) + (" second" if r == 1 else " seconds")
    if r == 0: return str(m) + (" minute" if m == 1 else " minutes")
    return str(m) + (" minute" if m == 1 else " minutes") + " " + str(r) + (" second" if r == 1 else " seconds")

def stops(a, b, k):
    return [a + i * k for i in range((b - a) // k + 1)]

def inn(start, end, step, beats, meas):
    a = p(start, BPM, 20, 400); b = p(end, BPM, 20, 400)
    if b < a:
        raise ValueError("the end tempo must not be below the start tempo")
    return a, b, p(step, STEP, 1, 100), p(beats, BEATS, 1, 12), p(meas, MEAS, 1, 64)

def stopTruth(bpm, beats, meas):
    b = p(bpm, BPM, 20, 400); bt = p(beats, BEATS, 1, 12); m = p(meas, MEAS, 1, 64)
    tot = bt * m
    return "One stop of " + str(m) + (" measure" if m == 1 else " measures") + " at " + str(bt) + (" beat" if bt == 1 else " beats") + " each makes " + str(tot) + (" beat" if tot == 1 else " beats") + ", which at " + str(b) + " BPM takes " + time_s(ms(b, bt, m)) + "."

def rampTruth(start, end, step, beats, meas):
    a, b, k, bt, m = inn(start, end, step, beats, meas)
    xs = stops(a, b, k); tot = sum(ms(x, bt, m) for x in xs)
    s = "From " + str(a) + " to " + str(b) + " BPM in steps of " + str(k) + " the ramp holds " + str(len(xs)) + (" stop" if len(xs) == 1 else " stops") + ". "
    if xs[-1] != b:
        s += "The steps never land on " + str(b) + "; the last stop is " + str(xs[-1]) + " BPM. "
    return s + "At " + str(m) + (" measure" if m == 1 else " measures") + " of " + str(bt) + (" beat" if bt == 1 else " beats") + " per stop the whole ramp takes " + time_s(tot) + "."

def budgetTruth(start, end, step, beats, meas, budget):
    a, b, k, bt, m = inn(start, end, step, beats, meas)
    cap = p(budget, BUDGET, 1, 600) * 60000
    xs = stops(a, b, k); tot = 0; done = 0
    for x in xs:
        t = ms(x, bt, m)
        if tot + t > cap: break
        tot += t; done += 1
    bb = p(budget, BUDGET, 1, 600)
    s = "With " + str(bb) + (" minute" if bb == 1 else " minutes") + " on the clock, "
    if done == 0:
        return s + "even the first stop at " + str(xs[0]) + " BPM (" + time_s(ms(xs[0], bt, m)) + ") does not fit."
    s += "you finish " + str(done) + (" stop" if done == 1 else " stops") + ", ending at " + str(xs[done - 1]) + " BPM, in " + time_s(tot) + "."
    if done == len(xs):
        return s + " That is the whole ramp, with " + time_s(cap - tot) + " to spare."
    return s + " The next stop at " + str(xs[done]) + " BPM asks for " + time_s(ms(xs[done], bt, m)) + "."

FNS = {"stopTruth": stopTruth, "rampTruth": rampTruth, "budgetTruth": budgetTruth}

cases = []
starts = ["20", "60", "100", "240", "399"]
ends = ["60", "120", "240", "400"]
steps = ["1", "5", "7", "33", "100"]
beats = ["1", "3", "4", "7", "12"]
measures = ["1", "2", "8", "33", "64"]
for s in starts:
    for e in ends:
        for k in steps:
            cases.append(("rampTruth", [s, e, k, "4", "8"]))
for b in beats:
    for m in measures:
        cases.append(("stopTruth", ["60", b, m]))
cases.append(("stopTruth", ["20", "12", "64"]))
cases.append(("stopTruth", ["400", "1", "1"]))
for bud in ["1", "2", "5", "10", "600"]:
    cases.append(("budgetTruth", ["60", "120", "5", "4", "8", bud]))
cases.append(("budgetTruth", ["20", "400", "100", "12", "64", "1"]))
cases.append(("budgetTruth", ["60", "60", "1", "4", "8", "600"]))
errs = ["19", "401", "0", "20.5", "x", ""]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for bad in errs:
    for name, args in [("stopTruth", [bad, "4", "8"]), ("rampTruth", [bad, "120", "5", "4", "8"]),
                       ("rampTruth", ["60", bad, "5", "4", "8"]), ("rampTruth", ["60", "120", bad, "4", "8"]),
                       ("rampTruth", ["60", "120", "5", bad, "8"]), ("rampTruth", ["60", "120", "5", "4", bad]),
                       ("budgetTruth", ["60", "120", "5", "4", "8", bad]), ("rampTruth", ["120", "60", "5", "4", "8"])]:
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
