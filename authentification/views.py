from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import  CustomUserSerializer,UserProfileSerializer,WebsitesSerializer
from rest_framework import status, permissions,viewsets
from rest_framework.decorators import action
from .models import *
from urllib.parse import urlparse
from django.http import StreamingHttpResponse
import subprocess
import re
import time
import wayback
import subenum
import dirbrute
import tech
import ip_add
import Zap
import Nuclei
import portscan
import json




class HomeView(APIView):
     
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
       return Response(content)
   
class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)

class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserData(viewsets.ViewSet):

    @action(methods=['get'],permission_classes=([IsAuthenticated]),detail=True,url_path='profile',url_name='Get-User-Details')
    def profile(self,request,pk=None):
        user= request.user
        return Response({"username":f"{user}"})
    

    @action(methods=['get'],permission_classes=([IsAuthenticated]),detail=True,url_path='scandata',url_name='Get-User-Scan-Details')
    def dashboard(self,request,pk=None):
        url = request.query_params.get('url')
        url=url.strip()
        user=request.user
        parsed_url = urlparse(url)
        subdomain = parsed_url.netloc

        sub = Subdomain.objects.get(subdomain_name=url, user=user)
        info = sub.tech_stack
        ips = sub.ip_address
        dir_count = len(sub.directories)
        endpt_count = len(sub.endpoints)
        ports = sub.open_ports



        # Vulnerbaility counts according to their severity
        low_count =0
        mid_count =0
        high_count=0

        url = subdomain
        #1.For zap
        zap_scan = Zapscan.objects.filter(subdomain_name=url,user=user)

        zap_all=[{"vuln":res.vulnerability,"severity":res.severity,"vuln_url":res.vulnerable_url}for res in zap_scan]

        for res in zap_scan:
            if(res.severity=='High'):
                high_count+=1
            elif(res.severity=='Medium'):
                mid_count+=1
            elif(res.severity=='Low'):
                low_count+=1

        #2.For Nuclei
        nuclei_scan = Nucleiscan.objects.filter(subdomain_name=url,user=user)

        nuclei_all=[{"vuln":res.vulnerability,"severity":res.severity,"vuln_url":res.vulnerable_url}for res in nuclei_scan]


        for res in nuclei_scan:
            if(res.severity=='high'):
                high_count+=1
            elif(res.severity=='medium'):
                mid_count+=1
            elif(res.severity=='info'):
                low_count+=1

        return Response({"technology": info, "ip": ips,"dir_count":dir_count,"endpt_count":endpt_count ,"ports":ports,"low":low_count,"medium":mid_count,"high":high_count,"zap_out":zap_all,"nuclei_out":nuclei_all})


        

        

