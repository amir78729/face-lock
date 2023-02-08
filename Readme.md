<div align="center">

# Face Detection and Recognition using Neural Network

</div>

## Install Requirements

Required libraries are listed in `requirements.txt` file. You can install all dependencies using this command

```shell
pip install -r requirements.txt
```

## Usage

| Input command | Description          |
|---------------|----------------------|
| `a`           | Add new user         |
| `d`           | Delete existing user |
| `q`, `Esc`    | Quit                 |


```mermaid
graph LR
    
    train(Train Model) --> main
    
    main(Main view) -->|press: a|enter_admin_id_add(Enter ID: Admin)
    enter_admin_id_add --> |enter valid username|enter_password_add(Enter Password)
    enter_password_add --> |enter correct password|enter_name_add(Enter Name)
    enter_name_add --> |enter name for new user|take_pic_add(Take Picture from user)
    take_pic_add --> |save pictures and train model|train
    
    main(Main view) -->|press: d|enter_admin_id_delete(Enter ID: Admin)
    enter_admin_id_delete --> |enter valid username|enter_password_delete(Enter Password)
    enter_password_delete --> |enter correct password|enter_id_delete(Enter ID to Delete)
    enter_id_delete --> |delete user|train
    
    
```