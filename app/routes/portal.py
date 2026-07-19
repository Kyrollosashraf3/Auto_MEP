from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Portal"])

PORTAL_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auto MEP &mdash; Engineering Portal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0c1a28;
    --bg-panel:#0f2136;
    --bg-elevated:#16304a;
    --line:#23425f;
    --line-soft:rgba(94,200,242,0.10);
    --cyan:#5ec8f2;
    --cyan-dim:#3a7fa0;
    --amber:#e0a03d;
    --text:#e8eef4;
    --text-dim:#8aa5ba;
    --text-faint:#526e85;
    --danger:#e2574c;
    --success:#4fc38a;
    --font-display:'Space Grotesk',sans-serif;
    --font-body:'IBM Plex Sans',sans-serif;
    --font-mono:'IBM Plex Mono',monospace;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;height:100%;}
  body{
    font-family:var(--font-body);
    background:var(--bg);
    color:var(--text);
    background-image:
      linear-gradient(var(--line-soft) 1px, transparent 1px),
      linear-gradient(90deg, var(--line-soft) 1px, transparent 1px);
    background-size:36px 36px;
    min-height:100vh;
  }
  ::selection{background:var(--cyan);color:#06121d;}
  a{color:var(--cyan);}
  button{font-family:var(--font-body);cursor:pointer;}
  input,select,textarea{font-family:var(--font-body);}

  .hidden{display:none !important;}

  /* ---------- corner-tick "drawing frame" utility ---------- */
  .framed{position:relative;}
  .framed::before,.framed::after,
  .framed .tick-tl,.framed .tick-br{position:absolute;width:10px;height:10px;pointer-events:none;}
  .framed::before{content:"";top:-1px;left:-1px;border-top:2px solid var(--cyan-dim);border-left:2px solid var(--cyan-dim);}
  .framed::after{content:"";bottom:-1px;right:-1px;border-bottom:2px solid var(--cyan-dim);border-right:2px solid var(--cyan-dim);}

  /* ---------- AUTH VIEW ---------- */
  #authView{
    min-height:100vh;display:flex;align-items:center;justify-content:center;
    padding:24px;
  }
  .auth-card{
    width:100%;max-width:420px;
    background:var(--bg-panel);
    border:1px solid var(--line);
    padding:40px 36px 32px;
  }
  .brand{
    display:flex;align-items:baseline;gap:10px;margin-bottom:6px;
  }
  .brand-mark{
    font-family:var(--font-mono);font-weight:600;font-size:13px;color:var(--amber);
    border:1px solid var(--amber);padding:2px 6px;letter-spacing:.08em;
  }
  .brand-name{font-family:var(--font-display);font-weight:700;font-size:20px;letter-spacing:.01em;}
  .auth-sub{font-family:var(--font-mono);font-size:11px;color:var(--text-faint);letter-spacing:.12em;text-transform:uppercase;margin-bottom:28px;}

  .tabbar{display:flex;border:1px solid var(--line);margin-bottom:24px;}
  .tabbar button{
    flex:1;background:transparent;border:none;color:var(--text-dim);
    font-family:var(--font-mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;
    padding:10px 0;border-bottom:2px solid transparent;transition:.15s;
  }
  .tabbar button.active{color:var(--cyan);border-bottom-color:var(--cyan);background:var(--line-soft);}

  .field{margin-bottom:16px;}
  .field label{
    display:block;font-family:var(--font-mono);font-size:10.5px;color:var(--text-faint);
    text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;
  }
  .field input,.field select{
    width:100%;background:var(--bg);border:1px solid var(--line);color:var(--text);
    padding:10px 12px;font-size:14px;outline:none;transition:border-color .15s;
  }
  .field input:focus,.field select:focus{border-color:var(--cyan);}

  .btn{
    display:inline-flex;align-items:center;justify-content:center;gap:8px;
    background:var(--cyan);color:#06121d;border:none;font-weight:600;font-size:13.5px;
    padding:11px 18px;transition:.15s;
  }
  .btn:hover{background:#7ed4f6;}
  .btn:disabled{opacity:.5;cursor:not-allowed;}
  .btn-block{width:100%;}
  .btn-ghost{background:transparent;border:1px solid var(--line);color:var(--text);}
  .btn-ghost:hover{border-color:var(--cyan);color:var(--cyan);}
  .btn-amber{background:var(--amber);color:#231404;}
  .btn-amber:hover{background:#eeb15c;}
  .btn-danger{background:transparent;border:1px solid var(--danger);color:var(--danger);}
  .btn-danger:hover{background:rgba(226,87,76,.12);}
  .btn-sm{padding:6px 12px;font-size:12px;}

  .auth-error{
    background:rgba(226,87,76,.1);border:1px solid var(--danger);color:#ff9188;
    font-size:13px;padding:10px 12px;margin-bottom:16px;font-family:var(--font-mono);
  }

  /* ---------- APP SHELL ---------- */
  #appView{display:flex;min-height:100vh;}

  .sidebar{
    width:280px;flex-shrink:0;background:var(--bg-panel);border-right:1px solid var(--line);
    display:flex;flex-direction:column;
  }
  .sidebar-head{padding:22px 20px 18px;border-bottom:1px solid var(--line);}
  .sidebar-projects{flex:1;overflow-y:auto;padding:14px 12px;}
  .sidebar-section-label{
    font-family:var(--font-mono);font-size:10px;color:var(--text-faint);
    text-transform:uppercase;letter-spacing:.12em;padding:0 8px;margin-bottom:10px;
    display:flex;justify-content:space-between;align-items:center;
  }
  .project-item{
    display:flex;flex-direction:column;gap:2px;
    padding:10px 12px;margin-bottom:4px;border:1px solid transparent;cursor:pointer;
    transition:.12s;
  }
  .project-item:hover{background:var(--line-soft);}
  .project-item.active{background:var(--line-soft);border-color:var(--cyan-dim);}
  .project-item-name{font-size:13.5px;font-weight:500;}
  .project-item-meta{font-family:var(--font-mono);font-size:10.5px;color:var(--text-faint);}
  .empty-projects{padding:20px 8px;color:var(--text-faint);font-size:12.5px;font-family:var(--font-mono);}

  .sidebar-foot{border-top:1px solid var(--line);padding:16px 20px;}
  .user-stamp{
    font-family:var(--font-mono);font-size:11px;color:var(--text-dim);
    display:flex;flex-direction:column;gap:2px;margin-bottom:12px;
  }
  .user-stamp .u-name{color:var(--text);font-size:13px;font-weight:500;font-family:var(--font-body);}
  .u-role{color:var(--amber);text-transform:uppercase;letter-spacing:.08em;font-size:10px;}

  .main{flex:1;display:flex;flex-direction:column;min-width:0;}
  .topbar{
    height:64px;flex-shrink:0;border-bottom:1px solid var(--line);
    display:flex;align-items:center;justify-content:space-between;padding:0 28px;
  }
  .crumb{font-family:var(--font-mono);font-size:11px;color:var(--text-faint);letter-spacing:.06em;}
  .crumb b{color:var(--cyan);}
  .topbar-actions{display:flex;gap:10px;}

  .content{flex:1;overflow-y:auto;padding:32px;}

  .empty-state{
    height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;
    color:var(--text-faint);gap:10px;text-align:center;
  }
  .empty-state .glyph{font-family:var(--font-mono);font-size:34px;color:var(--line);}
  .empty-state h3{font-family:var(--font-display);font-weight:600;color:var(--text-dim);margin:0;}
  .empty-state p{font-size:13px;max-width:320px;margin:0;}

  /* ---------- title block ---------- */
  .title-block{
    background:var(--bg-panel);border:1px solid var(--line);padding:22px 26px;margin-bottom:24px;
  }
  .title-block-top{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin-bottom:14px;}
  .tb-name{font-family:var(--font-display);font-size:22px;font-weight:700;}
  .tb-desc{color:var(--text-dim);font-size:13.5px;margin-top:6px;max-width:520px;}
  .tb-meta{display:flex;gap:24px;border-top:1px solid var(--line);padding-top:12px;margin-top:4px;flex-wrap:wrap;}
  .tb-meta-item{font-family:var(--font-mono);font-size:10.5px;color:var(--text-faint);text-transform:uppercase;letter-spacing:.08em;}
  .tb-meta-item span{display:block;color:var(--text-dim);font-size:12.5px;text-transform:none;letter-spacing:0;margin-top:3px;font-family:var(--font-mono);}

  .panel{background:var(--bg-panel);border:1px solid var(--line);}
  .panel-head{
    display:flex;justify-content:space-between;align-items:center;
    padding:16px 22px;border-bottom:1px solid var(--line);
  }
  .panel-head h4{margin:0;font-family:var(--font-display);font-size:15px;font-weight:600;}

  table{width:100%;border-collapse:collapse;}
  th{
    text-align:left;font-family:var(--font-mono);font-size:10px;color:var(--text-faint);
    text-transform:uppercase;letter-spacing:.08em;padding:12px 22px;border-bottom:1px solid var(--line);
  }
  td{padding:13px 22px;border-bottom:1px solid var(--line);font-size:13.5px;}
  tr:last-child td{border-bottom:none;}
  td.mono{font-family:var(--font-mono);font-size:12.5px;color:var(--text-dim);}
  tr:hover td{background:var(--line-soft);}
  .row-actions{display:flex;gap:8px;}
  .table-empty{padding:36px 22px;text-align:center;color:var(--text-faint);font-size:13px;font-family:var(--font-mono);}

  /* ---------- modal ---------- */
  .modal-overlay{
    display:none;position:fixed;inset:0;background:rgba(6,14,22,.72);
    align-items:center;justify-content:center;z-index:1000;padding:20px;
  }
  .modal-overlay.active{display:flex;}
  .modal-box{
    background:var(--bg-panel);border:1px solid var(--line);width:100%;max-width:560px;
    max-height:82vh;display:flex;flex-direction:column;
  }
  .modal-box.wide{max-width:720px;}
  .modal-head{
    display:flex;justify-content:space-between;align-items:center;
    padding:18px 22px;border-bottom:1px solid var(--line);flex-shrink:0;
  }
  .modal-head h3{margin:0;font-family:var(--font-display);font-size:16px;font-weight:600;}
  .modal-close{background:none;border:none;color:var(--text-faint);font-size:20px;line-height:1;padding:4px;}
  .modal-close:hover{color:var(--text);}
  .modal-body{padding:22px;overflow-y:auto;}
  .modal-foot{padding:16px 22px;border-top:1px solid var(--line);display:flex;justify-content:flex-end;gap:10px;flex-shrink:0;}

  .spec-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);}
  .spec-cell{background:var(--bg-panel);padding:12px 16px;}
  .spec-cell.full{grid-column:1 / -1;}
  .spec-label{font-family:var(--font-mono);font-size:10px;color:var(--text-faint);text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px;}
  .spec-value{font-family:var(--font-mono);font-size:15px;color:var(--cyan);font-weight:600;}
  .spec-value.amber{color:var(--amber);}
  .spec-value small{font-size:11px;color:var(--text-dim);font-weight:400;margin-left:4px;}

  .report-text{white-space:pre-wrap;line-height:1.65;font-size:13.5px;color:var(--text);font-family:var(--font-body);}

  .status-line{font-family:var(--font-mono);font-size:12.5px;color:var(--text-faint);display:flex;align-items:center;gap:8px;}
  .spin{
    width:12px;height:12px;border:2px solid var(--line);border-top-color:var(--cyan);
    border-radius:50%;animation:spin .7s linear infinite;
  }
  @keyframes spin{to{transform:rotate(360deg);}}

  .toast{
    position:fixed;bottom:24px;right:24px;background:var(--bg-elevated);border:1px solid var(--danger);
    color:#ff9188;padding:12px 16px;font-size:13px;font-family:var(--font-mono);z-index:2000;max-width:340px;
  }
  .toast.success{border-color:var(--success);color:#a4f0cf;}

  ::-webkit-scrollbar{width:8px;height:8px;}
  ::-webkit-scrollbar-track{background:transparent;}
  ::-webkit-scrollbar-thumb{background:var(--line);}

  /* ---------- Home Page Styles ---------- */
  .home-landing {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 128px);
    animation: fadeIn 0.25s ease-out;
  }
  .hero-card {
    background: var(--bg-panel);
    border: 1px solid var(--line);
    padding: 48px;
    text-align: center;
    max-width: 580px;
    border-radius: 4px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  }
  .hero-brand {
    display: inline-flex;
    background: var(--cyan);
    color: #06121d;
    font-family: var(--font-display);
    font-size: 24px;
    font-weight: 700;
    padding: 8px 16px;
    margin-bottom: 24px;
    letter-spacing: .05em;
  }
  .hero-card h2 {
    margin: 0 0 12px 0;
    font-family: var(--font-display);
    font-size: 28px;
    font-weight: 700;
  }
  .hero-card p {
    margin: 0;
    font-size: 15px;
    color: var(--text-dim);
    line-height: 1.65;
  }
  .home-container {
    max-width: 900px;
    margin: 0 auto;
    animation: fadeIn 0.25s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .section-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    border-bottom: 1px solid var(--line);
    padding-bottom: 12px;
  }
  .section-title h3 {
    margin: 0;
    font-family: var(--font-display);
    font-size: 18px;
    font-weight: 600;
  }
  .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
  }
  .project-card {
    background: var(--bg-panel);
    border: 1px solid var(--line);
    padding: 20px;
    cursor: pointer;
    transition: all 0.15s ease-in-out;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 140px;
  }
  .project-card:hover {
    border-color: var(--cyan);
    background: var(--line-soft);
    transform: translateY(-2px);
  }
  .pc-title {
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--text);
  }
  .pc-desc {
    font-size: 13px;
    color: var(--text-dim);
    margin-bottom: 16px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.4;
    flex-grow: 1;
  }
  .pc-meta {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--text-faint);
  }
  .empty-projects-home {
    grid-column: 1 / -1;
    background: var(--bg-panel);
    border: 1px solid var(--line);
    padding: 40px;
    text-align: center;
    color: var(--text-faint);
    font-family: var(--font-mono);
    font-size: 13.5px;
  }
