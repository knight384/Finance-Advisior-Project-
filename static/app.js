// Interactive client-side logic for AI Personal Finance Advisor demo

function parseExpensesText(text){
  const lines = text.split(/\r?\n/).map(l=>l.trim()).filter(Boolean);
  const out = [];
  for(const ln of lines){
    const parts = ln.split(',');
    if(parts.length < 2) continue;
    const desc = parts[0].trim();
    let amt = parseFloat(parts[1].trim());
    if(Number.isNaN(amt)) continue;
    out.push({desc, amount: amt});
  }
  return out;
}

function renderKeyValueList(obj){
  const ul = document.createElement('ul');
  for(const k of Object.keys(obj)){
    const li = document.createElement('li');
    li.textContent = `${k}: ${obj[k]}`;
    ul.appendChild(li);
  }
  return ul;
}

function renderJsonPre(obj){
  const pre = document.createElement('pre');
  pre.className = 'code';
  pre.textContent = JSON.stringify(obj, null, 2);
  return pre;
}

function showLoading(container){
  container.innerHTML = '<div class="card"><em>Loading…</em></div>';
}

function showError(container, message){
  container.innerHTML = `<div class="alert alert-danger">${message}</div>`;
}

let categoryChart = null;

function renderChart(categorized){
  try{
    if(typeof Chart === 'undefined') return; // Chart.js not loaded
  }catch(e){
    return;
  }
  const canvas = document.getElementById('category-chart');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  const labels = Object.keys(categorized);
  const values = labels.map(k => categorized[k]);
  const colors = [
    '#2563eb','#059669','#f97316','#ef4444','#8b5cf6','#06b6d4','#f59e0b','#10b981'
  ];
  if(categoryChart){
    categoryChart.data.labels = labels;
    categoryChart.data.datasets[0].data = values;
    categoryChart.update();
    return;
  }
  categoryChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{ data: values, backgroundColor: colors.slice(0, labels.length) }]
    },
    options: { responsive: true, maintainAspectRatio: false, animation: { animateRotate: true, duration: 900 } }
  });
}

// Fallback: simple horizontal bar chart using DIVs (no Chart.js needed)
function renderMiniBars(containerId, categorized){
  const container = document.getElementById(containerId);
  if(!container) return;
  // remove previous
  container.innerHTML = '';
  const wrapper = document.createElement('div');
  wrapper.className = 'mini-bars card';
  const entries = Object.entries(categorized || {});
  if(entries.length === 0){
    const p = document.createElement('p'); p.className = 'small'; p.textContent = 'No category data to display.'; wrapper.appendChild(p); container.appendChild(wrapper); return;
  }
  const max = Math.max(...entries.map(e=>e[1])) || 1;
  for(const [k,v] of entries){
    const row = document.createElement('div'); row.className = 'bar-row';
    const label = document.createElement('div'); label.className = 'bar-label'; label.textContent = `${k} (${v})`;
    const barOuter = document.createElement('div'); barOuter.className = 'bar-outer';
    const barInner = document.createElement('div'); barInner.className = 'bar-inner';
    const pct = Math.round((v / max) * 100);
    barInner.style.width = pct + '%';
    barInner.setAttribute('title', `${v}`);
    barOuter.appendChild(barInner);
    row.appendChild(label);
    row.appendChild(barOuter);
    wrapper.appendChild(row);
  }
  container.appendChild(wrapper);
}

