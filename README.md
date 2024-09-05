# 2FA-Code-Retriever---Gmail

2FA Code Retriever - Gmail版
このPythonスクリプトは、Gmailアカウントを使用して特定の送信者からのメールをチェックし、2段階認証コード（2FAコード）を自動的に取得するためのツールです、
他のサービスにも簡単に適用可能です。

特徴
IMAPプロトコルを使用: Gmailの受信ボックスにアクセスし、メールを取得します。
未読メールをターゲット: 特定の送信者からの未読メールのみを検索します。
2FAコードの抽出: メール本文から6桁の2FAコードを抽出します。
必要条件
Python 3.x
imaplib, email, re, time, dotenv ライブラリ
GoogleアカウントのApp Password

インストール
リポジトリをクローン
```
git clone https://github.com/yourusername/2fa-code-retriever.git
cd 2fa-code-retriever
```
