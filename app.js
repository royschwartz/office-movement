'use strict';

const exercises = window.EXERCISES;
const byId = new Map(exercises.map(exercise => [exercise.id, exercise]));
const categories = { strength: 'Strength', cardio: 'Cardio', mobility: 'Mobility', stretch: 'Stretching', balance: 'Balance' };
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const strengthIds = ['sit-to-stand', 'wall-push-up', 'hip-hinge', 'band-row', 'calf-raise', 'wall-plank'];
const strengthNote = 'Do the suggested slow reps, then rest for the rest of the minute. Pause the timer for more rest. Use light resistance for the row.';
const strengthRound = round => strengthIds.map(id => ({ id, seconds: 60, note: id === 'wall-plank' ? 'Hold for 10–20 seconds, then rest. Repeat only if comfortable. Keep breathing.' : strengthNote, round }));
const stretching = [
  { id: 'chest-stretch', seconds: 60, note: 'Hold gently for 5–10 seconds, release, and repeat up to 3–5 times.' },
  { id: 'seated-hamstring', seconds: 60, note: 'Allow about 20–30 seconds per side, with time to change legs. Take longer if needed.' },
  { id: 'calf-stretch', seconds: 60, note: 'Allow about 20–30 seconds per side. Keep your rear heel comfortably on the floor.' }
];
const plans = {
  5: {
    title: 'Desk reset',
    description: 'Easy movement to break up sitting. This is a mobility break, not a full strength session.',
    equipment: 'You’ll need a stable chair and a little clear space.',
    steps: [
      { id: 'march', seconds: 60, note: 'Start easy. Small, quiet steps are enough.' },
      { id: 'shoulder-roll', seconds: 60, note: 'Take 5 slow circles each way. Relax between sets.' },
      { id: 'wrist-mobility', seconds: 60, note: 'Move gently 5–10 times in each direction. No forcing.' },
      { id: 'seated-rotation', seconds: 60, note: 'Turn slowly 3–5 times each way. Stay in an easy range.' },
      stretching[0]
    ]
  },
  15: {
    title: 'Everyday circuit',
    description: '5-minute warm-up → 1 strength round → gentle cardio → balance → stretch.',
    equipment: 'A stable chair, a wall, and a light band or weights for the row. Add more warm-up or rest as needed.',
    steps: [
      { id: 'march', seconds: 240, note: 'Warm up gradually, starting slowly. Take extra time if you still feel stiff.' },
      { id: 'shoulder-roll', seconds: 60, note: 'Loosen up with 5 gentle rolls each way. Relax and repeat if comfortable.' },
      ...strengthRound(1),
      { id: 'step-touch', seconds: 60, note: 'Keep one foot on the ground and stay able to talk. Slow down for the final 20 seconds.' },
      { id: 'tandem-balance', seconds: 60, note: 'Keep a hand on stable support as needed. Hold 10–20 seconds with each foot in front; rest between.' },
      { ...stretching[0], seconds: 30, note: 'Hold gently for 5–10 seconds, then release. Repeat 2–3 times.' },
      { ...stretching[1], seconds: 45, note: 'Hold gently for about 20 seconds per side. Pause for extra time to change legs.' },
      { ...stretching[2], seconds: 45, note: 'Hold gently for about 20 seconds per side. Pause for extra time to change legs.' }
    ]
  },
  25: {
    title: 'Build it up',
    description: 'Warm up → 2 strength rounds → longer cardio → balance + mobility → stretch.',
    equipment: 'A stable chair, a wall, and a light band or weights for the row. Pause for extra recovery between rounds.',
    steps: [
      { id: 'march', seconds: 240, note: 'Start slow and gradually warm up. Take a few more minutes if you need them.' },
      { id: 'shoulder-roll', seconds: 60, note: 'Take 5 gentle circles each way. Relax and repeat only if comfortable.' },
      ...strengthRound(1), ...strengthRound(2),
      { id: 'step-touch', seconds: 90, note: 'Aim for a steady, comfortable pace. Moderate effort means you can talk but not sing.' },
      { id: 'march', seconds: 90, note: 'Keep breathing comfortably. Slow down during the final 30 seconds.' },
      { id: 'tandem-balance', seconds: 60, note: 'Hold 10–20 seconds per lead foot, resting between. Use stable support; no need to fill all the time.' },
      { id: 'wall-slide', seconds: 60, note: 'Take 5–8 slow reps. Keep your ribs relaxed and your reach comfortable.' },
      ...stretching
    ]
  }
};

