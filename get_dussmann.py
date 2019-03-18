import imaplib
import email
import re
import os
import datetime

server = os.environ.get('MAILSERVER')
username = os.environ.get('MAILUSER')
password = os.environ.get('MAILPASSWORD')
targetdir = os.environ.get('DATAFOLDER', './data/')
targetdir += "dussmann/"

mark_as_read = True 


def getDate():
    week = datetime.date.today().isocalendar()[1]
    year = datetime.datetime.now().year
    dow = datetime.datetime.today().weekday()
    if dow > 4:
        week += 1
    if week > 52:
        year += 1
        week = 1
    return dow, week, year

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

# Connect to an IMAP server
def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    m.select()
    return m


# extract and generate a new filename
def generateFilename(maildate, filename):
    filename = filename.lower()
    reg_kw = re.compile(r"kw.?\d\d")
    match_kw = re.search(reg_kw, filename)
    reg_kw = re.compile(r"\d\d")
    match_kw = re.search(reg_kw, match_kw.group(0))

    if match_kw != None:
        dow, week, year = getDate()
        kw = match_kw.group(0)
        return str(year) + kw + ".pdf"
    else:
        week = datetime.date(maildate).isocalendar()[1]
        year = datetime.now().year
        if maildate.weekday() >= 3:
            week = week + 1
            week = str(week).zfill(2)
            return str(year) + str(week) + ".pdf"


# Download all attachment files for a given email
def downloadAttachmentsInEmail(m, emailid, outputdir):
    if mark_as_read:
        resp, data = m.fetch(emailid, "(RFC822)")
    else:
        resp, data = m.fetch(emailid, "(BODY.PEEK[])")
    email_body = data[0][1]
    mail = email.message_from_bytes(email_body)
    if not mail.is_multipart():
        return
    maildate = datetime.datetime.strptime(mail.__getitem__(
        "Date"), "%a, %d %b %Y %H:%M:%S %z")
    createFolder(outputdir)
    for part in mail.walk():
        attachment_filename = part.get_filename()
        if part.get_filename() != None:
            attachment_filename = attachment_filename.lower()
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None and attachment_filename.lower().endswith("pdf"):
            filename = generateFilename(maildate, attachment_filename)
            open(outputdir + '/' + filename,
                 'wb').write(part.get_payload(decode=True))


# get all unread mails
def downloadNewAttachements(server, user, password, outputdir):
    m = connect(server, user, password)
    resp, items = m.search(None, "(UNSEEN)")
    items = items[0].split()
    for emailid in items:
        downloadAttachmentsInEmail(m, emailid, outputdir)


def getDussmann():
    downloadNewAttachements(server, username, password, targetdir)


if __name__ == "__main__":
    downloadNewAttachements(server, username, password, targetdir)
