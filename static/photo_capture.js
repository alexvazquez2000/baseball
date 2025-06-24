document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const preview = document.getElementById("preview");
    const photoField = document.getElementById("photo_filename");
    const captureBtn = document.getElementById("captureBtn");
    const fileUpload = document.getElementById("fileUpload");

    let streamStarted = false;

    captureBtn.addEventListener("click", async () => {
        if (!streamStarted) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                video.style.display = "block";
                streamStarted = true;
                captureBtn.textContent = "Take Photo";
            } catch (err) {
                alert("Camera not available, please use the file upload option.");
            }
        } else {
            takePhoto();
        }
    });

    function takePhoto() {
        if (!video.videoWidth || !video.videoHeight) {
            alert("Camera not ready. Try again in a moment.");
            return;
        }
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            if (!blob) {
                alert("Error capturing photo. Try again.");
                return;
            }
            const formData = new FormData();
            formData.append("photo", blob, "photo.png");

            fetch("/upload_photo", {
                method: "POST",
                body: formData
            })
            .then(response => response.text())
            .then(filename => {
                photoField.value = filename;
                preview.src = `/uploads/${filename}`;
                preview.style.display = "inline";
            })
            .catch(error => alert("Upload failed: " + error.message));
        }, "image/png");
    }

    fileUpload.addEventListener("change", async () => {
        const file = fileUpload.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("photo", file);

        fetch("/upload_photo", {
            method: "POST",
            body: formData
        })
        .then(response => response.text())
        .then(filename => {
            photoField.value = filename;
            preview.src = `/uploads/${filename}`;
            preview.style.display = "inline";
        })
        .catch(error => alert("Upload failed: " + error.message));
    });
});
