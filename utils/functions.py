from random import choice


def get_ticket():
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_'
    ticket = ''
    for i in range(30):
        ticket += choice(s)
    return ticket
