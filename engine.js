// Practice Math engine: metronome ramp arithmetic - seconds at one tempo, total time across a ramp of tempos, and how far a time budget carries you. Exact integer milliseconds (rounded half up per stop), sums exact.
function _p(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,4}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _BPM = "each tempo must be a whole number from 20 to 400 BPM";
var _STEP = "the step must be a whole number from 1 to 100 BPM";
var _BEATS = "the beats per measure must be a whole number from 1 to 12";
var _MEAS = "the measures per stop must be a whole number from 1 to 64";
var _BUDGET = "the time budget must be a whole number from 1 to 600 minutes";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _ms(bpm, beats, meas) { return _hu(60000 * beats * meas, bpm); } // ms for one stop, half up
function _time(ms) {
  var s = _hu(ms, 1000), m = Math.floor(s / 60), r = s % 60;
  if (m === 0) return r + (r === 1 ? " second" : " seconds");
  if (r === 0) return m + (m === 1 ? " minute" : " minutes");
  return m + (m === 1 ? " minute" : " minutes") + " " + r + (r === 1 ? " second" : " seconds");
}
function _stops(start, end, step) {
  var n = Math.floor((end - start) / step) + 1, out = [];
  for (var i = 0; i < n; i++) out.push(start + i * step);
  return out;
}
function _in(start, end, step, beats, meas) {
  var a = _p(start, _BPM, 20, 400), b = _p(end, _BPM, 20, 400);
  if (b < a) throw new Error("the end tempo must not be below the start tempo");
  return { a: a, b: b, k: _p(step, _STEP, 1, 100), bt: _p(beats, _BEATS, 1, 12), m: _p(meas, _MEAS, 1, 64) };
}

function stopTruth(bpm, beats, meas) {
  var b = _p(bpm, _BPM, 20, 400), bt = _p(beats, _BEATS, 1, 12), m = _p(meas, _MEAS, 1, 64);
  var beats_total = bt * m;
  return "One stop of " + m + (m === 1 ? " measure" : " measures") + " at " + bt + (bt === 1 ? " beat" : " beats") + " each makes " + beats_total + (beats_total === 1 ? " beat" : " beats") + ", which at " + b + " BPM takes " + _time(_ms(b, bt, m)) + ".";
}
function rampTruth(start, end, step, beats, meas) {
  var p = _in(start, end, step, beats, meas), xs = _stops(p.a, p.b, p.k), tot = 0;
  for (var i = 0; i < xs.length; i++) tot += _ms(xs[i], p.bt, p.m);
  var s = "From " + p.a + " to " + p.b + " BPM in steps of " + p.k + " the ramp holds " + xs.length + (xs.length === 1 ? " stop" : " stops") + ". ";
  if (xs[xs.length - 1] !== p.b) s += "The steps never land on " + p.b + "; the last stop is " + xs[xs.length - 1] + " BPM. ";
  return s + "At " + p.m + (p.m === 1 ? " measure" : " measures") + " of " + p.bt + (p.bt === 1 ? " beat" : " beats") + " per stop the whole ramp takes " + _time(tot) + ".";
}
function budgetTruth(start, end, step, beats, meas, budget) {
  var p = _in(start, end, step, beats, meas), cap = _p(budget, _BUDGET, 1, 600) * 60000;
  var xs = _stops(p.a, p.b, p.k), tot = 0, done = 0;
  for (var i = 0; i < xs.length; i++) {
    var t = _ms(xs[i], p.bt, p.m);
    if (tot + t > cap) break;
    tot += t; done++;
  }
  var b = _p(budget, _BUDGET, 1, 600);
  var s = "With " + b + (b === 1 ? " minute" : " minutes") + " on the clock, ";
  if (done === 0) return s + "even the first stop at " + xs[0] + " BPM (" + _time(_ms(xs[0], p.bt, p.m)) + ") does not fit.";
  s += "you finish " + done + (done === 1 ? " stop" : " stops") + ", ending at " + xs[done - 1] + " BPM, in " + _time(tot) + ".";
  if (done === xs.length) return s + " That is the whole ramp, with " + _time(cap - tot) + " to spare.";
  return s + " The next stop at " + xs[done] + " BPM asks for " + _time(_ms(xs[done], p.bt, p.m)) + ".";
}
