## Server
- Each server components should be interconnected **except Web Management Panel**
    - Posts server **does not listen** via network socket
    - API Server is listened via HTTPS
    - Web Management Panel is listened separately via HTTPS

## `pyposts.PostManager`
- MySQL
    - Amount of database required: 1
        - Tables:
            - Authors
                - Columns:
                    - `title`
                    - `content`
                    - `posted_date`
                    - `last_modified`
                    - `author`
                    - `modified`
                    - `id`
            - Posts