import gnupg

gpg = gnupg.GPG()
gpg.encoding = 'utf-8'
inputd=gpg.gen_key_input(key_type="RSA",key_length=1024,name_real="Angel Romero",name_email="angelo102@gmail.com")
key = gpg.gen_key(inputd)