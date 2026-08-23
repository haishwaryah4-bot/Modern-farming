"""
Unified 'Ask AI Agents' Interactive Prompt Bar Component for AgriSense AI.
High-Contrast, Zero-Cutoff, Ultra-Legible Typography & Controls.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_ask_ai_agents_bar(
    placeholder: str = "Type farming question or click '🎙️ Ask AI Agents' to speak...",
    latest_response: str = "",
):
    """
    Renders an ultra-clean, high-contrast '🎙️ Ask AI Agents' prompt bar with zero clipping.
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
        * {{
          box-sizing: border-box;
          margin: 0;
          padding: 0;
          -webkit-font-smoothing: antialiased;
        }}
        body {{
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          background: transparent;
          overflow: hidden;
          padding: 4px;
        }}

        /* Container Card */
        .agent-bar-card {{
          background: #ffffff;
          border: 2.5px solid #059669;
          border-radius: 18px;
          padding: 16px 22px;
          box-shadow: 0 12px 36px rgba(0, 20, 10, 0.35), 0 0 20px rgba(16, 185, 129, 0.25);
          display: flex;
          flex-direction: column;
          gap: 14px;
        }}

        /* Workflow Step Indicator */
        .workflow-indicator {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 0.88rem;
          font-weight: 800;
          color: #047857;
          background: #ecfdf5;
          border: 1.5px solid #10b981;
          padding: 8px 18px;
          border-radius: 12px;
        }}

        .workflow-step {{
          display: flex;
          align-items: center;
          gap: 6px;
          color: #064e3b;
        }}

        .workflow-arrow {{
          color: #059669;
          font-weight: 900;
          font-size: 1.1rem;
        }}

        /* Main Input Bar Row */
        .input-row {{
          display: flex;
          align-items: center;
          gap: 12px;
        }}

        /* Text Input */
        .prompt-input {{
          flex: 1;
          border: 2px solid #94a3b8;
          border-radius: 14px;
          background: #ffffff;
          font-size: 1rem;
          font-weight: 700;
          color: #031c0e;
          padding: 14px 18px;
          outline: none;
          transition: all 0.2s ease;
        }}

        .prompt-input:focus {{
          border-color: #059669;
          box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.25);
        }}

        .prompt-input::placeholder {{
          color: #475569 !important;
          font-weight: 600 !important;
          opacity: 1 !important;
        }}

        /* Single Prominent 'Ask AI Agents' Button */
        .ask-agents-btn {{
          background: linear-gradient(135deg, #059669 0%, #047857 100%);
          color: #ffffff !important;
          border: none;
          border-radius: 14px;
          padding: 14px 28px;
          font-weight: 900;
          font-size: 1rem;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 10px;
          box-shadow: 0 6px 18px rgba(5, 150, 105, 0.45);
          transition: all 0.2s ease;
          white-space: nowrap;
          text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        }}

        .ask-agents-btn span {{
          color: #ffffff !important;
        }}

        .ask-agents-btn:hover {{
          transform: translateY(-2px);
          box-shadow: 0 10px 26px rgba(5, 150, 105, 0.6);
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }}

        .ask-agents-btn.listening {{
          background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
          animation: pulse-ring 1.5s infinite;
        }}

        @keyframes pulse-ring {{
          0% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }}
          70% {{ box-shadow: 0 0 0 12px rgba(220, 38, 38, 0); }}
          100% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }}
        }}

        /* Controls Cluster (Read Aloud + Stop Voice + Language) */
        .controls-cluster {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 10px;
          flex-wrap: nowrap;
        }}

        .status-badge {{
          background: #ecfdf5;
          border: 1.5px solid #10b981;
          color: #047857;
          font-weight: 800;
          font-size: 0.88rem;
          padding: 8px 16px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          gap: 6px;
        }}

        .action-buttons-group {{
          display: flex;
          align-items: center;
          gap: 10px;
        }}

        .read-aloud-btn {{
          background: #ffffff;
          border: 2px solid #059669;
          color: #065f46;
          border-radius: 10px;
          padding: 9px 18px;
          font-weight: 800;
          font-size: 0.88rem;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          transition: all 0.2s ease;
          box-shadow: 0 2px 6px rgba(5, 150, 105, 0.15);
        }}

        .read-aloud-btn:hover {{
          background: #ecfdf5;
          transform: translateY(-1px);
        }}

        .stop-voice-btn {{
          background: #ffffff;
          border: 2px solid #ef4444;
          color: #991b1b;
          border-radius: 10px;
          padding: 9px 16px;
          font-size: 0.86rem;
          font-weight: 800;
          cursor: pointer;
          transition: all 0.2s ease;
        }}

        .stop-voice-btn:hover {{
          background: #fee2e2;
          transform: translateY(-1px);
        }}

        .lang-dropdown {{
          padding: 9px 14px;
          border-radius: 10px;
          border: 2px solid #94a3b8;
          font-size: 0.88rem;
          font-weight: 800;
          color: #0f172a;
          outline: none;
          background: #ffffff;
          cursor: pointer;
        }}
      </style>
    </head>
    <body>
      <div class="agent-bar-card">
        <!-- 1. Visual Multi-Agent Workflow Indicator -->
        <div class="workflow-indicator">
          <div class="workflow-step"><span>🎙️</span><span>Voice Question</span></div>
          <span class="workflow-arrow">➔</span>
          <div class="workflow-step"><span>🤖</span><span>Multiple AI Agents</span></div>
          <span class="workflow-arrow">➔</span>
          <div class="workflow-step"><span>🧠</span><span>Combined Analysis</span></div>
          <span class="workflow-arrow">➔</span>
          <div class="workflow-step"><span>🔊</span><span>Voice Answer</span></div>
        </div>

        <!-- 2. Main Question Input + Prominent '🎙️ Ask AI Agents' Button -->
        <div class="input-row">
          <input 
            id="agentPromptInput" 
            type="text" 
            class="prompt-input" 
            placeholder="{placeholder}" 
            onkeydown="handleKeyPress(event)"
          />
          <button id="askAgentsBtn" class="ask-agents-btn" onclick="handleAskAgentsClick()" title="Click to speak hands-free or send question">
            <span id="btnIcon">🎙️</span>
            <span id="btnText">Ask AI Agents</span>
          </button>
        </div>

        <!-- 3. Bottom Controls: Status Badge + Read Aloud + Stop Voice + Language -->
        <div class="controls-cluster">
          <div id="statusText" class="status-badge">
            <span>⚡ Ready for Voice or Text</span>
          </div>
          <div class="action-buttons-group">
            <button class="read-aloud-btn" onclick="readAnswerAloud()" title="Listen to synthesized recommendation">
              <span>🔊 Read Answer Aloud</span>
            </button>
            <button class="stop-voice-btn" onclick="stopAllSpeech()" title="Stop voice recording or readout">
              <span>⏹️ Stop Voice</span>
            </button>
            <select id="voiceLanguage" class="lang-dropdown" onchange="updateLang()">
              <option value="en-IN">English (India)</option>
              <option value="hi-IN">हिन्दी (Hindi)</option>
              <option value="en-US">English (US)</option>
            </select>
          </div>
        </div>
      </div>

      <script>
        let recognition = null;
        let isListening = false;
        let speechDispatched = false;
        const currentAnswer = `{sanitized_text}`;

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
          const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
          recognition = new SpeechRec();
          recognition.continuous = false;
          recognition.interimResults = false;

          recognition.onstart = function() {{
            isListening = true;
            speechDispatched = false;
            document.getElementById('askAgentsBtn').classList.add('listening');
            document.getElementById('btnIcon').innerText = '🔴';
            document.getElementById('btnText').innerText = 'Listening...';
            document.getElementById('statusText').innerHTML = '<span>🎙️ Listening to your question...</span>';
          }};

          recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            document.getElementById('agentPromptInput').value = transcript;
            document.getElementById('statusText').innerHTML = '<span>✅ Transcribed: "' + transcript + '"</span>';
            if (!speechDispatched) {{
              speechDispatched = true;
              submitQueryToAgents(transcript);
            }}
          }};

          recognition.onerror = function(e) {{
            document.getElementById('statusText').innerHTML = '<span>⚠️ Speech error: ' + e.error + '</span>';
            resetBtn();
          }};

          recognition.onend = function() {{
            resetBtn();
          }};
        }} else {{
          document.getElementById('askAgentsBtn').title = 'Speech recognition not supported in browser. Type question and click Ask AI Agents.';
        }}

        function resetBtn() {{
          isListening = false;
          document.getElementById('askAgentsBtn').classList.remove('listening');
          document.getElementById('btnIcon').innerText = '🎙️';
          document.getElementById('btnText').innerText = 'Ask AI Agents';
        }}

        function handleAskAgentsClick() {{
          const textVal = document.getElementById('agentPromptInput').value.trim();
          
          if (textVal && textVal.length > 0 && !isListening) {{
            submitQueryToAgents(textVal);
            return;
          }}

          if (!recognition) {{
            alert('Web Speech API is not supported in this browser. Please type your question or use Google Chrome / Microsoft Edge.');
            return;
          }}

          if (isListening) {{
            recognition.stop();
            resetBtn();
          }} else {{
            const lang = document.getElementById('voiceLanguage').value;
            recognition.lang = lang;
            recognition.start();
          }}
        }}

        function handleKeyPress(e) {{
          if (e.key === 'Enter') {{
            const textVal = document.getElementById('agentPromptInput').value.trim();
            if (textVal) {{
              submitQueryToAgents(textVal);
            }}
          }}
        }}

        function submitQueryToAgents(query) {{
          if (!query || !query.trim()) return;

          document.getElementById('statusText').innerHTML = '<span>🤖 Orchestrating Multiple AI Agents...</span>';

          // 1. Submit to parent Streamlit chat input if on AI Agent Studio page
          const parentChat = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
          if (parentChat) {{
            parentChat.value = query;
            parentChat.dispatchEvent(new Event('input', {{ bubbles: true }}));
            const sendBtn = window.parent.document.querySelector('button[data-testid="stChatInputSubmitButton"]');
            if (sendBtn) {{
              sendBtn.click();
              return;
            }}
          }}

          // 2. Submit to parent Streamlit input on Home dashboard
          const parentText = window.parent.document.querySelector('input[data-testid="stTextInput"]');
          if (parentText) {{
            parentText.value = query;
            parentText.dispatchEvent(new Event('input', {{ bubbles: true }}));
            // Trigger Streamlit rerun by pressing enter or firing change
            parentText.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
          }}
        }}

        function readAnswerAloud() {{
          if (!('speechSynthesis' in window)) {{
            alert('Text-to-Speech is not supported in this browser.');
            return;
          }}
          window.speechSynthesis.cancel();
          const textToSpeak = currentAnswer || "Welcome to AgriSense AI. How can I assist your crop operations today?";
          const utterance = new SpeechSynthesisUtterance(textToSpeak);
          utterance.lang = document.getElementById('voiceLanguage').value;
          utterance.rate = 1.0;
          utterance.pitch = 1.0;

          document.getElementById('statusText').innerHTML = '<span>🔊 Reading answer aloud...</span>';
          utterance.onend = function() {{
            document.getElementById('statusText').innerHTML = '<span>⚡ Ready for Voice or Text</span>';
          }};
          window.speechSynthesis.speak(utterance);
        }}

        function stopAllSpeech() {{
          if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
          }}
          if (recognition && isListening) {{
            recognition.stop();
          }}
          document.getElementById('statusText').innerHTML = '<span>⏹️ Voice stopped</span>';
          resetBtn();
        }}

        function updateLang() {{
          // Language selector
        }}
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=195)
