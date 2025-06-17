// Fetch steps data and initialize the wizard
let stepsData = {};
let currentState = "AL";
let currentOrderType = "main_llc";
let currentStep = 0;
let isEditing = false;
let isAdding = false;

async function loadStepsData() {
  const res = await fetch('data/stepsData.json');
  stepsData = await res.json();
}

function renderSteps() {
  const list = document.getElementById('stepsList');
  list.innerHTML = '';
  const orderData = stepsData[currentOrderType][currentState];
  if (!orderData || orderData.length === 0) return;
  orderData.forEach((step, idx) => {
    const btn = document.createElement('button');
    btn.textContent = `Step ${idx + 1}`;
    btn.className = 'step-item' + (idx === currentStep ? ' selected' : '');
    btn.onclick = () => {
      if(isEditing || isAdding) return;
      currentStep = idx;
      renderStepDetails();
      renderSteps();
    };
    list.appendChild(btn);
  });
}

function renderStepDetails() {
  const orderData = stepsData[currentOrderType][currentState];
  const noStepsMsg = document.getElementById('noStepsMsg');
  if (!orderData || orderData.length === 0) {
    document.getElementById('stepTitle').style.display = 'none';
    document.getElementById('stepDetails').style.display = 'none';
    document.getElementById('editControls').style.display = 'flex';
    document.getElementById('editStepBtn').style.display = 'none';
    document.getElementById('deleteStepBtn').style.display = 'none';
    document.getElementById('addStepBtn').style.display = '';
    document.getElementById('editStepForm').style.display = 'none';
    document.getElementById('addStepForm').style.display = 'none';
    noStepsMsg.style.display = '';
    document.getElementById('prevBtn').disabled = true;
    document.getElementById('nextBtn').disabled = true;
    return;
  }
  noStepsMsg.style.display = 'none';
  document.getElementById('stepTitle').style.display = '';
  document.getElementById('stepDetails').style.display = '';
  document.getElementById('editControls').style.display = 'flex';
  document.getElementById('editStepBtn').style.display = '';
  document.getElementById('deleteStepBtn').style.display = '';
  document.getElementById('addStepBtn').style.display = '';
  document.getElementById('editStepForm').style.display = 'none';
  document.getElementById('addStepForm').style.display = 'none';
  const s = orderData[currentStep] || {title:'',details:['']};
  document.getElementById('stepTitle').textContent = s.title;
  document.getElementById('stepDetails').innerHTML = s.details.map(l =>
    l.trim().startsWith('•')
      ? `<span class='fennec-bullet'>•</span> ${l.replace(/^•/, '').trim()}`
      : l.replace(/  •/g, "<span class='fennec-bullet'>•</span>")
  ).join('<br>');
  document.getElementById('prevBtn').disabled = currentStep === 0;
  document.getElementById('nextBtn').disabled = currentStep === orderData.length - 1;
  setupEditControls();
}

function showEditForm() {
  if(isAdding) return;
  isEditing = true;
  const step = stepsData[currentOrderType][currentState][currentStep];
  document.getElementById('editTitle').value = step.title;
  document.getElementById('editDetails').value = step.details.join('\n');
  document.getElementById('editStepForm').style.display = '';
  document.getElementById('editControls').style.display = 'none';
  document.getElementById('stepTitle').style.display = 'none';
  document.getElementById('stepDetails').style.display = 'none';
}
function hideEditForm() {
  isEditing = false;
  document.getElementById('editStepForm').style.display = 'none';
  document.getElementById('editControls').style.display = 'flex';
  document.getElementById('stepTitle').style.display = '';
  document.getElementById('stepDetails').style.display = '';
}
function saveEditForm() {
  const newTitle = document.getElementById('editTitle').value;
  const newDetails = document.getElementById('editDetails').value.split('\n');
  stepsData[currentOrderType][currentState][currentStep] = {
    title: newTitle,
    details: newDetails
  };
  isEditing = false;
  hideEditForm();
  renderStepDetails();
}
function deleteStep() {
  if(confirm("¿Seguro que quieres borrar este paso?")) {
    stepsData[currentOrderType][currentState].splice(currentStep, 1);
    if(currentStep > 0) currentStep--;
    renderSteps();
    renderStepDetails();
  }
}
function showAddForm() {
  if(isEditing) return;
  isAdding = true;
  document.getElementById('addTitle').value = '';
  document.getElementById('addDetails').value = '';
  document.getElementById('addStepForm').style.display = '';
  document.getElementById('editControls').style.display = 'none';
  document.getElementById('editStepForm').style.display = 'none';
  document.getElementById('stepTitle').style.display = 'none';
  document.getElementById('stepDetails').style.display = 'none';
}
function hideAddForm() {
  isAdding = false;
  document.getElementById('addStepForm').style.display = 'none';
  document.getElementById('editControls').style.display = 'flex';
  document.getElementById('stepTitle').style.display = '';
  document.getElementById('stepDetails').style.display = '';
}
function saveAddForm() {
  const newTitle = document.getElementById('addTitle').value;
  const newDetails = document.getElementById('addDetails').value.split('\n');
  if(!stepsData[currentOrderType][currentState]) stepsData[currentOrderType][currentState] = [];
  stepsData[currentOrderType][currentState].push({title: newTitle, details: newDetails});
  currentStep = stepsData[currentOrderType][currentState].length - 1;
  isAdding = false;
  hideAddForm();
  renderSteps();
  renderStepDetails();
}
function setupEditControls() {
  document.getElementById('editStepBtn').onclick = showEditForm;
  document.getElementById('deleteStepBtn').onclick = deleteStep;
  document.getElementById('addStepBtn').onclick = showAddForm;
  document.getElementById('saveEditBtn').onclick = saveEditForm;
  document.getElementById('cancelEditBtn').onclick = hideEditForm;
  document.getElementById('saveAddBtn').onclick = saveAddForm;
  document.getElementById('cancelAddBtn').onclick = hideAddForm;
}

function initListeners() {
  document.getElementById('sidebarState').onchange = (e) => {
    currentState = e.target.value;
    currentStep = 0;
    renderSteps();
    renderStepDetails();
  };
  document.getElementById('orderTypeSelect').onchange = (e) => {
    currentOrderType = e.target.value;
    currentStep = 0;
    renderSteps();
    renderStepDetails();
  };
  document.getElementById('prevBtn').onclick = () => {
    if (currentStep > 0) {
      currentStep--;
      renderStepDetails();
      renderSteps();
    }
  };
  document.getElementById('nextBtn').onclick = () => {
    if (currentStep < stepsData[currentOrderType][currentState].length - 1) {
      currentStep++;
      renderStepDetails();
      renderSteps();
    }
  };
}

async function init() {
  await loadStepsData();
  renderSteps();
  renderStepDetails();
  setupEditControls();
  initListeners();
}

window.addEventListener('DOMContentLoaded', init);
