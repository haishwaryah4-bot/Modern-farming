"""
Unified 'Speak AI' & 'Ask AI' Combined Console Component for AgriSense AI.
Combines Speech-to-Text (Speak AI), Text Input (Ask AI), Text-to-Speech Audio Readout,
and Language Switching into one unified interactive interface.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_speak_and_ask_ai_bar(latest_response: str = ""):
    """
    Renders an all-in-one 'Speak AI' and 'Ask AI' unified console.
    """
    sanitized_text = (
        latest_response.replace("`", "'")
        .replace('"', "'")
        .replace("\n", " ")
        .replace("*", "")
        .replace("#", "")
    )

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
          font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
          background: transparent;
          overflow: hidden;
        }}
        .speak-ask-container {{
          background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.96) 100%);
          border: 2px solid #059669;
          border-radius: 16px;
          padding: 14px 20px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 14px;
          box-shadow: 0 6px 20px rgba(0, 20, 10, 0.15);
          margin-bottom: 12px;
        }}
        .action-group-left {{
          display: flex;
          align-items: center;
          gap: 10px;
          flex: 1;
        }}
        .speak-ai-btn {{
          background: linear-gradient(135deg, #059669 0%, #047857 100%);
          color: #ffffff;
          border: none;
          border-radius: 12px;
          padding: 10px 20px;
          font-weight: 800;
          font-size: 0.94rem;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 8px;
          box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35);
          transition: all 0.2s ease;
          white-space: nowrap;
        }}
        .speak-ai-btn:hover {{
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(5, 150, 105, 0.5);
        }}
        .speak-ai-btn.listening {{
          background: linear-gradient(135deg, #dc2626, #b91c1c);
          animation: pulse-ring 1.5s infinite;
        }}
        @keyframes pulse-ring {{
          0% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }}
          70% {{ box-shadow: 0 0 0 12px rgba(220, 38, 38, 0); }}
          100% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }}
        }}
        .status-pill {{
          font-size: 0.88rem;
          color: #064e3b;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 6px;
        }}
        .action-group-right {{
          display: flex;
          align-items: center;
          gap: 8px;
        }}
        .tts-btn {{
          background: #ffffff;
          border: 1.5px solid #059669;
          color: #065f46;
          border-radius: 10px;
          padding: 8px 16px;
          font-weight: 800;
          font-size: 0.86rem;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          box-shadow: 0 2px 6px rgba(5, 150, 105, 0.15);
          transition: all 0.2s ease;
          white-space: nowrap;
        }}
        .tts-btn:hover {{
          background: #ecfdf5;
          transform: translateY(-1px);
        }}
        .stop-btn {{
          background: #ffffff;
          border: 1.5px solid #cbd5e1;
          color: #031c0e;
          border-radius: 8px;
          padding: 8px 12px;
          font-size: 0.84rem;
          font-weight: 700;
          cursor: pointer;
          white-space: nowrap;
        }}
        .stop-btn:hover {{
          background: #fee2e2;
          border-color: #ef4444;
          color: #991b1b;
        }}
        .lang-select {{
          padding: 8px 12px;
          border-radius: 10px;
          border: 1.5px solid #cbd5e1;
          font-size: 0.84rem;
          font-weight: 700;
          color: #0f172a;
          outline: none;
          background: #ffffff;
        }}
      </style>
    </head>
    <body>
      <div class="speak-ask-container">
        <!-- Speak AI Button & Status -->
        <div class="action-group-left">
          <button id="micBtn" class="speak-ai-btn" onclick="toggleSpeechRecognition()">
            <span id="micIcon">🎙️</span>
            <span id="micText">Speak AI (Voice)</span>
          </button>
          <div id="voiceStatus" class="status-pill">
            <span>⚡ Speak AI & Ask AI Active</span>
          </div>
        </div>

        <!-- Voice Output / Listen AI Controls -->
        <div class="action-group-right">
          <button id="ttsBtn" class="tts-btn" onclick="speakResponse()">
            <span>🔊</span>
            <span>Listen AI (Voice)</span>
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

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
          const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
          recognition = new SpeechRec();
          recognition.continuous = false;
          recognition.interimResults = false;

          recognition.onstart = function() {{
            isListening = true;
            document.getElementById('micBtn').classList.add('listening');
            document.getElementById('micText').innerText = 'Listening to speech...';
            document.getElementById('voiceStatus').innerHTML = '<span>🔴 Recording your question...</span>';
          }};

          recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            document.getElementById('voiceStatus').innerHTML = '<span>✅ Heard: "' + transcript + '"</span>';
            const parentInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
            if (parentInput) {{
              parentInput.value = transcript;
              parentInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
          }};

          recognition.onerror = function(e) {{
            document.getElementById('voiceStatus').innerHTML = '<span>⚠️ Speech error: ' + e.error + '</span>';
            resetMic();
          }};

          recognition.onend = function() {{
            resetMic();
          }};
        }} else {{
          document.getElementById('micBtn').style.opacity = '0.7';
          document.getElementById('micText').innerText = 'Speak AI (Not Supported)';
        }}

        function resetMic() {{
          isListening = false;
          document.getElementById('micBtn').classList.remove('listening');
          document.getElementById('micText').innerText = 'Speak AI (Voice)';
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
          const textToSpeak = currentAnswer || "Welcome to AgriSense AI. You can speak or ask any crop or soil question.";
          const utterance = new SpeechSynthesisUtterance(textToSpeak);
          utterance.lang = document.getElementById('voiceLang').value;
          utterance.rate = 1.0;
          utterance.pitch = 1.0;

          document.getElementById('voiceStatus').innerHTML = '<span>🔊 Reading answer aloud...</span>';
          utterance.onend = function() {{
            document.getElementById('voiceStatus').innerHTML = '<span>⚡ Speak AI & Ask AI Active</span>';
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
          document.getElementById('voiceStatus').innerHTML = '<span>⏹️ Voice stopped</span>';
          resetMic();
        }}
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=80)
