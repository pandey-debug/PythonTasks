let tasks = [
  { id: 1, text: 'Review project proposal', done: false },
  { id: 2, text: 'Schedule team standup', done: true },
  { id: 3, text: 'Update documentation', done: false }
];
let filter = 'all';
let nextId = 4;

function esc(s) {
  return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function render() {
  const list = document.getElementById('list');
  const visible = tasks.filter(t =>
    filter === 'all' ? true : filter === 'done' ? t.done : !t.done
  );

  if (!visible.length) {
    list.innerHTML = '<p class="empty">No tasks here.</p>';
  } else {
    list.innerHTML = visible.map(t => `
      <div class="todo-item${t.done ? ' done' : ''}">
        <input type="checkbox" ${t.done ? 'checked' : ''} onchange="toggle(${t.id})" />
        <span class="label">${esc(t.text)}</span>
        <button class="del-btn" onclick="remove(${t.id})" title="Delete">&#x2715;</button>
      </div>
    `).join('');
  }

  const active = tasks.filter(t => !t.done).length;
  const hasDone = tasks.some(t => t.done);
  const footer = document.getElementById('footer');
  footer.style.display = tasks.length ? 'flex' : 'none';
  document.getElementById('count-label').textContent = `${active} item${active !== 1 ? 's' : ''} left`;
  document.querySelector('.clear-btn').style.visibility = hasDone ? 'visible' : 'hidden';
}

function addTask() {
  const inp = document.getElementById('new-task');
  const text = inp.value.trim();
  if (!text) return;
  tasks.unshift({ id: nextId++, text, done: false });
  inp.value = '';
  render();
}

function toggle(id) {
  tasks = tasks.map(t => t.id === id ? { ...t, done: !t.done } : t);
  render();
}

function remove(id) {
  tasks = tasks.filter(t => t.id !== id);
  render();
}

function clearDone() {
  tasks = tasks.filter(t => !t.done);
  render();
}

function setFilter(f, btn) {
  filter = f;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  render();
}

document.getElementById('new-task').addEventListener('keydown', e => {
  if (e.key === 'Enter') addTask();
});

render();
