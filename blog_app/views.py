from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.viewsets import ModelViewSet # ModelViewSet - To automatically get all CRUD operations
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated # Built-in permission class
from .permissions import IsAuthorOrReadOnly # Importing your custom permission
from .forms import PostCreateForm, SignUpForm

# Create your views here.

# Creating a ViewSet for Post - To handle all crud operations in one class
class PostViewSet(ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Only logged-in users can access API
    # Applying multiple permissions
    # IsAuthenticated - Only logged-in users can access
    # IsAuthorOrReadOnly - Only author can edit/delete
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign logged-in user as author
        serializer.save(author=self.request.user)


def home_view(request):
    posts = Post.objects.select_related('author').order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


def blog_detail_view(request, pk):
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
    return render(request, 'blog_detail.html', {'post': post})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('home')
    return render(request, 'signup.html', {'form': form})


@login_required
def create_post_view(request):
    form = PostCreateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, 'Post created successfully.')
        return redirect('blog-detail', pk=post.pk)
    return render(request, 'create_post.html', {'form': form})
