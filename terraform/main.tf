terraform {
	required_providers {
		yandex = {
			source = "yandex-cloud/yandex"
		}
	}
}

provider "yandex" {
	service_account_key_file = var.sa_key_file
	cloud_id                 = var.cloud_id
    folder_id                = var.folder_id
    zone                     = var.zone
}

resource "yandex_compute_instance" "vm" {
	name = "my-first-vm"

	metadata = {
	  ssh-keys = "ubuntu:${file(var.ssh_pub_key)}"
	  user-data = "#cloud-config\nusers:\n  - name: ubuntu\n    sudo: ALL=(ALL) NOPASSWD:ALL\n    ssh_authorized_keys:\n      - ${file(var.ssh_pub_key)}"
	}

	resources {
		cores  = 2
		memory = 2
	}

	boot_disk {
		initialize_params {
			image_id = "fd817i7o8012578061ra"
		}
	}

	network_interface {
		subnet_id = var.subnet_id
		nat       = true
	}
}

resource "null_resource" "ansible" {
  depends_on = [yandex_compute_instance.vm]

  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i '${yandex_compute_instance.vm.network_interface[0].nat_ip_address},' -u ubuntu --private-key ~/.ssh/yc_key ~/homelab/ansible/cloud-playbook.yml"
  }
}
