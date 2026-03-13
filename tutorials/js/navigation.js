/* ============================================================
   DSA Visual Tutorials — Navigation & TOC
   ============================================================ */

// Apply saved theme immediately (before DOM renders) to prevent flash
(function() {
  var t = localStorage.getItem('dsa-theme');
  if (t === 'light') document.documentElement.setAttribute('data-theme', 'light');
})();

// All 211 exercises grouped by topic (in curriculum order)
const EXERCISES = [
  { topic: "Arrays", exercises: [
    { id: 1, name: "Min" }, { id: 2, name: "Max" }, { id: 3, name: "Sum" },
    { id: 4, name: "Contains" }, { id: 5, name: "Average" }, { id: 6, name: "Count of value" },
    { id: 20, name: "Find index" }, { id: 21, name: "Find all indices" },
    { id: 23, name: "Reversed copy" }, { id: 26, name: "Reverse in place" },
    { id: 29, name: "Is sorted?" }, { id: 37, name: "Binary search" },
    { id: 46, name: "Merge sorted" }, { id: 56, name: "Rotate by k" },
    { id: 61, name: "Two sum" }, { id: 69, name: "Remove duplicates (sorted)" },
    { id: 75, name: "Partition by pivot" }, { id: 83, name: "Sliding window sum" },
    { id: 96, name: "Max subarray sum" }, { id: 140, name: "Longest consecutive sequence" },
  ]},
  { topic: "Linked List", exercises: [
    { id: 7, name: "Length" }, { id: 8, name: "Find" }, { id: 9, name: "Min" },
    { id: 10, name: "Max" }, { id: 11, name: "Sum" }, { id: 12, name: "Average" },
    { id: 13, name: "Count of value" }, { id: 22, name: "Get kth element" },
    { id: 24, name: "Append" }, { id: 27, name: "Prepend" },
    { id: 32, name: "Remove first match" }, { id: 41, name: "Insert at index" },
    { id: 50, name: "Remove at index" }, { id: 57, name: "Reverse (iterative)" },
    { id: 63, name: "Middle node" }, { id: 70, name: "Detect cycle" },
    { id: 78, name: "Merge sorted" }, { id: 86, name: "Nth from end" },
  ]},
  { topic: "Stack", exercises: [
    { id: 14, name: "Define, push, pop, peek" },
    { id: 25, name: "Valid parentheses" },
    { id: 34, name: "Evaluate expression" },
    { id: 54, name: "Min stack" },
  ]},
  { topic: "Queue", exercises: [
    { id: 15, name: "Define, enqueue, dequeue, peek" },
    { id: 28, name: "Implement using two stacks" },
  ]},
  { topic: "Recursion", exercises: [
    { id: 16, name: "Factorial" }, { id: 17, name: "Factorial (memoized)" },
    { id: 18, name: "Sum array" }, { id: 19, name: "Reverse string" },
    { id: 48, name: "Power" }, { id: 49, name: "Power (memoized)" },
    { id: 97, name: "Fibonacci (recursive)" }, { id: 98, name: "Fibonacci (memoized)" },
  ]},
  { topic: "Sorting", exercises: [
    { id: 30, name: "Bubble sort" }, { id: 31, name: "Selection sort" },
    { id: 33, name: "Insertion sort" }, { id: 47, name: "Merge sort" },
    { id: 76, name: "Quick sort" }, { id: 194, name: "Counting sort" },
    { id: 199, name: "Radix sort" },
  ]},
  { topic: "Bits", exercises: [
    { id: 35, name: "Is power of two?" }, { id: 36, name: "Count set bits" },
    { id: 55, name: "Find the unique number" },
    { id: 105, name: "Get / set / clear bit" },
    { id: 192, name: "Subsets via bitmask" },
  ]},
  { topic: "Binary Search", exercises: [
    { id: 38, name: "First occurrence" }, { id: 39, name: "Last occurrence" },
    { id: 40, name: "Search insert position" },
    { id: 141, name: "Search rotated sorted array" },
    { id: 147, name: "Min in rotated sorted array" },
    { id: 170, name: "Find peak element" },
    { id: 181, name: "Koko eating bananas" },
    { id: 190, name: "Capacity to ship packages" },
  ]},
  { topic: "Maps (dict)", exercises: [
    { id: 42, name: "Get or default" }, { id: 51, name: "Increment count" },
    { id: 58, name: "Merge counts" }, { id: 64, name: "Most common key" },
    { id: 71, name: "Invert mapping" }, { id: 79, name: "First non-repeating" },
  ]},
  { topic: "Math", exercises: [
    { id: 43, name: "Greatest common divisor" }, { id: 44, name: "Least common multiple" },
    { id: 52, name: "Is prime?" }, { id: 93, name: "Find all primes up to n" },
    { id: 198, name: "Fast exponentiation" },
  ]},
  { topic: "Trees (Binary)", exercises: [
    { id: 45, name: "Define node" },
    { id: 53, name: "Preorder traversal" }, { id: 59, name: "Inorder traversal" },
    { id: 66, name: "Postorder traversal" }, { id: 72, name: "Level-order traversal" },
    { id: 80, name: "Size" }, { id: 89, name: "Height" },
    { id: 101, name: "Contains" }, { id: 103, name: "Min" },
    { id: 104, name: "Max" }, { id: 110, name: "Sum" },
    { id: 111, name: "Average" }, { id: 112, name: "Count of value" },
    { id: 159, name: "Is balanced?" }, { id: 166, name: "Is symmetric?" },
    { id: 175, name: "Diameter" }, { id: 182, name: "Serialize / deserialize" },
  ]},
  { topic: "Heap", exercises: [
    { id: 60, name: "Min-heap: define & insert", hasContent: true, file: "heap-min-insert.html" },
    { id: 67, name: "Min-heap: extract min" },
    { id: 73, name: "Min-heap: peek & size" },
    { id: 81, name: "Build heap from array" },
    { id: 90, name: "Heap sort" },
    { id: 106, name: "Max-heap (convert min to max)" },
    { id: 113, name: "Kth largest element" },
    { id: 123, name: "Kth smallest element" },
    { id: 134, name: "Merge two heaps" },
    { id: 135, name: "Merge k sorted lists" },
    { id: 146, name: "Top k frequent elements" },
    { id: 161, name: "Sliding window maximum" },
  ]},
  { topic: "Two Pointers", exercises: [
    { id: 62, name: "Two sum (sorted)" },
    { id: 65, name: "Three sum" },
    { id: 68, name: "Container with most water" },
  ]},
  { topic: "Trie", exercises: [
    { id: 74, name: "Define TrieNode" }, { id: 82, name: "Insert word" },
    { id: 92, name: "Search word" }, { id: 107, name: "Starts with" },
    { id: 116, name: "Count words with prefix" }, { id: 125, name: "Delete word" },
    { id: 136, name: "Autocomplete" }, { id: 152, name: "Count total words" },
    { id: 167, name: "Longest common prefix" },
  ]},
  { topic: "Monotonic Stack", exercises: [
    { id: 77, name: "Next greater element" }, { id: 85, name: "Next smaller element" },
    { id: 160, name: "Daily temperatures" },
    { id: 162, name: "Largest rectangle in histogram" },
    { id: 168, name: "Trapping rain water" },
  ]},
  { topic: "Sliding Window", exercises: [
    { id: 84, name: "Max sum subarray of size k" },
    { id: 87, name: "Longest substring with k distinct" },
    { id: 102, name: "Longest substring without repeating" },
    { id: 108, name: "Minimum window substring" },
  ]},
  { topic: "Backtracking", exercises: [
    { id: 88, name: "Generate subsets" }, { id: 91, name: "Generate permutations" },
    { id: 95, name: "Generate combinations" }, { id: 118, name: "Generate parentheses" },
    { id: 143, name: "N-queens" }, { id: 158, name: "Sudoku solver" },
    { id: 186, name: "Word search" },
    { id: 203, name: "Combination sum" }, { id: 205, name: "Combination sum II" },
  ]},
  { topic: "Graph", exercises: [
    { id: 94, name: "Define adjacency list" }, { id: 109, name: "Add edge" },
    { id: 117, name: "Has edge & neighbors" },
    { id: 126, name: "DFS traversal" }, { id: 138, name: "BFS traversal" },
    { id: 149, name: "Is connected?" }, { id: 153, name: "Detect cycle (directed)" },
    { id: 157, name: "Detect cycle (undirected)" },
    { id: 163, name: "Shortest path (BFS)" },
    { id: 171, name: "Topological sort (BFS)" },
    { id: 173, name: "Topological sort (DFS)" },
    { id: 178, name: "Count connected components" },
    { id: 185, name: "Bipartite check" },
    { id: 191, name: "Shortest path (weighted)" },
    { id: 196, name: "Minimum spanning tree (edge sort)" },
    { id: 197, name: "All-pairs shortest path" },
    { id: 201, name: "Minimum spanning tree (grow)" },
  ]},
  { topic: "Dynamic Programming", exercises: [
    { id: 99, name: "Fibonacci (tabulation)" }, { id: 100, name: "Climbing stairs" },
    { id: 114, name: "House robber" }, { id: 119, name: "Min cost climbing stairs" },
    { id: 124, name: "Coin change" }, { id: 128, name: "Coin change II" },
    { id: 137, name: "Longest increasing subsequence" },
    { id: 142, name: "Unique paths" }, { id: 151, name: "Unique paths with obstacles" },
    { id: 155, name: "Min path sum" },
    { id: 164, name: "Longest common subsequence" },
    { id: 169, name: "Longest palindromic substring" },
    { id: 176, name: "Longest palindromic subsequence" },
    { id: 180, name: "Edit distance" },
    { id: 183, name: "House robber III" }, { id: 187, name: "Word break" },
    { id: 189, name: "Max path sum (tree)" },
    { id: 193, name: "0/1 Knapsack" },
    { id: 195, name: "Partition equal subset sum" },
    { id: 200, name: "Matrix chain multiplication" },
    { id: 202, name: "Burst balloons" },
    { id: 204, name: "Shortest tour (bitmask)" },
  ]},
  { topic: "Greedy", exercises: [
    { id: 115, name: "Jump game" }, { id: 120, name: "Jump game II" },
    { id: 133, name: "Merge intervals" }, { id: 139, name: "Insert interval" },
    { id: 145, name: "Meeting rooms" }, { id: 154, name: "Meeting rooms II" },
    { id: 172, name: "Gas station" }, { id: 179, name: "Activity selection" },
    { id: 188, name: "Fractional knapsack" },
  ]},
  { topic: "Trees (BST)", exercises: [
    { id: 121, name: "Insert" }, { id: 122, name: "Search" },
    { id: 130, name: "Delete" }, { id: 132, name: "Validate BST" },
    { id: 144, name: "Inorder successor" }, { id: 150, name: "Lowest common ancestor" },
  ]},
  { topic: "Union-Find", exercises: [
    { id: 127, name: "Basic find & union" }, { id: 129, name: "Path compression" },
    { id: 131, name: "Union by rank" },
    { id: 148, name: "Count connected components" },
    { id: 156, name: "Detect cycle (undirected)" },
  ]},
  { topic: "String Matching", exercises: [
    { id: 165, name: "Naive pattern search" },
    { id: 174, name: "Build prefix table" },
    { id: 177, name: "Fast pattern search" },
    { id: 184, name: "Hash-based pattern search" },
  ]},
  { topic: "Conversions", exercises: [
    { id: 206, name: "List to linked list" },
    { id: 207, name: "Linked list to list" },
    { id: 208, name: "BST to sorted array" },
    { id: 209, name: "Sorted array to balanced BST" },
    { id: 210, name: "Adjacency list to matrix" },
    { id: 211, name: "Adjacency matrix to list" },
  ]},
];

