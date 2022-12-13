## Credential Manager in python

## Usage

`credman.py --help`
`credman.py <get | add | delete | update | update-master> <name_of_secret> [--password <password>]`

password parameter is only used for adding or updating a secret
It will always prompt for the master password 

Invoke it like this: `python credman.py get name_of_secret`

In a bash script: `pass=$(python credman.py get name_of_secret)`

It requires a master password - the file is encrypted with this password, so losing it is bad.
You can change the master password, it will re-encrypt the file.

