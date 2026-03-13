/* ============================================================
   Shared Linked List Visualizer
   Renders a singly linked list as a chain of node boxes with arrows.
   ============================================================ */

class LinkedListVisualizer {
  constructor({ containerId, narrationId }) {
    this.container = document.getElementById(containerId);
    this.narration = document.getElementById(narrationId);
    this.nodes = []; // array of values representing the list
    this.steps = [];
    this.stepIdx = 0;
    this.isPlaying = false;
    this._playingPromise = null;
    this.speed = 1000;
  }

  setList(values) {
    this.nodes = [...values];
    this.steps = [];
    this.stepIdx = 0;
    this.isPlaying = false;
    this.render();
    this.narrate('List loaded.');
    this.updateButtons();
  }

  setSteps(steps) { this.steps = steps; this.stepIdx = 0; this.updateButtons(); }

  render(step) {
    while (this.container.firstChild) this.container.removeChild(this.container.firstChild);
    const data = (step && step.nodes) ? step.nodes : this.nodes;

    data.forEach((val, i) => {
      // Node box
      const node = document.createElement('div');
      node.style.cssText = 'display:flex;align-items:center;gap:0;flex-shrink:0;';

      const box = document.createElement('div');
      box.style.cssText = 'display:flex;flex-direction:column;align-items:center;';

      const valBox = document.createElement('div');
      valBox.className = 'array-cell-value';
      valBox.style.cssText += 'border-radius:6px;position:relative;';
      valBox.textContent = val;

      if (step && step.highlights && step.highlights[i]) {
        const cls = step.highlights[i];
        if (cls === 'active') { valBox.style.borderColor = 'var(--node-active)'; valBox.style.background = 'var(--red-light)'; }
        if (cls === 'settled') { valBox.style.borderColor = 'var(--node-settled)'; valBox.style.background = 'var(--green-light)'; }
        if (cls === 'swapping') { valBox.style.borderColor = 'var(--swap-glow)'; valBox.style.background = '#fef3c7'; }
      }

      box.appendChild(valBox);

      // Pointer label below node
      if (step && step.pointers) {
        const labels = [];
        for (const [name, idx] of Object.entries(step.pointers)) {
          if (idx === i) labels.push(name);
        }
        if (labels.length) {
          const lbl = document.createElement('div');
          lbl.style.cssText = 'font-family:var(--font-mono);font-size:0.6rem;color:var(--red);margin-top:2px;';
          lbl.textContent = labels.join(',');
          box.appendChild(lbl);
        }
      }

      node.appendChild(box);

      // Arrow to next
      if (i < data.length - 1) {
        const arrow = document.createElement('div');
        arrow.style.cssText = 'color:var(--ink-muted);font-size:1.2rem;margin:0 4px;';
        arrow.textContent = '\u2192';
        node.appendChild(arrow);
      }

      this.container.appendChild(node);
    });

    // Null terminator
    const nil = document.createElement('div');
    nil.style.cssText = 'font-family:var(--font-mono);font-size:0.75rem;color:var(--ink-muted);display:flex;align-items:center;margin-left:4px;';
    nil.textContent = '\u2192 null';
    this.container.appendChild(nil);

    if (step && step.nodes) this.nodes = [...step.nodes];
  }

  applyStep() {
    if (this.stepIdx >= this.steps.length) return;
    const step = this.steps[this.stepIdx];
    this.render(step);
    this.narrate(step.msg, 'Step ' + (this.stepIdx + 1) + '/' + this.steps.length);
    if (step.trackers) {
      for (const [key, val] of Object.entries(step.trackers)) {
        if (this.trackers && this.trackers[key]) this.trackers[key].textContent = val;
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
  resetSteps() { this.stepIdx = 0; this.render(); this.narrate('Reset.'); this.updateButtons(); }

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

  bindControls({ stepId, playId, pauseId, resetId, speedId }) {
    const stepBtn = document.getElementById(stepId);
    const playBtn = document.getElementById(playId);
    const pauseBtn = document.getElementById(pauseId);
    const resetBtn = document.getElementById(resetId);
    const speedSlider = document.getElementById(speedId);
    if (stepBtn) stepBtn.addEventListener('click', () => this.applyStep());
    if (playBtn) playBtn.addEventListener('click', () => this.playAll());
    if (pauseBtn) pauseBtn.addEventListener('click', () => this.pause());
    if (resetBtn) resetBtn.addEventListener('click', () => this.resetSteps());
    if (speedSlider) speedSlider.addEventListener('input', () => {
      this.speed = 1400 - parseInt(speedSlider.value, 10) * 240;
    });
    this._stepBtn = stepBtn;
    this._playBtn = playBtn;
    this._pauseBtn = pauseBtn;
  }

  trackers = {};
  registerTracker(key, elementId) { this.trackers[key] = document.getElementById(elementId); }

  updateButtons() {
    const has = this.stepIdx < this.steps.length;
    if (this._stepBtn) this._stepBtn.disabled = !has || this.isPlaying;
    if (this._playBtn) this._playBtn.disabled = !has || this.isPlaying;
    if (this._pauseBtn) this._pauseBtn.disabled = !this.isPlaying;
  }
}

/** Build scan steps for linked list traversal (length, min, max, sum, find, etc.) */
LinkedListVisualizer.buildScanSteps = function(nodes, { initTracked, compare, update, initMsg, visitMsg, updateMsg, doneMsg }) {
  const steps = [];
  if (nodes.length === 0) { steps.push({ nodes, highlights: {}, msg: 'Empty list.' }); return steps; }
  let tracked = initTracked(nodes[0]);
  let trackedIdx = 0;
  const h0 = {}; h0[0] = 'settled';
  steps.push({ nodes, highlights: h0, pointers: { curr: 0 }, trackers: { tracked: tracked }, msg: initMsg(nodes[0], tracked) });
  for (let i = 1; i < nodes.length; i++) {
    if (compare(nodes[i], tracked)) {
      const old = tracked;
      tracked = update(nodes[i], tracked);
      trackedIdx = i;
      const hi = {}; hi[i] = 'swapping';
      steps.push({ nodes, highlights: hi, pointers: { curr: i }, trackers: { tracked: tracked }, msg: updateMsg(i, nodes[i], old, tracked) });
    } else {
      const hi = {}; hi[i] = 'active'; hi[trackedIdx] = 'settled';
      steps.push({ nodes, highlights: hi, pointers: { curr: i }, trackers: { tracked: tracked }, msg: visitMsg(i, nodes[i], tracked) });
    }
  }
  const hf = {}; hf[trackedIdx] = 'settled';
  steps.push({ nodes, highlights: hf, pointers: {}, trackers: { tracked: tracked }, msg: doneMsg(tracked, trackedIdx) });
  return steps;
};
