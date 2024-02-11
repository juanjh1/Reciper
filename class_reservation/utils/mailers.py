import logging
from typing import Dict
import os
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)


def send(
    subject: str,
    from_email: str,
    to_email: list,
    txt_path: str,
    ctx: Dict[str, str],
    html_path=None,
):
    """Email engine that processes sending of mails

    parameters:
    ===========
    subject     <str>
        Email Subject/Header

    txt_path    <str>
        Path to where email content is located

    from_email  <str>
        Sender of the mail

    to_email    <list>
        A list of email addresses to send the given message to

    html_path   <str>
        An html markup with same content as the body. Only difference is this
        content can be styled to taste.
    """
    body = render_to_string(txt_path, ctx)
    msg = EmailMultiAlternatives(subject, body, from_email, to_email)

    if html_path:
        html = render_to_string(html_path, ctx)
        msg.attach_alternative(html, "text/html")

    try:
        msg.send()
    except Exception as e:
        logger.exception(f"Error encountered while sending mail.\n{e}")


def email_client(
    subject: str, body: str, to_email: str, ctx: Dict[str, str], html=None
):
    """This sends transactional emails to clients"""
    send(
        ctx=ctx,
        txt_path=body,
        html_path=html,
        subject=subject,
        to_email=to_email,
        from_email=os.environ.get("DEFAULT_FROM_EMAIL"),
    )


def email_admin(
    subject: str,
    body: str,
    ctx: Dict[str, str],
    html=None,
):
    """Sends client's email to admins"""
    send(
        ctx=ctx,
        txt_path=body,
        html_path=html,
        subject=subject,
        to_email=(os.environ.get("ADMIN_EMAILS"),),
        from_email=os.environ.get("DEFAULT_FROM_EMAIL"),
    )
