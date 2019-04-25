# LockerRoom 
A very simple player to team mapping application. Create a team, add players get ready for the next seasons beer league hockey team. tyling, schedule, email/sms notifications and beer rotation funtionality coming in future iterations. Enjoy!
### System requirements:
* [Python 2.7](https://www.python.org/download/releases/2.7/) installation is a requirement to run this application. 
* [Git Bash](https://git-scm.com/downloads) (Preferred)
* Oracle VM [Virtual box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Google](https://accounts.google.com/signin/v2/sl/pwd?service=CPanel&flowName=GlifWebSignIn&flowEntry=ServiceLogin) Account
### Configuration:
* VM Configuuation
    * Download or fork from [Github](https://github.com/udacity/fullstack-nanodegree-vm)
    * In command line
        *  Locate vagrant dir 
            * `$cd FSND` 
            * `$cd vagrant`
        * Start Ubuntu 
            * `$vagrant up`
        * Log into VM 
            * `$vagrant ssh`


### Execution
```Last login: Wed Apr  3 01:17:52 2019 from 10.0.2.2
vagrant@vagrant:/vagrant/LockerRoom$ cd
vagrant@vagrant:~$ cd /vagrant/
vagrant@vagrant:/vagrant$ cd LockerRoom/
vagrant@vagrant:/vagrant/LockerRoom$ python AddTeams.py
Added some teams!
vagrant@vagrant:/vagrant/LockerRoom$ python AddPlayers.py                      
Added some players!
vagrant@vagrant:/vagrant/LockerRoom$ python LockerRoomProject.py
 * Serving Flask app "LockerRoomProject" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 313-249-912

```
### Endpoints
* http://localhost:8080
* http://localhost:8080/teams/<int:team_id>/




