const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const n = (v, d = 1, u = '') => v == null ? '—' : Number(v).toFixed(d) + u;
const when = s => s ? new Date(s).toLocaleString('en-ZA', {day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit'}) : '—';

// Colour encodes temperature everywhere: cool blue, teal, amber, red.
const STOPS = [[8,[47,111,159]],[18,[62,148,150]],[26,[221,163,56]],[34,[200,66,44]]];
function heat(t) {
  if (t == null) return '#9aa7b3';
  if (t <= STOPS[0][0]) return `rgb(${STOPS[0][1]})`;
  for (let i = 1; i < STOPS.length; i++) {
    if (t <= STOPS[i][0]) {
      const [a, ca] = STOPS[i-1], [b, cb] = STOPS[i], f = (t - a) / (b - a);
      return `rgb(${ca.map((c, k) => Math.round(c + (cb[k] - c) * f))})`;
    }
  }
  return `rgb(${STOPS[STOPS.length-1][1]})`;
}
const PALETTE = ['#0b5c8c','#c8442c','#3e9496','#b07d12','#6b4c9a','#2f7d4f','#d1608a','#5b6977','#8a5a2b','#1d8fb3','#7a8f1c'];

let chart, rows = [], showAll = false, selected = '';
const PAGE = 25;

async function get(path) {
  const r = await fetch(path);
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).error || 'Request failed with status ' + r.status);
  return r.json();
}
function setMessage(text) { const m = $('message'); m.textContent = text || ''; m.classList.toggle('show', !!text); }

async function loadCities() {
  const list = await get('/api/cities');
  $('city').innerHTML = '<option value="">All cities</option>' + list.map(c => `<option value="${esc(c.city)}">${esc(c.city)}</option>`).join('');
  $('city').value = selected;
}

function renderLatest(latest) {
  const sorted = latest.slice().sort((a, b) => (b.temperature_c ?? -99) - (a.temperature_c ?? -99));
  $('readings').innerHTML = sorted.length ? sorted.map(x => {
    const w = Math.max(2, Math.min(100, (x.temperature_c ?? 0) / 40 * 100));
    return `<li><button class="reading" type="button" data-city="${esc(x.city)}" aria-pressed="${x.city === selected}">
      <span class="name">${esc(x.city)}<small>${esc(x.condition || 'No condition recorded')}, ${n(x.humidity_percent, 0, '%')} humidity</small></span>
      <span class="track" aria-hidden="true"><i style="width:${w}%;background:${heat(x.temperature_c)}"></i></span>
      <span class="temp">${n(x.temperature_c, 1, '°')}</span></button></li>`;
  }).join('') : '<li class="empty">No readings yet. Run the ETL pipeline to collect weather data.</li>';
}

function renderRows() {
  const shown = showAll ? rows : rows.slice(0, PAGE);
  $('rows').innerHTML = shown.length ? shown.map(x => `<tr>
    <td><span class="dot" style="background:${heat(x.temperature_c)}"></span>${esc(x.city)}</td>
    <td>${esc(x.condition || '—')}</td>
    <td class="num">${n(x.temperature_c, 1, '°C')}</td>
    <td class="num">${n(x.feels_like_c, 1, '°C')}</td>
    <td class="num">${n(x.humidity_percent, 0, '%')}</td>
    <td class="num">${n(x.wind_speed_mps, 1, ' m/s')}</td>
    <td>${when(x.extracted_at)}</td></tr>`).join('')
    : '<tr><td colspan="7" class="empty">No records found. Run the ETL pipeline to collect weather data.</td></tr>';
  $('logNote').textContent = rows.length ? `Newest ${rows.length} records` : '';
  $('more').hidden = rows.length <= PAGE;
  $('moreNote').textContent = `Showing ${shown.length} of ${rows.length}`;
  $('toggle').textContent = showAll ? 'Show fewer' : 'Show all ' + rows.length;
}

function renderChart() {
  const byCity = {};
  rows.slice().reverse().forEach(r => { (byCity[r.city] ||= []).push({x: new Date(r.extracted_at).getTime(), y: r.temperature_c}); });
  const names = Object.keys(byCity).sort();
  if (chart) chart.destroy();
  if (!window.Chart) { setMessage('The chart library could not load, so the chart is hidden. The tables still work.'); return; }
  chart = new Chart($('chart'), {
    type: 'line',
    data: { datasets: names.map((c, i) => ({ label: c, data: byCity[c], borderColor: PALETTE[i % PALETTE.length], backgroundColor: PALETTE[i % PALETTE.length], borderWidth: 1.75, pointRadius: 0, pointHoverRadius: 4, tension: .25 })) },
    options: {
      responsive: true, maintainAspectRatio: false, interaction: {mode: 'nearest', intersect: false},
      plugins: {
        legend: {position: 'bottom', labels: {usePointStyle: true, boxWidth: 8, color: '#5b6977', font: {family: 'Schibsted Grotesk', size: 12}}},
        tooltip: {callbacks: {title: c => c[0].dataset.label + ', ' + when(c[0].parsed.x), label: c => c.parsed.y.toFixed(1) + '°C'}}
      },
      scales: {
        x: {type: 'linear', ticks: {maxTicksLimit: 8, color: '#5b6977', callback: v => new Date(v).toLocaleDateString('en-ZA', {day: 'numeric', month: 'short'})}, grid: {display: false}},
        y: {title: {display: true, text: '°C', color: '#5b6977'}, ticks: {color: '#5b6977'}, grid: {color: '#e6ebef'}}
      }
    }
  });
}

async function load() {
  selected = $('city').value;
  const qs = selected ? '?city=' + encodeURIComponent(selected) : '';
  setMessage('');
  try {
    const [summary, latest, history] = await Promise.all([
      get('/api/summary' + qs), get('/api/latest'), get('/api/history' + (qs ? qs + '&' : '?') + 'limit=200')
    ]);
    $('scope').textContent = selected || 'All cities';
    $('records').textContent = Number(summary.total_records).toLocaleString('en-ZA');
    $('cities').textContent = summary.cities;
    $('temp').textContent = n(summary.avg_temperature_c, 1, '°C');
    $('humidity').textContent = n(summary.avg_humidity_percent, 0, '%');
    $('updated').textContent = when(summary.last_recorded_at);
    rows = history; showAll = false;
    renderLatest(latest); renderRows(); renderChart();
  } catch (e) {
    setMessage("Can't load readings from the database. Check that PostgreSQL is running and the ETL pipeline has created the weather_data table. Details: " + e.message);
    $('readings').innerHTML = '<li class="empty">Readings unavailable.</li>';
  }
}

$('readings').addEventListener('click', e => {
  const b = e.target.closest('.reading'); if (!b) return;
  $('city').value = b.dataset.city === selected ? '' : b.dataset.city;
  load();
});
$('toggle').addEventListener('click', () => { showAll = !showAll; renderRows(); });
$('city').addEventListener('change', load);
$('refresh').addEventListener('click', async () => { try { await loadCities(); } catch (e) {} await load(); });
(async () => { try { await loadCities(); } catch (e) {} await load(); })();
