from django.db import models


POST_TYPE_A = "typea"
POST_TYPE_B = "typeb"
POST_TYPES = (
   (POST_TYPE_A, "Post Type A"),
   (POST_TYPE_B, "Post Type B"),
)


class AuditFields(models.Model):
    """
    Defines abstract model for adding some basic audit fields. 
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    preformed_by = models.ForeignKey('auth.User', blank=True, null=True, 
        help_text="Username of who created this object.")
    ipaddress = models.CharField(max_length=32, blank=True, null=True,
        help_text="IP of who created this object. ")

    class Meta:
        abstract = True


class PostTag(models.Model):
    """
    Tag model to demo ManyToMany relationship with Post.  
    We will assume that this table could get fairly large as
    people tag posts. 
    """
    name = models.CharField(max_length=24)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Post Tag'
        verbose_name_plural = 'Post Tags'


class PostCategory(models.Model):
    """
    Category model to demo ManyToMany relationship with Post.  
    For this demo, we assume that category will remain 
    relatively small as only Admins will add categories. 
    """ 
    name = models.CharField(max_length=24)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Post Category'
        verbose_name_plural = 'Post Categories'


class Post(AuditFields, models.Model):
  
    """
    This example uses a Blog Post as the core model
    that we will demo with.  
    """

    title = models.CharField(max_length=64) 
    type = models.CharField(choices=POST_TYPES, max_length=10)
    message = models.TextField() 
    featured = models.BooleanField(default=False,
        help_text="Is the Post Featured on main page. ")
    tags = models.ManyToManyField('a.PostTag', blank=True, null=True)
    category = models.ManyToManyField('a.PostCategory', blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.title)



