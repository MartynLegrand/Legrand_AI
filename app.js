// Legrand 3D AI Assistant - Main Application
class LegrandAI {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.avatar = null;
        this.isListening = false;
        this.apiKey = localStorage.getItem('openai_api_key') || '';
        this.conversationHistory = [];
        
        this.init();
        this.setupEventListeners();
        this.initAvatar();
    }

    init() {
        // Load saved API key
        const savedKey = localStorage.getItem('openai_api_key');
        if (savedKey) {
            document.getElementById('api-key').value = savedKey;
        }

        // Load settings
        const voiceEnabled = localStorage.getItem('voice_enabled') !== 'false';
        const animationsEnabled = localStorage.getItem('animations_enabled') !== 'false';
        
        document.getElementById('voice-enabled').checked = voiceEnabled;
        document.getElementById('avatar-animations').checked = animationsEnabled;
    }

    setupEventListeners() {
        // Chat input
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Voice button
        document.getElementById('voice-btn').addEventListener('click', () => {
            this.toggleVoiceInput();
        });

        // Clear chat
        document.getElementById('clear-btn').addEventListener('click', () => {
            this.clearChat();
        });

        // Settings toggle
        document.getElementById('settings-toggle').addEventListener('click', () => {
            const content = document.getElementById('settings-content');
            content.classList.toggle('hidden');
        });

        // API Key input
        // Note: Storing API key in localStorage is intentional for this client-side only MVP
        // Users are informed in the UI that keys are stored locally
        // For production apps, consider using a backend proxy to avoid exposing API keys
        document.getElementById('api-key').addEventListener('change', (e) => {
            this.apiKey = e.target.value;
            localStorage.setItem('openai_api_key', this.apiKey);
        });

        // Voice setting
        document.getElementById('voice-enabled').addEventListener('change', (e) => {
            localStorage.setItem('voice_enabled', e.target.checked);
        });

        // Animation setting
        document.getElementById('avatar-animations').addEventListener('change', (e) => {
            localStorage.setItem('animations_enabled', e.target.checked);
        });
    }

    initAvatar() {
        const container = document.getElementById('avatar-canvas');
        const width = container.clientWidth;
        const height = container.clientHeight;

        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xe0e7ff);

        // Camera
        this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        this.camera.position.z = 5;

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(width, height);
        container.appendChild(this.renderer.domElement);

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 5, 5);
        this.scene.add(directionalLight);

        // Create simple avatar (sphere with features)
        this.createAvatar();

        // Handle window resize
        window.addEventListener('resize', () => {
            const newWidth = container.clientWidth;
            const newHeight = container.clientHeight;
            
            this.camera.aspect = newWidth / newHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(newWidth, newHeight);
        });

        // Start animation loop
        this.animate();
    }

    createAvatar() {
        // Avatar group
        const avatarGroup = new THREE.Group();

        // Head (sphere)
        const headGeometry = new THREE.SphereGeometry(1, 32, 32);
        const headMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x7c3aed,
            shininess: 100
        });
        const head = new THREE.Mesh(headGeometry, headMaterial);
        avatarGroup.add(head);

        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.15, 16, 16);
        const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
        
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.3, 0.2, 0.8);
        avatarGroup.add(leftEye);

        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.3, 0.2, 0.8);
        avatarGroup.add(rightEye);

        // Pupils
        const pupilGeometry = new THREE.SphereGeometry(0.08, 16, 16);
        const pupilMaterial = new THREE.MeshBasicMaterial({ color: 0x1e293b });
        
        const leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
        leftPupil.position.set(-0.3, 0.2, 0.95);
        avatarGroup.add(leftPupil);

        const rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
        rightPupil.position.set(0.3, 0.2, 0.95);
        avatarGroup.add(rightPupil);

        // Mouth
        const mouthGeometry = new THREE.TorusGeometry(0.3, 0.05, 16, 100, Math.PI);
        const mouthMaterial = new THREE.MeshBasicMaterial({ color: 0x1e293b });
        const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
        mouth.position.set(0, -0.3, 0.8);
        mouth.rotation.x = Math.PI;
        avatarGroup.add(mouth);

        // Body (cone)
        const bodyGeometry = new THREE.ConeGeometry(0.8, 2, 32);
        const bodyMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x8b5cf6,
            shininess: 80
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.position.y = -2;
        avatarGroup.add(body);

        this.avatar = avatarGroup;
        this.avatar.userData = {
            leftEye: leftEye,
            rightEye: rightEye,
            leftPupil: leftPupil,
            rightPupil: rightPupil,
            mouth: mouth
        };
        
        this.scene.add(avatarGroup);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Idle animation - gentle floating
        if (this.avatar && localStorage.getItem('animations_enabled') !== 'false') {
            const time = Date.now() * 0.001;
            this.avatar.position.y = Math.sin(time) * 0.1;
            this.avatar.rotation.y = Math.sin(time * 0.5) * 0.1;
            
            // Blink animation
            if (Math.random() < 0.01) {
                this.blink();
            }
        }

        this.renderer.render(this.scene, this.camera);
    }

    blink() {
        if (!this.avatar || !this.avatar.userData) return;
        
        const { leftEye, rightEye } = this.avatar.userData;
        const originalScale = leftEye.scale.y;
        
        leftEye.scale.y = 0.1;
        rightEye.scale.y = 0.1;
        
        setTimeout(() => {
            leftEye.scale.y = originalScale;
            rightEye.scale.y = originalScale;
        }, 100);
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Get AI response
        try {
            const response = await this.getAIResponse(message);
            this.removeTypingIndicator();
            this.addMessage(response, 'assistant');
            
            // Speak response if voice is enabled
            if (document.getElementById('voice-enabled').checked) {
                this.speak(response);
            }
            
            // Animate avatar when speaking
            this.animateSpeaking();
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please make sure you have set your OpenAI API key in the settings.', 'assistant');
            console.error('Error:', error);
        }
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<p>${this.escapeHtml(text)}</p>`;
        
        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const indicator = document.createElement('div');
        indicator.className = 'message assistant-message';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    async getAIResponse(message) {
        if (!this.apiKey) {
            return "Please set your OpenAI API key in the settings to enable AI responses.";
        }

        // Add message to conversation history
        this.conversationHistory.push({
            role: 'user',
            content: message
        });

        // Keep only last 10 messages to manage context
        if (this.conversationHistory.length > 10) {
            this.conversationHistory = this.conversationHistory.slice(-10);
        }

        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify({
                    model: 'gpt-3.5-turbo',
                    messages: [
                        {
                            role: 'system',
                            content: 'You are Legrand, a helpful and friendly 3D AI assistant. Keep your responses concise and helpful.'
                        },
                        ...this.conversationHistory
                    ],
                    max_tokens: 150,
                    temperature: 0.7
                })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            const aiMessage = data.choices[0].message.content;
            
            // Add AI response to conversation history
            this.conversationHistory.push({
                role: 'assistant',
                content: aiMessage
            });

            return aiMessage;
        } catch (error) {
            console.error('Error calling OpenAI API:', error);
            throw error;
        }
    }

    toggleVoiceInput() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
            return;
        }

        const voiceBtn = document.getElementById('voice-btn');

        if (this.isListening) {
            this.stopListening();
            voiceBtn.classList.remove('active');
        } else {
            this.startListening();
            voiceBtn.classList.add('active');
        }
    }

    startListening() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('chat-input').value = transcript;
            this.sendMessage();
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            document.getElementById('voice-btn').classList.remove('active');
        };

        recognition.onend = () => {
            this.isListening = false;
            document.getElementById('voice-btn').classList.remove('active');
        };

        recognition.start();
        this.isListening = true;
        this.recognition = recognition;
        
        this.updateStatus('Listening...');
    }

    stopListening() {
        if (this.recognition) {
            this.recognition.stop();
            this.isListening = false;
        }
        this.updateStatus('Ready');
    }

    speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            window.speechSynthesis.speak(utterance);
        }
    }

    animateSpeaking() {
        if (!this.avatar || !this.avatar.userData || !this.avatar.userData.mouth) return;
        
        const mouth = this.avatar.userData.mouth;
        let count = 0;
        const maxCount = 10;
        
        const interval = setInterval(() => {
            if (count >= maxCount) {
                clearInterval(interval);
                mouth.scale.y = 1;
                return;
            }
            
            mouth.scale.y = Math.random() * 0.5 + 0.8;
            count++;
        }, 200);
    }

    clearChat() {
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = `
            <div class="message assistant-message">
                <div class="message-content">
                    <p>Hello! I'm Legrand, your 3D AI assistant. How can I help you today?</p>
                </div>
            </div>
        `;
        this.conversationHistory = [];
    }

    updateStatus(status) {
        document.querySelector('.status-text').textContent = status;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when the page loads
window.addEventListener('DOMContentLoaded', () => {
    new LegrandAI();
});
