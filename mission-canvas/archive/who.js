(function () {
  const query = new URLSearchParams(window.location.search);
  const CONFIG = {
    apiBase: (window.MISSIONCANVAS_CONFIG && window.MISSIONCANVAS_CONFIG.apiBase) || "",
    identityPath: "/v1/missioncanvas/who-are-you",
    backendAgent:
      query.get("backend_agent") ||
      ((window.MISSIONCANVAS_CONFIG && window.MISSIONCANVAS_CONFIG.identityBackendAgent) || "claude.analysis")
  };

  const refs = {
    button: document.getElementById("identitySpeakButton"),
    status: document.getElementById("identityStatus"),
    transcript: document.getElementById("identityTranscript"),
    answer: document.getElementById("identityAnswer"),
    backend: document.getElementById("identityBackend")
  };

  const STATE = {
    listening: false,
    transcript: "",
    recognition: null
  };

  function setStatus(message) {
    if (refs.status) refs.status.textContent = message;
  }

  function setTranscript(text, muted) {
    if (!refs.transcript) return;
    refs.transcript.textContent = text || "Waiting for voice.";
    refs.transcript.classList.toggle("identity-panel-body-muted", Boolean(muted));
  }

  function setAnswer(text) {
    if (refs.answer) refs.answer.textContent = text;
  }

  function setBackend(text, muted) {
    if (!refs.backend) return;
    refs.backend.textContent = text;
    refs.backend.classList.toggle("identity-panel-body-muted", Boolean(muted));
  }

  function speakText(text) {
    if (!text || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1;
    utter.pitch = 1;
    window.speechSynthesis.speak(utter);
  }

  async function askIdentity(question) {
    const res = await fetch(`${CONFIG.apiBase}${CONFIG.identityPath}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question || "Who are you?",
        source: "who.html",
        backend_agent: CONFIG.backendAgent
      })
    });
    if (!res.ok) throw new Error(`identity request failed: ${res.status}`);
    return res.json();
  }

  async function submitQuestion(question) {
    setStatus("Thinking...");
    setTranscript(question, false);

    try {
      const data = await askIdentity(question);
      setAnswer(data.answer || "No answer returned.");
      const channel = data.backend_channel || {};
      const relayText = [
        channel.status ? `relay: ${channel.status}` : "relay unavailable",
        channel.to_agent ? `to ${channel.to_agent}` : "",
        channel.message_id ? `message ${channel.message_id}` : ""
      ].filter(Boolean).join(" · ");
      setBackend(relayText || "No backend relay details.", !relayText);
      setStatus("Answered.");
      speakText(data.answer || "");
    } catch (err) {
      setAnswer("I am Mission Canvas. I translate intent into structured decisions, surface what is known and unknown, and help move work from ambiguity to action.");
      setBackend("Backend request failed. The local voice artifact still answered.", false);
      setStatus("Fallback answer used.");
    }
  }

  function initBrowserSpeech() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      setStatus("Voice unsupported in this browser. The page is ready for Voxtral or browser speech.");
      refs.button.disabled = true;
      return;
    }

    const recognition = new SR();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = true;
    STATE.recognition = recognition;

    let finalText = "";

    recognition.onstart = function () {
      STATE.listening = true;
      refs.button.classList.add("is-listening");
      setStatus("Listening...");
    };

    recognition.onresult = function (event) {
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i += 1) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalText += `${text} `;
        else interim += text;
      }
      STATE.transcript = `${finalText}${interim}`.trim();
      setTranscript(STATE.transcript || "Listening...", false);
    };

    recognition.onerror = function () {
      STATE.listening = false;
      refs.button.classList.remove("is-listening");
      setStatus("Voice error.");
    };

    recognition.onend = async function () {
      STATE.listening = false;
      refs.button.classList.remove("is-listening");
      const question = STATE.transcript || "Who are you?";
      await submitQuestion(question);
    };
  }

  function startVoiceTurn() {
    if (!STATE.recognition) return;
    STATE.transcript = "";
    setTranscript("Listening...", false);
    try {
      STATE.recognition.start();
    } catch (_err) {
      setStatus("Microphone unavailable.");
    }
  }

  function stopVoiceTurn() {
    if (STATE.recognition && STATE.listening) STATE.recognition.stop();
  }

  function init() {
    initBrowserSpeech();
    setBackend(`Ready to relay to ${CONFIG.backendAgent}.`, true);
    if (!refs.button) return;
    refs.button.addEventListener("click", function () {
      if (STATE.listening) stopVoiceTurn();
      else startVoiceTurn();
    });
  }

  init();
})();
