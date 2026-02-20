(function () {
  'use strict';

  // --- CSS Animations (injected once) ---
  const STYLE_ID = 'oc-voice-animations';
  if (!document.getElementById(STYLE_ID)) {
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
      @keyframes oc-pulse {
        0%   { box-shadow: 0 0 0 0 rgba(192,57,43,0.6); }
        70%  { box-shadow: 0 0 0 10px rgba(192,57,43,0); }
        100% { box-shadow: 0 0 0 0 rgba(192,57,43,0); }
      }
      @keyframes oc-spin {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `;
    document.head.appendChild(style);
  }

  const TRANSCRIBE_URL = location.port === '8443' ? '/transcribe' : 'http://127.0.0.1:18790/transcribe';
  const STORAGE_KEY = 'oc-voice-beep';
  const MODE_KEY = 'oc-voice-mode';
  const LANG_KEY = 'oc-voice-lang';
  let beepEnabled = localStorage.getItem(STORAGE_KEY) !== 'false'; // default: on
  let pttMode = localStorage.getItem(MODE_KEY) !== 'toggle'; // default: PTT

  // --- i18n ---
  const I18N = {
    en: {
      tooltip_ptt: "Hold to talk",
      tooltip_toggle: "Click to start/stop",
      tooltip_next_toggle: "Toggle mode",
      tooltip_next_ptt: "Push-to-Talk",
      tooltip_beep_off: "Disable beep",
      tooltip_beep_on: "Enable beep",
      tooltip_dblclick: "Double-click",
      tooltip_rightclick: "Right-click",
      toast_ptt: "Push-to-Talk",
      toast_toggle: "Toggle mode",
      toast_beep_on: "Beep enabled",
      toast_beep_off: "Beep disabled",
      placeholder_suffix: " \u2014 Voice: (Ctrl+Space Push-To-Talk, Ctrl+Shift+M start/stop continuous recording)"
    },
    de: {
      tooltip_ptt: "Gedr\u00fcckt halten zum Sprechen",
      tooltip_toggle: "Klick zum Starten/Stoppen",
      tooltip_next_toggle: "Klick-Modus",
      tooltip_next_ptt: "Push-to-Talk",
      tooltip_beep_off: "Beep ausschalten",
      tooltip_beep_on: "Beep anschalten",
      tooltip_dblclick: "Doppelklick",
      tooltip_rightclick: "Rechtsklick",
      toast_ptt: "Push-to-Talk",
      toast_toggle: "Klick-Modus",
      toast_beep_on: "Beep aktiviert",
      toast_beep_off: "Beep deaktiviert",
      placeholder_suffix: " \u2014 Sprache: (Strg+Leertaste Push-To-Talk, Strg+Umschalt+M Start/Stop Daueraufnahme)"
    },
    zh: {
      tooltip_ptt: "\u6309\u4f4f\u8bf4\u8bdd",
      tooltip_toggle: "\u70b9\u51fb\u5f00\u59cb/\u505c\u6b62",
      tooltip_next_toggle: "\u70b9\u51fb\u6a21\u5f0f",
      tooltip_next_ptt: "\u6309\u4f4f\u8bf4\u8bdd\u6a21\u5f0f",
      tooltip_beep_off: "\u5173\u95ed\u63d0\u793a\u97f3",
      tooltip_beep_on: "\u5f00\u542f\u63d0\u793a\u97f3",
      tooltip_dblclick: "\u53cc\u51fb",
      tooltip_rightclick: "\u53f3\u952e",
      toast_ptt: "\u6309\u4f4f\u8bf4\u8bdd\u6a21\u5f0f",
      toast_toggle: "\u70b9\u51fb\u6a21\u5f0f",
      toast_beep_on: "\u63d0\u793a\u97f3\u5df2\u5f00\u542f",
      toast_beep_off: "\u63d0\u793a\u97f3\u5df2\u5173\u95ed",
      placeholder_suffix: " \u2014 \u8bed\u97f3\uff1a(Ctrl+\u7a7a\u683c \u6309\u4f4f\u8bf4\u8bdd\uff0cCtrl+Shift+M \u5f00\u59cb/\u505c\u6b62\u8fde\u7eed\u5f55\u97f3)"
    }
  };

  function getLang() {
    const override = localStorage.getItem(LANG_KEY);
    if (override && I18N[override]) return override;
    const nav = (navigator.language || 'en').slice(0, 2);
    return I18N[nav] ? nav : 'en';
  }

  function t(key) {
    return (I18N[getLang()] || I18N.en)[key] || I18N.en[key] || key;
  }
  const MIN_TEXT_CHARS = 2;
  const MIN_CONFIDENCE = 0.15;
  const MAX_NO_SPEECH = 0.95;

  let mediaRecorder = null;
  let audioChunks = [];
  let recording = false;
  let processing = false;
  let starting = false;
  let stream = null;
  let btn = null;
  let observer = null;
  let recordingStartedAt = 0;
  const MIN_RECORDING_MS = 250;
  let analyser = null;
  let audioCtx = null;
  let vuRAF = null;

  const MIC_ICON = `
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M9 8a3 3 0 1 1 6 0v4a3 3 0 1 1 -6 0z" />
      <path d="M5 10v2a7 7 0 0 0 14 0v-2" />
      <path d="M12 19v3" />
      <path d="M8 22h8" />
    </svg>
  `;

  const STOP_ICON = `
    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true">
      <rect x="5" y="5" width="14" height="14" rx="2.5" ry="2.5" />
    </svg>
  `;

  const HOURGLASS_ICON = `
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M7 4h10" />
      <path d="M7 20h10" />
      <path d="M8 4c0 4 4 4 4 8s-4 4-4 8" />
      <path d="M16 4c0 4-4 4-4 8s4 4 4 8" />
    </svg>
  `;

  let toastEl = null;
  let toastTimer = null;
  function showToast(text) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);z-index:100000;background:rgba(20,20,24,.92);color:#fff;border:1px solid rgba(255,255,255,.15);border-radius:8px;padding:8px 16px;font-size:13px;pointer-events:none;opacity:0;transition:opacity .25s;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,.3);';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = text;
    toastEl.style.opacity = '1';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { if (toastEl) toastEl.style.opacity = '0'; }, 1500);
  }

  function getApp() {
    return document.querySelector('openclaw-app');
  }

  function sendMessage(text) {
    const app = getApp();
    if (!app || typeof app.handleSendChat !== 'function') return false;
    app.handleSendChat(text);
    return true;
  }

  function setIdleStyle() {
    if (!btn) return;
    btn.style.background = '#e52b31';
    btn.style.border = '1px solid #d3272f';
    btn.style.color = '#fff';
    btn.style.boxShadow = '0 1px 3px rgba(0,0,0,0.16)';
    btn.style.animation = 'none';
    btn.innerHTML = MIC_ICON;
  }

  function setRecordingStyle() {
    if (!btn) return;
    btn.style.background = '#c0392b';
    btn.style.border = '1px solid #ffffff';
    btn.style.color = '#fff';
    btn.style.boxShadow = '0 0 0 4px rgba(255,255,255,0.16), 0 1px 3px rgba(0,0,0,0.16)';
    btn.style.animation = 'none';
    btn.innerHTML = STOP_ICON;
  }

  function startVU() {
    if (!stream) return;
    try {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioCtx.createMediaStreamSource(stream);
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 256;
      analyser.smoothingTimeConstant = 0.4;
      source.connect(analyser);
      const data = new Uint8Array(analyser.frequencyBinCount);
      function tick() {
        if (!recording || !analyser) return;
        analyser.getByteFrequencyData(data);
        let sum = 0;
        for (let i = 0; i < data.length; i++) sum += data[i];
        const avg = sum / data.length / 255;
        const level = Math.min(1, avg * 3);
        const spread = 4 + level * 22;
        const alpha = 0.2 + level * 0.6;
        if (btn) {
          btn.style.boxShadow = '0 0 0 ' + spread.toFixed(1) + 'px rgba(192,57,43,' + alpha.toFixed(2) + '), 0 1px 3px rgba(0,0,0,0.16)';
          btn.style.transform = 'scale(' + (1 + level * 0.25).toFixed(3) + ')';
        }
        vuRAF = requestAnimationFrame(tick);
      }
      vuRAF = requestAnimationFrame(tick);
    } catch (_) {}
  }

  function stopVU() {
    if (vuRAF) { cancelAnimationFrame(vuRAF); vuRAF = null; }
    if (audioCtx) { try { audioCtx.close(); } catch (_) {} audioCtx = null; }
    analyser = null;
    if (btn) btn.style.transform = 'scale(1)';
  }

  function setProcessingStyle() {
    if (!btn) return;
    btn.style.background = '#d6452f';
    btn.style.border = '1px solid #ffffff';
    btn.style.color = '#fff';
    btn.style.boxShadow = '0 1px 3px rgba(0,0,0,0.16)';
    btn.style.animation = 'none';
    btn.innerHTML = `<span style="display:inline-flex;animation:oc-spin 1.2s linear infinite">${HOURGLASS_ICON}</span>`;
  }

  function styleInline(sendBtn) {
    if (!btn) return;
    const h = Math.round(sendBtn?.getBoundingClientRect?.().height || 52);
    const radius = Math.max(10, Math.round(h * 0.22));
    btn.style.cssText = `
      width:${h}px;height:${h}px;border-radius:${radius}px;
      border:1px solid #d3272f;background:#e52b31;color:#fff;
      display:inline-flex;align-items:center;justify-content:center;
      cursor:pointer;user-select:none;flex:0 0 auto;margin:0 10px;
      box-shadow:0 1px 3px rgba(0,0,0,0.16);transition:all .15s ease;
    `;
  }

  function styleFloating() {
    if (!btn) return;
    btn.style.cssText = `
      position:fixed;bottom:24px;right:24px;z-index:99999;
      width:48px;height:48px;border-radius:50%;
      border:1px solid #d3272f;background:#e52b31;color:#fff;
      display:flex;align-items:center;justify-content:center;
      cursor:pointer;user-select:none;box-shadow:0 2px 8px rgba(0,0,0,.25);
    `;
  }

  let ignoreNextClick = false;
  let pttDown = false;
  let aborted = false;

  function updateButtonTitle() {
    if (!btn) return;
    const mode = pttMode ? t('tooltip_ptt') : t('tooltip_toggle');
    const nextMode = pttMode ? t('tooltip_next_toggle') : t('tooltip_next_ptt');
    const beep = beepEnabled ? t('tooltip_beep_off') : t('tooltip_beep_on');
    btn.title = `🎤 ${mode}\n${t('tooltip_dblclick')}: ${nextMode}\n${t('tooltip_rightclick')}: ${beep}`;
  }

  function switchMode() {
    pttMode = !pttMode;
    localStorage.setItem(MODE_KEY, pttMode ? 'ptt' : 'toggle');
    showToast(pttMode ? t('toast_ptt') : t('toast_toggle'));
    updateButtonTitle();
  }

  function bindButton(el) {
    if (!el || el.dataset.ocVoiceBound === '1') return;
    el.dataset.ocVoiceBound = '1';

    el.addEventListener('pointerdown', (e) => {
      if (e.button !== 0) return;
      e.preventDefault();
      e.stopPropagation();
      if (processing) return;

      if (pttMode) {
        // PTT: hold to record, immediate start
        if (!recording) {
          pttDown = true;
          ignoreNextClick = true;
          starting = true;
          setRecordingStyle();
          startRecording();
        }
      } else {
        // Toggle: pointerdown starts
        if (!recording) {
          ignoreNextClick = true;
          setTimeout(() => { ignoreNextClick = false; }, 500);
          starting = true;
          setRecordingStyle();
          startRecording();
        }
      }
    });

    el.addEventListener('pointerup', (e) => {
      if (e.button !== 0) return;
      if (pttMode && pttDown) {
        pttDown = false;
        ignoreNextClick = true;
        setTimeout(() => { ignoreNextClick = false; }, 300);
        if (recording) stopRecording();
      }
    });

    el.addEventListener('pointerleave', () => {
      if (pttMode && pttDown) {
        pttDown = false;
        if (recording) stopRecording();
      }
    });

    el.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (ignoreNextClick) {
        ignoreNextClick = false;
        return;
      }
      // Toggle mode: click to stop
      if (!pttMode && recording) stopRecording();
    });

    el.addEventListener('dblclick', (e) => {
      e.preventDefault();
      e.stopPropagation();
      pttDown = false;
      // Abort any running recording — flag ensures stop-handler discards audio
      if (recording) {
        aborted = true;
        if (mediaRecorder?.state === 'recording') {
          try { mediaRecorder.stop(); } catch (_) {}
        } else {
          // Recorder already stopped, clean up manually
          aborted = false;
          recording = false;
          mediaRecorder = null;
          audioChunks = [];
          stopVU();
          if (stream) { stream.getTracks().forEach((t) => t.stop()); stream = null; }
          setIdleStyle();
        }
      }
      if (!processing) switchMode();
    });

    el.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      e.stopPropagation();
      beepEnabled = !beepEnabled;
      localStorage.setItem(STORAGE_KEY, beepEnabled ? 'true' : 'false');
      showToast(beepEnabled ? t('toast_beep_on') : t('toast_beep_off'));
      updateButtonTitle();
    });
  }

  function findSendButton() {
    return Array.from(document.querySelectorAll('button')).find((b) => /send/i.test((b.textContent || '').trim()));
  }

  function renderButton() {
    if (!btn) {
      btn = document.createElement('button');
      btn.id = 'oc-voice-btn';
      btn.type = 'button';
      btn.title = '';
      bindButton(btn);
    }

    const sendBtn = findSendButton();
    if (sendBtn && sendBtn.parentElement) {
      styleInline(sendBtn);
      if (btn.parentElement !== sendBtn.parentElement || btn.nextSibling !== sendBtn) {
        btn.remove();
        sendBtn.parentElement.insertBefore(btn, sendBtn);
      }
    } else if (!document.body.contains(btn)) {
      styleFloating();
      document.body.appendChild(btn);
    }

    if (recording) setRecordingStyle();
    else if (processing) setProcessingStyle();
    else setIdleStyle();
    updateButtonTitle();
  }

  async function sendToTranscribe(blob) {
    processing = true;
    setProcessingStyle();
    try {
      const resp = await fetch(TRANSCRIBE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/octet-stream' },
        body: blob,
      });
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      const data = await resp.json();
      const text = (data.text || '').trim();
      const confidence = typeof data.confidence === 'number' ? data.confidence : null;
      const noSpeech = typeof data.no_speech_prob === 'number' ? data.no_speech_prob : null;

      if (!text) return;
      if (text.length < MIN_TEXT_CHARS) return;
      if (confidence !== null && confidence < MIN_CONFIDENCE) return;
      if (noSpeech !== null && noSpeech > MAX_NO_SPEECH) return;

      sendMessage(text);
    } catch (_) {
    } finally {
      processing = false;
      if (!recording) setIdleStyle();
    }
  }

  async function startRecording() {
    if (recording || processing) return;
    try {
      if (stream) {
        stream.getTracks().forEach((t) => t.stop());
        stream = null;
      }

      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];

      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')
          ? 'audio/ogg;codecs=opus' : '';

      mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});

      mediaRecorder.addEventListener('dataavailable', (e) => {
        if (e.data?.size > 0) audioChunks.push(e.data);
      });

      mediaRecorder.addEventListener('stop', () => {
        stopVU();
        if (stream) {
          stream.getTracks().forEach((t) => t.stop());
          stream = null;
        }
        recording = false;
        recordingStartedAt = 0;

        // If aborted (e.g. dblclick mode switch), discard everything
        if (aborted) {
          aborted = false;
          audioChunks = [];
          mediaRecorder = null;
          setIdleStyle();
          return;
        }

        const total = audioChunks.reduce((s, c) => s + c.size, 0);
        if (!audioChunks.length || total < 20) {
          mediaRecorder = null;
          setIdleStyle();
          return;
        }

        const blob = new Blob(audioChunks, { type: mediaRecorder?.mimeType || 'audio/webm' });
        audioChunks = [];
        mediaRecorder = null;
        sendToTranscribe(blob);
      }, { once: true });

      mediaRecorder.addEventListener('start', () => {
        recording = true;
        starting = false;
        recordingStartedAt = Date.now();
        setRecordingStyle();
        startVU();
        if (beepEnabled && audioCtx) {
          try {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.value = 880;
            gain.gain.value = 0.15;
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.08);
          } catch (_) {}
        }
      }, { once: true });
      mediaRecorder.start();
    } catch (_) {
      recording = false;
      starting = false;
      mediaRecorder = null;
      setIdleStyle();
    }
  }

  function stopRecording() {
    if (!recording) return;

    const elapsed = Date.now() - recordingStartedAt;
    if (elapsed < MIN_RECORDING_MS) {
      setTimeout(() => {
        if (recording) stopRecording();
      }, MIN_RECORDING_MS - elapsed);
      return;
    }

    if (mediaRecorder?.state === 'recording') {
      try { mediaRecorder.requestData(); } catch (_) {}
      try { mediaRecorder.stop(); } catch (_) {
        recording = false;
        mediaRecorder = null;
        setIdleStyle();
      }
      return;
    }

    recording = false;
    mediaRecorder = null;
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      stream = null;
    }
    setIdleStyle();
  }

  function toggle() {
    // Self-heal stale state: if UI thinks recording but recorder is gone/stopped
    if (recording && (!mediaRecorder || mediaRecorder.state !== 'recording')) {
      recording = false;
      mediaRecorder = null;
      setIdleStyle();
    }

    if (recording) stopRecording();
    else startRecording();
  }

  // --- Keyboard shortcuts ---
  let spaceDown = false;

  function isTextInput(el) {
    if (!el) return false;
    const tag = el.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return true;
    if (el.isContentEditable) return true;
    return false;
  }

  document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+M → toggle recording
    if (e.ctrlKey && e.shiftKey && e.key === 'M') {
      e.preventDefault();
      toggle();
      return;
    }
    // Ctrl+Space PTT (hold to talk) — works even when text field is focused
    if (e.ctrlKey && !e.shiftKey && e.code === 'Space' && !e.repeat) {
      e.preventDefault();
      e.stopPropagation();
      if (!recording && !processing) {
        spaceDown = true;
        startRecording();
      }
    }
  });

  document.addEventListener('keyup', (e) => {
    if (e.code === 'Space' && spaceDown) {
      e.preventDefault();
      spaceDown = false;
      if (recording) stopRecording();
    }
  });

  function patchPlaceholder() {
    const ta = document.querySelector('textarea');
    if (!ta) return;
    const orig = ta.placeholder || '';
    if (orig && !orig.includes('Ctrl+Space') && !orig.includes('Ctrl+')) {
      ta.placeholder = orig + t('placeholder_suffix');
    }
  }

  function boot() {
    renderButton();
    patchPlaceholder();
    let queued = false;
    observer = new MutationObserver(() => {
      if (recording || processing || starting) return;
      if (queued) return;
      queued = true;
      requestAnimationFrame(() => {
        queued = false;
        renderButton();
        patchPlaceholder();
      });
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(boot, 500));
  } else {
    setTimeout(boot, 500);
  }
})();
