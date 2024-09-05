import email.utils
import os  
from dotenv import load_dotenv
import imaplib 
import email
from email.header import decode_header
import re
import time

class get_2fa_code:
    def __init__(self) -> None:
        load_dotenv("Linkedin.env")
        #自分のmailadress
        self.my_email = "test@gmail.com"
        #GoogleアカウントのApp Passwordの設定URL: https://myaccount.google.com/security-checkup
        self.key_ = os.getenv("passkey")
        pass

    def get_latest_2fa_code(self,start_time):
        #今回はgmailを選択
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(self.my_email, self. key_)
        # どの受信ボックスを選択するか（ここでは「inbox」）
        imap.select("inbox")
        # UNSEENは未読メールを取得。FROMで特定の送信者からのメールを指定
        # messagesはタプル形式で返ってくるので、分解して処理
        status, messages = imap.search(None, '(UNSEEN FROM "security-noreply@linkedin.com")')

        #mail id 取得　
        mail_ids = messages[0].split()
        #最新だけ取得ならfor文ではなくmail_ids[0]を使う
        for mail_id in mail_ids:
            #取得したidからヘッダー部分の中身を検証もし取得できたなら、残りも実行
            status, mas_data = imap.fetch(mail_id, "(BODY[HEADER.FIELDS (DATE)])")
            for response_part in mas_data:
                if isinstance(response_part, tuple):
                    # 「0=メタデータ, 1=メッセージデータ」
                    msg = email.message_from_bytes(response_part[1])
                    date_tuple = email.utils.parsedate_tz(msg["Date"])
                    if date_tuple:
                        local_date = email.utils.mktime_tz(date_tuple)
                        # local_dateがstart_timeより後のメールを処理　お好みで変化可能 
                        if local_date > start_time:
                            #(FRC822) mailの内容全般取得
                            status, msg_data = imap.fetch(mail_id, "(RFC822)")
                            for response_part in msg_data:
                                if isinstance(response_part, tuple):
                                    #メール内容を解析　
                                    msg = email.message_from_bytes(response_part[1])
                                    #件名をデコード decode_subject[0][0]文章中身,[0][1] = 件名のエンコーディング（例: 'utf-8'）
                                    decode_subject = decode_header(msg["Subject"])
                                    subject = decode_subject[0][0]
                                    if decode_subject[0][1]:
                                        subject = subject.decode(decode_subject[0][1])
                                        #! print(f"Decoded Subject: {subject}") バックテスト
                                    if msg.is_multipart():
                                        for part in msg.walk():
                                            content_type = part.get_content_type()
                                            content_disposition = str(part.get("Content-Disposition"))
                                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                                body = part.get_payload(decode=True).decode()
                                                # 左右スペースがある６桁した連続番号取得
                                                match = re.search(r"\b\d{6}\b", body)
                                                if match:
                                                    #! print(match.group(0)) バックテスト

                                                    return match.group(0)
                                    else:
                                        body = msg.get_payload(decode=True).decode()
                                        match = re.search(r"\b\d{6}\b", body)
                                        if match:
                                            #! print(match.group(0))　バックテスト
                                            return match.group(0)
                                                
# *57行、64行の部分を変更すると、このメールから2段階認証コードを取得できます。
