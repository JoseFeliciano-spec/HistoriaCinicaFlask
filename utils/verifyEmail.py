import re;
""" Return true or false """
def verifyEmail(email):
    expression = re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',email.lower());
    if(expression):
        return True;
    else:
        return False; 
    
