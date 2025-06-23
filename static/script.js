const uploadSection = document.getElementById('upload-section');
const cameraSection = document.getElementById('camera-section');
const previewSection = document.getElementById('preview-section');
const resultSection = document.getElementById('result-section');
const mainMenu = document.getElementById('main-menu');

const previewImage = document.getElementById('previewImage');
const predictionText = document.getElementById('prediction');
const confidenceText = document.getElementById('confidence');

let video = document.getElementById('video');
let stream;

function showUpload() {
  // Sembunyikan semua dulu
  mainMenu.style.display = 'none';
  cameraSection.style.display = 'none';
  previewSection.style.display = 'none';
  resultSection.style.display = 'none';

  // Tampilkan upload
  uploadSection.style.display = 'block';
}

function showCamera() {
  // Sembunyikan semua dulu
  mainMenu.style.display = 'none';
  uploadSection.style.display = 'none';
  previewSection.style.display = 'none';
  resultSection.style.display = 'none';

  // Tampilkan kamera
  cameraSection.style.display = 'block';
  startCamera();
}

function goBack() {
  stopCamera();
  uploadSection.style.display = 'none';
  cameraSection.style.display = 'none';
  previewSection.style.display = 'none';
  resultSection.style.display = 'none';
  mainMenu.style.display = 'block';
}

function uploadImage() {
    const fileInput = document.getElementById('uploadInput');
    const file = fileInput.files[0];
    if (!file) return;
  
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = new Image();
      img.onload = function() {
        const canvas = document.getElementById('previewCanvas');
        const ctx = canvas.getContext('2d');
  
        // Bersihkan canvas dan gambar ulang
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, 300, 300);
  
        previewSection.style.display = 'block';
        sendToServer(canvas.toDataURL('image/jpeg'));
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
  

function startCamera() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(s) {
      stream = s;
      video.srcObject = stream;
    })
    .catch(function(err) {
      alert("Gagal mengakses kamera: " + err);
    });
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
}

function capturePhoto() {
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');
  
    // Gambar dari video ke canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, 300, 300);
  
    previewSection.style.display = 'block';
  
    const dataUrl = canvas.toDataURL('image/jpeg');
    sendToServer(dataUrl);
  }
  

function sendToServer(imageData) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ image: imageData })
  })
  .then(response => response.json())
  .then(data => {
    predictionText.textContent = "Penyakit: " + data.prediction;
    confidenceText.textContent = "Confidence: " + data.confidence;
    resultSection.style.display = 'block';
  })
  .catch(error => {
    predictionText.textContent = "Terjadi kesalahan: " + error;
    resultSection.style.display = 'block';
  });
}
