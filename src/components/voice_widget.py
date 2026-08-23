"""
Voice Agent Component for AgriSense AI.
Provides browser-native Speech-to-Text (STT) and Text-to-Speech (TTS) audio synthesis
using the Web Speech API with animated microphone pulses and audio controls.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_voice_agent_controls(latest_response: str = ""):
    """
    Renders an interactive HTML5 Voice Assistant control bar
    supporting Speech Recognition and Speech Synthesis.
    """
    # Clean string for JS injection
    sanitized_text = (
        latest_response.replace("`", "'")
        .replace('"', "'")
        .replace("\n", " ")
        .replace("*", "")
        .replace("#", "")
    )

    voice_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{
          margin: 0;
          padding: 0;
          font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
          background: transparent;
        }}
        .voice-bar {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(240, 253, 244, 0.95));
          border: 1.5px solid #059669;
          border-radius: 14px;
          padding: 12px 20px;
          box-shadow: 0 4px 16px rgba(0, 20, 10, 0.12);
        }}
        .voice-left {{
          display: flex;
          align-items: center;
          gap: 12px;
        }}
        .voice-btn {{
          background: linear-gradient(135deg, #059669, #047857);
          color: #ffffff;
          border: none;
          border-radius: 10px;
          padding: 8px 16px;
          font-weight: 700;
          font-size: 0.88rem;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
          transition: all 0.2s ease;
        }}
        .voice-btn:hover {{
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(5, 150, 105, 0.45);
        }}
        .voice-btn.listening {{
          background: linear-gradient(135deg, #dc2626, #b91c1c);
          animation: pulse-red 1.5s infinite;
        }}
        @keyframes pulse-red {{
          0% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }}
          70% {{ box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }}
          100% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }}
        }}
        .voice-status {{
          font-size: 0.85rem;
          color: #064e3b;
          font-weight: 700;
        }}
        .voice-controls {{
          display: flex;
          align-items: center;
          gap: 10px;
        }}
        .stop-btn {{
          background: #ffffff;
          border: 1.5px solid #cbd5e1;
          color: #031c0e;
          border-radius: 8px;
          padding: 6px 12px;
          font-size: 0.82rem;
          font-weight: 700;
          cursor: pointer;
        }}
        .stop-btn:hover {{
          background: #f8fafc;
          border-color: #94a3b8;
        }}
        .lang-select {{
          padding: 6px 10px;
          border-radius: 8px;
          border: 1.5px solid #cbd5e1;
          font-size: 0.82rem;
          font-weight: 600;
          color: #0f172a;
          outline: none;
        }}
      </style>
    </head>
    <body>
      <div class="voice-bar">
        <div class="voice-left">
          <button id="micBtn" class="voice-btn" onclick="toggleSpeechRecognition()">
            <span id="micIcon">🎙️</span>
            <span id="micText">Voice Input (Speak)</span>
          </button>
          <span id="voiceStatus" class="voice-status">⚡ Voice Agent Ready</span>
        </div>
        <div class="voice-controls">
          <button id="ttsBtn" class="voice-btn" onclick="speakResponse()">
            <span>🔊</span>
            <span>Read Answer Aloud</span>
          </button>
          <button class="stop-btn" onclick="stopSpeech()">⏹️ Stop</button>
          <select id="voiceLang" class="lang-select">
            <option value="en-IN">English (India)</option>
            <option value="hi-IN">Hindi (हिन्दी)</option>
            <option value="en-US">English (US)</option>
          </select>
        </div>
      </div>

      <script>
        let recognition = null;
        let isListening = false;
        const currentAnswer = `{sanitized_text}`;

        // Initialize Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
          const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
          recognition = new SpeechRec();
          recognition.continuous = false;
          recognition.interimResults = false;

          recognition.onstart = function() {{
            isListening = true;
            document.getElementById('micBtn').classList.add('listening');
            document.getElementById('micText').innerText = 'Listening...';
            document.getElementById('voiceStatus').innerText = '🎙️ Listening to your question...';
          }};

          recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            document.getElementById('voiceStatus').innerText = '✅ Heard: "' + transcript + '"';
            // Set into Streamlit / Parent chat if possible
            const parentInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
            if (parentInput) {{
              parentInput.value = transcript;
              parentInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
          }};

          recognition.onerror = function(e) {{
            document.getElementById('voiceStatus').innerText = '⚠️ Speech recognition error: ' + e.error;
            resetMic();
          }};

          recognition.onend = function() {{
            resetMic();
          }};
        }} else {{
          document.getElementById('micBtn').style.opacity = '0.6';
          document.getElementById('micText').innerText = 'Mic Not Supported';
        }}

        function resetMic() {{
          isListening = false;
          document.getElementById('micBtn').classList.remove('listening');
          document.getElementById('micText').innerText = 'Voice Input (Speak)';
        }}

        function toggleSpeechRecognition() {{
          if (!recognition) {{
            alert('Web Speech API is not supported in this browser. Please use Chrome, Edge, or Safari.');
            return;
          }}
          if (isListening) {{
            recognition.stop();
            resetMic();
          }} else {{
            const lang = document.getElementById('voiceLang').value;
            recognition.lang = lang;
            recognition.start();
          }}
        }}

        function speakResponse() {{
          if (!('speechSynthesis' in window)) {{
            alert('Text-to-Speech is not supported in this browser.');
            return;
          }}
          window.speechSynthesis.cancel();
          const textToSpeak = currentAnswer || "Welcome to AgriSense AI. How can I assist your crop operations today?";
          const utterance = new SpeechSynthesisUtterance(textToSpeak);
          utterance.lang = document.getElementById('voiceLang').value;
          utterance.rate = 1.0;
          utterance.pitch = 1.0;

          document.getElementById('voiceStatus').innerText = '🔊 Speaking response aloud...';
          utterance.onend = function() {{
            document.getElementById('voiceStatus').innerText = '⚡ Voice Agent Ready';
          }};
          window.speechSynthesis.speak(utterance);
        }}

        function stopSpeech() {{
          if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
          }}
          if (recognition && isListening) {{
            recognition.stop();
          }}
          document.getElementById('voiceStatus').innerText = '⏹️ Audio stopped';
          resetMic();
        }}
      </script>
    </body>
    </html>
    """

    components.html(voice_html, height=75)