</style>
</head>
<body>

<!-- ================= AUTH VIEW ================= -->
<div id="authView">
  <div class="auth-card framed">
    <div class="brand">
      <span class="brand-mark">MEP</span>
      <span class="brand-name">Auto MEP</span>
    </div>
    <div class="auth-sub">Engineering Analysis Portal</div>

    <div class="tabbar">
      <button id="tabSignIn" class="active" onclick="switchTab('signin')">Sign In</button>
      <button id="tabSignUp" onclick="switchTab('signup')">Sign Up</button>
    </div>

    <div id="authError" class="auth-error hidden"></div>

    <form id="signInForm" onsubmit="return handleSignIn(event)">
      <div class="field">
        <label>Email</label>
        <input type="email" id="siEmail" required autocomplete="username">
      </div>
      <div class="field">
        <label>Password</label>
        <input type="password" id="siPassword" required autocomplete="current-password">
      </div>
      <button type="submit" class="btn btn-block" id="siSubmit">Sign In</button>
    </form>

    <form id="signUpForm" class="hidden" onsubmit="return handleSignUp(event)">
      <div class="field">
        <label>Full Name</label>
        <input type="text" id="suName" required>
      </div>
      <div class="field">
        <label>Email</label>
        <input type="email" id="suEmail" required autocomplete="username">
      </div>
      <div class="field">
        <label>Password</label>
        <input type="password" id="suPassword" required autocomplete="new-password">
      </div>
      <div class="field">
        <label>Role</label>
        <select id="suRole">
          <option value="engineer" selected>Engineer</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit" class="btn btn-block" id="suSubmit">Create Account</button>
    </form>
  </div>
