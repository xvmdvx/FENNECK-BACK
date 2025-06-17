const sections = [
  'Order Review',
  'Information Listed in the Articles',
  'Professional Service',
  'Most Common Rejections',
  'Special Notes',
  'Instructions'
];
let kbData = {};
let globalIssues = [];
async function loadData() {
  kbData = await fetch('data/state_kb.json').then(r => r.json());
  globalIssues = await fetch('data/global_issues.json').then(r => r.json());
}
function populateStates() {
  const sel = document.getElementById('stateSelect');
  sel.innerHTML = Object.keys(kbData)
    .map(s => `<option value="${s}">${s}</option>`)
    .join('');
}
function renderState() {
  const state = document.getElementById('stateSelect').value;
  const data = kbData[state] || {};
  const container = document.getElementById('content');
  container.innerHTML = '';
  sections.forEach(sec => {
    const items = data[sec] || [];
    const div = document.createElement('div');
    div.className = 'section';
    div.innerHTML = `<h2>${sec}</h2><ul>` +
      items.map(t => `<li>${t}</li>`).join('') +
      '</ul>';
    container.appendChild(div);
  });
}
function renderIssues() {
  const container = document.getElementById('content');
  container.innerHTML =
    '<div class="section"><h2>Global Issues</h2><ul>' +
    globalIssues.map(i => `<li>${i}</li>`).join('') +
    '</ul></div>';
}
document.addEventListener('DOMContentLoaded', async () => {
  await loadData();
  populateStates();
  document.getElementById('stateSelect').onchange = renderState;
  document.getElementById('showIssuesBtn').onclick = renderIssues;
  renderState();
});