// Which exercises have tutorial content
const CONTENT_MAP = {
  // Arrays
  1: "exercises/array-min.html",
  2: "exercises/array-max.html",
  3: "exercises/array-sum.html",
  4: "exercises/array-contains.html",
  5: "exercises/array-average.html",
  6: "exercises/array-count-of.html",
  20: "exercises/array-find-index.html",
  21: "exercises/array-find-all-indices.html",
  23: "exercises/array-reversed-copy.html",
  26: "exercises/array-reverse-in-place.html",
  29: "exercises/array-is-sorted.html",
  37: "exercises/array-binary-search.html",
  46: "exercises/array-merge-sorted.html",
  56: "exercises/array-rotate-k.html",
  61: "exercises/array-two-sum.html",
  69: "exercises/array-remove-dupes-sorted.html",
  75: "exercises/array-partition-pivot.html",
  83: "exercises/array-sliding-window-sum.html",
  96: "exercises/array-kadane.html",
  // Linked list
  7: "exercises/ll-length.html",
  8: "exercises/ll-find.html",
  9: "exercises/ll-min.html",
  10: "exercises/ll-max.html",
  11: "exercises/ll-sum.html",
  12: "exercises/ll-average.html",
  13: "exercises/ll-count-of.html",
  22: "exercises/ll-get-kth.html",
  24: "exercises/ll-append.html",
  27: "exercises/ll-prepend.html",
  32: "exercises/ll-remove-first.html",
  41: "exercises/ll-insert-at-index.html",
  50: "exercises/ll-remove-at-index.html",
  57: "exercises/ll-reverse.html",
  63: "exercises/ll-middle-node.html",
  70: "exercises/ll-detect-cycle.html",
  78: "exercises/ll-merge-sorted.html",
  86: "exercises/ll-nth-from-end.html",
  // Stack
  14: "exercises/stack-define.html",
  25: "exercises/stack-valid-parens.html",
  34: "exercises/stack-evaluate-postfix.html",
  54: "exercises/stack-min-stack.html",
  // Queue
  15: "exercises/queue-define.html",
  28: "exercises/queue-two-stacks.html",
  // Recursion
  16: "exercises/recursion-factorial.html",
  17: "exercises/recursion-factorial-memo.html",
  18: "exercises/recursion-sum-array.html",
  19: "exercises/recursion-reverse-string.html",
  48: "exercises/recursion-power.html",
  49: "exercises/recursion-power-memo.html",
  97: "exercises/recursion-fibonacci.html",
  98: "exercises/recursion-fibonacci-memo.html",
  // Sorting
  30: "exercises/sorting-bubble.html",
  31: "exercises/sorting-selection.html",
  33: "exercises/sorting-insertion.html",
  47: "exercises/sorting-merge.html",
  76: "exercises/sorting-quicksort.html",
  // Bits
  35: "exercises/bits-power-of-two.html",
  36: "exercises/bits-count-set.html",
  55: "exercises/bits-single-number.html",
  105: "exercises/bits-get-set-clear.html",
  // Binary search
  38: "exercises/bsearch-first-occurrence.html",
  39: "exercises/bsearch-last-occurrence.html",
  40: "exercises/bsearch-insert-position.html",
  // Maps
  42: "exercises/maps-get-or-default.html",
  51: "exercises/maps-increment-count.html",
  58: "exercises/maps-merge-counts.html",
  64: "exercises/maps-most-common.html",
  71: "exercises/maps-invert.html",
  79: "exercises/maps-first-non-repeating.html",
  // Math
  43: "exercises/math-gcd.html",
  44: "exercises/math-lcm.html",
  52: "exercises/math-is-prime.html",
  93: "exercises/math-sieve.html",
  // Trees
  45: "exercises/tree-define-node.html",
  53: "exercises/tree-preorder.html",
  59: "exercises/tree-inorder.html",
  66: "exercises/tree-postorder.html",
  72: "exercises/tree-level-order.html",
  80: "exercises/tree-size.html",
  89: "exercises/tree-height.html",
  101: "exercises/tree-contains.html",
  103: "exercises/tree-min.html",
  104: "exercises/tree-max.html",
  110: "exercises/tree-sum.html",
  111: "exercises/tree-average.html",
  112: "exercises/tree-count-of.html",
  159: "exercises/tree-is-balanced.html",
  166: "exercises/tree-is-symmetric.html",
  175: "exercises/tree-diameter.html",
  182: "exercises/tree-serialize.html",
  // Heap
  60: "exercises/heap-min-insert.html",
  67: "exercises/heap-extract-min.html",
  73: "exercises/heap-peek-size.html",
  81: "exercises/heap-heapify.html",
  90: "exercises/heap-sort.html",
  106: "exercises/heap-max-heap.html",
  113: "exercises/heap-kth-largest.html",
  123: "exercises/heap-kth-smallest.html",
  134: "exercises/heap-merge.html",
  135: "exercises/heap-merge-k-lists.html",
  146: "exercises/heap-top-k-frequent.html",
  161: "exercises/heap-sliding-window-max.html",
  // Two Pointers
  62: "exercises/tp-two-sum-sorted.html",
  65: "exercises/tp-three-sum.html",
  68: "exercises/tp-container-water.html",
  // Trie
  74: "exercises/trie-define.html",
  82: "exercises/trie-insert.html",
  92: "exercises/trie-search.html",
  107: "exercises/trie-starts-with.html",
  116: "exercises/trie-count-prefix.html",
  125: "exercises/trie-delete.html",
  136: "exercises/trie-autocomplete.html",
  152: "exercises/trie-count-words.html",
  167: "exercises/trie-longest-common-prefix.html",
  // Trees (BST)
  121: "exercises/bst-insert.html",
  122: "exercises/bst-search.html",
  130: "exercises/bst-delete.html",
  132: "exercises/bst-validate.html",
  144: "exercises/bst-inorder-successor.html",
  150: "exercises/bst-lca.html",
  // Monotonic Stack
  77: "exercises/mstack-next-greater.html",
  85: "exercises/mstack-next-smaller.html",
  // Sliding Window
  84: "exercises/sw-max-sum-subarray-k.html",
  87: "exercises/sw-longest-k-distinct.html",
  102: "exercises/sw-longest-no-repeat.html",
  108: "exercises/sw-min-window-substring.html",
  // Backtracking
  88: "exercises/bt-generate-subsets.html",
  91: "exercises/bt-permutations.html",
  95: "exercises/bt-combinations.html",
  // Graph
  94: "exercises/graph-adjacency-list.html",
  109: "exercises/graph-add-edge.html",
  // Dynamic Programming
  99: "exercises/dp-fibonacci-tabulation.html",
  100: "exercises/dp-climbing-stairs.html",
};

