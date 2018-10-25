from django.db import models

# Create your models here.


class UserInfo(models.Model):

    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='username', max_length=32, unique=True)
    password = models.CharField(verbose_name='password', max_length=64)
    nickname = models.CharField(verbose_name='nickname', max_length=32)
    email = models.EmailField(verbose_name='email', unique=True)
    avatar = models.ImageField(verbose_name='photo')

    create_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='fans', to='UserInfo',
                                  through='UserFans', related_name='f', through_fields=('user', 'follower'))


class Blog(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='title', max_length=64)
    site = models.CharField(verbose_name='site', max_length=32, unique=True)
    theme = models.CharField(verbose_name='theme', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid', on_delete=models.DO_NOTHING)


class UserFans(models.Model):
    user = models.ForeignKey(verbose_name='user', to='UserInfo', to_field='nid', related_name='users', on_delete=models.DO_NOTHING)
    follower = models.ForeignKey(verbose_name='follower', to='UserInfo', to_field='nid', related_name='followers', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]


class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    category_title = models.CharField(verbose_name='category_title', max_length=32)
    blog = models.ForeignKey(verbose_name='blog', to='Blog', to_field='nid', on_delete=models.DO_NOTHING)


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='tag_title', max_length=32)
    blog = models.ForeignKey(verbose_name='tag_blog', to='Blog', to_field='nid', on_delete=models.DO_NOTHING)


class ArticleDetail(models.Model):
    content = models.TextField(verbose_name='content')


class UpDown(models.Model):

    article = models.ForeignKey(verbose_name='article', to='Article', to_field='nid', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(verbose_name='user', to='UserInfo', to_field='nid', on_delete=models.DO_NOTHING)
    up = models.BooleanField(verbose_name='is_up')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):

    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='content', max_length=255)
    create_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='reply', to='self', related_name='back', null=True, on_delete=models.DO_NOTHING)
    article = models.ForeignKey(verbose_name='article', to='Article', to_field='nid', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(verbose_name='user', to='UserInfo', to_field='nid', on_delete=models.DO_NOTHING)


class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='article_title', max_length=128)
    summary = models.CharField(verbose_name='article_summary', max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='blog', to='Blog', to_field='nid', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(verbose_name='category', to='Category', to_field='nid', null=True, on_delete=models.DO_NOTHING)

    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "GoLang"),
    ]
    # 1,2,3,4
    article_type_id = models.IntegerField(choices=type_choices, default=None)

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='article', to='Article', to_field='nid', on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(verbose_name='tag', to='Tag', to_field='nid', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


