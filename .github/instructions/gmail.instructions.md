---
applyTo: 'gmail.py'
description: 'This script connects to Gmail using IMAP, retrieves the most recent email with a specific subject, extracts a verification code from the email, and returns it as a string.'
---
# About

This is a python script that takes a Gmail email and password, and uses IMAP to download the most recent email from the inbox. It should looks for an email with the subject "Your ChatGPT code is" and extract the verification code from the email subject and verify it by checking the body. The script should then return the verification code as a string.

Use Python's built-in `imaplib` library to connect to the Gmail IMAP server, authenticate with the provided email and password, and search for the most recent email with the specified subject. Once the email is found, extract the verification code from the subject and verify it by checking the email body for a matching code. Finally, return the verification code as a string.

Name the file `gmail.py` and place it in the root directory of the project.
