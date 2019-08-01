# PyPosts

## Navigation
- [**Security**](#security)
- [**Backend**](#backend)
- [**Dependencies**](#dependencies)
- [**Backend Information: `MySQL`**](#backend_information:mysql)

## Security
- Vulnerable HTML Tags Scan and Removal
- File Permission (rw-r--)
- Process run by a standalone user (applicable on unix via systemd)
- GPG authentication to protect post files (content)

## Backend
- **MySQL**
    - Stores post's and user's info
- **Local File Storage**
    - Stores post's content (Export/Archiving)

## Dependencies
- MySQL Backend: `mysql-connector`
- JSON: Python's `JSON`
- Compressing/Archiving: Python's `tarfile`
- XML:
- GPG: `GnuPG` and Python's `python-gnupg`

## Backend Information: `MySQL`
### Database requirements
- Database required: 1
- Table required: 3
    - User's info
        - Columns:
            -
    - Author's info
        - Columns:
            -
    - Post's info
        - Columns:
            - Post's Author
            - Post ID
            - Post Title
            - Posted Date
            - Last Modified Date
            - Modified (`true` or `false`)