</div>

<!-- ================= APP VIEW ================= -->
<div id="appView" class="hidden">
  <aside class="sidebar">
    <div class="sidebar-head" style="cursor:pointer;" onclick="showHomePage()">
      <div class="brand">
        <span class="brand-mark">MEP</span>
        <span class="brand-name">Auto MEP</span>
      </div>
    </div>
    <div class="sidebar-projects">
      <div class="sidebar-section-label">
        <span>Projects</span>
        <span style="cursor:pointer;color:var(--cyan);" onclick="openNewProjectModal()">+ New</span>
      </div>
      <div id="projectList"></div>
    </div>
    <div class="sidebar-foot">
      <div class="user-stamp">
        <span class="u-name" id="userName">&mdash;</span>
        <span id="userEmail">&mdash;</span>
        <span class="u-role" id="userRole">&mdash;</span>
      </div>
      <button class="btn btn-ghost btn-block btn-sm" onclick="logout()">Sign Out</button>
    </div>
  </aside>

  <div class="main">
    <div class="topbar">
      <div class="crumb" id="crumb">No project selected</div>
      <div class="topbar-actions" id="topbarActions"></div>
    </div>
    <div class="content" id="content">
      <div class="empty-state">
        <div class="glyph">&#9633;</div>
        <h3>No project selected</h3>
        <p>Pick a project from the sidebar, or create a new one to start uploading room data and running load analysis.</p>
      </div>
    </div>
  </div>
