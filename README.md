# python-smtp-server
Python smtp server

This is a simple smtp server written in python. It is a very simple smtp server that can be used for testing purposes. It is not meant to be used in production.

# Configuration
First of all create a `.env` file in the main directory. The file should contain the following variables:

```
SMTP_HOST=smtp.your_service_host.com
# or 25 or 465
SMTP_PORT=587
SMTP_ADDRESS=your@address.com
SMTP_PASSWORD=your_password
```

# Usage
Simply run these commands:

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```