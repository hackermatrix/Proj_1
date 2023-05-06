from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from django.contrib.auth.models import  AbstractUser
# Create your models here.
class Clients(AbstractUser):
    fav_color = models.CharField(blank=True, max_length=120)
    def __str__(self):
        return self.username

class Websites(models.Model):
    website_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=100)
    subdomains = models.TextField()
    metadata = models.TextField()
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)
    # Add other relevant website fields here

    def __str__(self):
        return self.domain_name
    
class Subdomain(models.Model):
    subdomain_id = models.AutoField(primary_key=True)
    subdomain_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)
    tech_stack = models.JSONField(null=True)
    ip_address = models.CharField(max_length=50,null=True)
    open_ports = models.TextField(null=True)
    directories = models.JSONField(null=True)
    endpoints = models.JSONField(null=True)

    def __str__(self):
        return f"{self.subdomain_id} - {self.domain} "
    
class Zapscan(models.Model):
    endpoint_id = models.AutoField(primary_key=True)
    endpoint_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    vulnerability = models.CharField(max_length=100)
    vulnerable_url = models.CharField(max_length=100)
    param = models.JSONField(max_length=30)
    subdomain_name = models.CharField(max_length=100)
    user =models.ForeignKey(Clients,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subdomain_name} - {self.user}"
    
class Nucleiscan(models.Model):
    endpoint_id = models.AutoField(primary_key=True)
    endpoint_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    vulnerability = models.CharField(max_length=100)
    vulnerable_url = models.CharField(max_length=100)
    subdomain_name = models.CharField(max_length=100)
    user =models.ForeignKey(Clients,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subdomain_name} - {self.user}"