</div>

<!-- ================= MODALS ================= -->
<div class="modal-overlay" id="newProjectModal">
  <div class="modal-box framed">
    <div class="modal-head"><h3>New Project</h3><button class="modal-close" onclick="closeModal('newProjectModal')">&times;</button></div>
    <form onsubmit="return handleCreateProject(event)">
      <div class="modal-body">
        <div id="npError" class="auth-error hidden"></div>
        <div class="field">
          <label>Project Name</label>
          <input type="text" id="npName" required>
        </div>
        <div class="field" style="margin-bottom:0;">
          <label>Description</label>
          <input type="text" id="npDescription" placeholder="Optional">
        </div>
      </div>
      <div class="modal-foot">
        <button type="button" class="btn btn-ghost" onclick="closeModal('newProjectModal')">Cancel</button>
        <button type="submit" class="btn" id="npSubmit">Create Project</button>
      </div>
    </form>
  </div>
</div>

<div class="modal-overlay" id="editProjectModal">
  <div class="modal-box framed">
    <div class="modal-head"><h3>Edit Project</h3><button class="modal-close" onclick="closeModal('editProjectModal')">&times;</button></div>
    <form onsubmit="return handleEditProject(event)">
      <div class="modal-body">
        <div id="epError" class="auth-error hidden"></div>
        <div class="field">
          <label>Project Name</label>
          <input type="text" id="epName" required>
        </div>
        <div class="field" style="margin-bottom:0;">
          <label>Description</label>
          <input type="text" id="epDescription" placeholder="Optional">
        </div>
      </div>
      <div class="modal-foot">
        <button type="button" class="btn btn-ghost" onclick="closeModal('editProjectModal')">Cancel</button>
        <button type="submit" class="btn" id="epSubmit">Save Changes</button>
      </div>
    </form>
  </div>
