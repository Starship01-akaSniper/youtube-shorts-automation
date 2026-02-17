/**
 * API Client for YouTube Shorts Automation
 */

const API_BASE = window.location.origin;

class APIClient {
    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Configuration
    async getConfigStatus() {
        return this.request('/api/config/status');
    }

    async saveConfig(config) {
        return this.request('/api/config/save', {
            method: 'POST',
            body: JSON.stringify(config),
        });
    }

    // Videos
    async getVideos(status = null, limit = 50) {
        const params = new URLSearchParams();
        if (status) params.append('status', status);
        params.append('limit', limit);
        return this.request(`/api/videos?${params}`);
    }

    async getVideo(videoId) {
        return this.request(`/api/videos/${videoId}`);
    }

    async createVideo(data) {
        return this.request('/api/videos/create', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    // Jobs
    async getJobs(status = null, limit = 50) {
        const params = new URLSearchParams();
        if (status) params.append('status', status);
        params.append('limit', limit);
        return this.request(`/api/jobs?${params}`);
    }

    async getJob(jobId) {
        return this.request(`/api/jobs/${jobId}`);
    }

    async getQueueStatus() {
        return this.request('/api/jobs/queue/status');
    }

    // Statistics
    async getStats() {
        return this.request('/api/stats');
    }

    // Health
    async healthCheck() {
        return this.request('/api/health');
    }
}

// Export global instance
window.api = new APIClient();
