document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const preview = document.getElementById('preview');
    const photoField = document.getElementById('photo_filename');
    const captureBtn = document.getElementById('captureBtn');
    const fileUpload = document.getElementById('fileUpload');

    let streamStarted = false;

    captureBtn.addEventListener('click', async () => {
        if (!streamStarted) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                video.style.display = 'block';
                streamStarted = true;
            } catch (err) {
                alert("Camera not available, please use the file upload below.");
                return;
            }
        } else {
            takePhoto();
        }
    });

    function takePhoto() {
        if (!video.videoWidth || !video.videoHeight) {
            alert("Camera not ready. Please wait a second and try again.");
            return;
        }

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);

        canvas.toBlob(blob => {
            uploadBlob(blob);
        }, 'image/jpeg', 0.9);
    }

    function uploadBlob(blob) {
        const formData = new FormData();
        formData.append('photo', blob, 'photo.jpg');

        fetch('upload_photo.php', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
          .then(filename => {
              photoField.value = filename;
              preview.src = 'uploads/' + filename;
              preview.style.display = 'inline';
          }).catch(err => alert("Upload failed: " + err.message));
    }

    fileUpload.addEventListener('change', () => {
        const file = fileUpload.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('photo', file);

        fetch('upload_photo.php', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
          .then(filename => {
              photoField.value = filename;
              preview.src = 'uploads/' + filename;
              preview.style.display = 'inline';
          }).catch(err => alert("Upload failed: " + err.message));
    });
});
