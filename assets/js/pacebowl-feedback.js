/**
 * PaceBowl — Sitewide Bug Report & User Feedback Widget
 * Sends reports directly to https://hub.252698.xyz/api/public/feedback (D1 + DingTalk)
 */
(function () {
  'use strict';
  if (typeof document === 'undefined') return;

  function init() {
    if (document.getElementById('pb-feedback-root')) return;
    const wrap = document.createElement('div');
    wrap.id = 'pb-feedback-root';
    wrap.innerHTML = `
      <style>
        #pb-feedback-btn{position:fixed;bottom:16px;right:16px;z-index:999;display:inline-flex;align-items:center;gap:6px;padding:9px 14px;border-radius:999px;background:#1B4332;color:#fff;font:600 12px/1 system-ui,sans-serif;border:1px solid #2D6A4F;box-shadow:0 6px 20px rgba(0,0,0,.18);cursor:pointer}
        #pb-feedback-btn:hover{background:#143326}
        #pb-fb-overlay{position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.48);display:none;align-items:center;justify-content:center;padding:16px}
        #pb-fb-overlay.open{display:flex}
        #pb-fb-card{width:100%;max-width:420px;background:#fff;border-radius:16px;padding:20px;box-shadow:0 20px 50px rgba(0,0,0,.25);font-family:system-ui,sans-serif;color:#1c1917}
        #pb-fb-card label{display:block;font-size:12px;font-weight:600;margin:10px 0 4px;color:#44403c}
        #pb-fb-card select,#pb-fb-card textarea,#pb-fb-card input{width:100%;box-sizing:border-box;border:1px solid #d6d3d1;border-radius:10px;padding:8px 10px;font-size:13px;font-family:inherit}
        #pb-fb-msg-box{margin-top:8px;padding:8px 10px;border-radius:8px;font-size:12px;display:none}
        @media print{#pb-feedback-root{display:none!important}}
      </style>
      <button id="pb-feedback-btn" type="button" aria-label="Report a bug or suggest a pet calculator">💬 Feedback / Bug</button>
      <div id="pb-fb-overlay" role="dialog" aria-modal="true" aria-label="Send Feedback">
        <div id="pb-fb-card">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <strong style="font-size:15px;">Report a Bug or Suggest a Tool</strong>
            <button id="pb-fb-close" type="button" style="background:none;border:none;font-size:18px;cursor:pointer;color:#78716c;">✕</button>
          </div>
          <p style="font-size:12px;color:#57534e;margin:4px 0 8px;">Spot a formula question, PDF issue, or want a new pet diet calculator?</p>
          <form id="pb-fb-form">
            <input type="text" name="website" style="display:none" tabindex="-1" autocomplete="off">
            <label for="pb-fb-cat">Topic</label>
            <select id="pb-fb-cat" name="category">
              <option value="bug_math">Formula / Portion Math Question</option>
              <option value="bug_pdf">PDF Chart Download Issue</option>
              <option value="feature">Request New Pet Calculator</option>
              <option value="general">General Feedback</option>
            </select>
            <label for="pb-fb-text">Details *</label>
            <textarea id="pb-fb-text" name="message" rows="3" required minlength="3" maxlength="2000" placeholder="Tell us your pet's weight/diet or what we can improve..."></textarea>
            <label for="pb-fb-email">Email (optional)</label>
            <input id="pb-fb-email" name="email" type="email" placeholder="you@example.com">
            <div id="pb-fb-msg-box"></div>
            <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:14px;">
              <button id="pb-fb-cancel" type="button" style="padding:8px 14px;border-radius:10px;border:1px solid #d6d3d1;background:#fff;font-size:12px;font-weight:600;cursor:pointer;">Cancel</button>
              <button id="pb-fb-submit" type="submit" style="padding:8px 16px;border-radius:10px;border:none;background:#1B4332;color:#fff;font-size:12px;font-weight:700;cursor:pointer;">Send</button>
            </div>
          </form>
        </div>
      </div>
    `;
    document.body.appendChild(wrap);

    const overlay = document.getElementById('pb-fb-overlay');
    const form = document.getElementById('pb-fb-form');
    const msgBox = document.getElementById('pb-fb-msg-box');
    const submitBtn = document.getElementById('pb-fb-submit');

    const close = () => overlay.classList.remove('open');
    document.getElementById('pb-feedback-btn').addEventListener('click', () => {
      msgBox.style.display = 'none';
      overlay.classList.add('open');
    });
    document.getElementById('pb-fb-close').addEventListener('click', close);
    document.getElementById('pb-fb-cancel').addEventListener('click', close);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(form);
      const payload = {
        site: 'pacebowl',
        category: String(fd.get('category') || 'general'),
        message: String(fd.get('message') || '').trim(),
        email: String(fd.get('email') || '').trim(),
        website: String(fd.get('website') || '').trim(),
        page_url: window.location.href,
        viewport: window.innerWidth + 'x' + window.innerHeight,
      };
      if (payload.message.length < 3) return;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';
      try {
        const res = await fetch('https://hub.252698.xyz/api/public/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (res.ok && data.success) {
          msgBox.style.display = 'block';
          msgBox.style.background = '#ecfdf5';
          msgBox.style.color = '#065f46';
          msgBox.textContent = 'Thank you! Sent directly to the PaceBowl team.';
          form.reset();
          setTimeout(close, 1600);
        } else {
          throw new Error(data.error || 'Send failed');
        }
      } catch (err) {
        msgBox.style.display = 'block';
        msgBox.style.background = '#fef2f2';
        msgBox.style.color = '#991b1b';
        msgBox.textContent = err.message || 'Could not send right now.';
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send';
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
