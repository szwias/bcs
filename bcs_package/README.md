## Setup manual
Following manual is for Linux only, sorry Windows users ...
### Installing Multipass
```shell
sudo snap install multipass
```

### Change to right directory
First make sure you're in the right directory in the terminal: `bcs_package/`. 

If not, you can right-click on the `bcs_package` directory (the one the `README.md` is in), 
go to "Properties" and copy the file path. Then in the terminal run this (without the <> brackets):
```shell
cd <here paste copied path>/bcs_package/
```
If you're still not sure, you can run:
```shell
ls
```
You should see something like this:
```shell
README.md  scripts  setup-host.sh  src  start-host.sh  stop.sh
```
### Building app for the first time
In the terminal run:
```shell
bash setup-host.sh
```
When this message shows up:
```text
USING WEB-BASED LOGIN

i Info → To sign in with credentials on the command line, use 'docker login -u <username>'
         

Your one-time device confirmation code is: ZLPJ-WZHG
Press ENTER to open your browser or submit your device code here: https://login.docker.com/activate

Waiting for authentication in the browser…
```
do the following steps:
1. Copy the *"confirmation code"* from your terminal
2. Follow the link: https://login.docker.com/activate
3. Paste the code in "Enter your one-time code*" field
4. Hit "Continue" button
5. Hit "Confirm" button

When this message shows up:
```text
Create your account:
Username (leave blank to use 'root'): 
```
You have enter a new username and password, but you can ignore email by pressing Enter.
### Closing the app
```shell
bash stop.sh
```
### Reopening the app
```shell
bash start-host.sh
```
### Troubleshooting
For now, you can contact me privately through email:
[zwiasszymon@gmail.com](https://mail.google.com/mail/?view=cm&fs=1&to=zwiasszymon@gmail.com)