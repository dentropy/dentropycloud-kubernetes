# velero Helper Commands

## Delete Backup Locations

    ``` bash
    kubectl -n velero delete backupstoragelocation.velero.io NAME_OF_BACKUP_LOCATION
    ```

## Perform a restore

    ``` bash
    velero restore create $RESTORE_NAME --from-backup $BACKUP_NAME
    velero restore describe $RESTORE_NAME
    velero restore logs $RESTORE_NAME
    ```