from django.contrib import admin
from blogs.models import Post, PostComment, PostImage, PostLike, Category, PostSave


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Category)
class UserAdminCategory(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Post)
class UserAdminPost(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    inlines = [PostImageInline]


@admin.register(PostSave)
class UserAdminCategory(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')


@admin.register(PostComment)
class UserAdminPostComment(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text')


@admin.register(PostImage)
class UserAdminPostImage(admin.ModelAdmin):
    list_display = ('id', 'post')


@admin.register(PostLike)
class UserAdminPostLike(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
