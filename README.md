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

2FA - https://github.com/ronitarv/cyber_security_base_project1/blob/main/app/views.py#L94
Signup - https://github.com/ronitarv/cyber_security_base_project1/blob/main/app/views.py#L105
Brute-force prevention - https://github.com/ronitarv/cyber_security_base_project1/blob/main/mysite/settings.py#L135
Session logout - https://github.com/ronitarv/cyber_security_base_project1/blob/main/mysite/settings.py#L137


Broken Authentication involve basically all factor that might help and attacker access a site with more privilages than given or access an other users account. A big flaw in the application is not using two-factor authentication. Without two-factor authentication attackers can access a users account just by knowing their username and password. A big security risk is also weak passwords, which will ease brute-force attacks. Using short passwords will make guessing random passwords easier and using common passwords will make brute-force from a password list easy. The application also has a flaw where the is not limitation to how many guesses can be made and therefore brute-force is possible in the first place. The application also doesn't log you out automaticly after brower closed or after some time idle. If automatic logout is not implemented, it can result harm in public computers where the user could forget to logout and some stranger could use the application authenticated as the user.

Implementing two-factor authentication can prevent Brute-force attacks and also protect users if theirs passwords are somehow leaked. 2FA can be made in many ways and the most common is to use some kind of code sent or stored to a safe place where the owner can only access. This could be sms, email or an authenticator app. The application implements a code that could be sent somewhere to the owner, however in the project creating many emails just for this or sharing sms doesn't seem like a good idea and therefore if the 2FA is uncommented and tested the code will just appear in the same page as it will need to be inputted.

The signup should include some requirements for passwords. In the application Django UserCreationForm is used with has pretty good requirements for a password and it also makes sure it is not a common password. Brute-force prevention by limiting guess attempts can be made using the axes module. To implement the axes module it needs to be added to project settings.py installed apps, middleware and authetication backends. The number of guesses is set to 3 and the cooldown time in case if the user guesses too many times is 2 hours. Implementing this should prevent guessing by brute-force. Automatic logins will prevent the problem of accidentaly staying authenticated to an application. In the application the user is logged out if the browser is closed and also if the user is idle for certain amount of time which is set to 60 seconds.

The application also has a super user with default username and password of admin: admin. The fix is to either remove the superuser or change the username and password to something stronger.