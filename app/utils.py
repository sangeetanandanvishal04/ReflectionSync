from passlib.context import CryptContext
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def generate_otp():
    return str(random.randint(1000, 9999))

def send_email(subject: str, recipient_email: str, html_content: str):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = settings.email
    password = settings.smtp_password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def send_signup_email(recipient_email: str):
    subject = "Welcome — ReflectionSync Floor Plan Management"
    html_content = f"""
    <html>
    <body>
        <h2>Welcome to ReflectionSync Floor Plan Management</h2>
        <p>Hi,</p>
        <p>Thank you for registering with the ReflectionSync Floor Plan Management system.</p>
        <p>With this tool you can:</p>
        <ul>
            <li>Upload and manage floor plans (images/PDF).</li>
            <li>Create and edit rooms and seats as overlays on your floor plans.</li>
            <li>Book meeting rooms and check availability.</li>
            <li>Collaborate with admins to keep layouts up-to-date.</li>
        </ul>
        <p>If you have any questions, contact your admin or reply to this email.</p>
        <p>Best regards,<br/>ReflectionSync Floor Plan Team</p>
        <p style="font-size: small; color: gray;">This is an automated message. Please do not reply to this email.</p>
    </body>
    </html>
    """
    send_email(subject, recipient_email, html_content)

def send_otp_email(recipient_email: str, otp: str):
    subject = "ReflectionSync — Your OTP for Password Reset"
    html_content = f"""
    <html>
    <body>
        <h2>ReflectionSync — Password Reset OTP</h2>
        <p>Hi,</p>
        <p>Your One-Time Password (OTP) to reset your ReflectionSync account password is:</p>
        <h1 style="color: #d9534f;">{otp}</h1>
        <p>This OTP is valid for a short time. If you did not request a password reset, please ignore this email or contact your administrator.</p>
        <p>Best regards,<br/>ReflectionSync Floor Plan Team</p>
        <p style="font-size: small; color: gray;">This is an automated message. Please do not reply to this email.</p>
    </body>
    </html>
    """
    send_email(subject, recipient_email, html_content)