/**
 * CareerVerse AI - Main Client Engine
 * Handles Theme Toggling, Code Execution, Speech Recognition, AI Evaluation & Live Resume Preview
 */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initMobileNav();
    initAptitudeTimer();
    initResumeLivePreview();
    initCodeWorkbench();
    initInterviewSpeech();
});

/* ==============================================================================
   1. THEME SWITCHER (Dark & Light Mode)
   ============================================================================== */
function initTheme() {
    const savedTheme = localStorage.getItem('careerverse_theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', nextTheme);
            localStorage.setItem('careerverse_theme', nextTheme);
            updateThemeIcon(nextTheme);
        });
    });
}

function updateThemeIcon(theme) {
    const icons = document.querySelectorAll('.theme-toggle-icon');
    icons.forEach(icon => {
        if (theme === 'dark') {
            icon.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
        } else {
            icon.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
        }
    });
}

/* ==============================================================================
   2. MOBILE NAVIGATION DRAWER
   ============================================================================== */
function initMobileNav() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !menuBtn.contains(e.target) && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
            }
        });
    }
}

/* ==============================================================================
   3. TIMED APTITUDE QUIZ COUNTDOWN TIMER
   ============================================================================== */
function initAptitudeTimer() {
    const timerElem = document.getElementById('quiz-countdown');
    const quizForm = document.getElementById('quiz-form');
    if (!timerElem || !quizForm) return;

    let timeRemaining = parseInt(timerElem.getAttribute('data-seconds') || '600', 10);

    const interval = setInterval(() => {
        timeRemaining--;
        const mins = Math.floor(timeRemaining / 60);
        const secs = timeRemaining % 60;
        timerElem.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

        if (timeRemaining <= 60) {
            timerElem.style.color = '#ef4444';
            timerElem.style.animation = 'pulse 1s infinite';
        }

        if (timeRemaining <= 0) {
            clearInterval(interval);
            alert("⏰ Time is up! Submitting your test automatically...");
            quizForm.submit();
        }
    }, 1000);
}

/* ==============================================================================
   4. RESUME LIVE PREVIEW & TEMPLATE ENGINE
   ============================================================================== */
function initResumeLivePreview() {
    const inputs = document.querySelectorAll('.resume-live-input');
    if (!inputs.length) return;

    function updatePreview() {
        inputs.forEach(input => {
            const field = input.getAttribute('data-preview');
            const target = document.getElementById(`preview-${field}`);
            if (target) {
                target.textContent = input.value || target.getAttribute('data-placeholder') || '';
            }
        });
    }

    inputs.forEach(input => {
        input.addEventListener('input', updatePreview);
    });

    // Template switcher
    const templateRadios = document.querySelectorAll('input[name="template"]');
    const previewSheet = document.getElementById('resume-preview-sheet');
    templateRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (previewSheet) {
                previewSheet.className = `resume-preview-sheet template-${radio.value}`;
            }
        });
    });
}

/* ==============================================================================
   5. CODING WORKBENCH & TEST RUNNER
   ============================================================================== */
function initCodeWorkbench() {
    const runBtn = document.getElementById('run-code-btn');
    const codeArea = document.getElementById('code-editor');
    const outputConsole = document.getElementById('console-output');
    if (!runBtn || !codeArea || !outputConsole) return;

    runBtn.addEventListener('click', async () => {
        const code = codeArea.value;
        const problemId = runBtn.getAttribute('data-problem-id');
        
        runBtn.disabled = true;
        runBtn.innerHTML = `<span>Running...</span>`;
        outputConsole.innerHTML = `<span style="color:#94a3b8;">🚀 Executing code in Python sandbox...</span>`;

        try {
            const res = await fetch('/coding/run/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ code: code, problem_id: problemId })
            });

            const data = await res.json();
            runBtn.disabled = false;
            runBtn.innerHTML = `<span>▶ Run Code</span>`;

            if (data.error) {
                outputConsole.innerHTML = `<span style="color:#ef4444; font-weight:bold;">❌ Error / Traceback:</span>\n${data.error}`;
                return;
            }

            let resultHtml = `<div style="margin-bottom:10px;">`;
            if (data.total_tests > 0) {
                if (data.passed_count === data.total_tests) {
                    resultHtml += `<span class="badge badge-success" style="font-size:0.9rem;">✅ ALL ${data.total_tests}/${data.total_tests} TESTS PASSED!</span>`;
                } else {
                    resultHtml += `<span class="badge badge-warning" style="font-size:0.9rem;">⚠️ Passed ${data.passed_count}/${data.total_tests} Tests</span>`;
                }
            } else {
                resultHtml += `<span class="badge badge-success">✅ Executed Successfully</span>`;
            }
            resultHtml += ` <span style="color:#94a3b8; font-size:0.8rem; margin-left:10px;">Runtime: ${data.execution_time}s</span></div>`;

            if (data.output) {
                resultHtml += `<div style="margin-top:8px;"><strong>Standard Output:</strong>\n${escapeHtml(data.output)}</div>`;
            }

            if (data.test_results && data.test_results.length > 0) {
                resultHtml += `<div style="margin-top:12px;"><strong>Test Cases Breakdown:</strong>\n`;
                data.test_results.forEach(tr => {
                    const statusColor = tr.passed ? '#10b981' : '#ef4444';
                    const icon = tr.passed ? '✓' : '✗';
                    resultHtml += `<div style="color:${statusColor}; margin:4px 0;">[${icon}] Case ${tr.index}: Input(${tr.input}) => Expected (${tr.expected})</div>`;
                });
                resultHtml += `</div>`;
            }

            outputConsole.innerHTML = resultHtml;
        } catch (err) {
            runBtn.disabled = false;
            runBtn.innerHTML = `<span>▶ Run Code</span>`;
            outputConsole.innerHTML = `<span style="color:#ef4444;">Network error running code. Please retry.</span>`;
        }
    });
}

