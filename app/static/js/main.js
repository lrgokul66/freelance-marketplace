/**
 * Freelance Marketplace — main.js
 * Theme toggle, toast notifications, chat polling, loading spinner,
 * confirm dialogs, file preview, and misc UI helpers.
 */

/* ── Theme Toggle ─────────────────────────────────────────── */
(function () {
    const THEME_KEY = 'fm_theme';
    const btn = document.getElementById('themeToggle');
    const root = document.documentElement;

    function applyTheme(theme) {
        root.setAttribute('data-theme', theme);
        if (btn) {
            btn.innerHTML = theme === 'dark'
                ? '<i class="bi bi-sun-fill"></i>'
                : '<i class="bi bi-moon-fill"></i>';
            btn.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
        }
    }

    // Load saved preference
    const saved = localStorage.getItem(THEME_KEY) ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(saved);

    if (btn) {
        btn.addEventListener('click', () => {
            const current = root.getAttribute('data-theme') || 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            localStorage.setItem(THEME_KEY, next);
            applyTheme(next);
        });
    }
})();

/* ── Toast Helper ─────────────────────────────────────────── */
function showToast(message, type = 'success', duration = 4000) {
    const container = document.getElementById('toastContainer') ||
        (() => {
            const c = document.createElement('div');
            c.id = 'toastContainer';
            c.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(c);
            return c;
        })();

    const icons = {
        success: 'check-circle-fill', danger: 'x-circle-fill',
        warning: 'exclamation-triangle-fill', info: 'info-circle-fill'
    };
    const colors = { success: '#10b981', danger: '#ef4444', warning: '#f59e0b', info: '#3b82f6' };

    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white border-0 show`;
    toastEl.style.background = colors[type] || colors.success;
    toastEl.style.borderRadius = '12px';
    toastEl.innerHTML = `
    <div class="d-flex">
      <div class="toast-body fw-semibold">
        <i class="bi bi-${icons[type] || icons.success} me-2"></i>${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto"
              onclick="this.closest('.toast').remove()"></button>
    </div>`;
    container.appendChild(toastEl);
    setTimeout(() => toastEl.remove(), duration);
}

/* ── Loading Spinner ──────────────────────────────────────── */
function showSpinner() {
    const el = document.getElementById('loadingOverlay');
    if (el) el.style.display = 'flex';
}
function hideSpinner() {
    const el = document.getElementById('loadingOverlay');
    if (el) el.style.display = 'none';
}

// Show spinner on form submit (all forms with data-loading)
document.addEventListener('submit', function (e) {
    const form = e.target;
    if (form.dataset.loading !== undefined) showSpinner();
});

/* ── Confirm Delete / Dangerous Actions ───────────────────── */
document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-confirm]');
    if (!btn) return;
    const msg = btn.dataset.confirm || 'Are you sure?';
    if (!confirm(msg)) e.preventDefault();
});

/* ── Delete Account — require "DELETE" typed ──────────────── */
const deleteAccountForm = document.getElementById('deleteAccountForm');
if (deleteAccountForm) {
    deleteAccountForm.addEventListener('submit', function (e) {
        const typed = document.getElementById('delete_confirm_input')?.value?.trim();
        const pwd = document.getElementById('delete_password_input')?.value?.trim();
        if (typed !== 'DELETE') {
            e.preventDefault();
            showToast('You must type DELETE exactly to confirm.', 'danger');
            return;
        }
        if (!pwd) {
            e.preventDefault();
            showToast('Please enter your current password.', 'danger');
        }
    });
}

/* ── Avatar Preview ───────────────────────────────────────── */
document.querySelectorAll('.avatar-file-input').forEach(function (input) {
    input.addEventListener('change', function () {
        const preview = document.getElementById(this.dataset.preview);
        if (!preview) return;
        const file = this.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = e => { preview.src = e.target.result; };
        reader.readAsDataURL(file);
    });
});

/* ── File input label update ──────────────────────────────── */
document.querySelectorAll('.custom-file-input-label').forEach(function (label) {
    const inputId = label.dataset.for;
    if (!inputId) return;
    const input = document.getElementById(inputId);
    if (!input) return;
    input.addEventListener('change', function () {
        const names = Array.from(this.files).map(f => f.name).join(', ');
        label.textContent = names || 'Choose file…';
    });
});

/* ── Chat Auto-scroll & AJAX Polling ─────────────────────── */
(function () {
    const chatMessages = document.getElementById('chatMessages');
    const pollUrl = document.getElementById('chatPollUrl')?.value;
    const sendForm = document.getElementById('chatSendForm');

    if (!chatMessages) return;

    // Auto-scroll to bottom on load
    function scrollBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    scrollBottom();

    if (!pollUrl) return;

    let lastId = parseInt(document.getElementById('chatLastId')?.value || '0', 10);
    const myId = parseInt(document.getElementById('chatMyId')?.value || '0', 10);

    function buildBubble(msg) {
        const isMine = msg.sender_id === myId;
        const cls = isMine ? 'sent' : 'received';
        let body = '';
        if (msg.content) body += `<div>${escapeHtml(msg.content)}</div>`;
        if (msg.file_path) {
            const ext = msg.file_path.split('.').pop().toLowerCase();
            const isImg = ['png', 'jpg', 'jpeg', 'gif', 'webp'].includes(ext);
            body += isImg
                ? `<img src="/static/uploads/chat_files/${escapeHtml(msg.file_path)}" class="img-fluid rounded mt-1" style="max-width:200px;">`
                : `<a href="/static/uploads/chat_files/${escapeHtml(msg.file_path)}" class="text-white d-block mt-1" target="_blank">
             <i class="bi bi-paperclip"></i> ${escapeHtml(msg.file_name || msg.file_path)}
           </a>`;
        }
        return `<div class="d-flex ${isMine ? 'justify-content-end' : ''} fade-in">
      <div class="chat-bubble ${cls}">
        ${body}
        <div class="chat-meta">${msg.first_name} • ${msg.created_at}</div>
      </div>
    </div>`;
    }

    function escapeHtml(s) {
        if (!s) return '';
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function poll() {
        fetch(`${pollUrl}?last_id=${lastId}`)
            .then(r => r.json())
            .then(data => {
                if (data.messages && data.messages.length) {
                    data.messages.forEach(m => {
                        chatMessages.insertAdjacentHTML('beforeend', buildBubble(m));
                        lastId = Math.max(lastId, m.id);
                    });
                    scrollBottom();
                    const lastIdInput = document.getElementById('chatLastId');
                    if (lastIdInput) lastIdInput.value = lastId;
                }
            })
            .catch(() => { }); // silent fail
    }

    // Poll every 3 seconds
    setInterval(poll, 3000);
})();

/* ── Notification Badge Polling ───────────────────────────── */
(function () {
    const notifBadge = document.getElementById('notifBadgeCount');
    const msgBadge = document.getElementById('msgBadgeCount');
    if (!notifBadge && !msgBadge) return;

    function updateBadges() {
        if (notifBadge) {
            fetch('/notifications/count')
                .then(r => r.json())
                .then(d => {
                    notifBadge.textContent = d.count || '';
                    notifBadge.style.display = d.count ? 'flex' : 'none';
                }).catch(() => { });
        }
        if (msgBadge) {
            fetch('/chat/unread-count')
                .then(r => r.json())
                .then(d => {
                    msgBadge.textContent = d.count || '';
                    msgBadge.style.display = d.count ? 'flex' : 'none';
                }).catch(() => { });
        }
    }
    updateBadges();
    setInterval(updateBadges, 30000);
})();

/* ── Skills Tag Input (comma-separated) ───────────────────── */
(function () {
    const newSkillInput = document.getElementById('newSkillInput');
    const skillsContainer = document.getElementById('skillTagsContainer');
    if (!newSkillInput || !skillsContainer) return;

    newSkillInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            const val = this.value.trim().replace(/,/g, '');
            if (!val) return;
            addSkillTag(val);
            this.value = '';
        }
    });

    function addSkillTag(name) {
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.innerHTML = `${name} <input type="hidden" name="new_skill" value="${name}">
      <span onclick="this.parentElement.remove()" style="cursor:pointer;margin-left:4px;">×</span>`;
        skillsContainer.appendChild(tag);
    }
})();

/* ── Animate cards on scroll ──────────────────────────────── */
(function () {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.classList.add('fade-in-up');
                observer.unobserve(e.target);
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.card, .stat-card').forEach(el => observer.observe(el));
})();

/* ── Star Rating Input ────────────────────────────────────── */
(function () {
    document.querySelectorAll('.star-rating-input').forEach(function (container) {
        const stars = container.querySelectorAll('input[type=radio]');
        const labels = container.querySelectorAll('label');
        labels.forEach((label, idx) => {
            label.addEventListener('mouseover', () => {
                labels.forEach((l, i) => {
                    l.style.color = i >= labels.length - 1 - idx ? '#f59e0b' : '#e2e8f0';
                });
            });
            label.addEventListener('mouseleave', () => {
                const checked = container.querySelector('input:checked');
                if (checked) {
                    const val = parseInt(checked.value);
                    labels.forEach((l, i) => {
                        l.style.color = i >= labels.length - val ? '#f59e0b' : '#e2e8f0';
                    });
                } else {
                    labels.forEach(l => l.style.color = '#e2e8f0');
                }
            });
        });
    });
})();

/* ── Initial Page Load Preloader ──────────────────────────── */
(function () {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        if (!sessionStorage.getItem('preloader_shown')) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    preloader.classList.add('fade-out');
                    sessionStorage.setItem('preloader_shown', 'true');
                }, 800);
            });
        } else {
            preloader.style.display = 'none';
        }
    }
})();

/* ── Chunked File Upload Helper ───────────────────────────── */
window.initChunkedUpload = function (fileInputId, progressContainerId, progressBarId, hiddenInputId, submitButtonId, removeButtonId) {
    const fileInput = document.getElementById(fileInputId);
    const progressContainer = document.getElementById(progressContainerId);
    const progressBar = document.getElementById(progressBarId);
    const hiddenInput = document.getElementById(hiddenInputId);
    const submitButton = submitButtonId ? document.getElementById(submitButtonId) : null;
    const removeButton = removeButtonId ? document.getElementById(removeButtonId) : null;

    if (!fileInput || !progressContainer || !progressBar || !hiddenInput) {
        console.warn('initChunkedUpload: Missing HTML elements', { fileInputId, progressContainerId, progressBarId, hiddenInputId });
        return;
    }

    const originalName = fileInput.getAttribute('name') || 'attachments_direct';
    const CHUNK_SIZE = 5 * 1024 * 1024; // 5 MB chunks

    fileInput.addEventListener('change', async function (e) {
        const file = e.target.files[0];
        if (!file) return;

        // Disable submit button during upload
        if (submitButton) {
            submitButton.disabled = true;
        }

        const fileIdentifier = 'upload_' + Math.random().toString(36).substring(2, 15) + '_' + Date.now();
        const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

        progressContainer.classList.remove('d-none');
        progressBar.style.width = '0%';
        progressBar.classList.remove('bg-success', 'bg-danger');
        progressBar.textContent = 'Preparing upload...';
        if (removeButton) removeButton.classList.add('d-none');

        for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
            const start = chunkIndex * CHUNK_SIZE;
            const end = Math.min(start + CHUNK_SIZE, file.size);
            const chunkBlob = file.slice(start, end);

            const formData = new FormData();
            formData.append('file', chunkBlob);
            formData.append('chunkIndex', chunkIndex);
            formData.append('totalChunks', totalChunks);
            formData.append('fileIdentifier', fileIdentifier);
            formData.append('filename', file.name);

            try {
                const response = await fetch('/upload/upload-chunk', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                const percentComplete = Math.round(((chunkIndex + 1) / totalChunks) * 100);
                progressBar.style.width = percentComplete + '%';
                progressBar.textContent = percentComplete + '%';

                if (data.status === 'completed') {
                    progressBar.classList.add('bg-success');
                    progressBar.textContent = 'Upload Complete!';

                    // Correctly append hidden input element within the container div
                    hiddenInput.innerHTML = `<input type="hidden" name="chunked_attachments" value="${data.filename}">`;

                    // Remove name attribute from fileInput to prevent uploading raw large file during form submit
                    fileInput.removeAttribute('name');

                    if (removeButton) removeButton.classList.remove('d-none');
                    if (submitButton) {
                        submitButton.disabled = false;
                    }
                    break;
                }
            } catch (error) {
                console.error('Error uploading chunk:', chunkIndex, error);
                progressBar.classList.add('bg-danger');
                progressBar.textContent = 'Upload Failed! Please try again.';
                fileInput.value = ''; // Clean up input
                fileInput.setAttribute('name', originalName);
                hiddenInput.innerHTML = '';
                if (removeButton) removeButton.classList.add('d-none');
                if (submitButton) {
                    submitButton.disabled = false;
                }
                break;
            }
        }
    });

    if (removeButton) {
        removeButton.addEventListener('click', function () {
            fileInput.value = '';
            fileInput.setAttribute('name', originalName);
            hiddenInput.innerHTML = '';
            progressContainer.classList.add('d-none');
            progressBar.style.width = '0%';
            progressBar.textContent = '0%';
            progressBar.classList.remove('bg-success', 'bg-danger');
            removeButton.classList.add('d-none');
            if (submitButton) {
                submitButton.disabled = false;
            }
        });
    }
};


