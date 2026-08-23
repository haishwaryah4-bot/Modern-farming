"""
Unified AgriSense AI & Voice Assistant Chat Box Component.
Features Professional Agricultural AI Robot Avatar with Dynamic Thinking & Listening Animations
and Visual Image Dataset Evidence Cards.
"""

import base64
import re
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from src.agents import ai_agent
import config


def _get_avatar_base64() -> str:
    """Encodes the professional agricultural AI assistant avatar into base64."""
    avatar_path = config.BASE_DIR / "assets" / "images" / "agrisense_ai_avatar.jpg"
    if avatar_path.exists():
        with open(avatar_path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    return ""


def _format_chat_content(content: str) -> str:
    """Formats markdown headers and bolding while preserving raw HTML image cards."""
    if not content:
        return ""
    
    formatted = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", content)
    formatted = re.sub(r"^### (.*$)", r"<h4 style='color:#052e16; margin: 14px 0 6px 0; font-size: 1.15rem; font-weight: 900;'>\1</h4>", formatted, flags=re.MULTILINE)
    formatted = re.sub(r"^## (.*$)", r"<h3 style='color:#052e16; margin: 16px 0 8px 0; font-size: 1.25rem; font-weight: 900;'>\1</h3>", formatted, flags=re.MULTILINE)
    formatted = re.sub(r"^# (.*$)", r"<h2 style='color:#052e16; margin: 18px 0 10px 0; font-size: 1.35rem; font-weight: 900;'>\1</h2>", formatted, flags=re.MULTILINE)

    # Split by HTML div blocks to preserve inner image markup
    parts = re.split(r'(<div[\s\S]*?</div>)', formatted)
    out = []
    for p in parts:
        if p.startswith('<div'):
            out.append(p)
        else:
            out.append(p.replace("\n", "<br>"))
    return "".join(out)


def render_unified_chat_box(key_prefix: str = "dash"):
    """
    Renders the unified AI Chat Box with integrated ⌨️ Type + 🎙️ Speak inputs,
    professional AI avatar with thinking/listening glow animations, audio readout,
    and visual image dataset evidence cards.
    """
    avatar_b64 = _get_avatar_base64()

    # Initialize chat history in session state
    chat_key = f"{key_prefix}_unified_chat_messages"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am your **AgriSense AI Assistant**. You can **type a question** or click **🎙️ to speak** hands-free.\n\n"
                    "Ask anything about crops, pests, modern farming, or smart irrigation, and I will retrieve both **actionable farming guidance and verified photographic evidence** from the ingested agricultural dataset."
                ),
                "agents_status": [
                    {"name": "🌾 Farming Knowledge Agent", "status": "Ready"},
                    {"name": "🌦️ Weather Agent", "status": "Ready"},
                    {"name": "🌱 Soil Agent", "status": "Ready"},
                    {"name": "🤖 Advisory Agent", "status": "Ready"},
                ],
                "traces": [],
            }
        ]

    # Check for incoming query from 1-click scenario buttons
    scenario_query_key = f"{key_prefix}_selected_query"
    incoming_scenario = st.session_state.get(scenario_query_key)
    if incoming_scenario:
        user_query = incoming_scenario
        st.session_state[scenario_query_key] = ""
        _process_query(user_query, chat_key)

    # Get latest assistant answer for voice readout
    latest_answer = ""
    for msg in reversed(st.session_state[chat_key]):
        if msg.get("role") == "assistant":
            latest_answer = msg.get("content", "")
            break

    # Clean text and encode to base64 for safe JS speech synthesis
    clean_text = re.sub(r"<[^>]+>", " ", latest_answer)
    sanitized_answer = (
        clean_text.replace("`", "'")
        .replace('"', "'")
        .replace("\n", " ")
        .replace("*", "")
        .replace("#", "")
        .replace("  ", " ")
        .strip()
    )
    latest_speech_b64 = base64.b64encode(sanitized_answer.encode("utf-8")).decode("utf-8")

    # Render Conversation Messages HTML
    messages_html = ""
    for msg in st.session_state[chat_key]:
        if msg["role"] == "user":
            messages_html += f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 18px;">
                <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); color: #ffffff; padding: 14px 20px; border-radius: 16px 16px 4px 16px; max-width: 80%; box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35); font-size: 0.98rem; font-weight: 700; line-height: 1.5;">
                    <div style="font-size: 0.82rem; opacity: 0.92; margin-bottom: 4px; font-weight: 800; display: flex; align-items: center; gap: 6px;">
                        <span>👤</span><span>User Question</span>
                    </div>
                    {msg['content']}
                </div>
            </div>
            """
        else:
            # Assistant Message with Agent Status Badges
            agent_badges = ""
            if msg.get("agents_status"):
                badge_items = "".join(
                    f"<span style='background: #ecfdf5; color: #047857; border: 1.5px solid #10b981; font-weight: 800; font-size: 0.8rem; padding: 3px 10px; border-radius: 8px; margin-right: 6px;'>{ag['name']} ✓</span>"
                    for ag in msg["agents_status"]
                )
                agent_badges = f"""
                <div style="margin-bottom: 10px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center;">
                    <span style="font-size: 0.82rem; font-weight: 800; color: #0f172a;">🤖 AI Agents:</span>
                    {badge_items}
                </div>
                """

            formatted_content = _format_chat_content(msg["content"])
            
            # Single message speech b64
            msg_clean_text = re.sub(r"<[^>]+>", " ", msg["content"])
            msg_sanitized = msg_clean_text.replace("`", "'").replace('"', "'").replace("\n", " ").replace("*", "").replace("#", "").strip()
            msg_speech_b64 = base64.b64encode(msg_sanitized.encode("utf-8")).decode("utf-8")

            avatar_img_tag = (
                f'<img src="{avatar_b64}" style="width: 44px; height: 44px; border-radius: 50%; border: 2px solid #059669; box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3); flex-shrink: 0; object-fit: cover;" alt="AgriSense AI Avatar">'
                if avatar_b64
                else '<div style="width: 44px; height: 44px; border-radius: 50%; background: #ecfdf5; border: 2px solid #059669; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; flex-shrink: 0;">🤖</div>'
            )

            messages_html += f"""
            <div style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 22px;">
                {avatar_img_tag}
                <div style="background: #ffffff; color: #0f172a; border: 2px solid #cbd5e1; padding: 18px 22px; border-radius: 4px 18px 18px 18px; max-width: 90%; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08); font-size: 0.96rem; line-height: 1.6;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 8px;">
                        <span style="font-weight: 900; color: #031c0e; font-size: 1.05rem; display: flex; align-items: center; gap: 6px;">
                            AgriSense AI Assistant
                        </span>
                        <button onclick="speakFromB64('{msg_speech_b64}')" style="background: #ecfdf5; border: 1.5px solid #059669; color: #065f46; border-radius: 8px; padding: 5px 12px; font-weight: 800; font-size: 0.82rem; cursor: pointer;">
                            🔊 Read Aloud
                        </button>
                    </div>
                    {agent_badges}
                    <div style="color: #1e293b; font-weight: 600;">
                        {formatted_content}
                    </div>
                </div>
            </div>
            """

    # Interactive Unified Box Component with Speech-to-Text, Visual Cards & Avatar Glow
    unified_widget_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background: transparent; padding: 2px; }}

        /* Unified Card Container */
        .chat-container {{
          background: #ffffff;
          border: 2.5px solid #059669;
          border-radius: 22px;
          box-shadow: 0 16px 40px rgba(0, 20, 10, 0.35), 0 0 24px rgba(16, 185, 129, 0.25);
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }}

        /* Header Bar */
        .chat-header {{
          background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
          border-bottom: 2px solid #86efac;
          padding: 16px 24px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          flex-wrap: wrap;
          gap: 12px;
        }}

        .avatar-container {{
          position: relative;
          width: 56px;
          height: 56px;
          flex-shrink: 0;
        }}

        .header-avatar {{
          width: 56px;
          height: 56px;
          border-radius: 50%;
          border: 2.5px solid #059669;
          box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35);
          object-fit: cover;
          display: block;
          transition: all 0.3s ease;
        }}

        /* Avatar Glow Keyframe Animations */
        @keyframes thinking-pulse {{
          0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7), 0 4px 14px rgba(5, 150, 105, 0.35); transform: scale(1); }}
          50% {{ box-shadow: 0 0 22px 6px rgba(16, 185, 129, 0.9), 0 4px 20px rgba(5, 150, 105, 0.6); transform: scale(1.05); }}
          100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7), 0 4px 14px rgba(5, 150, 105, 0.35); transform: scale(1); }}
        }}

        @keyframes listening-pulse {{
          0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7), 0 4px 14px rgba(220, 38, 38, 0.35); transform: scale(1); }}
          50% {{ box-shadow: 0 0 24px 8px rgba(239, 68, 68, 0.9), 0 4px 20px rgba(220, 38, 38, 0.6); transform: scale(1.06); }}
          100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7), 0 4px 14px rgba(220, 38, 38, 0.35); transform: scale(1); }}
        }}

        .header-avatar.thinking-glow {{
          animation: thinking-pulse 1.4s infinite ease-in-out;
          border-color: #10b981;
        }}

        .header-avatar.listening-glow {{
          animation: listening-pulse 1.2s infinite ease-in-out;
          border-color: #ef4444;
        }}

        .sprout-badge {{
          position: absolute;
          bottom: -2px;
          right: -2px;
          background: #ffffff;
          border: 1.5px solid #059669;
          border-radius: 50%;
          width: 20px;
          height: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.8rem;
          box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }}

        .header-identity {{
          display: flex;
          align-items: center;
          gap: 14px;
        }}

        .header-title-text {{
          font-size: 1.28rem;
          font-weight: 900;
          color: #031c0e;
          letter-spacing: -0.02em;
          margin: 0;
        }}

        .header-status-text {{
          font-size: 0.86rem;
          font-weight: 700;
          color: #047857;
          display: flex;
          align-items: center;
          gap: 6px;
          margin-top: 2px;
        }}

        .header-controls {{
          display: flex;
          align-items: center;
          gap: 12px;
        }}

        .status-pill {{
          background: #dcfce7;
          border: 1.5px solid #16a34a;
          color: #14532d;
          font-size: 0.86rem;
          font-weight: 800;
          padding: 6px 14px;
          border-radius: 9999px;
          display: flex;
          align-items: center;
          gap: 6px;
        }}

        .pulse-dot {{
          width: 8px;
          height: 8px;
          background: #16a34a;
          border-radius: 50%;
          display: inline-block;
          box-shadow: 0 0 6px #16a34a;
        }}

        .lang-select {{
          background: #ffffff;
          border: 1.5px solid #cbd5e1;
          border-radius: 8px;
          padding: 6px 12px;
          font-size: 0.84rem;
          font-weight: 700;
          color: #0f172a;
          outline: none;
        }}

        /* Message Scroll Area */
        .messages-area {{
          padding: 24px;
          max-height: 480px;
          overflow-y: auto;
          background: #f8fafc;
          scroll-behavior: smooth;
        }}

        /* Unified Bottom Input Bar */
        .input-bar {{
          background: #ffffff;
          border-top: 2px solid #e2e8f0;
          padding: 16px 20px;
          display: flex;
          align-items: center;
          gap: 12px;
        }}

        .text-input-field {{
          flex: 1;
          background: #f1f5f9;
          border: 2px solid #cbd5e1;
          border-radius: 12px;
          padding: 12px 18px;
          font-size: 0.98rem;
          font-weight: 600;
          color: #0f172a;
          outline: none;
          transition: all 0.2s ease;
        }}

        .text-input-field:focus {{
          border-color: #059669;
          background: #ffffff;
          box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
        }}

        .btn-mic {{
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          border: none;
          color: #ffffff;
          border-radius: 12px;
          padding: 12px 18px;
          font-size: 1.15rem;
          font-weight: 800;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 14px rgba(5, 150, 105, 0.4);
          transition: all 0.2s ease;
          min-width: 48px;
        }}

        .btn-mic:hover {{
          transform: translateY(-2px);
          box-shadow: 0 6px 18px rgba(5, 150, 105, 0.5);
        }}

        .btn-mic.listening {{
          background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
          animation: listening-pulse 1.2s infinite ease-in-out;
        }}

        .btn-send {{
          background: linear-gradient(135deg, #022c15 0%, #064e3b 100%);
          border: none;
          color: #ffffff;
          border-radius: 12px;
          padding: 12px 24px;
          font-size: 0.96rem;
          font-weight: 800;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;
          box-shadow: 0 4px 14px rgba(2, 44, 21, 0.35);
          transition: all 0.2s ease;
        }}

        .btn-send:hover {{
          transform: translateY(-2px);
          box-shadow: 0 6px 18px rgba(2, 44, 21, 0.45);
        }}

        .status-footer {{
          background: #f8fafc;
          border-top: 1px solid #e2e8f0;
          padding: 8px 20px;
          font-size: 0.78rem;
          font-weight: 700;
          color: #64748b;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }}
      </style>
    </head>
    <body>
      <div class="chat-container">
        <!-- Header -->
        <div class="chat-header">
          <div class="header-identity">
            <div class="avatar-container">
              <img id="headerAvatar" class="header-avatar" src="{avatar_b64}" alt="AgriSense AI Avatar">
              <span class="sprout-badge">🌱</span>
            </div>
            <div>
              <div class="header-title-text">AgriSense AI Assistant</div>
              <div id="headerSubtitle" class="header-status-text">
                <span class="pulse-dot"></span> 🟢 AI Agents Online • Visual Evidence Active
              </div>
            </div>
          </div>

          <div class="header-controls">
            <select id="voiceLangSelect" class="lang-select" title="Speech Language">
              <option value="en-IN">English (India)</option>
              <option value="hi-IN">हिन्दी (Hindi)</option>
              <option value="en-US">English (US)</option>
            </select>
            <div class="status-pill">
              <span class="pulse-dot"></span>
              <span>Online</span>
            </div>
            <button onclick="stopAllSpeech()" style="background: #f1f5f9; border: 1.5px solid #cbd5e1; color: #475569; border-radius: 8px; padding: 6px 12px; font-weight: 700; font-size: 0.8rem; cursor: pointer;">
              ⏹️ Stop Voice
            </button>
          </div>
        </div>

        <!-- Conversation History Area -->
        <div id="messagesArea" class="messages-area">
          {messages_html}
        </div>

        <!-- Unified Bottom Input -->
        <div class="input-bar">
          <input
            id="chatTextInput"
            type="text"
            class="text-input-field"
            placeholder="Ask anything about farming, crops, pests, or irrigation..."
            onkeydown="handleKeyDown(event)"
          />
          <button id="micBtn" class="btn-mic" onclick="toggleMic()" title="Click to speak hands-free">
            🎙️
          </button>
          <button class="btn-send" onclick="submitChat()">
            <span>Send</span> <span>➤</span>
          </button>
        </div>

        <!-- Status Footer -->
        <div class="status-footer">
          <span id="voiceStatusNotice">⚡ Ready for Voice or Text • Multi-Agent Visual Engine Active</span>
          <span>AgriSense Intelligence</span>
        </div>
      </div>

      <script>
        let isListening = false;
        let recognition = null;
        const headerAvatar = document.getElementById('headerAvatar');
        const headerSubtitle = document.getElementById('headerSubtitle');

        // Auto-scroll to bottom of conversation
        window.addEventListener('load', function() {{
          const area = document.getElementById('messagesArea');
          if (area) {{
            area.scrollTop = area.scrollHeight;
          }}
        }});

        // Speech-to-Text Setup (Web SpeechRecognition)
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          recognition = new SpeechRecognition();
          recognition.continuous = false;
          recognition.interimResults = false;

          recognition.onstart = function() {{
            isListening = true;
            const mic = document.getElementById('micBtn');
            if (mic) {{
              mic.classList.add('listening');
              mic.innerText = '🔴';
            }}
            document.getElementById('chatTextInput').placeholder = '🎙️ Listening to your question...';
            document.getElementById('voiceStatusNotice').innerText = '🎙️ Listening... speak now';
            
            if (headerAvatar) headerAvatar.classList.add('listening-glow');
            if (headerSubtitle) {{
              headerSubtitle.innerHTML = '<span style="color:#ef4444; font-weight:800;">🎙️ Listening to your question...</span>';
            }}
          }};

          recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            document.getElementById('chatTextInput').value = transcript;
            document.getElementById('voiceStatusNotice').innerText = '✅ Recognized: "' + transcript + '"';
            submitChat();
          }};

          recognition.onerror = function(e) {{
            document.getElementById('voiceStatusNotice').innerText = '⚠️ Speech notice: ' + (e.error || 'Check microphone permission');
            resetMic();
          }};

          recognition.onend = function() {{
            resetMic();
          }};
        }}

        function resetMic() {{
          isListening = false;
          const mic = document.getElementById('micBtn');
          if (mic) {{
            mic.classList.remove('listening');
            mic.innerText = '🎙️';
          }}
          if (headerAvatar) headerAvatar.classList.remove('listening-glow');
          document.getElementById('chatTextInput').placeholder = 'Ask anything about farming, crops, pests, or irrigation...';
        }}

        function toggleMic() {{
          if (!recognition) {{
            alert('Web Speech API is not supported in this browser. Please use Chrome/Edge or type your question in the box.');
            return;
          }}
          if (isListening) {{
            recognition.stop();
            resetMic();
          }} else {{
            recognition.lang = document.getElementById('voiceLangSelect').value;
            recognition.start();
          }}
        }}

        function handleKeyDown(e) {{
          if (e.key === 'Enter') {{
            submitChat();
          }}
        }}

        function submitChat() {{
          const textInput = document.getElementById('chatTextInput');
          const val = textInput.value.trim();
          if (!val) return;

          // Trigger AI Thinking Animation on Avatar
          if (headerAvatar) {{
            headerAvatar.classList.remove('listening-glow');
            headerAvatar.classList.add('thinking-glow');
          }}
          if (headerSubtitle) {{
            headerSubtitle.innerHTML = '<span style="color:#059669; font-weight:800;">🤖 AI Agents retrieving evidence & pictures...</span>';
          }}
          document.getElementById('voiceStatusNotice').innerText = '🤖 AI Agents analyzing farming, soil & visual models...';

          // Pass the question to Streamlit parent via hidden receiver
          const parentInputs = window.parent.document.querySelectorAll('input[type="text"]');
          for (let inp of parentInputs) {{
            if (inp.getAttribute('aria-label') === 'unified_query_receiver') {{
              inp.value = val;
              inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
              inp.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
              break;
            }}
          }}
        }}

        function speakFromB64(b64) {{
          try {{
            const decoded = decodeURIComponent(escape(window.atob(b64)));
            speakDirect(decoded);
          }} catch(e) {{
            console.error('TTS error:', e);
          }}
        }}

        function speakDirect(text) {{
          if (!('speechSynthesis' in window)) return;
          window.speechSynthesis.cancel();
          const utt = new SpeechSynthesisUtterance(text);
          utt.lang = document.getElementById('voiceLangSelect').value;
          utt.rate = 1.0;
          document.getElementById('voiceStatusNotice').innerText = '🔊 Reading response aloud...';
          utt.onend = function() {{
            document.getElementById('voiceStatusNotice').innerText = '⚡ Ready for Voice or Text';
          }};
          window.speechSynthesis.speak(utt);
        }}

        function stopAllSpeech() {{
          if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
          }}
          if (recognition && isListening) {{
            recognition.stop();
          }}
          document.getElementById('voiceStatusNotice').innerText = '⏹️ Voice stopped';
          resetMic();
        }}
      </script>
    </body>
    </html>
    """

    components.html(unified_widget_html, height=720)

    # Hidden Streamlit text input receiver for receiving queries from JS
    st.text_input(
        "unified_query_receiver",
        key=f"{key_prefix}_hidden_receiver",
        label_visibility="collapsed",
        on_change=_on_receiver_submit,
        args=(key_prefix, chat_key),
    )


