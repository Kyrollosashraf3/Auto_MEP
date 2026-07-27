from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.config.logger import get_logger, read_logs

logger = get_logger(__name__)

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("", response_class=HTMLResponse)
def logs_page():
    return LOGS_HTML


@router.get("/data")
def logs_data(level: str = None, search: str = None, limit: int = 200):
    return {"logs": read_logs(level=level, search=search, limit=limit)}


LOGS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Logs - Auto MEP</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', sans-serif; background: #f0f4f8; color: #1a202c; }

  .header {
    background: linear-gradient(135deg, #1565C0, #42A5F5);
    color: white; padding: 20px 30px;
    display: flex; align-items: center; gap: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }
  .header h1 { font-size: 22px; font-weight: 600; }
  .header span { font-size: 13px; opacity: 0.85; }

  .controls {
    padding: 15px 30px; background: white;
    border-bottom: 1px solid #e2e8f0;
    display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
  }
  .controls input, .controls select, .controls button {
    padding: 8px 14px; border-radius: 6px; font-size: 14px; border: 1px solid #cbd5e0;
    outline: none;
  }
  .controls input { flex: 1; min-width: 200px; }
  .controls select { min-width: 120px; }
  .controls button {
    background: #1565C0; color: white; border: none; cursor: pointer;
    transition: background 0.2s;
  }
  .controls button:hover { background: #0D47A1; }
  .controls .count { font-size: 13px; color: #718096; margin-left: auto; }

  .log-table {
    margin: 20px 30px; background: white; border-radius: 10px;
    overflow: hidden; box-shadow: 0 1px 6px rgba(0,0,0,0.08);
  }
  table { width: 100%; border-collapse: collapse; }
  thead { background: #edf2f7; }
  th { padding: 12px 16px; text-align: left; font-size: 12px;
       text-transform: uppercase; color: #4a5568; letter-spacing: 0.5px; }
  td { padding: 10px 16px; border-top: 1px solid #f0f0f0; font-size: 13px; }
  tr:hover { background: #f7fafc; }

  .level-badge {
    display: inline-block; padding: 3px 10px; border-radius: 12px;
    font-size: 11px; font-weight: 600; text-transform: uppercase;
  }
  .level-DEBUG    { background: #e2e8f0; color: #4a5568; }
  .level-INFO     { background: #bee3f8; color: #2b6cb0; }
  .level-WARNING  { background: #fefcbf; color: #975a16; }
  .level-ERROR    { background: #fed7d7; color: #c53030; }
  .level-CRITICAL { background: #fc8181; color: white; }

  .msg { word-break: break-word; }
  .empty { text-align: center; padding: 60px; color: #a0aec0; font-size: 15px; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>Application Logs</h1>
      <span>Auto MEP Backend Activity</span>
    </div>
  </div>

  <div class="controls">
    <input type="text" id="search" placeholder="Search logs...">
    <select id="levelFilter">
      <option value="">All Levels</option>
      <option value="DEBUG">Debug</option>
      <option value="INFO">Info</option>
      <option value="WARNING">Warning</option>
      <option value="ERROR">Error</option>
    </select>
    <button onclick="fetchLogs()">Refresh</button>
    <button onclick="clearFilters()" style="background:#718096">Clear</button>
    <span class="count" id="count"></span>
  </div>

  <div class="log-table">
    <table>
      <thead>
        <tr>
          <th style="width:170px">Timestamp</th>
          <th style="width:100px">Level</th>
          <th style="width:180px">Source</th>
          <th>Message</th>
        </tr>
      </thead>
      <tbody id="logsBody"></tbody>
    </table>
    <div class="empty" id="emptyState">No logs found.</div>
  </div>

<script>
  let debounceTimer;

  document.getElementById('search').addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(fetchLogs, 400);
  });

  document.getElementById('levelFilter').addEventListener('change', fetchLogs);

  function clearFilters() {
    document.getElementById('search').value = '';
    document.getElementById('levelFilter').value = '';
    fetchLogs();
  }

  async function fetchLogs() {
    const search = document.getElementById('search').value;
    const level = document.getElementById('levelFilter').value;
    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (level) params.set('level', level);

    try {
      const res = await fetch('/logs/data?' + params.toString());
      const data = await res.json();
      renderLogs(data.logs);
    } catch(e) {
      console.error('Failed to fetch logs', e);
    }
  }

  function renderLogs(logs) {
    const tbody = document.getElementById('logsBody');
    const empty = document.getElementById('emptyState');
    const countEl = document.getElementById('count');

    tbody.innerHTML = '';

    if (!logs || logs.length === 0) {
      empty.style.display = 'block';
      countEl.textContent = '0 entries';
      return;
    }

    empty.style.display = 'none';
    countEl.textContent = logs.length + ' entries';

    logs.reverse().forEach(log => {
      const tr = document.createElement('tr');
      const lvl = log.level.trim();
      tr.innerHTML = `
        <td style="color:#718096; white-space:nowrap">${log.timestamp}</td>
        <td><span class="level-badge level-${lvl}">${lvl}</span></td>
        <td style="color:#4a5568; font-size:12px">${log.logger}</td>
        <td class="msg">${escapeHtml(log.message)}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  fetchLogs();
</script>
</body>
</html>
"""
