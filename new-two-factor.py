import os  
from dotenv import load_dotenv
import imaplib 
import email
from email.header import decode_header
import re

class Get2FACode:
    def __init__(self) -> None:
        load_dotenv("test.env")
        self.my_email = "test@gmail.com"
        self.key_ = os.getenv("passkey")

    def get_latest_2fa_code(self, start_time):
        try:
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(self.my_email, self.key_)
            imap.select("inbox")

            status, messages = imap.search(None, '(UNSEEN FROM "security-noreply@linkedin.com")')
            if status != "OK":
                raise Exception("Failed to search emails")

            for mail_id in messages[0].split():
                status, mas_data = imap.fetch(mail_id, "(BODY[HEADER.FIELDS (DATE)])")
                if status != "OK":
                    raise Exception("Failed to fetch email headers")

                for response_part in mas_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        local_date = email.utils.mktime_tz(email.utils.parsedate_tz(msg["Date"]))
                        if local_date > start_time:
                            status, msg_data = imap.fetch(mail_id, "(RFC822)")
                            if status != "OK":
                                raise Exception("Failed to fetch full email")

                            for response_part in msg_data:
                                if isinstance(response_part, tuple):
                                    msg = email.message_from_bytes(response_part[1])
                                    subject = decode_header(msg["Subject"])[0][0].decode() if decode_header(msg["Subject"])[0][1] else decode_header(msg["Subject"])[0][0]

                                    for part in msg.walk() if msg.is_multipart() else [msg]:
                                        if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                                            body = part.get_payload(decode=True).decode()
                                            match = re.search(r"\b\d{6}\b", body)
                                            if match:
                                                return match.group(0)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            imap.logout()
