## Server
- Each server components should be interconnected **except Web Management Panel**
    - Posts server **does not listen** via network socket
    - API Server is listened via HTTPS
    - Web Management Panel is listened separately via HTTPS

## `pyposts.PostManager`
- MySQL
    - Amount of database required: 1
        - Tables:
            - Posts
                - Columns (name,datatype):
                    - `title`, `TEXT`
                    - `content`, `LONGTEXT`
                    - `posted_date`, `DATETIME`
                    - `last_modified`, `DATETIME`
                    - `author`, `int`
                    - `modified`, `tinyint(1)`, which is a representation of `boolean`
                    - `id`, `int`
            - Authors
                -  Columns (name,datatype):
                    -  `author`, `TEXT`
                    -  `id`, `int`
                    -  `username`, `TEXT`