// Flatten all exercises with topic info, sorted by ID
function _flatExercises() {
  const flat = [];
  EXERCISES.forEach(group => {
    group.exercises.forEach(ex => {
      flat.push({ id: ex.id, name: ex.name, topic: group.topic, hasContent: ex.hasContent, file: ex.file });
    });
  });
  flat.sort((a, b) => a.id - b.id);
  return flat;
}

let _sidebarGrouped = localStorage.getItem('sidebar-grouped') === 'true'; // default: flat (by #)

/**
 * Build the sidebar navigation from EXERCISES data.
 * Supports grouped (by topic) and flat (sorted by ID) modes.
 */
function buildSidebar() {
  const nav = document.getElementById('sidebar-nav');
  if (!nav) return;

  const currentPage = window.location.pathname.split('/').pop();
  const inExercisesDir = window.location.pathname.includes('/exercises/');

  // Wrap search input if not already wrapped
  const searchInput = document.getElementById('sidebar-search');
  if (searchInput && !searchInput.parentElement.classList.contains('sidebar-search-wrap')) {
    const wrap = document.createElement('div');
    wrap.className = 'sidebar-search-wrap';
    searchInput.parentNode.insertBefore(wrap, searchInput);
    wrap.appendChild(searchInput);
  }

  // Segmented toggle goes in the header (fixed area), not the scrollable nav
  const header = document.querySelector('.sidebar-header');
  let toggleWrap = header ? header.querySelector('.sidebar-toggle-mode') : null;
  if (header && !toggleWrap) {
    toggleWrap = document.createElement('div');
    toggleWrap.className = 'sidebar-toggle-mode';
    const btnGrouped = document.createElement('button');
    btnGrouped.textContent = 'By Topic';
    if (_sidebarGrouped) btnGrouped.className = 'active-mode';
    const btnFlat = document.createElement('button');
    btnFlat.textContent = 'By #';
    if (!_sidebarGrouped) btnFlat.className = 'active-mode';

    function switchMode(grouped) {
      _sidebarGrouped = grouped;
      localStorage.setItem('sidebar-grouped', _sidebarGrouped);
      buildSidebar();
      initSearch();
    }
    btnGrouped.addEventListener('click', () => switchMode(true));
    btnFlat.addEventListener('click', () => switchMode(false));
    toggleWrap.appendChild(btnGrouped);
    toggleWrap.appendChild(btnFlat);
    header.appendChild(toggleWrap);
  } else if (toggleWrap) {
    // Update active state on existing toggle
    const btns = toggleWrap.querySelectorAll('button');
    btns[0].className = _sidebarGrouped ? 'active-mode' : '';
    btns[1].className = !_sidebarGrouped ? 'active-mode' : '';
  }

  // Clear existing content in the scrollable nav area
  while (nav.firstChild) nav.removeChild(nav.firstChild);

  if (_sidebarGrouped) {
    _buildGroupedSidebar(nav, currentPage, inExercisesDir);
  } else {
    _buildFlatSidebar(nav, currentPage, inExercisesDir);
  }
}

