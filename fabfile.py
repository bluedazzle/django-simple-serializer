from fabric.api import run, env, local


def push(commit, title, desc):
    mail = "rapospectre@gmail.com"
    commit_message = '<{0}>  {1}\r\n\r\nAuthor:{2}\r\n\r\nDesc: {3}'.format(commit, title, mail, desc)
    local("git add .")
    local("git commit -m '{0}'".format(commit_message))
    local("git push origin master")
