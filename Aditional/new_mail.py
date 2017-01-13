import smtplib

gmail_user = 'cristi26.gabor@gmail.com'
gmail_password = 'k3blinuxmint_26'

fro = gmail_user
to = ['cristi26_gabor@yahoo.com']
subject = 'OMG Super Important Message'
body = "Hey, what's up?\n\n- You "

email_text = """n\
From: %s
To: %s
Subject: %s

%s
""" % (fro, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(from, to, email_text)
    server.close()

    print('Email sent!')
except:
    print('Something went wrong...')