function _makeExerciseLink(ex, topic, currentPage, inExercisesDir, showTopic) {
  const hasContent = !!CONTENT_MAP[ex.id];
  let href = hasContent
    ? CONTENT_MAP[ex.id]
    : 'exercises/placeholder.html?id=' + ex.id + '&name=' + encodeURIComponent(ex.name) + '&topic=' + encodeURIComponent(topic);

  if (inExercisesDir && href.startsWith('exercises/')) {
    href = href.replace('exercises/', '');
  }

  const a = document.createElement('a');
  a.className = 'exercise-link';
  a.href = href;

  const isActive = hasContent && currentPage === href.split('/').pop().split('?')[0];
  if (isActive) a.classList.add('active');

  const numSpan = document.createElement('span');
  numSpan.className = 'ex-num';
  numSpan.textContent = ex.id;
  a.appendChild(numSpan);

  const nameSpan = document.createElement('span');
  nameSpan.className = 'ex-name';
  // Insert <wbr> after underscores so long snake_case names wrap at meaningful points
  const parts = ex.name.split('_');
  parts.forEach((part, i) => {
    if (i > 0) {
      nameSpan.appendChild(document.createTextNode('_'));
      nameSpan.appendChild(document.createElement('wbr'));
    }
    nameSpan.appendChild(document.createTextNode(part));
  });
  a.appendChild(nameSpan);

  if (showTopic) {
    const topicSpan = document.createElement('span');
    topicSpan.style.cssText = 'font-size:0.6rem;color:var(--ink-muted);opacity:0.7;flex-shrink:0;white-space:nowrap;';
    topicSpan.textContent = topic;
    a.appendChild(topicSpan);
  }

  if (hasContent) {
    const badge = document.createElement('span');
    badge.className = 'badge-ready';
    a.appendChild(badge);
  }

  return a;
}

