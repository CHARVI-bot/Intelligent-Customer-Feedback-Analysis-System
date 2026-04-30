const API_BASE = '/api';

// Show notification
function showNotification(message, isError = false) {
    const notif = document.getElementById('notification');
    if(!notif) return;
    
    notif.textContent = message;
    if (isError) {
        notif.classList.add('error');
    } else {
        notif.classList.remove('error');
    }
    
    notif.classList.add('show');
    setTimeout(() => {
        notif.classList.remove('show');
    }, 3000);
}

// Handle Form Submission
const feedbackForm = document.getElementById('feedbackForm');
if (feedbackForm) {
    feedbackForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = document.getElementById('submitBtn');
        const originalText = btn.textContent;
        btn.innerHTML = '<div class="loader"></div>';
        btn.disabled = true;

        const customer_name = document.getElementById('customer_name').value;
        const feedback_text = document.getElementById('feedback_text').value;
        const ratingEle = document.querySelector('input[name="rating"]:checked');
        const rating = ratingEle ? parseInt(ratingEle.value) : 0;

        try {
            const response = await fetch(`${API_BASE}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    customer_name,
                    feedback_text,
                    rating
                })
            });

            if (response.ok) {
                showNotification('Feedback submitted successfully!');
                feedbackForm.reset();
            } else {
                showNotification('Failed to submit feedback.', true);
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred.', true);
        } finally {
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });
}

// Load Dashboard Data
async function loadDashboardData() {
    try {
        // Load stats
        const statsRes = await fetch(`${API_BASE}/stats`);
        const stats = await statsRes.json();
        
        document.getElementById('stat-total').textContent = stats.total;
        document.getElementById('stat-rating').textContent = stats.average_rating + ' / 5';
        document.getElementById('stat-positive').textContent = stats.positive;
        document.getElementById('stat-negative').textContent = stats.negative;

        // Load feedbacks
        const fbRes = await fetch(`${API_BASE}/feedbacks?limit=10`);
        const feedbacks = await fbRes.json();
        
        const listContainer = document.getElementById('feedbackList');
        const loader = document.getElementById('loader');
        
        if (loader) loader.style.display = 'none';
        listContainer.innerHTML = '';

        if (feedbacks.length === 0) {
            listContainer.innerHTML = '<p style="text-align:center; color: var(--text-secondary);">No feedback received yet.</p>';
            return;
        }

        feedbacks.forEach(fb => {
            const date = new Date(fb.created_at).toLocaleDateString();
            const themesHtml = fb.themes.split(',').map(t => `<span class="theme-tag">${t.trim()}</span>`).join('');
            
            const item = document.createElement('div');
            item.className = 'feedback-item fade-in';
            item.innerHTML = `
                <div class="feedback-header">
                    <div class="name">${fb.customer_name} <span style="color:#fbbf24; margin-left:10px;">${'★'.repeat(fb.rating)}${'☆'.repeat(5-fb.rating)}</span></div>
                    <div class="date">${date}</div>
                </div>
                <div class="feedback-text">
                    "${fb.feedback_text}"
                </div>
                <div class="feedback-meta">
                    <span class="badge sentiment-${fb.sentiment.toLowerCase()}">AI Sentiment: ${fb.sentiment} (${fb.sentiment_score})</span>
                    <span class="badge urgency-${fb.urgency.toLowerCase()}">Urgency: ${fb.urgency}</span>
                    ${themesHtml}
                </div>
            `;
            listContainer.appendChild(item);
        });

    } catch (error) {
        console.error('Error loading dashboard data:', error);
        if (document.getElementById('loader')) document.getElementById('loader').style.display = 'none';
        const listContainer = document.getElementById('feedbackList');
        if (listContainer) listContainer.innerHTML = '<p style="color:var(--danger); text-align:center;">Error loading data.</p>';
    }
}