</div>

<div class="modal-overlay" id="resultModal">
  <div class="modal-box wide framed">
    <div class="modal-head"><h3 id="resultTitle">Result</h3><button class="modal-close" onclick="closeModal('resultModal')">&times;</button></div>
    <div class="modal-body" id="resultBody"></div>
  </div>
</div>

<script>
const API = "";
let state = { token: null, user: null, projects: [], currentProject: null };

try { state.token = localStorage.getItem('automep_token'); } catch(e) { state.token = null; }

/* ---------------- API helper ---------------- */
async function api(path, opts={}) {
  const headers = opts.headers || {};
  if (state.token) headers["Authorization"] = "Bearer " + state.token;
  const res = await fetch(API + path, {...opts, headers});
  let data = null;
  try { data = await res.json(); } catch(e) { data = null; }
  if (!res.ok) {
    const detail = (data && data.detail) ? data.detail : ("Request failed (" + res.status + ")");
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return data;
}

function showToast(msg, type) {
  const t = document.createElement('div');
  t.className = 'toast' + (type === 'success' ? ' success' : '');
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 4200);
}

/* ---------------- AUTH ---------------- */
function switchTab(tab) {
  document.getElementById('tabSignIn').classList.toggle('active', tab === 'signin');
  document.getElementById('tabSignUp').classList.toggle('active', tab === 'signup');
  document.getElementById('signInForm').classList.toggle('hidden', tab !== 'signin');
  document.getElementById('signUpForm').classList.toggle('hidden', tab !== 'signup');
  document.getElementById('authError').classList.add('hidden');
}

function showAuthError(msg) {
  const el = document.getElementById('authError');
  el.textContent = msg;
  el.classList.remove('hidden');
}

