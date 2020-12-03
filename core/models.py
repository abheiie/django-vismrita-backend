from django.db import models
from accounts.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='posts', null=True, blank = True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.content


class Like(models.Model):
    owner = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return str(self.id)


class Bookmark(models.Model):
    owner = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='bookmarks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    content = models.CharField(max_length=500, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.content

# class ReportType(models.Model):
#     detail=models.CharField(max_length=200, null=True, blank=True)


# class Report(models.Model):
#     reporter = models.ForeignKey(User, related_name='reporters', on_delete=models.CASCADE)
#     report_type = models.ForeignKey(ReportType, related_name='couser_report_types', on_delete=models.CASCADE)
#     post =  models.ForeignKey(Post, related_name='post_posts',
#                              on_delete=models.CASCADE, null = True, blank = True, default = None)
#     couser = models.ForeignKey(Couser, related_name='report_cousers',
#                              on_delete=models.CASCADE, null = True, blank = True, default = None)
#     comment = models.ForeignKey(Comment, related_name='report_comments',
#                              on_delete=models.CASCADE, null = True, blank = True, default = None)
#     entity_type = models.CharField(max_length=40, null=True, blank=True)
#     custome_report = models.CharField(max_length=200, null=True, blank=True)