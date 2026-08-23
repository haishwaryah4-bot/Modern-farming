"""
Floating Corner AI Agent Component for AgriSense AI.
Unifies both Voice (Speech-to-Text & Text-to-Speech) and Chat into 1 sleek,
floating bottom-right corner AI Agent drawer accessible across the platform.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_corner_ai_agent_widget(latest_response: str = ""):
    """
    Renders an interactive floating bottom-right corner AI Agent with unified voice and text.
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
        
        /* Floating Corner Container */
        .corner-agent-container {{
          position: fixed;
          bottom: 20px;
          right: 24px;
          z-index: 99999;
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 10px;
        }}

        /* Floating Pill Trigger */
        .corner-pill {{
          background: linear-gradient(135deg, #059669 0%, #047857 100%);
          color: #ffffff;
          border: 2px solid #34d399;
          border-radius: 9999px;
          padding: 10px 22px;
          display: inline-flex;
          align-items: center;
          gap: 10px;
          box-shadow: 0 10px 30px rgba(0, 20, 10, 0.4), 0 0 20px rgba(16, 185, 129, 0.3);
          cursor: pointer;
          transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .corner-pill:hover {{
          transform: translateY(-3px) scale(1.03);
          box-shadow: 0 14px 38px rgba(0, 20, 10, 0.5), 0 0 25px rgba(16, 185, 129, 0.45);
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }}

        .pill-avatar {{
          width: 32px;
          height: 32px;
          background: rgba(255, 255, 255, 0.25);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1.15rem;
        }}

        .pill-label {{
          font-size: 0.94rem;
          font-weight: 800;
          letter-spacing: -0.01em;
        }}

        .pulse-beacon {{
          width: 8px;
          height: 8px;
          background: #34d399;
          border-radius: 50%;
          box-shadow: 0 0 10px #34d399;
          animation: pulse-ring 2s infinite;
        }}

        @keyframes pulse-ring {{
          0% {{ transform: scale(0.9); opacity: 0.7; }}
          50% {{ transform: scale(1.4); opacity: 1; box-shadow: 0 0 14px #6ee7b7; }}
          100% {{ transform: scale(0.9); opacity: 0.7; }}
        }}

        /* Quick Action Mini Controls inside the Corner Widget */
        .corner-quick-actions {{
          display: flex;
          align-items: center;
          gap: 8px;
          background: rgba(255, 255, 255, 0.96);
          border: 1.5px solid #059669;
          backdrop-filter: blur(16px);
          border-radius: 14px;
          padding: 8px 14px;
          box-shadow: 0 6px 20px rgba(0, 20, 10, 0.25);
        }}

        .corner-btn {{
          background: #ffffff;
          border: 1.5px solid #cbd5e1;
          color: #031c0e;
          border-radius: 10px;
          padding: 6px 12px;
          font-size: 0.82rem;
          font-weight: 800;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          transition: all 0.2s ease;
        }}

        .corner-btn:hover {{
          background: #ecfdf5;
          border-color: #059669;
          color: #047857;
          transform: translateY(-1px);
        }}

        .corner-btn.active-mic {{
          background: #dc2626;
          color: #ffffff;
          border-color: #b91c1c;
          animation: pulse-mic 1.5s infinite;
        }}

        @keyframes pulse-mic {{
          0% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }}
          70% {{ box-shadow: 0 0 0 8px rgba(220, 38, 38, 0); }}
          100% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }}
        }}

        .lang-select-mini {{
          padding: 6px 8px;
          border-radius: 8px;
          border: 1.5px solid #cbd5e1;
          font-size: 0.8rem;
          font-weight: 700;
          color: #0f172a;
          outline: none;
          background: #ffffff;
        }}
      </style>
    </head>
    <body>
      <div class="corner-agent-container">
        <!-- Quick Action Voice & Speech Strip -->
        <div class="corner-quick-actions">
          <button id="cornerMicBtn" class="corner-btn" onclick="toggleCornerMic()">
            <span id="cornerMicIcon">🎙️</span>
            <span id="cornerMicText">Voice</span>
          </button>
          <button class="corner-btn" onclick="speakCornerResponse()">
            <span>🔊</span>
            <span>Listen</span>
          </button>
          <button class="corner-btn" onclick="stopCornerAudio()">⏹️</button>
          <select id="cornerLang" class="lang-select-mini">
            <option value="en-IN">EN (India)</option>
            <option value="hi-IN">हिन्दी (Hindi)</option>
            <option value="en-US">EN (US)</option>
          </select>
        </div>

        <!-- 1 Unified Corner AI Agent Launcher -->
        <div class="corner-pill" onclick="focusMainChat()">
          <div class="pill-avatar">🌱</div>
          <span class="pill-label">1 AI Agent (Voice & Chat)</span>
          <div class="pulse-beacon"></div>
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
            document.getElementById('cornerMicBtn').classList.add('active-mic');
            document.getElementById('cornerMicText').innerText = 'Listening...';
          }};

          recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            const parentInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]') 
                             || window.parent.document.querySelector('input[data-testid="stTextInput"]');
            if (parentInput) {{
              parentInput.value = transcript;
              parentInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
          }};

          recognition.onerror = function(e) {{
            resetCornerMic();
          }};

          recognition.onend = function() {{
            resetCornerMic();
          }};
        }}

        function resetCornerMic() {{
          isListening = false;
          document.getElementById('cornerMicBtn').classList.remove('active-mic');
          document.getElementById('cornerMicText').innerText = 'Voice';
        }}

        function toggleCornerMic() {{
          if (!recognition) {{
            alert('Web Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.');
            return;
          }}
          if (isListening) {{
            recognition.stop();
            resetCornerMic();
          }} else {{
            recognition.lang = document.getElementById('cornerLang').value;
            recognition.start();
          }}
        }}

        function speakCornerResponse() {{
          if (!('speechSynthesis' in window)) {{
            alert('Text-to-speech is not supported in this browser.');
            return;
          }}
          window.speechSynthesis.cancel();
          const textToSpeak = currentAnswer || "Welcome to AgriSense AI. You can speak or chat with the 1 AI Agent.";
          const utterance = new SpeechSynthesisUtterance(textToSpeak);
          utterance.lang = document.getElementById('cornerLang').value;
          utterance.rate = 1.0;
          window.speechSynthesis.speak(utterance);
        }}

        function stopCornerAudio() {{
          if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
          }}
          if (recognition && isListening) {{
            recognition.stop();
          }}
          resetCornerMic();
        }}

        function focusMainChat() {{
          const chatInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
          if (chatInput) {{
            chatInput.focus();
          }}
        }}
      </script>
    </body>
    </html>
    """

    components.html(html_code, height=95)
