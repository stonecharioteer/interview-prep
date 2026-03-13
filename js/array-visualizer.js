/* ============================================================
   Shared Array Visualizer
   Renders an array with scan/swap/pointer animations.
   Used by array, sorting, binary search, and other tutorials.
   ============================================================ */

class ArrayVisualizer {
  constructor({ containerId, narrationId, pointersId }) {
    this.container = document.getElementById(containerId);
    this.narration = document.getElementById(narrationId);
    this.pointersRow = pointersId ? document.getElementById(pointersId) : null;

    this.data = [];
    this.steps = [];
    this.stepIdx = 0;
    this.isPlaying = false;
    this._playingPromise = null;
    this.speed = 1000;
    this.trackers = {}; // { label: element } for custom tracker displays
  }

  /* ---- Data ---- */
  setData(arr) {
    this.data = [...arr];
    this.steps = [];
    this.stepIdx = 0;
    this.isPlaying = false;
    this.render();
    this.narrate('Array loaded. Click Step or Play to begin.');
    this.updateButtons();
  }

  setSteps(steps) {
    this.steps = steps;
    this.stepIdx = 0;
    this.updateButtons();
  }

  /* ---- Rendering ---- */
  render(step) {
    while (this.container.firstChild) this.container.removeChild(this.container.firstChild);
    if (this.pointersRow) while (this.pointersRow.firstChild) this.pointersRow.removeChild(this.pointersRow.firstChild);

    this.data.forEach((val, i) => {
      const cell = document.createElement('div');
      cell.className = 'array-cell';

      if (step && step.highlights) {
        const h = step.highlights[i];
        if (h) cell.classList.add(h); // 'active', 'settled', 'swapping'
      }

      const v = document.createElement('div');
      v.className = 'array-cell-value';
      v.textContent = val;
      cell.appendChild(v);

      const idx = document.createElement('div');
      idx.className = 'array-cell-index';
      idx.textContent = i;
      cell.appendChild(idx);

      this.container.appendChild(cell);

      // Pointer labels
      if (this.pointersRow) {
        const ptr = document.createElement('div');
        ptr.style.cssText = 'font-family:var(--font-mono);font-size:0.65rem;color:var(--red);text-align:center;width:40px;min-height:1.2em;';
        if (step && step.pointers) {
          const labels = [];
          for (const [name, idx2] of Object.entries(step.pointers)) {
            if (idx2 === i) labels.push(name);
          }
          if (labels.length) ptr.textContent = labels.join(',');
        }
        this.pointersRow.appendChild(ptr);
      }
    });
  }

  applyStep() {
    if (this.stepIdx >= this.steps.length) return;
    const step = this.steps[this.stepIdx];

    // Apply data changes if any
    if (step.data) this.data = [...step.data];

    this.render(step);
    this.narrate(step.msg, 'Step ' + (this.stepIdx + 1) + '/' + this.steps.length);

    // Update custom trackers
    if (step.trackers) {
      for (const [key, val] of Object.entries(step.trackers)) {
        if (this.trackers[key]) this.trackers[key].textContent = val;
      }
    }

    this.stepIdx++;
    this.updateButtons();
  }

  async playAll() {
    if (this.isPlaying) return this._playingPromise;
    this.isPlaying = true;
    this.updateButtons();
    this._playingPromise = (async () => {
      while (this.stepIdx < this.steps.length && this.isPlaying) {
        this.applyStep();
        await new Promise(r => setTimeout(r, this.speed));
      }
      this.isPlaying = false;
      this._playingPromise = null;
      this.updateButtons();
    })();
    return this._playingPromise;
  }

  pause() { this.isPlaying = false; this.updateButtons(); }

  reset() {
    this.stepIdx = 0;
    this.isPlaying = false;
    this.render();
    this.narrate('Reset. Click Step or Play to begin.');
    this.updateButtons();
  }

  /* ---- Narration ---- */
  narrate(msg, label) {
    if (!this.narration) return;
    while (this.narration.firstChild) this.narration.removeChild(this.narration.firstChild);
    if (label) {
      const s = document.createElement('span');
      s.className = 'step-num';
      s.textContent = label;
      this.narration.appendChild(s);
    }
    const m = document.createElement('span');
    m.textContent = msg;
    this.narration.appendChild(m);
    this.narration.style.animation = 'none';
    this.narration.offsetHeight;
    this.narration.style.animation = '';
  }

  /* ---- Controls ---- */
  bindControls({ stepId, playId, pauseId, resetId, speedId }) {
    const stepBtn = document.getElementById(stepId);
    const playBtn = document.getElementById(playId);
    const pauseBtn = document.getElementById(pauseId);
    const resetBtn = document.getElementById(resetId);
    const speedSlider = document.getElementById(speedId);

    if (stepBtn) stepBtn.addEventListener('click', () => this.applyStep());
    if (playBtn) playBtn.addEventListener('click', () => this.playAll());
    if (pauseBtn) pauseBtn.addEventListener('click', () => this.pause());
    if (resetBtn) resetBtn.addEventListener('click', () => this.reset());
    if (speedSlider) speedSlider.addEventListener('input', () => {
      this.speed = 1400 - parseInt(speedSlider.value, 10) * 240;
    });

    this._stepBtn = stepBtn;
    this._playBtn = playBtn;
    this._pauseBtn = pauseBtn;
  }

  registerTracker(key, elementId) {
    this.trackers[key] = document.getElementById(elementId);
  }

  updateButtons() {
    const has = this.stepIdx < this.steps.length;
    if (this._stepBtn) this._stepBtn.disabled = !has || this.isPlaying;
    if (this._playBtn) this._playBtn.disabled = !has || this.isPlaying;
    if (this._pauseBtn) this._pauseBtn.disabled = !this.isPlaying;
  }
}

