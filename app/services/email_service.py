from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.core.config import settings

# Configure FastMail using our application settings
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)

fm = FastMail(conf)

class EmailService:
    @staticmethod
    async def send_reset_password_email(email_to: EmailStr, magic_link: str):
        """
        Constructs and sends the password reset email.
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 40px 0;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f7f6;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin: 0 auto; max-width: 600px;">
                            
                            <!-- Header / Logo -->
                            <tr>
                                <td align="center" style="padding: 30px 40px; border-bottom: 1px solid #f0f0f0;">
                                    <span style="font-size: 28px; font-weight: 800; color: #000000; letter-spacing: 2px;">
                                        DRONEX<span style="color: #ff6600;">.</span>
                                    </span>
                                </td>
                            </tr>
                            
                            <!-- Main Content -->
                            <tr>
                                <td style="padding: 40px; color: #333333; line-height: 1.6; font-size: 16px;">
                                    <h2 style="margin-top: 0; color: #111111; font-size: 22px;">Password Reset Request</h2>
                                    <p>Hello,</p>
                                    <p>We received a request to reset the password for your DRONEX account. Click the button below to securely set a new password. For security reasons, this link will expire in <strong>5 minutes</strong>.</p>
                                    
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 35px 0;">
                                        <tr>
                                            <td align="center">
                                                <a href="{magic_link}" style="display: inline-block; padding: 14px 32px; background-color: #000000; color: #ffffff; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 16px; letter-spacing: 1px;">Reset Password</a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p>If you didn't request a password reset, you can safely ignore this email. Your account remains completely secure.</p>
                                    <p style="margin-bottom: 0;">Best regards,<br><strong>The DRONEX Team</strong></p>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td align="center" style="padding: 20px 40px; background-color: #f9f9f9; color: #888888; font-size: 12px; border-top: 1px solid #eeeeee;">
                                    &copy; 2026 DRONEX. All rights reserved.<br>
                                    Please do not reply to this automated message.
                                </td>
                            </tr>
                            
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        message = MessageSchema(
            subject="Password Reset Instructions",
            recipients=[email_to],
            body=html_content,
            subtype=MessageType.html
        )

        # Send the email!
        await fm.send_message(message)
