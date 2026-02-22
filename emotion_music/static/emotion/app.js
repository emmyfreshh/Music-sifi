import { startWavRecording, stopWavRecording } from "/static/emotion/recorder-wav.js";

const voiceBtn = document.getElementById("voiceBtn");
const statusEl = document.getElementById("status");
const transcriptEl = document.getElementById("transcript");
const emotionEl = document.getElementById("emotion");
const confEl = document.getElementById("confidence");
const modeEl = document.getElementById("mode");
const player = document.getElementById("player");
const playlistEl = document.getElementById("playlist");

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
      // no Web Speech API: just record for ~4 seconds
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

  const tracks = data.tracks || [];
  for (const t of tracks){
    const li = document.createElement("li");
    li.textContent = `${t.title}${t.artist ? " - " + t.artist : ""}`;
    li.onclick = () => { player.src = t.url; player.play(); };
    playlistEl.appendChild(li);
  }

  if (tracks[0]){
    player.src = tracks[0].url;
    player.play();
  }
};