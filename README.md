## Installation:
pip install django-axes[ipware]


flaws are from owasp top 10 2017

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

# Essay

## Injection

https://github.com/ronitarv/cyber_security_base_project1/blob/main/app/views.py#L46

The line holds an SQL query where the user provided parameters are appeneded to the query it self so that SQL injection is possible. In to provided case an attacker can input a malicius input when posting in the post title or content box. When the input is appended to the query like this it is possible for the attacker to  input an SQL query which will fit in the middle of the programs actual query and possibly delete data from tables or reveal confidential information. In the project the following SQL injection would add someones private private content to the current posts content and post it public,
"sometitle', (SELECT content FROM app_post WHERE is_public = False LIMIT 1), True) --"

The Owasp top 10 2017 lists other types of injection also including LDAP, XPath and NoSQL queries, OS commands, XML parsers, SMTP headers, expression languages and ORM queries. However most of these injections are specific to certain mechanisms which aren't even made to the application. ORM query is notable in the fix, but Django shouldn't be vulnerable to it. SMTP headears should be considered if the two-factor authentication was made trought email, where the user input with could be an injection would be the email address.

The SQL query should at least parameterized so that the query is seperated from the user input provided. The simple and also an easier way to do this is to use the Django object-relational mapping layer (ORM). Django ORM uses query parameterization and also escaping of parameters. Some complicated queries might not be possible to do with basic functions and therefore Django provides functions and like raw, extra, a class RawSQL and even direct SQL query. Here it is possible to make the query unsafe, and the user provided input should be escaped by params and not quoting placeholders in SQL string. Howerver in this project the django ORM basic functions are enough and therefore the query should be pretty secure.

## Broken Authentication


Broken Authentication involve basically all factor that might help and attacker access a site with more privilages than given or access an other users account. A big vulnerability in 