from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

User = get_user_model()

MAX_TEXT_LENGTH = 50


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='groups',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:MAX_TEXT_LENGTH]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self) -> str:
        return self.text[:MAX_TEXT_LENGTH]


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title[:MAX_TEXT_LENGTH]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_following',
            ),
            models.CheckConstraint(
                # not (user is equal to the value of the following)
                check=~Q(user=F('following')),
                name='prevent_self_follow',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} follows {self.following}'
