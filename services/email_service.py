import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")


def send_invitation_email(to_email, name, invite_link):

    with open("templates/invite_template.html", "r") as file:
        html_template = file.read()

    html_content = (
        html_template
        .replace("{{name}}", name)
        .replace("{{link}}", invite_link)
    )

    params = {
        "from": "FastAPI Project <onboarding@resend.dev>",
        "to": [to_email],
        "subject": "You are invited 🚀",
        "html": html_content,
    }

    email = resend.Emails.send(params)

    return email