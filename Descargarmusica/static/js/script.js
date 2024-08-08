document.getElementById('downloadForm').onsubmit = function() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('notification').innerText = '';
    
    fetch('', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(new FormData(this))
    })
    .then(response => {
        document.getElementById('loading').style.display = 'none';
        if (response.ok) {
            response.blob().then(blob => {
                const contentDisposition = response.headers.get('Content-Disposition');
                const filename = contentDisposition.split('filename=')[1].replace(/"/g, '');
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.getElementById('notification').innerText = 'Descarga completa';
            });
        } else {
            response.json().then(data => {
                document.getElementById('notification').innerText = `Error: ${data.error}`;
            });
        }
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('notification').innerText = `Error: ${error}`;
    });

    return false;  // prevent form from submitting the default way
};
