<div align="center">

# Face Detection and Recognition using Neural Network

</div>

---

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

## Flow

```mermaid
graph 
    train(Train Model) --> main
    
    main(Main view) -->|press: d|admin_authentication_delete(Admin Authentication)
    admin_authentication_delete --> enter_id_delete(Enter ID to Delete)
    enter_id_delete --> train
    
    main(Main view) -->|opening the door|authentication{Authentication}
    authentication --> |Authenticated|door_open(Show Success Message)
    authentication --> |No Face Detected|door_close(Show Error Message)
    authentication --> |Not Authenticated|door_close(Show Error Message)
    door_close --> main
    door_open --> main
    
    main(Main view) -->|press: a|admin_authentication_add(Admin Authentication)
    admin_authentication_add --> enter_name_add(Enter Name)
    enter_name_add --> take_pic_add(Take Picture from user)
    take_pic_add --> train

```

## Admin Panel Dashboard

starting the server:

```shell
cd admin_panel && flask --app server run
```

## Running on Raspberry PI

[documentation](raspberry-pi-instruction.md)