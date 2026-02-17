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

    // Service selection listeners
    initServiceSelectors();
}

// Initialize service selector listeners
function initServiceSelectors() {
    // Video service selector
    const videoService = document.getElementById('video-service');
    if (videoService) {
        videoService.addEventListener('change', updateVideoServiceHints);
        updateVideoServiceHints(); // Initial update
    }

    // Content AI service selector
    const contentAI = document.getElementById('content-ai-service');
    if (contentAI) {
        contentAI.addEventListener('change', () => {
            // Could update hints/labels here
        });
    }

    // TTS service selector
    const ttsService = document.getElementById('tts-service');
    if (ttsService) {
        ttsService.addEventListener('change', () => {
            // Could update hints/labels here
        });
    }
}

// Update video service hints
function updateVideoServiceHints() {
    const service = document.getElementById('video-service').value;
    const link = document.getElementById('video-service-link');

    const services = {
        'luma': '<a href="https://piapi.ai/" target="_blank">piapi.ai</a>',
        'runway': '<a href="https://runwayml.com/" target="_blank">runwayml.com</a>',
        'skyreels': '<a href="https://piapi.ai/" target="_blank">piapi.ai</a>',
        'pika': '<a href="https://pika.art/" target="_blank">pika.art</a>'
    };

    if (link) {
        link.innerHTML = services[service] || '';
    }
}

// Quality preset selection
window.selectQualityPreset = function (preset) {
    const presets = {
        budget: {
            'content-ai-service': 'gemini',
            'tts-service': 'openai',
            'video-service': 'luma'
        },
        premium: {
            'content-ai-service': 'gpt4',
            'tts-service': 'elevenlabs',
            'video-service': 'runway'
        }
    };

    const config = presets[preset];
    if (config) {
        Object.keys(config).forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = config[id];
        });

        // Update hints
        updateVideoServiceHints();

        // Visual feedback
        document.querySelectorAll('.quality-preset').forEach(p => {
            p.style.border = '1px solid var(--glass-border)';
        });
        const selected = document.querySelector(`[data-preset="${preset}"]`);
        if (selected) {
            selected.style.border = '2px solid var(--primary)';
        }

        showToast(`${preset === 'budget' ? '💰 Budget' : '⭐ Premium'} preset selected!`);
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
                        <a href="/api/videos/${video.id}/download" class="btn btn-primary btn-sm" download>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="7 10 12 15 17 10"></polyline>
                                <line x1="12" y1="15" x2="12" y2="3"></line>
                            </svg>
                            Download
                        </a>
                        <button class="btn btn-secondary btn-sm" onclick="openEditor(${video.id})">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                            </svg>
                            Edit
                        </button>
                        ${!video.youtube_url ? `
                            <button class="btn btn-success btn-sm" onclick="handleUploadVideo(${video.id})">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                    <polyline points="17 8 12 3 7 8"></polyline>
                                    <line x1="12" y1="3" x2="12" y2="15"></line>
                                </svg>
                                Upload to YouTube
                            </button>
                        ` : `
                            <a href="${video.youtube_url}" class="btn btn-success btn-sm" target="_blank">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path>
                                    <polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon>
                                </svg>
                                View on YouTube
                            </a>
                        `}
                    ` : ''}
                    <button class="btn btn-danger btn-sm" onclick="handleDeleteVideo(${video.id})">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                        Delete
                    </button>
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

    // Gather all configuration data
    const config = {
        // Service selections
        content_ai_service: document.getElementById('content-ai-service')?.value,
        tts_service: document.getElementById('tts-service')?.value,
        video_service: document.getElementById('video-service')?.value,

        // API Keys
        gemini: document.getElementById('api-gemini')?.value.trim(),
        openai: document.getElementById('api-openai')?.value.trim(),
        video_api: document.getElementById('api-video')?.value.trim(),
        video_endpoint: document.getElementById('video-endpoint')?.value.trim(),
        whisper: document.getElementById('api-whisper')?.value.trim(),
        elevenlabs: document.getElementById('api-elevenlabs')?.value.trim(),
        youtube_client_id: document.getElementById('api-youtube-client-id')?.value.trim(),
        youtube_client_secret: document.getElementById('api-youtube-client-secret')?.value.trim(),
    };

    // Remove empty values
    Object.keys(config).forEach(key => {
        if (!config[key]) delete config[key];
    });

    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="loading"></div> Saving...';
    btn.disabled = true;

    try {
        await api.saveConfig(config);
        showToast('✅ Configuration saved successfully!');

        // Clear password fields for security (not service selections)
        const passwordFields = ['api-gemini', 'api-openai', 'api-video', 'api-whisper',
            'api-elevenlabs', 'api-youtube-client-id', 'api-youtube-client-secret'];
        passwordFields.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = '';
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

// Video Actions
window.handleUploadVideo = async function (videoId) {
    if (!confirm('Upload this video to YouTube? Make sure you have configured YouTube API credentials in Settings.')) {
        return;
    }

    try {
        showToast('Uploading to YouTube...');
        const result = await api.uploadVideo(videoId);
        showToast(`✅ Successfully uploaded to YouTube!`);

        // Reload videos to update UI
        if (currentPage === 'library') {
            loadLibrary();
        } else {
            loadVideos();
        }
    } catch (error) {
        showToast(`Failed to upload: ${error.message}`, 'error');
    }
}

window.handleDeleteVideo = async function (videoId) {
    if (!confirm('Are you sure you want to delete this video? This action cannot be undone.')) {
        return;
    }

    try {
        await api.deleteVideo(videoId);
        showToast('✅ Video deleted successfully');

        // Reload videos
        if (currentPage === 'library') {
            loadLibrary();
        } else {
            loadVideos();
        }

        // Refresh stats
        const stats = await api.getStats();
        updateStats(stats);
    } catch (error) {
        showToast(`Failed to delete video: ${error.message}`, 'error');
    }
}

window.openEditor = function (videoId) {
    // For now, show a message that editor is coming
    // Will be fully implemented next
    showToast('Video editor coming soon! Edit features in development.', 'info');
    // TODO: switchPage('editor'); editor.loadVideo(videoId);
}
