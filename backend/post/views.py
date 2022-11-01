from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from post.models import Post
from post.permissions import IsOwnerOrReadOnly
from post.serializers import PostSerializer, TogglePostSerializer, NewPostSerializer


class ListCreatePostView(ListCreateAPIView):
    """
        get:
        Get a List of all posts

        Get a List of all posts made by any user.
        Will be listed in chronological order of creation (newest first).

        post:
        Create a new Post

        Create a new Post. The current User will be set as Owner. You can even upload an Image.
        """
    permission_classes = [
        IsAuthenticated
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewPostSerializer
        return PostSerializer

    def get_queryset(self):
        # can be ordered here or in a Meta Class in the model
        return Post.objects.order_by("-created")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListOwnPostView(ListAPIView):
    """
       get:
       Get all posts of the logged-in user

       Get all posts of the current user by passing his access-Token in the header.
       Will be listed in chronological order of creation (newest first).
    """
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class ListUserPostView(ListAPIView):
    """
       get:
       Get all posts of a specific user

       Get all the posts of a user by passing the user-id as a parameter into the URL.
       Will be listed in chronological order of creation (newest first).
    """
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(owner=self.kwargs["userID"])

class ListLikedPostView(ListAPIView):
    """
       get:
       Get all posts the current user liked

       Get all posts that were liked by the logged-in user by passing his token.
    """
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(is_liked_by=self.request.user).distinct()


class RetrieveUpdateDestroyPostView(RetrieveUpdateDestroyAPIView):
    """
       get:
       Get a specific post by id

       Get the content of one post by passing the post-id as a parameter into the URL.

       put:
       Update a specific post by id

       Update the entire content of a specific post. The entire data is required and will be overwritten.
       Only allowed if user is owner of the post or staff.

       patch:
       Update parts of a specific post by id

       Update partial data of a specific post.
       Only allowed if user is owner of the post or staff.

       delete:
       Delete a post by id

       Delete a post by passing the post-id as a parameter into the URL.
       Only allowed if user is owner of the post or staff.
    """
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly
    ]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

class ToggleLikeView(GenericAPIView):
    """
    patch:
    Like / Unlike

    Toggle between "liking" or "not liking" a certain post, by passing the post-id into the url.
    This will add the logged-in users user-id to the post's "is_liked_by" List.
    """
    permission_classes = [
        IsAuthenticated
    ]

    queryset = Post
    serializer_class = PostSerializer
    lookup_url_kwarg = 'postID'

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        user_likes_post = user in post.is_liked_by.all()
        if user_likes_post:
            post.is_liked_by.remove(user)
        else:
            post.is_liked_by.add(user)

        return Response(self.get_serializer(post).data)

