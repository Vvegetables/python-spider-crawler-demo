'''
发送邮件
问题
在web.py中，如何发送邮件？

解法
在web.py中使用web.sendmail()发送邮件.
'''

web.sendmail('cookbook@webpy.org', 'user@example.com', 'subject', 'message')
#如果在web.config中指定了邮件服务器，就会使用该服务器发送邮件，否则，就根据/usr/lib/sendmail中的设置发送邮件。

web.config.smtp_server = 'mail.mydomain.com'
#如果要发送邮件给多个收件人，就给to_address赋值一个邮箱列表。

web.sendmail('cookbook@webpy.org', ['user1@example.com', 'user2@example.com'], 'subject', 'message')
#cc和bcc关键字参数是可选的，分别表示抄送和暗送接收人。这两个参数也可以是列表，表示抄送/暗送多人。

web.sendmail('cookbook@webpy.org', 'user@example.com', 'subject', 'message', cc='user1@example.com', bcc='user2@example.com')
#headers参数是一个元组，表示附加标头信息(Addition headers)

web.sendmail('cookbook@webpy.org', 'user@example.com', 'subject', 'message',
        cc='user1@example.com', bcc='user2@example.com',
        headers=({'User-Agent': 'webpy.sendmail', 'X-Mailer': 'webpy.sendmail',})
        )