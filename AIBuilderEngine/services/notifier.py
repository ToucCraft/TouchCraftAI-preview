import aiosmtplib
from email.message import EmailMessage
from core.config import settings


async def send_activation_link(user_id: str, user_email: str):
    activation_url = f"{settings.BASE_API_URL}/api/v1/activate-user/{user_id}"

    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = settings.ADMIN_EMAIL
    message["Subject"] = "TouchCraft: New User Activation Request"

    text_content = f"""
    New user registration: {user_email}
    To authorize this user, please visit: {activation_url}
    """

    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <div style="background-color: #0f172a; padding: 24px; text-align: center;">
                <h1 style="color: #3b82f6; margin: 0; font-size: 24px;">TouchCraft Admin</h1>
            </div>
            <div style="padding: 32px; background-color: #ffffff;">
                <h2 style="margin-top: 0; color: #1e293b;">New Access Request</h2>
                <p>A new user has registered and is waiting for your approval to use the platform:</p>
                <div style="background-color: #f1f5f9; padding: 16px; border-radius: 8px; margin-bottom: 24px;">
                    <strong>User Email:</strong> {user_email}
                </div>
                <p>Click the button below to activate this account and grant access to the builder:</p>
                <div style="text-align: center; margin-top: 32px;">
                    <a href="{activation_url}" 
                       style="background-color: #2563eb; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                       Approve User
                    </a>
                </div>
                <p style="font-size: 12px; color: #64748b; margin-top: 32px; text-align: center;">
                    If you don't recognize this user, simply ignore this email. No access will be granted.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    message.set_content(text_content)
    message.add_alternative(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True
        )
    except Exception as e:
        print(f"Failed to send admin email: {str(e)}")


async def send_landing_contact_email(name: str, email: str, message_text: str):
    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = settings.ADMIN_EMAIL
    message["Subject"] = f"🚀 TouchCraft: New Contact Request from {name}"

    text_content = f"""
    New message from TouchCraft Landing Page!

    Name: {name}
    Email: {email}

    Message:
    {message_text}
    """

    html_content = f"""
    <html>
    <body style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; padding: 5px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="background-color: #0f172a; padding: 24px; text-align: center;">
                <h1 style="color: #22d3ee; margin: 0; font-size: 20px;">New Website Inquiry</h1>
            </div>
            <div style="padding: 32px;">
                <div style="margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">From</p>
                    <p style="margin: 4px 0 0 0; font-size: 16px; font-weight: bold; color: #0f172a;">{name}</p>
                    <a href="mailto:{email}" style="color: #3b82f6; text-decoration: none; font-size: 14px;">{email}</a>
                </div>
                <div style="background-color: #f1f5f9; padding: 20px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                    <p style="margin: 0; font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; mb-2;">Message</p>
                    <p style="margin: 8px 0 0 0; color: #334155; white-space: pre-wrap;">{message_text}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    message.set_content(text_content)
    message.add_alternative(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True
        )
    except Exception as e:
        print(f"Failed to send landing contact email: {str(e)}")


async def send_support_email(user_email: str, user_name: str, subject: str, message_text: str, attachments: list = None):
    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = settings.ADMIN_EMAIL
    message["Subject"] = f"🛠️ TouchCraft Support: [{subject}] from {user_name}"

    text_content = f"""
    New support request from TouchCraft Dashboard!

    User: {user_name} ({user_email})
    Type: {subject}

    Message:
    {message_text}
    """

    html_content = f"""
    <html>
    <body style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; background-color: #f8fafc; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="background-color: #0f172a; padding: 24px; text-align: center;">
                <h1 style="color: #22d3ee; margin: 0; font-size: 20px;">New Support Ticket</h1>
            </div>
            <div style="padding: 32px;">
                <div style="margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 12px; color: #64748b; text-transform: uppercase;">From</p>
                    <p style="margin: 4px 0 0 0; font-size: 16px; font-weight: bold; color: #0f172a;">{user_name}</p>
                    <a href="mailto:{user_email}" style="color: #3b82f6; text-decoration: none; font-size: 14px;">{user_email}</a>
                </div>
                <div style="margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 12px; color: #64748b; text-transform: uppercase;">Type</p>
                    <span style="display: inline-block; background-color: #e2e8f0; padding: 4px 8px; border-radius: 4px; font-size: 14px; font-weight: bold; margin-top: 4px;">{subject}</span>
                </div>
                <div style="background-color: #f1f5f9; padding: 20px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                    <p style="margin: 0; font-size: 12px; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">Message</p>
                    <p style="margin: 0; color: #334155; white-space: pre-wrap;">{message_text}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    message.set_content(text_content)
    message.add_alternative(html_content, subtype="html")

    if attachments:
        for att in attachments:
            maintype, subtype = att["content_type"].split("/", 1) if "/" in att["content_type"] else ("application", "octet-stream")
            message.add_attachment(att["content"], maintype=maintype, subtype=subtype, filename=att["filename"])

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True
        )
    except Exception as e:
        print(f"Failed to send support email: {str(e)}")

async def send_approval_email(user_email: str, user_name: str):
    dashboard_url = "https://touchcraftai.com/dashboard"

    message = EmailMessage()
    message["From"] = f"TouchCraft AI <{settings.SMTP_USER}>"
    message["To"] = user_email
    message["Bcc"] = "ivan@touch-craft.com"
    message["Subject"] = "🚀 Welcome to TouchCraft: Your account is ready!"

    text_content = f"""
    Hello, {user_name}
    Your account has been successfully approved. You can now log in and start using the TouchCraft Builder platform.
    Go to Dashboard: {dashboard_url}
    """

    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; padding: 5px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">

            <div style="background-color: #0f172a; padding: 24px; text-align: center;">
                <h1 style="color: #3b82f6; margin: 0; font-size: 24px; font-weight: bold; letter-spacing: 0.5px;">TouchCraft</h1>
            </div>

            <div style="padding: 32px;">
                <h2 style="margin-top: 0; color: #1e293b; font-size: 20px;">Your Access Is Ready!</h2>

                <p style="color: #475569; font-size: 16px; margin-bottom: 24px;">
                    Hello, {user_name}<br><br>
                    Your account has been successfully approved. You can now log in and start using the TouchCraft Builder platform.
                </p>

                <div style="text-align: center; margin: 32px 0;">
                    <a href="{dashboard_url}" 
                       style="background-color: #3b82f6; color: #ffffff; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 16px; font-weight: bold; display: inline-block;">
                        Go to Dashboard
                    </a>
                </div>

                <p style="color: #475569; font-size: 15px; margin-bottom: 24px;">
                    If the button above doesn't work, you can copy and paste the following link into your browser:<br>
                    <a href="{dashboard_url}" style="color: #3b82f6; word-break: break-all;">{dashboard_url}</a>
                </p>

                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 24px 0;">

                <p style="color: #64748b; font-size: 14px; margin: 0;">
                    If you have any questions or need help getting started, feel free to reply to this email. We're here to help!<br><br>
                    Best regards,<br>
                    <strong>The TouchCraft Team</strong>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    message.set_content(text_content)
    message.add_alternative(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True
        )
    except Exception as e:
        print(f"❌ Ошибка при отправке Welcome письма: {str(e)}")
