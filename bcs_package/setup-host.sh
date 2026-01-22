#!/usr/bin/env bash
set -e

VM=bcs-test
wait_for_multipass() {
  local vm="$1"
  echo "==> Waiting for VM SSH to become ready..."
  until multipass exec "$vm" -- true >/dev/null 2>&1; do
    sleep 2
  done
}


echo "==> Creating Multipass VM"
multipass delete $VM --purge 2>/dev/null || true
multipass launch --name $VM --cpus 2 --memory 4G --disk 20G

echo "==> Installing Docker in VM"
multipass exec $VM -- bash -c "
  sudo apt update -qq &&
  sudo apt install -y docker.io docker-compose &&
  sudo usermod -aG docker ubuntu
"

echo "==> Restarting VM to apply docker group"
multipass restart $VM
wait_for_multipass $VM

echo "==> Copying project files"
multipass transfer -r src scripts $VM:/home/ubuntu/

echo "==> Running project setup"
multipass exec $VM -- bash /home/ubuntu/scripts/setup.sh

IP=$(multipass exec $VM -- hostname -I | awk '{print $1}')
echo ""
echo "✅ Setup complete"
echo "BCS Dashboard: http://$IP:8000/dashboard/"

echo "Create your account:"
multipass exec bcs-test -- docker exec -it bcs_web python manage.py createsuperuser