def _on_receiver_submit(key_prefix: str, chat_key: str):
    """Callback when JS passes user query to hidden text receiver."""
    query = st.session_state.get(f"{key_prefix}_hidden_receiver", "").strip()
    if query:
        st.session_state[f"{key_prefix}_hidden_receiver"] = ""
        _process_query(query, chat_key)


def _process_query(user_query: str, chat_key: str):
    """Executes the AI multi-agent workflow and appends response to chat history."""
    if not user_query:
        return

    # Append user question
    st.session_state[chat_key].append(
        {"role": "user", "content": user_query, "agents_status": [], "traces": []}
    )

    # Execute Multi-Agent Plan (with visual image retrieval)
    response = ai_agent.plan_and_execute(
        user_query=user_query,
        farm_context=st.session_state.get("farm_profile", config.DEFAULT_FARM_PROFILE),
    )

    # Extract dynamic agents status
    agents_status = [
        {"name": "🌾 Farming Knowledge / RAG Agent", "status": "Done"},
        {"name": "🌦️ Weather & Agro-Climatic Agent", "status": "Done"},
        {"name": "🌱 Soil Nutrient & Health Agent", "status": "Done"},
        {"name": "📸 Visual Image Dataset Agent", "status": "Done"},
        {"name": "🤖 Agricultural Advisory Agent", "status": "Done"},
    ]

    # Append assistant response with image cards
    st.session_state[chat_key].append(
        {
            "role": "assistant",
            "content": response.get("answer", "Analysis complete."),
            "agents_status": agents_status,
            "traces": response.get("execution_traces", []),
        }
    )
    st.session_state["dash_last_ai_answer"] = response.get("answer", "")