function _buildGroupedSidebar(nav, currentPage, inExercisesDir) {
  EXERCISES.forEach(group => {
    const div = document.createElement('div');
    div.className = 'topic-group';

    const label = document.createElement('div');
    label.className = 'topic-label';
    const labelTextSpan = document.createElement('span');
    labelTextSpan.textContent = group.topic + ' ';
    const countSpan = document.createElement('span');
    countSpan.className = 'topic-count';
    countSpan.textContent = '(' + group.exercises.length + ')';
    labelTextSpan.appendChild(countSpan);
    const chevron = document.createElement('span');
    chevron.className = 'chevron';
    chevron.textContent = '\u25BC';
    label.appendChild(labelTextSpan);
    label.appendChild(chevron);
    label.addEventListener('click', () => div.classList.toggle('collapsed'));
    div.appendChild(label);

    const ul = document.createElement('ul');
    ul.className = 'topic-exercises';

    group.exercises.forEach(ex => {
      const li = document.createElement('li');
      li.appendChild(_makeExerciseLink(ex, group.topic, currentPage, inExercisesDir, false));
      ul.appendChild(li);
    });

    div.appendChild(ul);
    nav.appendChild(div);
  });
}

function _buildFlatSidebar(nav, currentPage, inExercisesDir) {
  const flat = _flatExercises();
  const ul = document.createElement('ul');
  ul.className = 'topic-exercises';

  flat.forEach(ex => {
    const li = document.createElement('li');
    li.appendChild(_makeExerciseLink(ex, ex.topic, currentPage, inExercisesDir, true));
    ul.appendChild(li);
  });

  nav.appendChild(ul);
}

