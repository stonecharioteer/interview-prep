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
    { id: 1, name: "min" }, { id: 2, name: "max" }, { id: 3, name: "sum" },
    { id: 4, name: "contains(n)" }, { id: 5, name: "average" }, { id: 6, name: "count_of(n)" },
    { id: 20, name: "find_index(n)" }, { id: 21, name: "find_all_indices(n)" },
    { id: 23, name: "reversed_copy" }, { id: 26, name: "reverse_in_place" },
    { id: 29, name: "is_sorted" }, { id: 37, name: "binary_search" },
    { id: 46, name: "merge_sorted" }, { id: 56, name: "rotate_k" },
    { id: 61, name: "two_sum" }, { id: 69, name: "remove_duplicates_sorted" },
    { id: 75, name: "partition_by_pivot" }, { id: 83, name: "sliding_window_sum(k)" },
    { id: 96, name: "max_subarray_sum (Kadane)" }, { id: 140, name: "longest_consecutive_sequence" },
  ]},
  { topic: "Linked List", exercises: [
    { id: 7, name: "length" }, { id: 8, name: "find(n)" }, { id: 9, name: "min" },
    { id: 10, name: "max" }, { id: 11, name: "sum" }, { id: 12, name: "average" },
    { id: 13, name: "count_of(n)" }, { id: 22, name: "get_kth(k)" },
    { id: 24, name: "append" }, { id: 27, name: "prepend" },
    { id: 32, name: "remove_first(n)" }, { id: 41, name: "insert_at_index" },
    { id: 50, name: "remove_at_index" }, { id: 57, name: "reverse (iterative)" },
    { id: 63, name: "middle_node" }, { id: 70, name: "detect_cycle" },
    { id: 78, name: "merge_sorted" }, { id: 86, name: "nth_from_end(n)" },
  ]},
  { topic: "Stack", exercises: [
    { id: 14, name: "define, push, pop, peek, is_empty" },
    { id: 25, name: "valid_parentheses" },
    { id: 34, name: "evaluate_postfix" },
    { id: 54, name: "min_stack" },
  ]},
  { topic: "Queue", exercises: [
    { id: 15, name: "define, enqueue, dequeue, peek, is_empty" },
    { id: 28, name: "implement using two stacks" },
  ]},
  { topic: "Recursion", exercises: [
    { id: 16, name: "factorial(n)" }, { id: 17, name: "factorial_memo(n)" },
    { id: 18, name: "sum_array" }, { id: 19, name: "reverse_string" },
    { id: 48, name: "power(base, exp)" }, { id: 49, name: "power_memo(base, exp)" },
    { id: 97, name: "fibonacci_recursive(n)" }, { id: 98, name: "fibonacci_memo(n)" },
  ]},
  { topic: "Sorting", exercises: [
    { id: 30, name: "bubble_sort" }, { id: 31, name: "selection_sort" },
    { id: 33, name: "insertion_sort" }, { id: 47, name: "merge_sort" },
    { id: 76, name: "quick_sort" }, { id: 194, name: "counting_sort" },
    { id: 199, name: "radix_sort" },
  ]},
  { topic: "Bits", exercises: [
    { id: 35, name: "is power of two" }, { id: 36, name: "count set bits" },
    { id: 55, name: "single_number (XOR)" },
    { id: 105, name: "get/set/clear bit" },
    { id: 192, name: "subsets via bitmask" },
  ]},
  { topic: "Binary Search", exercises: [
    { id: 38, name: "find_first_occurrence" }, { id: 39, name: "find_last_occurrence" },
    { id: 40, name: "search_insert_position" },
    { id: 141, name: "search_rotated_sorted_array" },
    { id: 147, name: "find_min_rotated_sorted_array" },
    { id: 170, name: "find_peak_element" },
    { id: 181, name: "koko_eating_bananas" },
    { id: 190, name: "capacity_to_ship_packages" },
  ]},
  { topic: "Maps (dict)", exercises: [
    { id: 42, name: "get_or_default" }, { id: 51, name: "increment_count" },
    { id: 58, name: "merge_counts" }, { id: 64, name: "most_common key" },
    { id: 71, name: "invert mapping" }, { id: 79, name: "first_non_repeating" },
  ]},
  { topic: "Math", exercises: [
    { id: 43, name: "gcd (Euclidean)" }, { id: 44, name: "lcm" },
    { id: 52, name: "is_prime" }, { id: 93, name: "sieve_of_eratosthenes" },
    { id: 198, name: "fast_exponentiation" },
  ]},
  { topic: "Trees (Binary)", exercises: [
    { id: 45, name: "define Node" },
    { id: 53, name: "preorder traversal" }, { id: 59, name: "inorder traversal" },
    { id: 66, name: "postorder traversal" }, { id: 72, name: "level-order traversal" },
    { id: 80, name: "size" }, { id: 89, name: "height" },
    { id: 101, name: "contains(value)" }, { id: 103, name: "min" },
    { id: 104, name: "max" }, { id: 110, name: "sum" },
    { id: 111, name: "average" }, { id: 112, name: "count_of(n)" },
    { id: 159, name: "is_balanced" }, { id: 166, name: "is_symmetric" },
    { id: 175, name: "diameter" }, { id: 182, name: "serialize/deserialize" },
  ]},
  { topic: "Heap", exercises: [
    { id: 60, name: "min-heap: define & insert", hasContent: true, file: "heap-min-insert.html" },
    { id: 67, name: "min-heap: extract_min" },
    { id: 73, name: "min-heap: peek & size" },
    { id: 81, name: "heapify (build from array)" },
    { id: 90, name: "heap_sort" },
    { id: 106, name: "max-heap (convert min to max)" },
    { id: 113, name: "kth_largest element" },
    { id: 123, name: "kth_smallest element" },
    { id: 134, name: "merge two heaps" },
    { id: 135, name: "merge_k_sorted_lists" },
    { id: 146, name: "top_k_frequent elements" },
    { id: 161, name: "sliding window maximum" },
  ]},
  { topic: "Two Pointers", exercises: [
    { id: 62, name: "two_sum_sorted" },
    { id: 65, name: "three_sum" },
    { id: 68, name: "container_with_most_water" },
  ]},
  { topic: "Trie", exercises: [
    { id: 74, name: "define TrieNode" }, { id: 82, name: "insert word" },
    { id: 92, name: "search word" }, { id: 107, name: "starts_with" },
    { id: 116, name: "count_words_with_prefix" }, { id: 125, name: "delete word" },
    { id: 136, name: "autocomplete" }, { id: 152, name: "count total words" },
    { id: 167, name: "longest_common_prefix" },
  ]},
  { topic: "Monotonic Stack", exercises: [
    { id: 77, name: "next_greater_element" }, { id: 85, name: "next_smaller_element" },
    { id: 160, name: "daily_temperatures" },
    { id: 162, name: "largest_rectangle_histogram" },
    { id: 168, name: "trapping_rain_water" },
  ]},
  { topic: "Sliding Window", exercises: [
    { id: 84, name: "max_sum_subarray_size_k" },
    { id: 87, name: "longest_substring_k_distinct" },
    { id: 102, name: "longest_substring_without_repeating" },
    { id: 108, name: "minimum_window_substring" },
  ]},
  { topic: "Backtracking", exercises: [
    { id: 88, name: "generate_subsets" }, { id: 91, name: "generate_permutations" },
    { id: 95, name: "generate_combinations" }, { id: 118, name: "generate_parentheses" },
    { id: 143, name: "n_queens" }, { id: 158, name: "sudoku_solver" },
    { id: 186, name: "word_search" },
    { id: 203, name: "combination_sum" }, { id: 205, name: "combination_sum_2" },
  ]},
  { topic: "Graph", exercises: [
    { id: 94, name: "define adjacency list" }, { id: 109, name: "add_edge" },
    { id: 117, name: "has_edge & neighbors" },
    { id: 126, name: "DFS traversal" }, { id: 138, name: "BFS traversal" },
    { id: 149, name: "is_connected" }, { id: 153, name: "detect_cycle (directed)" },
    { id: 157, name: "detect_cycle (undirected)" },
    { id: 163, name: "shortest_path (BFS)" },
    { id: 171, name: "topological_sort (Kahn)" },
    { id: 173, name: "topological_sort (DFS)" },
    { id: 178, name: "count connected components" },
    { id: 185, name: "bipartite_check" },
    { id: 191, name: "Dijkstra" },
    { id: 196, name: "Kruskal's MST" },
    { id: 197, name: "Floyd-Warshall" },
    { id: 201, name: "Prim's MST" },
  ]},
  { topic: "Dynamic Programming", exercises: [
    { id: 99, name: "fibonacci (tabulation)" }, { id: 100, name: "climbing_stairs" },
    { id: 114, name: "house_robber" }, { id: 119, name: "min_cost_climbing_stairs" },
    { id: 124, name: "coin_change" }, { id: 128, name: "coin_change_2" },
    { id: 137, name: "longest_increasing_subsequence" },
    { id: 142, name: "unique_paths" }, { id: 151, name: "unique_paths_with_obstacles" },
    { id: 155, name: "min_path_sum" },
    { id: 164, name: "longest_common_subsequence" },
    { id: 169, name: "longest_palindromic_substring" },
    { id: 176, name: "longest_palindromic_subsequence" },
    { id: 180, name: "edit_distance" },
    { id: 183, name: "house_robber_3" }, { id: 187, name: "word_break" },
    { id: 189, name: "max_path_sum (tree)" },
    { id: 193, name: "0/1 knapsack" },
    { id: 195, name: "partition_equal_subset_sum" },
    { id: 200, name: "matrix_chain_multiplication" },
    { id: 202, name: "burst_balloons" },
    { id: 204, name: "travelling_salesman (bitmask)" },
  ]},
  { topic: "Greedy", exercises: [
    { id: 115, name: "jump_game" }, { id: 120, name: "jump_game_2" },
    { id: 133, name: "merge_intervals" }, { id: 139, name: "insert_interval" },
    { id: 145, name: "meeting_rooms" }, { id: 154, name: "meeting_rooms_2" },
    { id: 172, name: "gas_station" }, { id: 179, name: "activity_selection" },
    { id: 188, name: "fractional_knapsack" },
  ]},
  { topic: "Trees (BST)", exercises: [
    { id: 121, name: "insert" }, { id: 122, name: "search" },
    { id: 130, name: "delete" }, { id: 132, name: "validate_bst" },
    { id: 144, name: "inorder_successor" }, { id: 150, name: "lowest_common_ancestor" },
  ]},
  { topic: "Union-Find", exercises: [
    { id: 127, name: "basic find & union" }, { id: 129, name: "path compression" },
    { id: 131, name: "union by rank" },
    { id: 148, name: "count connected components" },
    { id: 156, name: "detect cycle (undirected)" },
  ]},
  { topic: "String Matching", exercises: [
    { id: 165, name: "naive pattern search" },
    { id: 174, name: "KMP failure function" },
    { id: 177, name: "KMP search" },
    { id: 184, name: "Rabin-Karp" },
  ]},
  { topic: "Conversions", exercises: [
    { id: 206, name: "list -> linked list" },
    { id: 207, name: "linked list -> list" },
    { id: 208, name: "BST -> sorted array" },
    { id: 209, name: "sorted array -> balanced BST" },
    { id: 210, name: "adjacency list -> matrix" },
    { id: 211, name: "adjacency matrix -> list" },
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
  // Heap
  60: "exercises/heap-min-insert.html",
  67: "exercises/heap-extract-min.html",
  73: "exercises/heap-peek-size.html",
  81: "exercises/heap-heapify.html",
  90: "exercises/heap-sort.html",
  106: "exercises/heap-max-heap.html",
  // Two Pointers
  62: "exercises/tp-two-sum-sorted.html",
  65: "exercises/tp-three-sum.html",
  68: "exercises/tp-container-water.html",
  // Trie
  74: "exercises/trie-define.html",
  82: "exercises/trie-insert.html",
  92: "exercises/trie-search.html",
  107: "exercises/trie-starts-with.html",
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

let _sidebarGrouped = localStorage.getItem('sidebar-grouped') !== 'false'; // default: grouped by topic

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
