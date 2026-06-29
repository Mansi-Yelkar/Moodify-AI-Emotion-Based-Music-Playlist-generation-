let stream = null;
let isRecording = false;
let audioContext = null;
let scriptProcessor = null;
let audioInput = null;
let recordingBuffer = [];
let recordingLength = 0;

function hideAll() {
    document.getElementById('webcam-container').classList.add('hidden');
    document.getElementById('text-container').classList.add('hidden');
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('result-container').classList.add('hidden');
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

function showLoading() {
    hideAll();
    document.getElementById('loading').classList.remove('hidden');
}

function showResult(emotion) {
    hideAll();
    document.getElementById('detected-emotion').innerText = emotion;
    document.getElementById('result-container').classList.remove('hidden');
}

async function startWebcam() {
    hideAll();
    const container = document.getElementById('webcam-container');
    const video = document.getElementById('video-preview');
    container.classList.remove('hidden');
    
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        alert("Could not access webcam: " + err.message);
    }
}

function captureImage() {
    const video = document.getElementById('video-preview');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const dataUrl = canvas.toDataURL('image/jpeg');
    
    showLoading();
    
    fetch('/api/emotion/face', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataUrl })
    })
    .then(res => res.json())
    .then(data => {
        if(data.error) alert(data.error);
        else showResult(data.emotion);
    })
    .catch(err => {
        alert("Error analyzing image");
        hideAll();
    });
}

function showTextInput() {
    hideAll();
    document.getElementById('text-container').classList.remove('hidden');
}

function submitText() {
    const text = document.getElementById('emotion-text').value;
    if (!text) return;
    
    showLoading();
    
    fetch('/api/emotion/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(data => {
        if(data.error) alert(data.error);
        else showResult(data.emotion);
    });
}

async function toggleRecording() {
    const btn = document.getElementById('btn-record');
    
    if (!isRecording) {
        hideAll();
        recordingBuffer = [];
        recordingLength = 0;
        try {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            audioInput = audioContext.createMediaStreamSource(stream);
            
            // Create a ScriptProcessorNode with bufferSize = 4096, 1 input channel, 1 output channel
            scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
            
            scriptProcessor.onaudioprocess = function(e) {
                if (!isRecording) return;
                const input = e.inputBuffer.getChannelData(0);
                recordingBuffer.push(new Float32Array(input));
                recordingLength += input.length;
            };
            
            audioInput.connect(scriptProcessor);
            scriptProcessor.connect(audioContext.destination);
            
            isRecording = true;
            btn.innerText = "Stop Recording";
            btn.style.backgroundColor = "#ef4444";
        } catch (err) {
            alert("Could not access microphone: " + err.message);
        }
    } else {
        isRecording = false;
        btn.innerText = "Record";
        btn.style.backgroundColor = "";
        
        // Disconnect and stop tracks
        if (scriptProcessor) {
            scriptProcessor.disconnect();
        }
        if (audioInput) {
            audioInput.disconnect();
        }
        if (audioContext) {
            audioContext.close();
        }
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        
        // Process and send the recorded WAV
        sendAudio();
    }
}

function sendAudio() {
    if (recordingLength === 0) {
        alert("No audio recorded.");
        return;
    }
    
    showLoading();
    
    // Merge buffers
    const mergedBuffer = new Float32Array(recordingLength);
    let offset = 0;
    for (let i = 0; i < recordingBuffer.length; i++) {
        mergedBuffer.set(recordingBuffer[i], offset);
        offset += recordingBuffer[i].length;
    }
    
    // Encode as 16-bit PCM Mono WAV
    const sampleRate = audioContext ? audioContext.sampleRate : 44100;
    const wavBlob = encodeWAV(mergedBuffer, sampleRate);
    
    const formData = new FormData();
    formData.append('audio', wavBlob, 'recording.wav');
    
    fetch('/api/emotion/audio', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if(data.error) alert(data.error);
        else showResult(data.emotion);
    })
    .catch(err => {
        alert("Error analyzing audio");
        hideAll();
    });
}

function generatePlaylist() {
    const emotion = document.getElementById('detected-emotion').innerText;
    window.location.href = "/playlist?emotion=" + encodeURIComponent(emotion);
}

function encodeWAV(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);
    
    /* RIFF identifier */
    writeString(view, 0, 'RIFF');
    /* file length */
    view.setUint32(4, 36 + samples.length * 2, true);
    /* RIFF type */
    writeString(view, 8, 'WAVE');
    /* format chunk identifier */
    writeString(view, 12, 'fmt ');
    /* format chunk length */
    view.setUint32(16, 16, true);
    /* sample format (raw) */
    view.setUint16(20, 1, true);
    /* channel count */
    view.setUint16(22, 1, true);
    /* sample rate */
    view.setUint32(24, sampleRate, true);
    /* byte rate (sample rate * block align) */
    view.setUint32(28, sampleRate * 2, true);
    /* block align (channel count * bytes per sample) */
    view.setUint16(32, 2, true);
    /* bits per sample */
    view.setUint16(34, 16, true);
    /* data chunk identifier */
    writeString(view, 36, 'data');
    /* data chunk length */
    view.setUint32(40, samples.length * 2, true);
    
    floatTo16BitPCM(view, 44, samples);
    
    return new Blob([view], { type: 'audio/wav' });
}

function floatTo16BitPCM(output, offset, input) {
    for (let i = 0; i < input.length; i++, offset += 2) {
        let s = Math.max(-1, Math.min(1, input[i]));
        output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
}

function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}
