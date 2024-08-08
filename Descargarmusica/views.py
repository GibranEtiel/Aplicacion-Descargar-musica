from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import yt_dlp
import os
from subprocess import run
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
                'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [lambda d: print(d)],
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                audio_file = os.path.join(temp_dir, 'audio.mp3')
                with open(audio_file, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='audio/mp3')
                    response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
                    return response
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'Descargarmusica/index.html')