class ReconViewSet(viewsets.ViewSet):

    @action(methods=['get'],permission_classes=([IsAuthenticated,]),detail=True,url_path='sub',url_name='Find-Subdomains')
    def subdomains(self,request,pk=None):
        user = request.user

        # get the domain name from the URL query parameter
        domain_name = request.GET.get('url', None)

        if not domain_name:
            return Response({'errors': 'URL parameter not provided.'}, status=400)

        # check if a website with the specified domain_name already exists
        try:
            website = Websites.objects.get(domain_name=domain_name,user=user)
            # website already exists in the database, return its subdomains
           
            out = website.subdomains
            out = out.strip("[").strip("]").replace("\'","").replace("\"","").split(",")[:-1]
            print("already:",type(out))
            return Response({'subdomains':out})
        except Websites.DoesNotExist:
            # website doesn't exist in the database, run the scan_subs() function
            subdomains = subenum.sub_enum(domain_name)
            # save the new website object to the database with the subdomains
            website = Websites.objects.create(
                domain_name=domain_name,
                subdomains=subdomains,
                user=user
            )   
            subdomains = subdomains[:-1]
            print("new:",subdomains)
            return Response({'subdomains': subdomains})


        # url = request.query_params.get('url')
        # subdomains=["one","two","three","four"]
        # # subdomains = subenum.sub_enum(url)
        # return Response({"subdomains":subdomains})
    
    @action(methods=['get'],detail=True,permission_classes=([IsAuthenticated,]),url_path='dir',url_name='Find-Directories')
    def dir(self,request,pk=None):
        time.sleep(3)
        user = request.user
        url = request.query_params.get('url')
        url = url.lstrip(" ")
        domain = urlparse(url).netloc
        domain_name = ('.'.join(domain.split('.')[-2:]))
        mode = int(request.query_params.get('mode'))

        try:
            sub = Subdomain.objects.get(subdomain_name=url,domain=domain_name,user=user)
            out = sub.directories
            # print("THis is the retrived data",type(out))
            # out = out.strip("[").strip("]").replace("\'","").replace("\"","").split(",")[:-1]
            if out is None:
                sub.directories = dirbrute.godir(url,mode)
                sub.save()
            return Response({"directories":out})
        except Subdomain.DoesNotExist:
            dirs = dirbrute.godir(url,mode)
            subdomain = Subdomain.objects.create(
                subdomain_name = url,
                domain = domain_name,
                user = user,
                directories = dirs
            )
            return Response({"directories":dirs})
    

    @action(methods=['get'],detail=True,permission_classes=([IsAuthenticated,]),url_path='techip',url_name='Get-Tech')
    def tech(self,request,pk=None):
        url = request.query_params.get('url')
        url = url.lstrip(" ")
        user = request.user
        domain = urlparse(url).netloc
        domain_name = ('.'.join(domain.split('.')[-2:]))




        try:
            sub = Subdomain.objects.get(subdomain_name=url, domain=domain_name, user=user)
            info = sub.tech_stack
            ips = sub.ip_address
            if info =="null" and ips=="null":
                # If both `tech_stack` and `ip_address` are None, update the object
                sub.tech_stack = tech.get_tech_stack(url)
                sub.ip_address = ip_add.get_ips(url)
                sub.save()
            return Response({"technology": info, "ip": ips})
        except Subdomain.DoesNotExist:
            info = tech.get_tech_stack(url)
            ips = ip_add.get_ips(url)
            # If the object doesn't exist, create a new one with the given values
            sub = Subdomain(subdomain_name=url, domain=domain_name, user=user, tech_stack=info, ip_address=ips)
            sub.save()
            return Response({"technology": info, "ip": ips})


    
    # @action(methods=['post'],detail=True,permission_classes=([IsAuthenticated]),url_path='ip',url_name="Get-Ipaddresses")
    # def getip(self,request,pk=None):
    #     urls = request.data.get('urls')
    #     ips = ip_add.get_ips(urls)
    #     print(urls)
    #     return(Response(ips))
    
    @action(methods=['get'],detail=True,permission_classes=([IsAuthenticated,]),url_path='endpt',url_name="Get-Endpoints")
    def getpt(self,request,pk=None):
        time.sleep(3)
        url = request.query_params.get('url')
        # # count = request.query_params.get('count')
        url = url.strip()
        user = request.user
        domain = urlparse(url).netloc
        domain_name = ('.'.join(domain.split('.')[-2:]))

        try:
            sub = Subdomain.objects.get(subdomain_name=url, domain=domain_name, user=user)
            endpoints = sub.endpoints
            if endpoints ==None:
                # If both `tech_stack` and `ip_address` are None, update the object
                sub.endpoints = wayback.find_endpoints(url)
                sub.save()
            return Response({'endpoints': endpoints})
        except Subdomain.DoesNotExist:
            endpoints = wayback.find_endpoints(url)
            # If the object doesn't exist, create a new one with the given values
            sub = Subdomain(subdomain_name=url, domain=domain_name, user=user,endpoints=endpoints)
            sub.save()
            return Response({'endpoints': endpoints})
        
    
    @action(methods=['get'],detail=True,permission_classes=([IsAuthenticated,]),url_path='port',url_name='Get-OpenPorts')
    def getports(self,request,pk=None):
        time.sleep(3)
        target = request.query_params.get('url')
        target = target.lstrip(" ")
        scan_mode = request.query_params.get('scan_mode',default="quick")
        # cust_ports = request.data.get('custom_ports',default=[])
        user = request.user
        domain = urlparse(target).netloc
        domain_name = ('.'.join(domain.split('.')[-2:]))
        target = domain

        try:
            sub = Subdomain.objects.get(subdomain_name=target, domain=domain_name, user=user)
            open_ports = sub.open_ports
            if open_ports ==None:
                # If both `tech_stack` and `ip_address` are None, update the object
                sub.open_ports = portscan.scan_ports(target,scan_mode=scan_mode)
                sub.save()
            return Response({'open_ports': open_ports})
        except Subdomain.DoesNotExist:
            open_ports = portscan.scan_ports(target,scan_mode=scan_mode)
            # If the object doesn't exist, create a new one with the given values
            sub = Subdomain(subdomain_name=target, domain=domain_name, user=user,open_ports=open_ports)
            sub.save()
            return Response({'open_ports': open_ports})

        

