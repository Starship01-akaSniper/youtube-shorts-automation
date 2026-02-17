/**
 * Main Application Logic
 */

// State
let currentPage = 'dashboard';
let statsInterval = null;
let jobsInterval = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initForms();
    checkConfiguration();
    loadDashboard();

    // Start auto-refresh
    startAutoRefresh();
});

// Navigation
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            switchPage(page);
        });
    });

    // Filter buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const status = btn.dataset.status;
            loadLibrary(status === 'all' ? null : status);
        });
    });
}

function switchPage(pageName) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.page === pageName);
    });

    // Update pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(`${pageName}-page`).classList.add('active');

    currentPage = pageName;

    // Load page data
    switch (pageName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'library':
            loadLibrary();
            break;
        case 'settings':
            loadSettings();
            break;
    }
}

// Forms
function initForms() {
    // Script word count
    const scriptTextarea = document.getElementById('video-script');
    if (scriptTextarea) {
        scriptTextarea.addEventListener('input', (e) => {
            const words = e.target.value.trim().split(/\s+/).filter(w => w.length > 0).length;
            document.getElementById('script-word-count').textContent = `${words} words`;
        });
    }

    // Create video form
    const createForm = document.getElementById('create-video-form');
    if (createForm) {
        createForm.addEventListener('submit', handleCreateVideo);
    }

    // API config form
    const configForm = document.getElementById('api-config-form');
    if (configForm) {
        configForm.addEventListener('submit', handleSaveConfig);
    }
}

// Check configuration status
async function checkConfiguration() {
    try {
        const status = await api.getConfigStatus();

        if (!status.required_configured) {
            showToast('⚠️ Please configure your API keys in Settings', 'warning');
        }
    } catch (error) {
        console.error('Failed to check configuration:', error);
    }
}

// Dashboard
async function loadDashboard() {
    try {
        // Load stats
        const stats = await api.getStats();
        updateStats(stats);

        // Load recent videos
        await loadVideos();

        // Load active jobs
        await loadJobs();
    } catch (error) {
        console.error('Failed to load dashboard:', error);
        showToast('Failed to load dashboard data', 'error');
    }
}

function updateStats(stats) {
    document.getElementById('stat-total-videos').textContent = stats.total_videos;
    document.getElementById('stat-completed-videos').textContent = stats.completed_videos;
    document.getElementById('stat-processing-jobs').textContent = stats.processing_jobs;
    document.getElementById('stat-pending-jobs').textContent = stats.pending_jobs;
}

// Videos
async function loadVideos() {
    try {
        const videos = await api.getVideos(null, 6);
        renderVideos(videos, 'recent-videos-list');
    } catch (error) {
        console.error('Failed to load videos:', error);
    }
}

async function loadLibrary(status = null) {
    try {
        const videos = await api.getVideos(status, 50);
        renderVideos(videos, 'library-videos-grid');
    } catch (error) {
        console.error('Failed to load library:', error);
        showToast('Failed to load videos', 'error');
    }
}

function renderVideos(videos, containerId) {
    const container = document.getElementById(containerId);

    if (videos.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                </svg>
                <p>No videos yet. Create your first one!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = videos.map(video => `
        <div class="video-card">
            <div class="video-thumbnail">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 48px; height: 48px;">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
            </div>
            <div class="video-info">
                <h3 class="video-title">${escapeHtml(video.title || 'Untitled Video')}</h3>
                <div class="video-meta">
                    <span class="video-status ${video.status}">${video.status}</span>
                    <span>${formatDate(video.created_at)}</span>
                </div>
                <div class="video-actions">
                    ${video.status === 'completed' ? `
                        <a href="/api/videos/${video.id}/download" class="btn btn-primary" download>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="7 10 12 15 17 10"></polyline>
                                <line x1="12" y1="15" x2="12" y2="3"></line>
                            </svg>
                            Download
                        </a>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// Jobs
async function loadJobs() {
    try {
        const jobs = await api.getJobs('processing', 10);
        renderJobs(jobs);
    } catch (error) {
        console.error('Failed to load jobs:', error);
    }
}

function renderJobs(jobs) {
    const container = document.getElementById('active-jobs-list');

    if (jobs.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No active jobs</p>
            </div>
        `;
        return;
    }

    container.innerHTML = jobs.map(job => `
        <div class="job-card">
            <div class="job-header">
                <div>
                    <h4>${escapeHtml(job.title || 'Processing...')}</h4>
                    <small>${job.current_step}</small>
                </div>
                <span class="video-status ${job.status}">${job.status}</span>
            </div>
            <div class="job-progress">
                <div class="job-progress-bar" style="width: ${job.progress}%"></div>
            </div>
        </div>
    `).join('');
}

// Create Video
async function handleCreateVideo(e) {
    e.preventDefault();

    const script = document.getElementById('video-script').value;
    const title = document.getElementById('video-title').value;
    const description = document.getElementById('video-description').value;

    if (!script.trim()) {
        showToast('Please enter a video script', 'error');
        return;
    }

    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="loading"></div> Creating...';
    btn.disabled = true;

    try {
        const result = await api.createVideo({
            script: script.trim(),
            title: title || null,
            description: description || null
        });

        showToast('✅ Video creation started! Check dashboard for progress.');

        // Clear form
        document.getElementById('create-video-form').reset();
        document.getElementById('script-word-count').textContent = '0 words';

        // Switch to dashboard
        switchPage('dashboard');

    } catch (error) {
        showToast(`Failed to create video: ${error.message}`, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Settings
async function loadSettings() {
    try {
        const status = await api.getConfigStatus();
        // Could populate form with status indicators here
    } catch (error) {
        console.error('Failed to load settings:', error);
    }
}

async function handleSaveConfig(e) {
    e.preventDefault();

    const config = {
        gemini: document.getElementById('api-gemini').value.trim(),
        openai: document.getElementById('api-openai').value.trim(),
        luma: document.getElementById('api-luma').value.trim(),
        youtube_client_id: document.getElementById('api-youtube-client-id').value.trim(),
        youtube_client_secret: document.getElementById('api-youtube-client-secret').value.trim(),
    };

    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="loading"></div> Saving...';
    btn.disabled = true;

    try {
        await api.saveConfig(config);
        showToast('✅ Configuration saved successfully!');

        // Clear password fields for security
        Object.keys(config).forEach(key => {
            document.getElementById(`api-${key.replace('_', '-')}`).value = '';
        });

    } catch (error) {
        showToast(`Failed to save configuration: ${error.message}`, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Auto-refresh
function startAutoRefresh() {
    // Refresh stats every 10 seconds
    statsInterval = setInterval(async () => {
        if (currentPage === 'dashboard') {
            try {
                const stats = await api.getStats();
                updateStats(stats);
            } catch (error) {
                console.error('Failed to refresh stats:', error);
            }
        }
    }, 10000);

    // Refresh jobs every 5 seconds
    jobsInterval = setInterval(async () => {
        if (currentPage === 'dashboard') {
            try {
                await loadJobs();
            } catch (error) {
                console.error('Failed to refresh jobs:', error);
            }
        }
    }, 5000);
}

// Utilities
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = toast.querySelector('.toast-icon');

    toastMessage.textContent = message;

    // Update icon based on type
    if (type === 'error') {
        toastIcon.innerHTML = '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>';
        toastIcon.style.color = 'var(--danger)';
    } else {
        toastIcon.innerHTML = '<polyline points="20 6 9 17 4 12"></polyline>';
        toastIcon.style.color = 'var(--success)';
    }

    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;

    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;

    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString();
}