const grid = document.getElementById('exercise-grid');
grid.innerHTML = exercises.map((exercise, index) => `
  <article class="exercise-card" id="exercise-${escapeHtml(exercise.id)}" data-category="${escapeHtml(exercise.category)}">
    <div class="card-image"><span class="card-number">${String(index + 1).padStart(2, '0')} / 16</span><img src="assets/${escapeHtml(exercise.id)}.svg" alt="${escapeHtml(exercise.alt)}" width="600" height="380" loading="lazy"></div>
    <div class="card-content"><div class="card-meta"><span class="category category-${escapeHtml(exercise.category)}">${categories[exercise.category]}</span><span class="card-dose">${escapeHtml(exercise.dose)}</span></div>
    <h3>${escapeHtml(exercise.name)}</h3><p class="card-target">${escapeHtml(exercise.target)}</p><p class="card-intro">${escapeHtml(exercise.intro)}</p>
    <details class="card-details"><summary>How to do it + variations <span aria-hidden="true">+</span></summary><div class="card-details-body"><p class="card-equipment"><strong>Use:</strong> ${escapeHtml(exercise.equipment)}</p><ol>${exercise.steps.map(step => `<li>${escapeHtml(step)}</li>`).join('')}</ol>
      <div class="variation"><strong>Make it easier</strong>${escapeHtml(exercise.easier)}</div><div class="variation"><strong>Build up gently</strong>${escapeHtml(exercise.harder)}</div>
      <p class="watch"><strong>Keep in mind:</strong> ${escapeHtml(exercise.watch)}</p>
      ${exercise.sources.map(source => `<a class="card-source" href="${escapeHtml(source.url)}">${escapeHtml(source.title)} ↗</a>`).join('')}
    </div></details></div>
  </article>`).join('');

document.getElementById('sources-list').innerHTML = window.REFERENCE_SOURCES.map(source => `<li><a href="${escapeHtml(source.url)}">${escapeHtml(source.title)} ↗</a><span>${escapeHtml(source.note)}</span></li>`).join('');

function filterExercises(category) {
  let count = 0;
  document.querySelectorAll('.exercise-card').forEach(card => {
    card.hidden = category !== 'all' && card.dataset.category !== category;
    if (!card.hidden) count++;
  });
  document.querySelectorAll('[data-filter]').forEach(button => {
    const active = button.dataset.filter === category;
    button.setAttribute('aria-pressed', String(active));
    button.classList.toggle('active', active);
  });
  document.getElementById('result-count').textContent = `${count} movement${count === 1 ? '' : 's'}`;
}
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => filterExercises(button.dataset.filter)));

function revealLinkedExercise() {
  if (!location.hash.startsWith('#exercise-')) return;
  const card = document.getElementById(location.hash.slice(1));
  if (!card) return;
  filterExercises('all');
  card.querySelector('details').open = true;
  requestAnimationFrame(() => card.scrollIntoView({ block: 'start' }));
}
window.addEventListener('hashchange', revealLinkedExercise);
revealLinkedExercise();

let selectedPlan = 15;
const startButton = document.getElementById('start-routine');
function selectPlan(minutes) {
  selectedPlan = minutes;
  const plan = plans[minutes];
  document.querySelectorAll('[data-plan]').forEach(button => {
    const selected = Number(button.dataset.plan) === minutes;
    button.classList.toggle('selected', selected);
    button.setAttribute('aria-pressed', String(selected));
    button.querySelector('.option-check').textContent = selected ? '✓' : '↗';
  });
  document.getElementById('plan-description').textContent = plan.description;
  document.getElementById('plan-equipment').textContent = plan.equipment;
  startButton.innerHTML = `Start ${minutes}-minute routine <span aria-hidden="true">→</span>`;
  document.getElementById('routine-list').innerHTML = plan.steps.map(step => `<li><a href="#exercise-${step.id}">${escapeHtml(byId.get(step.id).name)}${step.round && minutes === 25 ? ` · round ${step.round}` : ''}</a><span>${step.seconds < 60 ? `${step.seconds} sec` : `${step.seconds / 60} min`}</span></li>`).join('');
}
document.querySelectorAll('[data-plan]').forEach(button => button.addEventListener('click', () => selectPlan(Number(button.dataset.plan))));
selectPlan(15);

const dialog = document.getElementById('workout-dialog');
const body = document.getElementById('workout-body');
const controls = document.getElementById('workout-controls');
const timerButton = document.getElementById('toggle-timer');
const previousButton = document.getElementById('previous-step');
const nextButton = document.getElementById('next-step');
let activePlan = null;
let stepIndex = 0;
let remainingMs = 0;
let deadline = 0;
let ticking = null;
let running = false;
let hasStarted = false;

function pauseTimer() {
  if (running) remainingMs = Math.max(0, deadline - Date.now());
  running = false;
  clearInterval(ticking);
  ticking = null;
}

function formatTime(milliseconds) {
  const seconds = Math.ceil(milliseconds / 1000);
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
}

