import { startWavRecording, stopWavRecording } from "/static/emotion/recorder-wav.js";

const voiceBtn = document.getElementById("voiceBtn");
const statusEl = document.getElementById("status");
const transcriptEl = document.getElementById("transcript");
const emotionEl = document.getElementById("emotion");
const confEl = document.getElementById("confidence");
const modeEl = document.getElementById("mode");
const player = document.getElementById("player");
const playlistEl = document.getElementById("playlist");

const btnPrev = document.getElementById("btnPrev");
const btnNext = document.getElementById("btnNext");
const btnPlay = document.getElementById("btnPlay");
const btnPause = document.getElementById("btnPause");
const btnStop = document.getElementById("btnStop");

let tracksState = [];
let currentIndex = -1;

function startSpeechRecognition(){
  const has = ("SpeechRecognition" in window) || ("webkitSpeechRecognition" in window);
  if (!has) return null;
  const R = window.SpeechRecognition || window.webkitSpeechRecognition;
  const rec = new R();
  rec.lang = "en-US";
  rec.interimResults = false;
  rec.maxAlternatives = 1;
  return rec;
}

function renderPlaylist(){
  playlistEl.innerHTML = "";
  tracksState.forEach((t, idx) => {
    const li = document.createElement("li");
    li.className = "list-group-item bg-black text-light d-flex justify-content-between align-items-center border-secondary";

    const left = document.createElement("div");
    left.innerHTML = `<div class="fw-semibold">${t.title}</div><div class="small text-secondary">${t.artist || ""}</div>`;

    const btn = document.createElement("button");
    btn.className = "btn btn-outline-light btn-sm";
    btn.textContent = "Play";
    btn.onclick = () => playIndex(idx);

    li.onclick = (e) => {
      // clicking the li (not the button) also plays
      if (e.target === btn) return;
      playIndex(idx);
    };

    li.appendChild(left);
    li.appendChild(btn);
    playlistEl.appendChild(li);
  });
}

function playIndex(idx){
  if (!tracksState.length) return;
  if (idx < 0) idx = 0;
  if (idx >= tracksState.length) idx = tracksState.length - 1;

  currentIndex = idx;
  const t = tracksState[currentIndex];
  player.src = t.url;
  player.play();
}

function stopPlayback(){
  player.pause();
  player.currentTime = 0;
}

function nextTrack(){
  if (!tracksState.length) return;
  playIndex((currentIndex + 1) % tracksState.length);
}

function prevTrack(){
  if (!tracksState.length) return;
  const idx = (currentIndex - 1 + tracksState.length) % tracksState.length;
  playIndex(idx);
}

btnPlay.onclick = () => {
  if (player.src) player.play();
  else if (tracksState.length) playIndex(0);
};
btnPause.onclick = () => player.pause();
btnStop.onclick = () => stopPlayback();
btnNext.onclick = () => nextTrack();
btnPrev.onclick = () => prevTrack();

// Auto-next when a track ends
player.addEventListener("ended", () => nextTrack());

voiceBtn.onclick = async () => {
  const rec = startSpeechRecognition();
  let transcript = "";

  transcriptEl.textContent = "-";
  statusEl.textContent = "Listening...";
  emotionEl.textContent = "-";
  confEl.textContent = "-";
  modeEl.textContent = "-";
  playlistEl.innerHTML = "";

  await startWavRecording();

  await new Promise((resolve) => {
    if (!rec){
      setTimeout(resolve, 4000);
      return;
    }
    rec.onresult = (e) => {
      transcript = e.results[0][0].transcript || "";
      transcriptEl.textContent = transcript;
    };
    rec.onerror = () => resolve();
    rec.onend = () => resolve();
    rec.start();
  });

  const wavBlob = await stopWavRecording();
  statusEl.textContent = "Analyzing...";

  const fd = new FormData();
  fd.append("transcript", transcript);
  fd.append("audio", wavBlob, "command.wav");

  const res = await fetch("/api/analyze/", { method: "POST", body: fd });
  const data = await res.json();

  if (data.error){
    statusEl.textContent = "Error";
    transcriptEl.textContent = data.error;
    return;
  }

  statusEl.textContent = "Done";
  transcriptEl.textContent = data.transcript || transcript;
  emotionEl.textContent = data.emotion;
  confEl.textContent = data.confidence;
  modeEl.textContent = data.mode;

  tracksState = data.tracks || [];
  currentIndex = -1;
  renderPlaylist();

  // optional: auto-play first track if available
  if (tracksState.length){
    playIndex(0);
  }
};