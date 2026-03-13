/* ============================================================
   Min-Heap Interactive Visualizer
   Renders a binary tree (SVG) + array representation side-by-side
   with step-by-step animated insertions and bubble-up operations.
   ============================================================ */

class MinHeapVisualizer {
  constructor({ treeSvgId, arrayContainerId, narrationId, controlsId, buttonIds }) {
    this.treeSvg = document.getElementById(treeSvgId);
    this.arrayContainer = document.getElementById(arrayContainerId);
    this.narration = document.getElementById(narrationId);
    this.controlsContainer = controlsId ? document.getElementById(controlsId) : null;
    this._buttonIds = buttonIds || {}; // optional override for scoped button IDs

    this.heap = [];
    this.stepQueue = [];
    this.isPlaying = false;
    this.animSpeed = 1000; // ms per step
    this.stepIndex = 0;
    this.totalSteps = 0;

    // Tree layout constants
    this.nodeRadius = 22;
    this.levelGap = 65;
    this.svgWidth = 420;
    this.svgHeight = 320;

    this.treeSvg.setAttribute('viewBox', `0 0 ${this.svgWidth} ${this.svgHeight}`);

    this._initControls();
    this._render();
    this._narrate('Empty heap. Add values to begin.');
  }

  /* ---- Public API ---- */

  /** Insert a value with animated bubble-up steps (auto-plays). */
  async insert(value) {
    // If currently animating, stop and finish remaining steps instantly
    if (this.isPlaying) {
      this.isPlaying = false;
      // Wait a tick for the playing loop to exit
      await this._sleep(0);
      // Apply remaining steps instantly
      while (this.stepIndex < this.stepQueue.length) {
        this._applyStep(this.stepQueue[this.stepIndex]);
        this.stepIndex++;
      }
    }
    this._queueInsert(value);
    this.playAll();
  }

  /** Queue insert steps without auto-playing. */
  _queueInsert(value) {
    const steps = this._computeInsertSteps(value);
    this.stepQueue = steps;
    this.stepIndex = 0;
    this.totalSteps = steps.length;
    this._updateControlStates();
  }