/* ==============================================================================
   6. AI INTERVIEW VOICE RECOGNITION & ANSWER EVALUATION
   ============================================================================== */
function initInterviewSpeech() {
    // Voice speech-to-text
    const micBtns = document.querySelectorAll('.speech-mic-btn');
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        micBtns.forEach(btn => {
            const targetId = btn.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            if (!targetInput) return;

            const recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            let isRecording = false;

            btn.addEventListener('click', () => {
                if (!isRecording) {
                    recognition.start();
                    isRecording = true;
                    btn.classList.add('btn-danger');
                    btn.innerHTML = `<span>🔴 Listening... (Click to stop)</span>`;
                } else {
                    recognition.stop();
                    isRecording = false;
                    btn.classList.remove('btn-danger');
                    btn.innerHTML = `<span>🎙️ Speak Answer</span>`;
                }
            });

            recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    transcript += event.results[i][0].transcript;
                }
                targetInput.value = transcript;
            };

            recognition.onerror = () => {
                isRecording = false;
                btn.classList.remove('btn-danger');
                btn.innerHTML = `<span>🎙️ Speak Answer</span>`;
            };
        });
    }

    // AI Evaluation AJAX
    const evaluateBtns = document.querySelectorAll('.ai-eval-btn');
    evaluateBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const question = btn.getAttribute('data-question');
            const targetInputId = btn.getAttribute('data-input-id');
            const outputId = btn.getAttribute('data-output-id');
            const role = btn.getAttribute('data-role') || 'Software Engineer';
            
            const inputElem = document.getElementById(targetInputId);
            const outputElem = document.getElementById(outputId);
            if (!inputElem || !outputElem) return;

            const answer = inputElem.value.trim();
            if (!answer) {
                alert("Please enter or dictate your answer first!");
                return;
            }

            btn.disabled = true;
            btn.innerHTML = `<span>Analyzing...</span>`;
            outputElem.style.display = 'block';
            outputElem.innerHTML = `<p style="color:#64748b;">🤖 CareerVerse AI is evaluating your response against industry benchmarks...</p>`;

            try {
                const res = await fetch('/interview/evaluate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify({
                        role: role,
                        question: question,
                        answer: answer,
                        interview_type: 'Technical'
                    })
                });

                const evalData = await res.json();
                btn.disabled = false;
                btn.innerHTML = `<span>⚡ Re-Evaluate Answer</span>`;

                const scoreColor = evalData.score >= 8 ? '#10b981' : (evalData.score >= 5 ? '#f59e0b' : '#ef4444');

                outputElem.innerHTML = `
                    <div style="background:var(--bg-subtle); border:1px solid var(--border-color); border-radius:12px; padding:18px; margin-top:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <h4 style="margin:0;">🎯 AI Assessment Score:</h4>
                            <span style="font-size:1.3rem; font-weight:800; color:${scoreColor};">${evalData.score} / 10</span>
                        </div>
                        <p style="margin:6px 0;"><strong>💪 Strengths:</strong> ${escapeHtml(evalData.strengths)}</p>
                        <p style="margin:6px 0;"><strong>🔍 Areas to Improve:</strong> ${escapeHtml(evalData.weaknesses)}</p>
                        <div style="margin-top:10px; padding:10px; background:var(--bg-surface); border-radius:8px; border-left:4px solid var(--primary);">
                            <strong>🌟 High-Scoring Model Answer:</strong>
                            <p style="margin-top:4px; font-size:0.9rem;">${escapeHtml(evalData.model_answer)}</p>
                        </div>
                        <p style="margin-top:8px; font-size:0.85rem; color:var(--text-muted);"><strong>💡 Pro-Tip:</strong> ${escapeHtml(evalData.actionable_tips)}</p>
                    </div>
                `;
            } catch (err) {
                btn.disabled = false;
                btn.innerHTML = `<span>⚡ AI Evaluate Answer</span>`;
                outputElem.innerHTML = `<p style="color:#ef4444;">Evaluation failed. Please try again.</p>`;
            }
        });
    });
}

/* ==============================================================================
   UTILITIES
   ============================================================================== */
function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === ('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

function escapeHtml(string) {
    if (!string) return '';
    return String(string)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