/**
 * Wire up the search box to filter sidebar exercises.
 */
function initSearch() {
  const input = document.getElementById('sidebar-search');
  if (!input) return;

  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();

    // Grouped mode: filter within topic groups
    document.querySelectorAll('.topic-group').forEach(group => {
      const links = group.querySelectorAll('.exercise-link');
      let anyVisible = false;
      links.forEach(link => {
        const text = link.textContent.toLowerCase();
        const visible = !q || text.includes(q);
        link.parentElement.style.display = visible ? '' : 'none';
        if (visible) anyVisible = true;
      });
      group.style.display = anyVisible ? '' : 'none';
      if (q && anyVisible) group.classList.remove('collapsed');
    });

    // Flat mode: filter exercise links directly in .topic-exercises > li
    const nav = document.getElementById('sidebar-nav');
    if (nav) {
      nav.querySelectorAll(':scope > ul.topic-exercises > li').forEach(li => {
        const link = li.querySelector('.exercise-link');
        if (!link) return;
        const text = link.textContent.toLowerCase();
        li.style.display = (!q || text.includes(q)) ? '' : 'none';
      });
    }
  });
}

/**
 * Mobile sidebar toggle.
 */
function initSidebarToggle() {
  const btn = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  if (!btn || !sidebar) return;

  btn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
}

