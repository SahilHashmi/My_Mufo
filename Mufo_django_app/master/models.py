from django.db import models

class Common(models.Model):
    Name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(max_length=20)
    phone = models.CharField(max_length=15)
    Gender = models.CharField(max_length=20, default='')
    Dob = models.DateField(blank=True,  default='')
    profile_picture = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_voice = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_text = models.CharField(max_length=500, default='')
    Invitation_Code = models.IntegerField(null=True, blank=True)
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.CharField(max_length=50, null=True, blank=True)
    usertype = models.CharField(max_length=50, null=True, blank=True)
    token = models.CharField(max_length=300, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    coins = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return (self.Name)



class Follow1(models.Model):
    user = models.ForeignKey(Common, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(Common, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
