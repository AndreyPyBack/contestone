from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):     
    if request.method == 'POST':
        user = Post()
        user.name = request.POST['user_name']
        user.content = request.POST['user_text']               
        user.save()        
    context = {
    	'posts': reversed(Post.objects.all())
	}
    
    return render(request, 'guestbook/index.html', context)