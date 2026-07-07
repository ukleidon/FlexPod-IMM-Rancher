echo "Setting up Tenant test01" 
echo "Phase 1:  Nexus configuration" 
ansible-playbook -i inventory -i inventory-test01 TENANT.yml --tags=nexus_config
echo "Sleep for 60 seconds"
sleep 60

echo "Phase 2:  Ontap configuration" 
ansible-playbook -i inventory -i inventory-test01 TENANT.yml --tags=ontap_config
echo "Sleep for 60 seconds"
sleep 60

echo "Phase 3:  UCS configuration" 
ansible-playbook -i inventory -i inventory-test01 TENANT.yml --tags=ucs_config
echo "Sleep for 60 seconds"
sleep 60

echo "Phase 4:  OS Installation" 
ansible-playbook -i inventory -i inventory-test01 TENANT.yml --tags=os_install
echo "Sleep for 60 seconds"
sleep 60

echo "Phase 5:  RKE2 Installation" 
ansible-playbook -i inventory -i inventory-test01 TENANT.yml --tags=rke_install

echo "Installation of Tenant test01 is finished"