class VulnScanViewSet(viewsets.ViewSet):


    @action(methods=['get'],detail=True,permission_classes=([IsAuthenticated,]),url_path='zap/spider',url_name="Spider")
    def zapspider(self,request,pk=None):
        url = request.query_params.get('url')
        res = Zap.perform_spidering(url)
        return Response({"spider":res})
    
    @action(methods=['get'],detail=True,permission_classes=([IsAuthenticated,]),url_path='zap/active',url_name="Active-scan")
    def zapactive(self,request,pk=None):
        url = request.query_params.get('url')
        user = request.user
        parsed_url = urlparse(url)
        subdomain = parsed_url.netloc
        zap_scan = Zapscan.objects.filter(endpoint_name=url,subdomain_name=subdomain,user=user)
        if(zap_scan.exists()):
            final=[]
            for entry in zap_scan:
                param = entry.param
                vulnerable_url = entry.vulnerable_url
                severity = entry.severity
                vulnerability = entry.vulnerability
                final.append({"endpoint_name":f"{url}","severity":f"{severity}","vulnerability":f"{vulnerability}","vulnerable_url":f"{vulnerable_url}","param":f"{param}","subdomain_name":f"{subdomain}"})
            return Response(final)
            
        else:
            res = Zap.perform_active_scan(url)
            final=[]
            for i in res:
                k = json.dumps(i)
                k = eval(k)
                param = k["param"]
                vulnerable_url = k["url"]
                severity = k["risk"]
                vulnerability = k["name"]
                scan = Zapscan(endpoint_name=url,
                           severity=severity,
                           vulnerability=vulnerability,
                           vulnerable_url=vulnerable_url,
                           param=param,
                           subdomain_name=subdomain,
                           user = user)
                scan.save()
                final.append({"endpoint_name":f"{url}","severity":f"{severity}","vulnerability":f"{vulnerability}","vulnerable_url":f"{vulnerable_url}","param":f"{param}","subdomain_name":f"{subdomain}"})
            return Response(final)


    
    @action(methods=['get'],detail=True,permission_classes=([IsAuthenticated,]),url_path='nuclei',url_name="Nuclei-scan")
    def nuclei(self,request,pk=None):
        url = request.query_params.get('url')  # Get URL parameter from request
        user = request.user
        parsed_url = urlparse(url)
        subdomain = parsed_url.netloc

        
        response = Nuclei.start_nuclei_scan(url,subdomain,user)
        # response = Response("HI AKASH!!!!!!!!!!!!!")
        print(f"RESPONSE:{response}")
        return response

