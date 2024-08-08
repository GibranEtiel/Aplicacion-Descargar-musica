document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('youtubeUrl').value;
    const loading = document.getElementById('loading');
    const notification = document.getElementById('notification');

    loading.classList.add('show');
    notification.textContent = '';

    const formData = new FormData();
    formData.append('url', url);

    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Failed to download file');
        }
    })
    .then(blob => {
        loading.classList.remove('show');
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'audio.mp3';
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => {
        loading.classList.remove('show');
        notification.textContent = 'An error occurred: ' + error.message;
    });
});