function renderResult(container, data){
  container.innerHTML = '';
  const grid = document.createElement('div');
  grid.className = 'result-grid';

  const left = document.createElement('div');
  left.className = 'panel animated';
  const right = document.createElement('div');
  right.className = 'panel animated';

  // Summary
  const sumTitle = document.createElement('h3'); sumTitle.textContent = 'Summary';
  left.appendChild(sumTitle);
  const total = document.createElement('p'); total.innerHTML = `<strong>Total:</strong> ${data.summary.total}`;
  left.appendChild(total);
  const catTitle = document.createElement('h4'); catTitle.textContent = 'By category';
  left.appendChild(catTitle);
  left.appendChild(renderKeyValueList(data.categorized));

  // Recommendation as sentences
  const recTitle = document.createElement('h3'); recTitle.textContent = 'Budget recommendation';
  right.appendChild(recTitle);
  const recPanel = document.createElement('div'); recPanel.className = 'panel small animated';
  const baseline = data.recommendation && data.recommendation.baseline ? data.recommendation.baseline : null;
  if(baseline){
    const p = document.createElement('p');
    p.innerHTML = `Baseline allocations — Essentials: $${baseline.Essentials}, Wants: $${baseline.Wants}, Savings: $${baseline.Savings} per month.`;
    recPanel.appendChild(p);
  }
  if(data.recommendation && Array.isArray(data.recommendation.adjustments) && data.recommendation.adjustments.length){
    const adj = document.createElement('p');
    adj.textContent = data.recommendation.adjustments.join(' ');
    recPanel.appendChild(adj);
  }
  right.appendChild(recPanel);

  // Debt and investment panels below
  const debtPanel = document.createElement('div'); debtPanel.className = 'panel animated';
  const debtTitle = document.createElement('h4'); debtTitle.textContent = 'Debt';
  debtPanel.appendChild(debtTitle);
  // render debt as a sentence
  if(!data.debt || data.debt.status === 'no_debt'){
    const p = document.createElement('p'); p.textContent = 'You have no tracked debt.'; debtPanel.appendChild(p);
  } else if(data.debt.status === 'ok'){
    const p = document.createElement('p');
    const apr = (data.debt.interest_rate !== undefined && data.debt.interest_rate !== null) ? data.debt.interest_rate : 'N/A';
    p.textContent = `Estimated payoff in ${data.debt.months_to_payoff} months using ${data.debt.strategy} strategy at APR ${apr}%`;
    debtPanel.appendChild(p);
  } else if(data.debt.message){
    const p = document.createElement('p'); p.textContent = data.debt.message; debtPanel.appendChild(p);
  }

  const investPanel = document.createElement('div'); investPanel.className = 'panel animated';
  const invTitle = document.createElement('h4'); invTitle.textContent = 'Investment suggestion (monthly)';
  investPanel.appendChild(invTitle);
  if(data.investment && Object.keys(data.investment).length){
    const list = document.createElement('p');
    const parts = [];
    for(const k of Object.keys(data.investment)){
      parts.push(`${k}: $${data.investment[k]}`);
    }
    list.textContent = parts.join(', ');
    investPanel.appendChild(list);
  }

  container.appendChild(grid);
  grid.appendChild(left);
  grid.appendChild(right);
  // render chart if possible
  // Ensure there's a chart area: either existing canvas or create a container for fallback
  let canvasWrapper = document.getElementById('category-chart');
  if(!canvasWrapper){
    // create a card with canvas for compatibility with Chart.js fallback
    const chartCard = document.createElement('div'); chartCard.className = 'card';
    const h = document.createElement('h4'); h.textContent = 'Expenses by category'; chartCard.appendChild(h);
    const canvas = document.createElement('canvas'); canvas.id = 'category-chart'; canvas.width = 400; canvas.height = 240;
    chartCard.appendChild(canvas);
    // insert at top of left panel
    left.insertBefore(chartCard, left.children[2] || null);
    canvasWrapper = document.getElementById('category-chart');
  }
  const parent = canvasWrapper.closest('.card') || canvasWrapper.parentElement;
  if(parent) parent.style.height = '260px';
  try{
    if(typeof Chart !== 'undefined'){
      renderChart(data.categorized);
    } else {
      // use mini-bars fallback in the card (create a container id)
      const fallbackId = 'mini-bars-container';
      let fb = parent.querySelector('#' + fallbackId);
      if(!fb){ fb = document.createElement('div'); fb.id = fallbackId; parent.appendChild(fb); }
      renderMiniBars(fallbackId, data.categorized);
    }
  }catch(e){ console.warn('Chart render failed', e); }
  container.appendChild(debtPanel);
  container.appendChild(investPanel);
}

window.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('advice-form');
  const resultContainer = document.getElementById('result-container');
  const clearBtn = document.getElementById('clear-btn');

  form.addEventListener('submit', async (e)=>{
    // allow normal POST fallback if user holds Shift (or for non-js)
    e.preventDefault();
    const monthly_income = parseFloat(document.getElementById('monthly_income').value || 0) || 0;
    const expensesText = document.getElementById('expenses').value || '';
    const expenses = parseExpensesText(expensesText);
    const debt_total = document.getElementById('debt_total').value;
    const debt_monthly = document.getElementById('debt_monthly').value;
    const debt_rate = document.getElementById('debt_rate').value;
    const goal_amount = document.getElementById('goal_amount').value;
    const goal_months = document.getElementById('goal_months').value;
    const risk = document.getElementById('risk_profile').value || 'moderate';

    // basic client-side validation
    if(!monthly_income || monthly_income <= 0){
      showError(resultContainer, 'Please enter a positive monthly income.');
      return;
    }

    const payload = {
      monthly_income,
      expenses,
      risk_profile: risk
    };
    if(debt_total) payload.debt = { total: parseFloat(debt_total)||0, monthly_payment: parseFloat(debt_monthly)||0, interest_rate: parseFloat(debt_rate)||0 };
    if(goal_amount && goal_months) payload.savings_goal = { amount: parseFloat(goal_amount)||0, months: parseInt(goal_months)||0 };

    showLoading(resultContainer);
    try{
      const resp = await fetch('/api/advice', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)});
      if(!resp.ok) throw new Error(`Server returned ${resp.status}`);
      const data = await resp.json();
      renderResult(resultContainer, data);
    }catch(err){
      showError(resultContainer, err.message || 'Request failed');
    }
  });

  clearBtn.addEventListener('click', ()=>{
    form.reset();
    resultContainer.innerHTML = '<div class="empty">Enter data and click <strong>Get Advice</strong> to see recommendations.</div>';
  });

  // If the server rendered a result (non-JS fallback), pick it up and render dynamic UI
  if(window.__SERVER_RESULT){
    try{
      renderResult(resultContainer, window.__SERVER_RESULT);
    }catch(e){
      console.warn('Could not render server result dynamically', e);
    }
  }
});