/* ---- Step builders ---- */

/** Linear scan: track a value (min, max, sum, etc.) */
ArrayVisualizer.buildScanSteps = function(arr, { initVal, compare, updateFn, initMsg, scanMsg, updateMsg, skipMsg, doneMsg }) {
  const steps = [];
  if (arr.length === 0) return steps;

  let tracked = initVal(arr[0]);
  let trackedIdx = 0;
  const h0 = {};
  h0[0] = 'settled';
  steps.push({ highlights: h0, pointers: { scan: 0 }, trackers: { tracked: tracked, trackedIdx: 0 }, msg: initMsg(arr[0], tracked) });

  for (let i = 1; i < arr.length; i++) {
    if (compare(arr[i], tracked)) {
      const old = tracked;
      tracked = updateFn(arr[i], tracked);
      trackedIdx = i;
      const hi = {};
      hi[i] = 'swapping';
      for (let j = 0; j < arr.length; j++) if (j === trackedIdx && j !== i) hi[j] = 'settled';
      steps.push({ highlights: hi, pointers: { scan: i }, trackers: { tracked: tracked, trackedIdx: trackedIdx }, msg: updateMsg(i, arr[i], old, tracked) });
    } else {
      const hi = {};
      hi[i] = 'active';
      hi[trackedIdx] = 'settled';
      steps.push({ highlights: hi, pointers: { scan: i }, trackers: { tracked: tracked, trackedIdx: trackedIdx }, msg: skipMsg(i, arr[i], tracked) });
    }
  }

  const hf = {};
  hf[trackedIdx] = 'settled';
  steps.push({ highlights: hf, pointers: {}, trackers: { tracked: tracked, trackedIdx: trackedIdx }, msg: doneMsg(tracked, trackedIdx) });
  return steps;
};

/** Two-pointer swap steps (for reverse, partition, etc.) */
ArrayVisualizer.buildTwoPointerSwapSteps = function(arr, { leftStart, rightStart, shouldSwap, swapMsg, noSwapMsg, doneMsg, advanceMsg }) {
  const steps = [];
  const data = [...arr];
  let left = leftStart !== undefined ? leftStart : 0;
  let right = rightStart !== undefined ? rightStart : data.length - 1;

  while (left < right) {
    // Show pointers
    const hi1 = {};
    hi1[left] = 'active';
    hi1[right] = 'active';
    steps.push({ data: [...data], highlights: hi1, pointers: { L: left, R: right },
      msg: (shouldSwap ? shouldSwap(data, left, right) : true)
        ? swapMsg(data, left, right)
        : noSwapMsg(data, left, right) });

    if (!shouldSwap || shouldSwap(data, left, right)) {
      [data[left], data[right]] = [data[right], data[left]];
      const hi2 = {};
      hi2[left] = 'swapping';
      hi2[right] = 'swapping';
      steps.push({ data: [...data], highlights: hi2, pointers: { L: left, R: right },
        msg: advanceMsg ? advanceMsg(data, left, right) : `Swapped. Move pointers inward.` });
    }
    left++;
    right--;
  }

  const hf = {};
  for (let i = 0; i < data.length; i++) hf[i] = 'settled';
  steps.push({ data: [...data], highlights: hf, pointers: {}, msg: doneMsg(data) });
  return steps;
};

/** Binary search steps */
ArrayVisualizer.buildBinarySearchSteps = function(arr, target, { variant }) {
  const steps = [];
  const data = [...arr];
  let lo = 0, hi = data.length - 1;
  let result = -1;

  while (lo <= hi) {
    const mid = Math.floor((lo + hi) / 2);
    const h = {};
    for (let i = lo; i <= hi; i++) h[i] = 'active';
    h[mid] = 'swapping';
    steps.push({ highlights: h, pointers: { lo: lo, mid: mid, hi: hi },
      msg: `Search range [${lo}..${hi}], mid=${mid}, arr[${mid}]=${data[mid]}.` });

    if (data[mid] === target) {
      result = mid;
      if (variant === 'first') { hi = mid - 1; }
      else if (variant === 'last') { lo = mid + 1; }
      else {
        const hf = {}; hf[mid] = 'settled';
        steps.push({ highlights: hf, pointers: { found: mid }, msg: `Found ${target} at index ${mid}!` });
        return steps;
      }
      const hf2 = {}; hf2[mid] = 'settled';
      steps.push({ highlights: hf2, pointers: variant === 'first' ? { lo: lo, hi: hi, best: mid } : { lo: lo, hi: hi, best: mid },
        msg: `Found ${target} at ${mid}. Continue searching ${variant === 'first' ? 'left' : 'right'} for ${variant} occurrence.` });
    } else if (data[mid] < target) {
      lo = mid + 1;
      steps.push({ highlights: h, pointers: { lo: lo, hi: hi },
        msg: `${data[mid]} < ${target}. Move lo to ${lo}.` });
    } else {
      hi = mid - 1;
      steps.push({ highlights: h, pointers: { lo: lo, hi: hi },
        msg: `${data[mid]} > ${target}. Move hi to ${hi}.` });
    }
  }

  if (result >= 0) {
    const hf = {}; hf[result] = 'settled';
    steps.push({ highlights: hf, pointers: { result: result }, msg: `${variant === 'first' ? 'First' : 'Last'} occurrence of ${target} is at index ${result}.` });
  } else {
    steps.push({ highlights: {}, pointers: {}, msg: `${target} not found in the array.` });
  }
  return steps;
};
