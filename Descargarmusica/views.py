from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import yt_dlp
import os
import tempfile

@csrf_exempt
def download_audio(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'error': 'No URL provided'}, status=400)
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info(url, download=True)
                    title = result.get('title', 'audio').replace("/", "-")
                    audio_file = os.path.join(temp_dir, f'{title}.mp3')

                    with open(audio_file, 'rb') as f:
                        response = HttpResponse(f.read(), content_type='audio/mp3')
                        response['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
                        return response
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'Descargarmusica/index.html')
