import smtplib
import ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "amir78729@gmail.com"  # Enter your address
receiver_email = "amirhosseinalibakhshi@gmail.com"  # Enter receiver address
password = 'amir13780729'
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)