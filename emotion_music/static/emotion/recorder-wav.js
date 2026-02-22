let audioCtx, stream, source, processor;
let recording = false;
let pcmChunks = [];
let inputSampleRate = 48000;

export async function startWavRecording(){
  stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  inputSampleRate = audioCtx.sampleRate;

  source = audioCtx.createMediaStreamSource(stream);
  processor = audioCtx.createScriptProcessor(4096, 1, 1);

  pcmChunks = [];
  recording = true;

  processor.onaudioprocess = (e) => {
    if (!recording) return;
    const input = e.inputBuffer.getChannelData(0);
    pcmChunks.push(new Float32Array(input));
  };

  source.connect(processor);
  processor.connect(audioCtx.destination);
}

export async function stopWavRecording(){
  recording = false;

  if (processor) processor.disconnect();
  if (source) source.disconnect();
  if (stream) stream.getTracks().forEach(t => t.stop());
  if (audioCtx) await audioCtx.close();

  const merged = mergeFloat32(pcmChunks);
  const down = downsample(merged, inputSampleRate, 16000);
  const wav = encodeWavMono16(down, 16000);
  return new Blob([wav], { type: "audio/wav" });
}

function mergeFloat32(chunks){
  let len = 0; for (const c of chunks) len += c.length;
  const out = new Float32Array(len);
  let off = 0;
  for (const c of chunks){ out.set(c, off); off += c.length; }
  return out;
}

function downsample(buf, inRate, outRate){
  if (inRate === outRate) return buf;
  const ratio = inRate / outRate;
  const newLen = Math.round(buf.length / ratio);
  const out = new Float32Array(newLen);
  let o = 0, i = 0;
  while (o < out.length){
    const nextI = Math.round((o + 1) * ratio);
    let sum = 0, count = 0;
    for (; i < nextI && i < buf.length; i++){ sum += buf[i]; count++; }
    out[o] = count ? sum / count : 0;
    o++;
  }
  return out;
}

function floatTo16PCM(float32){
  const out = new Int16Array(float32.length);
  for (let i=0;i<float32.length;i++){
    let s = Math.max(-1, Math.min(1, float32[i]));
    out[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
  }
  return out;
}

function encodeWavMono16(float32, sr){
  const pcm16 = floatTo16PCM(float32);
  const dataSize = pcm16.length * 2;
  const buf = new ArrayBuffer(44 + dataSize);
  const view = new DataView(buf);

  writeStr(view, 0, "RIFF");
  view.setUint32(4, 36 + dataSize, true);
  writeStr(view, 8, "WAVE");
  writeStr(view, 12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sr, true);
  view.setUint32(28, sr * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeStr(view, 36, "data");
  view.setUint32(40, dataSize, true);

  let off = 44;
  for (let i=0;i<pcm16.length;i++, off+=2){
    view.setInt16(off, pcm16[i], true);
  }
  return buf;
}

function writeStr(view, off, s){
  for (let i=0;i<s.length;i++) view.setUint8(off+i, s.charCodeAt(i));
}