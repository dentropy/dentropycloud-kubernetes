echo "Please enter name of backup"
read backup_name
echo "Creating backup named $backup_name"
velero backup create $backup_name
echo "Done creating backup $backup_name"
