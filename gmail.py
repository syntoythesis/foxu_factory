"""
Gmail IMAP module for extracting ChatGPT verification codes.

This module connects to Gmail using IMAP and extracts verification codes
from emails with the subject "Your ChatGPT code is".
"""

import imaplib
import email
from email.header import decode_header
import re


def get_chatgpt_verification_code(gmail_email, gmail_password):
    """
    Connect to Gmail via IMAP and extract the most recent ChatGPT verification code.
    
    Args:
        gmail_email (str): The Gmail email address
        gmail_password (str): The Gmail password or app-specific password
        
    Returns:
        str: The verification code extracted from the email, or None if not found
        
    Raises:
        imaplib.IMAP4.error: If authentication fails or connection issues occur
    """
    imap_server = "imap.gmail.com"
    imap_port = 993
    
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    
    try:
        # Login to the account
        mail.login(gmail_email, gmail_password)
        
        # Select the inbox
        mail.select("inbox")
        
        # Search for emails with the specific subject
        search_criteria = '(SUBJECT "Your ChatGPT code is")'
        status, message_ids = mail.search(None, search_criteria)
        
        if status != "OK" or not message_ids[0]:
            print("No emails found with the specified subject.")
            return None
        
        # Get the list of email IDs and fetch the most recent one
        email_ids = message_ids[0].split()
        latest_email_id = email_ids[-1]  # Get the last (most recent) email
        
        # Fetch the email
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        
        if status != "OK":
            print("Failed to fetch the email.")
            return None
        
        # Parse the email
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        
        # Extract the subject
        subject = email_message["Subject"]
        if subject:
            # Decode the subject if it's encoded
            decoded_subject = decode_header(subject)[0]
            if isinstance(decoded_subject[0], bytes):
                subject = decoded_subject[0].decode(decoded_subject[1] or "utf-8")
            else:
                subject = decoded_subject[0]
        
        # Extract code from subject (e.g., "Your ChatGPT code is 123456")
        subject_match = re.search(r'Your ChatGPT code is (\d+)', subject, re.IGNORECASE)
        if not subject_match:
            print("Could not extract verification code from subject.")
            return None
        
        verification_code = subject_match.group(1)
        
        # Get email body to verify the code
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Get text/plain or text/html parts
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            try:
                body = email_message.get_payload(decode=True).decode()
            except:
                pass
        
        # Verify the code appears in the body
        if verification_code in body:
            print(f"Verification code found and verified: {verification_code}")
            return verification_code
        else:
            print("Warning: Code found in subject but not verified in body.")
            return verification_code
        
    finally:
        # Logout and close the connection
        try:
            mail.logout()
        except:
            pass
    
    return None


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python gmail.py <email> <password>")
        sys.exit(1)
    
    email_address = sys.argv[1]
    password = sys.argv[2]
    
    code = get_chatgpt_verification_code(email_address, password)
    if code:
        print(f"Verification code: {code}")
    else:
        print("Failed to retrieve verification code.")
