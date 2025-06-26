document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const preview = document.getElementById("preview");
    const captureBtn = document.getElementById("captureBtn");
    const fileUpload = document.querySelector("input[name='photo']");
    const form = document.querySelector("form");
    const csrfToken = form.querySelector("input[name='csrf_token']").value;

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
                alert("Camera not available. Use the file upload option.");
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

            // Replace the camera stream with a Blob in the hidden field
            const fileInput = new File([blob], "photo.png", { type: "image/png" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(fileInput);
            fileUpload.files = dataTransfer.files;

            // Show the preview
            preview.src = URL.createObjectURL(blob);
            preview.style.display = "inline";
        }, "image/png", 0.95);
    }
});