  /** Insert a value instantly (no animation). */
  insertImmediate(value) {
    this.heap.push(value);
    let i = this.heap.length - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (this.heap[parent] > this.heap[i]) {
        [this.heap[parent], this.heap[i]] = [this.heap[i], this.heap[parent]];
        i = parent;
      } else break;
    }
    this._render();
  }

  /** Reset the heap to empty. */
  reset() {
    this.heap = [];
    this.stepQueue = [];
    this.stepIndex = 0;
    this.isPlaying = false;
    this._render();
    this._narrate('Heap cleared. Add values to begin.');
    this._updateControlStates();
  }

  /** Run the preset demo sequence. */
  async runDemo() {
    this.reset();
    const values = [15, 10, 20, 8, 12, 25, 5];
    for (const val of values) {
      this._queueInsert(val);
      await this._playAllAndWait();
      await this._sleep(300);
    }
    this._narrate('Demo complete! The min-heap property holds: every parent \u2264 its children.');
  }

  /** Step forward one step. */
  stepForward() {
    if (this.stepIndex < this.stepQueue.length) {
      this._applyStep(this.stepQueue[this.stepIndex]);
      this.stepIndex++;
      this._updateControlStates();
    }
  }

  /** Play all remaining steps automatically. Returns when done. */
  async playAll() {
    if (this.isPlaying) return this._playingPromise;
    this._playingPromise = this._doPlayAll();
    return this._playingPromise;
  }

  async _doPlayAll() {
    this.isPlaying = true;
    this._updateControlStates();
    while (this.stepIndex < this.stepQueue.length && this.isPlaying) {
      this._applyStep(this.stepQueue[this.stepIndex]);
      this.stepIndex++;
      this._updateControlStates();
      await this._sleep(this.animSpeed);
    }
    this.isPlaying = false;
    this._playingPromise = null;
    this._updateControlStates();
  }

  /** Queue insert and play, returning a promise that resolves when done. */
  async _playAllAndWait() {
    return this.playAll();
  }

  /** Pause auto-play. */
  pause() {
    this.isPlaying = false;
    this._updateControlStates();
  }

  /* ---- Step computation ---- */

  _computeInsertSteps(value) {
    const steps = [];
    const heapCopy = [...this.heap];

    // Step 1: append to end
    heapCopy.push(value);
    steps.push({
      type: 'append',
      heap: [...heapCopy],
      activeIndex: heapCopy.length - 1,
      message: `Append ${value} at index ${heapCopy.length - 1} (end of array).`,
    });

    // Bubble up
    let i = heapCopy.length - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (heapCopy[parent] > heapCopy[i]) {
        steps.push({
          type: 'compare',
          heap: [...heapCopy],
          activeIndex: i,
          compareIndex: parent,
          message: `Compare ${heapCopy[i]} (index ${i}) with parent ${heapCopy[parent]} (index ${parent}). ${heapCopy[i]} < ${heapCopy[parent]}, so swap.`,
        });

        [heapCopy[parent], heapCopy[i]] = [heapCopy[i], heapCopy[parent]];

        steps.push({
          type: 'swap',
          heap: [...heapCopy],
          activeIndex: parent,
          swappedFrom: i,
          message: `Swapped! ${heapCopy[parent]} is now at index ${parent}.`,
        });

        i = parent;
      } else {
        steps.push({
          type: 'settled',
          heap: [...heapCopy],
          activeIndex: i,
          compareIndex: parent,
          message: `Compare ${heapCopy[i]} (index ${i}) with parent ${heapCopy[parent]} (index ${parent}). ${heapCopy[i]} \u2265 ${heapCopy[parent]}, heap property satisfied!`,
        });
        break;
      }
    }

    if (i === 0 && heapCopy.length > 1) {
      steps.push({
        type: 'settled',
        heap: [...heapCopy],
        activeIndex: 0,
        message: `${heapCopy[0]} reached the root. Insertion complete!`,
      });
    }

    if (heapCopy.length === 1) {
      steps.push({
        type: 'settled',
        heap: [...heapCopy],
        activeIndex: 0,
        message: `${heapCopy[0]} is the only element, it's at the root. Done!`,
      });
    }

    return steps;
  }

  _applyStep(step) {
    this.heap = [...step.heap];
    this._renderTree(step);
    this._renderArray(step);
    this._narrate(step.message, `${this.stepIndex + 1}/${this.totalSteps}`);
    // Re-attach hover after last step
    if (step.type === 'settled' && this._hoverEnabled && this.stepIndex + 1 >= this.stepQueue.length) {
      setTimeout(() => this._attachHoverListeners(), 100);
    }
  }

  /* ---- Rendering ---- */

  _render(step) {
    this._renderTree(step);
    this._renderArray(step);
    // Re-attach hover listeners after re-render (only when not animating)
    if (!step && this._hoverEnabled) {
      this._attachHoverListeners();
    }
  }

  _renderTree(step) {
    // Clear SVG
    while (this.treeSvg.firstChild) {
      this.treeSvg.removeChild(this.treeSvg.firstChild);
    }

    if (this.heap.length === 0) {
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', this.svgWidth / 2);
      text.setAttribute('y', this.svgHeight / 2);
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('fill', '#8a8a9e');
      text.setAttribute('font-family', 'IBM Plex Mono, monospace');
      text.setAttribute('font-size', '14');
      text.textContent = 'Empty heap';
      this.treeSvg.appendChild(text);
      return;
    }

    const positions = this._computePositions();

    // Draw edges first (behind nodes)
    for (let i = 1; i < this.heap.length; i++) {
      const parent = Math.floor((i - 1) / 2);
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', positions[parent].x);
      line.setAttribute('y1', positions[parent].y);
      line.setAttribute('x2', positions[i].x);
      line.setAttribute('y2', positions[i].y);
      line.setAttribute('class', 'edge');

      if (step && (
        (step.activeIndex === i && step.compareIndex === parent) ||
        (step.activeIndex === parent && step.swappedFrom === i)
      )) {
        line.classList.add('highlight');
      }

      this.treeSvg.appendChild(line);
    }

    // Draw nodes
    for (let i = 0; i < this.heap.length; i++) {
      const pos = positions[i];
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');

      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', pos.x);
      circle.setAttribute('cy', pos.y);
      circle.setAttribute('r', this.nodeRadius);
      circle.setAttribute('class', 'node-circle');

      if (step) {
        if (step.type === 'append' && i === step.activeIndex) {
          circle.classList.add('active');
          circle.style.animation = 'nodeAppear 0.4s ease both';
        } else if (step.type === 'compare' && (i === step.activeIndex || i === step.compareIndex)) {
          circle.classList.add('active');
        } else if (step.type === 'swap' && (i === step.activeIndex || i === step.swappedFrom)) {
          circle.classList.add('swapping');
        } else if (step.type === 'settled' && i === step.activeIndex) {
          circle.classList.add('settled');
          circle.style.animation = 'settleGlow 0.6s ease';
        }
      }

      g.appendChild(circle);

      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', pos.x);
      text.setAttribute('y', pos.y);
      text.setAttribute('class', 'node-text');
      text.textContent = this.heap[i];
      g.appendChild(text);

      // Index label below node
      const idxLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      idxLabel.setAttribute('x', pos.x);
      idxLabel.setAttribute('y', pos.y + this.nodeRadius + 13);
      idxLabel.setAttribute('class', 'index-label');
      idxLabel.textContent = '[' + i + ']';
      g.appendChild(idxLabel);

      this.treeSvg.appendChild(g);
    }
  }

  _renderArray(step) {
    // Clear
    while (this.arrayContainer.firstChild) {
      this.arrayContainer.removeChild(this.arrayContainer.firstChild);
    }

    if (this.heap.length === 0) {
      const empty = document.createElement('div');
      empty.style.cssText = 'color: #8a8a9e; font-family: IBM Plex Mono, monospace; font-size: 0.85rem;';
      empty.textContent = '[ ]';
      this.arrayContainer.appendChild(empty);
      return;
    }

    this.heap.forEach((val, i) => {
      const cell = document.createElement('div');
      cell.className = 'array-cell';

      if (step) {
        if ((step.type === 'append' || step.type === 'compare') && i === step.activeIndex) {
          cell.classList.add('active');
        } else if (step.type === 'compare' && i === step.compareIndex) {
          cell.classList.add('active');
        } else if (step.type === 'swap' && (i === step.activeIndex || i === step.swappedFrom)) {
          cell.classList.add('swapping');
        } else if (step.type === 'settled' && i === step.activeIndex) {
          cell.classList.add('settled');
        }
      }

      const valDiv = document.createElement('div');
      valDiv.className = 'array-cell-value';
      valDiv.textContent = val;
      cell.appendChild(valDiv);

      const idxDiv = document.createElement('div');
      idxDiv.className = 'array-cell-index';
      idxDiv.textContent = i;
      cell.appendChild(idxDiv);

      this.arrayContainer.appendChild(cell);
    });
  }

  _computePositions() {
    const positions = [];
    const n = this.heap.length;

    for (let i = 0; i < n; i++) {
      const level = Math.floor(Math.log2(i + 1));
      const nodesAtLevel = Math.pow(2, level);
      const indexInLevel = i - (nodesAtLevel - 1);

      // Total possible at this level
      const totalWidth = this.svgWidth - 40;
      const spacing = totalWidth / nodesAtLevel;
      const x = 20 + spacing * (indexInLevel + 0.5);
      const y = 40 + level * this.levelGap;

      positions.push({ x, y });
    }

    return positions;
  }

  /* ---- Controls ---- */

  _initControls() {
    if (!this.controlsContainer && !this._buttonIds.step) return; // no controls for this instance
    // Buttons are already in HTML, just wire them up
    const ids = this._buttonIds;
    const stepBtn = document.getElementById(ids.step || 'btn-step');
    const playBtn = document.getElementById(ids.play || 'btn-play');
    const pauseBtn = document.getElementById(ids.pause || 'btn-pause');
    const resetBtn = document.getElementById(ids.reset || 'btn-reset');
    const demoBtn = document.getElementById(ids.demo || 'btn-demo');
    const addBtn = document.getElementById(ids.add || 'btn-add');
    const valueInput = document.getElementById(ids.input || 'input-value');
    const speedSlider = document.getElementById(ids.speed || 'speed-slider');

    if (stepBtn) stepBtn.addEventListener('click', () => this.stepForward());
    if (playBtn) playBtn.addEventListener('click', () => this.playAll());
    if (pauseBtn) pauseBtn.addEventListener('click', () => this.pause());
    if (resetBtn) resetBtn.addEventListener('click', () => this.reset());
    if (demoBtn) demoBtn.addEventListener('click', () => this.runDemo());

    if (addBtn && valueInput) {
      const doAdd = () => {
        const val = parseInt(valueInput.value, 10);
        if (!isNaN(val)) {
          this.insert(val);
          valueInput.value = '';
          valueInput.focus();
        }
      };
      addBtn.addEventListener('click', doAdd);
      valueInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') doAdd();
      });
    }

    if (speedSlider) {
      speedSlider.addEventListener('input', () => {
        // Slider 1 (slow) to 5 (fast): map to 1200ms..200ms
        this.animSpeed = 1400 - (parseInt(speedSlider.value, 10) * 240);
      });
    }
  }

  _updateControlStates() {
    const stepBtn = document.getElementById('btn-step');
    const playBtn = document.getElementById('btn-play');
    const pauseBtn = document.getElementById('btn-pause');

    const hasSteps = this.stepIndex < this.stepQueue.length;

    if (stepBtn) stepBtn.disabled = !hasSteps || this.isPlaying;
    if (playBtn) playBtn.disabled = !hasSteps || this.isPlaying;
    if (pauseBtn) pauseBtn.disabled = !this.isPlaying;
  }

  /* ---- Narration ---- */

  _narrate(message, stepLabel) {
    if (!this.narration) return;
    // Clear and rebuild
    while (this.narration.firstChild) {
      this.narration.removeChild(this.narration.firstChild);
    }

    if (stepLabel) {
      const stepSpan = document.createElement('span');
      stepSpan.className = 'step-num';
      stepSpan.textContent = 'Step ' + stepLabel;
      this.narration.appendChild(stepSpan);
    }

    const msgSpan = document.createElement('span');
    msgSpan.textContent = message;
    this.narration.appendChild(msgSpan);

    // Re-trigger animation
    this.narration.style.animation = 'none';
    this.narration.offsetHeight; // force reflow
    this.narration.style.animation = '';
  }

  /* ---- Interactive Hover: Explore Heap Relationships ---- */

  /**
   * Enable hover exploration on array cells and tree nodes.
   * Hovering a node highlights:
   *   - The node itself (blue/active)
   *   - Its parent (green/settled) — "I must be ≥ this"
   *   - Its children (amber) — "These must be ≥ me"
   * Plus a tooltip showing the relationship.
   */
  enableHoverExploration() {
    this._hoverEnabled = true;
    // Re-render to attach hover listeners
    this._render();
  }

  _attachHoverListeners() {
    if (!this._hoverEnabled || this.heap.length === 0) return;

    // Attach to array cells
    const cells = this.arrayContainer.querySelectorAll('.array-cell');
    cells.forEach((cell, i) => {
      cell.style.cursor = 'pointer';
      cell.addEventListener('mouseenter', () => this._highlightRelationships(i));
      cell.addEventListener('mouseleave', () => this._clearRelationshipHighlights());
    });

    // Attach to tree node groups
    const nodeGroups = this.treeSvg.querySelectorAll('g');
    const nodeGroupArr = Array.from(nodeGroups);
    nodeGroupArr.forEach((g, i) => {
      g.style.cursor = 'pointer';
      g.addEventListener('mouseenter', () => this._highlightRelationships(i));
      g.addEventListener('mouseleave', () => this._clearRelationshipHighlights());
    });
  }

  _highlightRelationships(index) {
    if (index >= this.heap.length) return;
    const parentIdx = index > 0 ? Math.floor((index - 1) / 2) : -1;
    const leftChild = 2 * index + 1;
    const rightChild = 2 * index + 2;

    // Build relationship description
    const val = this.heap[index];
    let desc = `Node ${val} at [${index}]`;
    if (parentIdx >= 0) {
      desc += ` — must be ≥ parent ${this.heap[parentIdx]}`;
    } else {
      desc += ` — root (no parent)`;
    }
    if (leftChild < this.heap.length) {
      desc += ` | children: ${this.heap[leftChild]}`;
      if (rightChild < this.heap.length) desc += `, ${this.heap[rightChild]}`;
      desc += ` must be ≥ ${val}`;
    }

    // Highlight array cells
    const cells = this.arrayContainer.querySelectorAll('.array-cell');
    cells.forEach((cell, i) => {
      cell.classList.remove('active', 'settled', 'swapping', 'heap-hover-parent', 'heap-hover-child', 'heap-hover-self');
      if (i === index) {
        cell.classList.add('active');
      } else if (i === parentIdx) {
        cell.classList.add('settled');
      } else if (i === leftChild || i === rightChild) {
        cell.classList.add('swapping');
      }
    });

    // Highlight tree nodes
    const circles = this.treeSvg.querySelectorAll('.node-circle');
    circles.forEach((circle, i) => {
      circle.classList.remove('active', 'settled', 'swapping');
      if (i === index) {
        circle.classList.add('active');
      } else if (i === parentIdx) {
        circle.classList.add('settled');
      } else if (i === leftChild || i === rightChild) {
        circle.classList.add('swapping');
      }
    });

    // Highlight edges
    const edges = this.treeSvg.querySelectorAll('.edge');
    edges.forEach(edge => edge.classList.remove('highlight'));
    // Edge from parent to this node
    if (parentIdx >= 0 && index < this.heap.length) {
      // Edge index: edges are drawn for nodes 1..n-1, so edge at index-1 corresponds to node index
      if (index - 1 >= 0 && index - 1 < edges.length) {
        edges[index - 1].classList.add('highlight');
      }
    }
    // Edges to children
    if (leftChild < this.heap.length && leftChild - 1 < edges.length) {
      edges[leftChild - 1].classList.add('highlight');
    }
    if (rightChild < this.heap.length && rightChild - 1 < edges.length) {
      edges[rightChild - 1].classList.add('highlight');
    }

    // Show relationship in narration
    this._narrate(desc);
  }

  _clearRelationshipHighlights() {
    // Clear array highlights
    const cells = this.arrayContainer.querySelectorAll('.array-cell');
    cells.forEach(cell => {
      cell.classList.remove('active', 'settled', 'swapping');
    });
    // Clear tree highlights
    const circles = this.treeSvg.querySelectorAll('.node-circle');
    circles.forEach(c => c.classList.remove('active', 'settled', 'swapping'));
    const edges = this.treeSvg.querySelectorAll('.edge');
    edges.forEach(e => e.classList.remove('highlight'));
    // Restore narration
    this._narrate('Hover over any node to explore heap relationships.');
  }

  /* ---- Utilities ---- */

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
