const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const preview = document.getElementById('preview');
const photoField = document.getElementById('photo_filename');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error("Camera error:", err));

function takePhoto() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('photo', blob);

        fetch('upload_photo.php', {
            method: 'POST',
            body: formData
        }).then(res => res.text()).then(filename => {
            photoField.value = filename;
            preview.src = 'uploads/' + filename;
            preview.style.display = 'inline';
        });
    }, 'image/jpeg');
}