/**
 * Cmd+K / Ctrl+K focuses the search bar.
 */
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      const input = document.getElementById('sidebar-search');
      if (input) {
        input.focus();
        input.select();
      }
    }
  });
}

/**
 * Theme toggle: dark (default) / light.
 * Persists choice in localStorage.
 */
function initThemeToggle() {
  // Apply saved theme before paint (called inline in <head> too)
  const saved = localStorage.getItem('dsa-theme');
  if (saved === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
  }
  // else: no attribute = dark (default via :root)

  // Create toggle button
  const btn = document.createElement('button');
  btn.className = 'theme-toggle';
  btn.setAttribute('aria-label', 'Toggle theme');
  btn.title = 'Toggle light/dark theme';

  function updateIcon() {
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    btn.textContent = isLight ? '\u263E' : '\u2600'; // ☾ or ☀
  }
  updateIcon();

  btn.addEventListener('click', () => {
    document.documentElement.classList.add('theme-transition');
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    if (isLight) {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('dsa-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('dsa-theme', 'light');
    }
    updateIcon();
    setTimeout(() => document.documentElement.classList.remove('theme-transition'), 350);
  });

  document.body.appendChild(btn);
}

// Init on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  buildSidebar();
  initSearch();
  initSidebarToggle();
  initKeyboardShortcuts();
  initThemeToggle();
});
