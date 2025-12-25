# vm_setup.sh
git add .
git commit -m "fix(docker): attempt at getting image to work on vm"
git push deploy deploy

multipass delete my-ubuntu
multipass purge
multipass launch --name my-ubuntu --disk 30G --memory 4G --cpus 2
multipass shell my-ubuntu

# dep_install.sh
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

sudo mkdir -m -0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER
#newgrp docker
sudo docker --version
sudo docker compose version

git clone https://github.com/szwias/bcs.git
cd bcs
git checkout deploy

# Add secrets
vim .env

# build.sh
sudo docker compose up --build -d
sudo docker compose logs -f django-web

sudo docker compose exec django-web python manage.py migrate --fake
sudo docker compose exec django-web python manage.py createsuperuser
sudo docker compose exec django-web python manage.py collectstatic --noinput

# run.sh
sudo docker compose exec django-web python manage.py shell
sudo docker compose ps
echo "http://localhost:8001"
