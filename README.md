## Installation:
pip install django-axes[ipware]

## Injection:
### Vulns:
- SQL Injection posting

### Fixes:
- Using Django ORM



## Broken Authentication:
### Vulns:
- superuser with admin: admin authentication credentials
### Fixes: 
- 2FA
- Brute-Force prevention
- password requirements on sign up



## Broken Access Control:
### Vulns:
- Private posts accessable trough GET parameters
### Fixes:
- Change to POST and validate user in open function




## Security Misconfiguration:
### Vulns:
- Debug = True
- Admin page enabled
- Default superuser admin: admin in app

### Fixes:
- Debug = False
- Disable admin page
- Superuser removed or username changed and password changed to a stronger one



## XSS:
### Vulns:
- XSS when opening post
- XSS when loading selection of viewable posts
### Fixes:
- Change displaying of post, more info in home.html comments