function updateTimer() {
  if (running) remainingMs = Math.max(0, deadline - Date.now());
  if (remainingMs <= 0 && running) pauseTimer();
  document.getElementById('timer-number').textContent = formatTime(remainingMs);
  document.getElementById('timer-fill').style.width = `${Math.max(0, remainingMs / (activePlan.steps[stepIndex].seconds * 1000) * 100)}%`;
  const status = document.getElementById('timer-status');
  const message = remainingMs <= 0 ? 'Time’s up. Move on when ready.' : running ? 'Move gently. Rest as needed.' : hasStarted ? 'Paused. Take your time.' : 'Ready when you are.';
  if (status.textContent !== message) status.textContent = message;
  timerButton.textContent = remainingMs <= 0 ? 'Restart timer' : running ? 'Pause' : hasStarted ? 'Resume' : 'Start timer';
}

function renderStep() {
  pauseTimer();
  const step = activePlan.steps[stepIndex];
  const exercise = byId.get(step.id);
  remainingMs = step.seconds * 1000;
  hasStarted = false;
  document.getElementById('workout-position').textContent = `${activePlan.title} · ${stepIndex + 1} of ${activePlan.steps.length}${step.round && selectedPlan === 25 ? ` · Round ${step.round}` : ''}`;
  body.innerHTML = `<div class="workout-main"><div class="workout-visual"><img src="assets/${escapeHtml(exercise.id)}.svg" alt="${escapeHtml(exercise.alt)}" width="600" height="380"><div class="workout-timer"><div class="timer-number" id="timer-number" role="timer" aria-label="Time remaining">${formatTime(remainingMs)}</div><p class="timer-status" id="timer-status" role="status">Ready when you are.</p><div class="timer-track" aria-hidden="true"><span id="timer-fill"></span></div></div></div><div class="workout-info"><span class="category category-${escapeHtml(exercise.category)}">${categories[exercise.category]}</span><h2 id="workout-title" tabindex="-1">${escapeHtml(exercise.name)}</h2><p class="dose">${escapeHtml(exercise.dose)}</p><ol>${exercise.steps.map(text => `<li>${escapeHtml(text)}</li>`).join('')}</ol><p class="step-note">${escapeHtml(step.note)}</p><p class="watch"><strong>Keep in mind:</strong> ${escapeHtml(exercise.watch)}</p><p class="equipment"><strong>Use:</strong> ${escapeHtml(exercise.equipment)}</p><details><summary class="subtle">Need an easier option?</summary><p class="subtle">${escapeHtml(exercise.easier)}</p></details></div></div>`;
  controls.hidden = false;
  document.getElementById('workout-footnote').hidden = false;
  previousButton.disabled = stepIndex === 0;
  nextButton.textContent = stepIndex === activePlan.steps.length - 1 ? 'Finish →' : 'Next →';
  updateTimer();
  dialog.scrollTop = 0;
}

startButton.addEventListener('click', () => {
  activePlan = plans[selectedPlan];
  stepIndex = 0;
  renderStep();
  document.body.classList.add('modal-open');
  dialog.showModal();
  document.getElementById('workout-title').focus();
});

timerButton.addEventListener('click', () => {
  if (running) pauseTimer();
  else {
    if (remainingMs <= 0) remainingMs = activePlan.steps[stepIndex].seconds * 1000;
    hasStarted = true;
    deadline = Date.now() + remainingMs;
    running = true;
    ticking = setInterval(updateTimer, 200);
  }
  updateTimer();
});

previousButton.addEventListener('click', () => {
  if (stepIndex > 0) { stepIndex--; renderStep(); document.getElementById('workout-title').focus(); }
});
nextButton.addEventListener('click', () => {
  if (stepIndex < activePlan.steps.length - 1) { stepIndex++; renderStep(); document.getElementById('workout-title').focus(); }
  else {
    pauseTimer();
    document.getElementById('workout-position').textContent = 'A little time for yourself';
    body.innerHTML = '<div class="completion"><span class="completion-mark" aria-hidden="true">✓</span><h2 id="workout-title" tabindex="-1">Room made for movement.</h2><p>Let your breathing settle. Come back for another small break, or give your muscles a rest after strength work.</p><button class="button primary" id="finish-workout">Back to the guide →</button></div>';
    controls.hidden = true;
    document.getElementById('workout-footnote').hidden = true;
    document.getElementById('finish-workout').addEventListener('click', () => dialog.close());
    document.getElementById('workout-title').focus();
    dialog.scrollTop = 0;
  }
});
document.getElementById('close-workout').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => { pauseTimer(); document.body.classList.remove('modal-open'); startButton.focus(); });
document.addEventListener('visibilitychange', () => { if (document.hidden && running) { pauseTimer(); updateTimer(); } });

let printState = null;
function preparePrint() {
  if (printState) return;
  printState = [...document.querySelectorAll('details')].map(detail => ({ detail, open: detail.open }));
  printState.forEach(({ detail }) => { detail.open = true; });
}
function restorePrint() {
  if (!printState) return;
  printState.forEach(({ detail, open }) => { detail.open = open; });
  printState = null;
}
window.addEventListener('beforeprint', preparePrint);
window.addEventListener('afterprint', restorePrint);
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => { preparePrint(); window.print(); }));
