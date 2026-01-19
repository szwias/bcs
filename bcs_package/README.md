## Project setup manual
### Installing Multipass
If you're on Linux, run this in terminal:
```shell
sudo snap remove multipass
sudo snap install multipass
```
If on Windows install Multipass from website: https://canonical.com/multipass/install

From this point the manual will work both for Windows and Linux.
### Setting up VM
Change directory to bcs_package/ and run those in terminal:
```shell
multipass delete bcs-test --purge 2> /dev/null
multipass launch --name bcs-test --cpus 2 --memory 4G --disk 20G
multipass shell bcs-test
```
```shell
sudo apt update &> /dev/null
sudo apt install -y docker.io docker-compose &> /dev/null
sudo usermod -aG docker ubuntu
```
```shell
exit
```
```shell
multipass restart bcs-test
multipass transfer -r src bcs-test:/home/ubuntu/
multipass shell bcs-test
```
```shell
cd src
docker login
```
### Setting up project
When "USING WEB-BASED LOGIN..." message appears:
1. Copy the 'one-time device confirmation code'
2. Follow the link
3. Paste the code into bracket on the site
4. Press 'Confirm'

Then run those:
```shell
docker pull --platform=linux/amd64 postgres:14
docker pull --platform=linux/amd64 szwias/bcs-web:latest
```
```shell
docker-compose up -d
```
```shell
docker exec -i bcs_db psql -U projectuser -d bcs_db < bcs_dump.sql
docker-compose restart web
echo "http://$(hostname -I | awk '{print $1}'):8000/dashboard/"
```
Follow the link and enjoy!

Bonus:
```shell
docker exec -it bcs_web python manage.py createsuperuser
```
Create your own username and password. Now whenever you get prompted to log in you can use those.