async function handleSignIn(ev) {
  ev.preventDefault();
  const btn = document.getElementById('siSubmit');
  btn.disabled = true; btn.textContent = 'Signing in\u2026';
  document.getElementById('authError').classList.add('hidden');
  try {
    const email = document.getElementById('siEmail').value;
    const password = document.getElementById('siPassword').value;
    const body = new URLSearchParams();
    body.set('username', email);
    body.set('password', password);
    const res = await fetch(API + '/auth/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: body.toString()
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Incorrect email or password');
    state.token = data.access_token;
    try { localStorage.setItem('automep_token', state.token); } catch(e) {}
    await bootApp();
  } catch (e) {
    showAuthError(e.message);
  } finally {
    btn.disabled = false; btn.textContent = 'Sign In';
  }
}

async function handleSignUp(ev) {
  ev.preventDefault();
  const btn = document.getElementById('suSubmit');
  btn.disabled = true; btn.textContent = 'Creating\u2026';
  document.getElementById('authError').classList.add('hidden');
  try {
    const payload = {
      name: document.getElementById('suName').value,
      email: document.getElementById('suEmail').value,
      password: document.getElementById('suPassword').value,
      role: document.getElementById('suRole').value
    };
    await api('/auth/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    showToast('Account created \u2014 signing you in\u2026', 'success');
    document.getElementById('siEmail').value = payload.email;
    document.getElementById('siPassword').value = payload.password;
    switchTab('signin');
    await handleSignIn({preventDefault(){}});
  } catch (e) {
    showAuthError(e.message);
  } finally {
    btn.disabled = false; btn.textContent = 'Create Account';
  }
}

function logout() {
  state.token = null; state.user = null; state.projects = []; state.currentProject = null;
  try { localStorage.removeItem('automep_token'); } catch(e) {}
  document.getElementById('appView').classList.add('hidden');
  document.getElementById('authView').classList.remove('hidden');
}

/* ---------------- BOOT ---------------- */
async function bootApp() {
  const me = await api('/auth/me');
  state.user = me;
  document.getElementById('userName').textContent = me.name;
  document.getElementById('userEmail').textContent = me.email;
  document.getElementById('userRole').textContent = me.role;
  document.getElementById('authView').classList.add('hidden');
  document.getElementById('appView').classList.remove('hidden');
  await loadProjects();
  showHomePage();
}

async function loadProjects() {
  const projects = await api('/projects');
  state.projects = projects;
  renderProjectList();
}

function renderProjectList() {
  const el = document.getElementById('projectList');
  if (!state.projects.length) {
    el.innerHTML = '<div class="empty-projects">No projects yet.<br>Create your first project.</div>';
    return;
  }
  el.innerHTML = state.projects.map(p => `
    <div class="project-item ${state.currentProject && state.currentProject.id === p.id ? 'active' : ''}" onclick="selectProject(${p.id})">
      <span class="project-item-name">${escapeHtml(p.name)}</span>
      <span class="project-item-meta">REF-${String(p.id).padStart(4,'0')} &middot; ${new Date(p.created_at).toLocaleDateString()}</span>
    </div>
  `).join('');
}

function showHomePage() {
  state.currentProject = null;
  renderProjectList();
  document.getElementById('crumb').innerHTML = '<b>Home</b>';
  document.getElementById('topbarActions').innerHTML = '';
  
  document.getElementById('content').innerHTML = `
    <div class="home-landing">
      <div class="hero-card">
        <div class="hero-brand">MEP</div>
        <h2>Auto MEP Portal</h2>
        <p>Automate your Mechanical, Electrical, and Plumbing load analyses with state-of-the-art AI calculations, RAG search, and reporting.</p>
        <button class="btn btn-lg" onclick="showProjectsGrid()" style="margin-top:24px; font-size:16px; padding:14px 28px;">
          &mdash; My Projects
        </button>
      </div>
    </div>
  `;
}

function showProjectsGrid() {
  document.getElementById('crumb').innerHTML = '<b>Home</b> &nbsp;/&nbsp; Projects';
  document.getElementById('topbarActions').innerHTML = `
    <button class="btn btn-ghost btn-sm" onclick="showHomePage()">Back Home</button>
    <button class="btn btn-amber btn-sm" onclick="openNewProjectModal()">+ New Project</button>
  `;

  const projectsHtml = state.projects && state.projects.length ? state.projects.map(p => `
    <div class="project-card" onclick="selectProject(${p.id})">
      <div class="pc-title">${escapeHtml(p.name)}</div>
      <div class="pc-desc">${p.description ? escapeHtml(p.description) : 'No description provided.'}</div>
      <div class="pc-meta">REF-${String(p.id).padStart(4,'0')} &middot; ${new Date(p.created_at).toLocaleDateString()}</div>
    </div>
  `).join('') : `
    <div class="empty-projects-home">
      <p>No projects created yet.</p>
      <button class="btn btn-sm" style="margin-top:10px;" onclick="openNewProjectModal()">Create Your First Project</button>
    </div>
  `;

  document.getElementById('content').innerHTML = `
    <div class="home-container">
      <div class="section-title">
        <h3>My Projects</h3>
        <button class="btn btn-ghost btn-sm" onclick="openNewProjectModal()">+ New Project</button>
      </div>
      <div class="projects-grid">
        ${projectsHtml}
      </div>
    </div>
  `;
}

/* ---------------- PROJECT DETAIL ---------------- */
async function selectProject(id) {
  try {
    const proj = await api('/projects/id/' + id);
    state.currentProject = proj;
    renderProjectList();
    renderProjectDetail();
  } catch (e) {
    showToast(e.message);
  }
}

function renderProjectDetail() {
  const p = state.currentProject;
  document.getElementById('crumb').innerHTML = '<b>' + escapeHtml(p.name) + '</b> &nbsp;/&nbsp; Files';

  document.getElementById('topbarActions').innerHTML = `
    <button class="btn btn-ghost btn-sm" onclick="openEditProjectModal()">Edit Project</button>
    <button class="btn btn-ghost btn-sm btn-danger" onclick="deleteCurrentProject()">Delete Project</button>
    <label class="btn btn-amber btn-sm" style="margin:0;">
      Upload File
      <input type="file" id="fileInput" accept=".xlsx,.csv" style="display:none;" onchange="handleUpload(event)">
    </label>
  `;

  const fileRows = p.files && p.files.length ? p.files.map(f => `
    <tr>
      <td class="mono">F-${String(f.id).padStart(4,'0')}</td>
      <td>${escapeHtml(f.file_name)}</td>
      <td class="mono">${new Date(f.uploaded_at).toLocaleString()}</td>
      <td>
        <div class="row-actions">
          <button class="btn btn-ghost btn-sm" onclick="runAnalysis(${f.id}, '${escapeHtml(f.file_name)}')">Analyze</button>
          <button class="btn btn-ghost btn-sm" onclick="runReport(${f.id}, '${escapeHtml(f.file_name)}')">Report</button>
          <button class="btn btn-ghost btn-sm btn-danger" onclick="deleteFile(${f.id}, '${escapeHtml(f.file_name)}')">Delete</button>
        </div>
      </td>
    </tr>
  `).join('') : `<tr><td colspan="4" class="table-empty">No files uploaded yet. Upload a room-data sheet (.xlsx / .csv) to run an analysis.</td></tr>`;

  document.getElementById('content').innerHTML = `
    <div class="title-block framed">
      <div class="title-block-top">
        <div>
          <div class="tb-name">${escapeHtml(p.name)}</div>
          <div class="tb-desc">${p.description ? escapeHtml(p.description) : 'No description provided.'}</div>
        </div>
      </div>
      <div class="tb-meta">
        <div class="tb-meta-item">Ref No<span>REF-${String(p.id).padStart(4,'0')}</span></div>
        <div class="tb-meta-item">Created<span>${new Date(p.created_at).toLocaleDateString()}</span></div>
        <div class="tb-meta-item">Files<span>${p.files ? p.files.length : 0}</span></div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-head">
        <h4>Room Data Files</h4>
      </div>
      <table>
        <thead>
          <tr><th>ID</th><th>File Name</th><th>Uploaded</th><th>Actions</th></tr>
        </thead>
        <tbody>${fileRows}</tbody>
      </table>
    </div>
  `;
}

async function deleteCurrentProject() {
  if (!state.currentProject) return;
  if (!confirm('Delete project "' + state.currentProject.name + '"? This cannot be undone.')) return;
  try {
    await api('/projects/' + state.currentProject.id, {method: 'DELETE'});
    await loadProjects();
    showHomePage();
    showToast('Project deleted', 'success');
  } catch (e) {
    showToast(e.message);
  }
}

function openEditProjectModal() {
  if (!state.currentProject) return;
  document.getElementById('epName').value = state.currentProject.name;
  document.getElementById('epDescription').value = state.currentProject.description || '';
  document.getElementById('epError').classList.add('hidden');
  document.getElementById('editProjectModal').classList.add('active');
}

async function handleEditProject(ev) {
  ev.preventDefault();
  const btn = document.getElementById('epSubmit');
  btn.disabled = true; btn.textContent = 'Saving\u2026';
  try {
    const payload = {
      name: document.getElementById('epName').value,
      description: document.getElementById('epDescription').value || null
    };
    const updatedProj = await api('/projects/' + state.currentProject.id, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    closeModal('editProjectModal');
    await loadProjects();
    await selectProject(updatedProj.id);
    showToast('Project updated', 'success');
  } catch (e) {
    const errEl = document.getElementById('epError');
    errEl.textContent = e.message;
    errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false; btn.textContent = 'Save Changes';
  }
}

async function deleteFile(fileId, fileName) {
  if (!state.currentProject) return;
  if (!confirm('Delete file "' + fileName + '"? This cannot be undone.')) return;
  try {
    await api('/projects/' + state.currentProject.id + '/files?file_id=' + fileId, {method: 'DELETE'});
    await selectProject(state.currentProject.id);
    showToast('File deleted', 'success');
  } catch (e) {
    showToast(e.message);
  }
}

async function handleUpload(ev) {
  const file = ev.target.files[0];
  if (!file || !state.currentProject) return;
  const fd = new FormData();
  fd.append('file', file);
  try {
    showToast('Uploading ' + file.name + '\u2026', 'success');
    await api('/projects/' + state.currentProject.id + '/files', {method: 'POST', body: fd});
    await selectProject(state.currentProject.id);
    showToast('File uploaded', 'success');
  } catch (e) {
    showToast(e.message);
  } finally {
    ev.target.value = '';
  }
}

/* ---------------- NEW PROJECT MODAL ---------------- */
function openNewProjectModal() {
  document.getElementById('npName').value = '';
  document.getElementById('npDescription').value = '';
  document.getElementById('npError').classList.add('hidden');
  document.getElementById('newProjectModal').classList.add('active');
}

async function handleCreateProject(ev) {
  ev.preventDefault();
  const btn = document.getElementById('npSubmit');
  btn.disabled = true; btn.textContent = 'Creating\u2026';
  try {
    const payload = {
      name: document.getElementById('npName').value,
      description: document.getElementById('npDescription').value || null
    };
    const proj = await api('/projects', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    closeModal('newProjectModal');
    await loadProjects();
    await selectProject(proj.id);
    showToast('Project created', 'success');
  } catch (e) {
    const el = document.getElementById('npError');
    el.textContent = e.message;
    el.classList.remove('hidden');
  } finally {
    btn.disabled = false; btn.textContent = 'Create Project';
  }
}

/* ---------------- ANALYSIS / REPORT ---------------- */
function openResultModal(title) {
  document.getElementById('resultTitle').textContent = title;
  document.getElementById('resultBody').innerHTML = '<div class="status-line"><span class="spin"></span> Processing\u2026</div>';
  document.getElementById('resultModal').classList.add('active');
}

async function runAnalysis(fileId, fileName) {
  openResultModal('Load Analysis \u2014 ' + fileName);
  try {
    const d = await api('/analysis/' + fileId);
    document.getElementById('resultBody').innerHTML = `
      <div class="spec-grid">
        <div class="spec-cell"><div class="spec-label">Total Rooms</div><div class="spec-value">${fmt(d.total_rooms)}</div></div>
        <div class="spec-cell"><div class="spec-label">Total Occupancy</div><div class="spec-value">${fmt(d.total_occupancy)}</div></div>
        <div class="spec-cell"><div class="spec-label">Total Area</div><div class="spec-value">${fmt(d.total_area_m2)}<small>m&sup2;</small></div></div>
        <div class="spec-cell"><div class="spec-label">Average Room Area</div><div class="spec-value">${fmt(d.average_room_area_m2)}<small>m&sup2;</small></div></div>
        <div class="spec-cell"><div class="spec-label">Total Lighting Load</div><div class="spec-value">${fmt(d.total_lighting_w)}<small>W</small></div></div>
        <div class="spec-cell"><div class="spec-label">Total Equipment Load</div><div class="spec-value">${fmt(d.total_equipment_w)}<small>W</small></div></div>
        <div class="spec-cell"><div class="spec-label">Total Fresh Air</div><div class="spec-value">${fmt(d.total_fresh_air_cfm)}<small>CFM</small></div></div>
        <div class="spec-cell"><div class="spec-label">Largest Room</div><div class="spec-value">${d.largest_room ? escapeHtml(d.largest_room) : '\u2014'}<small>${fmt(d.largest_room_area_m2)} m&sup2;</small></div></div>
        <div class="spec-cell full"><div class="spec-label">Estimated Total Load</div><div class="spec-value amber">${fmt(d.estimated_total_load_w)}<small>W</small></div></div>
        <div class="spec-cell full"><div class="spec-label">Estimated Cooling Load</div><div class="spec-value amber">${fmt(d.estimated_tr)}<small>TR</small></div></div>
      </div>
    `;
  } catch (e) {
    document.getElementById('resultBody').innerHTML = '<div class="auth-error">' + escapeHtml(e.message) + '</div>';
  }
}

async function runReport(fileId, fileName) {
  openResultModal('Summary Report \u2014 ' + fileName);
  try {
    const d = await api('/analysis/generate_report/' + fileId);
    let text = '';
    if (typeof d === 'string') text = d;
    else if (d.text) text = d.text;
    else if (d.candidates) { try { text = d.candidates[0].content.parts.map(p => p.text).join('\\n'); } catch(e){ text = JSON.stringify(d, null, 2); } }
    else if (d.choices) { try { text = d.choices[0].message.content; } catch(e){ text = JSON.stringify(d, null, 2); } }
    else if (d.content) { text = typeof d.content === 'string' ? d.content : JSON.stringify(d.content, null, 2); }
    else text = JSON.stringify(d, null, 2);
    document.getElementById('resultBody').innerHTML = '<div class="report-text">' + escapeHtml(text) + '</div>';
  } catch (e) {
    document.getElementById('resultBody').innerHTML = '<div class="auth-error">' + escapeHtml(e.message) + '</div>';
  }
}

/* ---------------- helpers ---------------- */
function closeModal(id) { document.getElementById(id).classList.remove('active'); }
function fmt(v) { return (v === null || v === undefined) ? '\u2014' : v; }
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

document.querySelectorAll('.modal-overlay').forEach(m => {
  m.addEventListener('click', e => { if (e.target === m) m.classList.remove('active'); });
});

/* ---------------- INIT ---------------- */
(async function init() {
  if (state.token) {
    try { await bootApp(); }
    catch (e) { logout(); }
  }
})();
</script>
</body>
</html>
"""

@router.get("/portal", response_class=HTMLResponse)
def get_portal():
    return HTMLResponse(content=PORTAL_HTML)
