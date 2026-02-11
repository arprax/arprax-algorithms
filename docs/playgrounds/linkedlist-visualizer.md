<style>
/* CSS Styles - Unified for both windows */
.nlp-tool-container {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 0.5rem;
  padding: 1.5rem;
  background-color: var(--md-default-bg-color);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 2em 0;
}
.visualizer-label {
  font-family: monospace;
  font-size: 0.9rem;
  color: var(--md-accent-fg-color);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.ll-canvas, .array-canvas {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  min-height: 100px;
  padding: 1rem;
  background-color: var(--md-code-bg-color);
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}
/* Linked List Node */
.ll-node {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 80px;
  background: var(--md-default-bg-color);
  border: 2px solid var(--md-primary-fg-color);
  border-radius: 6px;
}
/* Array Element */
.array-element {
  display: flex;
  flex-direction: column;
  border: 2px solid var(--md-accent-fg-color);
  background: var(--md-default-bg-color);
  min-width: 70px;
}
.cell-index {
  background: var(--md-accent-fg-color--lightest);
  font-size: 0.7rem;
  text-align: center;
  border-top: 1px solid var(--md-accent-fg-color);
}
.data-box { padding: 8px; text-align: center; font-weight: bold; }
.addr-box { font-size: 0.7rem; text-align: center; background: #eee; color: #333; }
.ll-arrow { font-size: 1.2rem; }
</style>

<div class="nlp-tool-container">
  <label class="nlp-input-label" for="nlpInput">Type a Sentence:</label>
  <input type="text" id="nlpInput" placeholder="Type here ..." style="width:100%; padding:10px; margin-bottom:20px; border-radius:4px; border:1px solid #ccc;">

  <div class="visualizer-label">1. Reference-Based (Linked List)</div>
  <div id="llCanvas" class="ll-canvas"></div>

  <div class="visualizer-label">2. Array-Based (Contiguous Memory)</div>
  <div id="arrayCanvas" class="array-canvas"></div>
</div>

<script>
(function() {
  const input = document.getElementById('nlpInput');
  const llCanvas = document.getElementById('llCanvas');
  const arrayCanvas = document.getElementById('arrayCanvas');
  const addressBook = {};

  function getAddr(word) {
    if (!addressBook[word]) addressBook[word] = '0x' + Math.floor(Math.random()*0xFFFF).toString(16).toUpperCase();
    return addressBook[word];
  }

  function updateVisuals(text) {
    llCanvas.innerHTML = '';
    arrayCanvas.innerHTML = '';
    const tokens = text.trim() === '' ? [] : text.trim().split(/\s+/);

    if (tokens.length === 0) {
      llCanvas.innerHTML = '<div style="color:gray">Empty List</div>';
      arrayCanvas.innerHTML = '<div style="color:gray">Empty Array [ ]</div>';
      return;
    }

    tokens.forEach((token, i) => {
      // --- LINKED LIST RENDER ---
      const node = document.createElement('div');
      node.className = 'll-node';
      node.innerHTML = `<div class="data-box">${token}</div><div class="addr-box">${getAddr(token)}</div>`;
      llCanvas.appendChild(node);
      const arrow = document.createElement('div');
      arrow.className = 'll-arrow';
      arrow.innerHTML = '&rarr;';
      llCanvas.appendChild(arrow);

      // --- ARRAY RENDER ---
      const cell = document.createElement('div');
      cell.className = 'array-element';
      cell.innerHTML = `<div class="data-box">${token}</div><div class="cell-index">Index ${i}</div>`;
      arrayCanvas.appendChild(cell);
    });

    llCanvas.innerHTML += '<div style="font-weight:bold; color:red">NULL</div>';
  }

  input.addEventListener('input', (e) => updateVisuals(e.target.value));
  updateVisuals("");
})();
</script>