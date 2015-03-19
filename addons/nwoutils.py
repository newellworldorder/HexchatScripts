import hexchat

__module_name__ = 'NWOutils'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1'
__module_description__ = 'Stealth op commands'

lock = 0

def op_op(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) == 1:
        hexchat.command('cs op %s' % chan)
    else:
        i = len(word) - 1
        while i > 0:
            hexchat.command('cs op %s %s' % (chan, word[i]))
            i -= 1
    return hexchat.EAT_ALL

def op_deop(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) == 1:
        hexchat.command('cs deop %s' % chan)
    else:
        i = len(word) - 1
        while i > 0:
            hexchat.command('cs deop %s %s' % (chan, word[i]))
            i -= 1
    return hexchat.EAT_ALL

def op_kick(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) > 1:
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 kickban %s' % word_eol[1])
        hexchat.command('timer 2 cs deop %s' % chan)
    return hexchat.EAT_ALL

def op_unban(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) == 2:
        hexchat.command('whois %s' % word[1])
        hexchat.hook_print('WhoIs Name Line', op_unban, userdata = 'unban')
        return hexchat.EAT_PLUGIN
    elif len(word) > 2 and userdata.lower() == 'unban':
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 MODE %s -b *!*@%s' % (chan, word[2]))
        hexchat.command('timer 2 cs deop %s' % chan)
        return hexchat.EAT_ALL

def op_quiet(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        for user in users:
            if hexchat.nickcmp(user.nick, word[1]) == 0 :
                break
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 mode %s +q *!*@%s' % (chan, user.host.split('@')[1]))
        hexchat.command('timer 2 cs deop %s' % chan)
    return hexchat.EAT_ALL

def op_unquiet(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        for user in users:
            if hexchat.nickcmp(user.nick, word[1]) == 0 :
                break
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 mode %s -q *!*@%s' % (chan, user.host.split('@')[1]))
        hexchat.command('timer 2 cs deop %s' % chan)
    return hexchat.EAT_ALL

def op_unlock(userdata):
    global lock
    lock = 0
    return 0

def op_recover(word, word_eol, userdata):
    global lock
    hexchat.command('join %s' % word[1])
    if lock == 0:
        hexchat.command('cs unban %s' % word[1])
        hexchat.command('timer 1 join %s' % word[1])
        lock = 1
        hexchat.hook_timer(10000, op_unlock)
    return hexchat.EAT_NONE

def nwo_greentext(word, word_eol, userdata):
    if len(word) > 0:
        hexchat.command('say \00303>%s' % word_eol[1])
    return hexchat.EAT_ALL

hexchat.hook_command('op', op_op)
hexchat.hook_command('deop', op_deop)
hexchat.hook_command('kick', op_kick)
hexchat.hook_command('unban', op_unban)
hexchat.hook_command('quiet', op_quiet)
hexchat.hook_command('unquiet', op_unquiet)
hexchat.hook_command('>', nwo_greentext)
hexchat.hook_print('You Kicked', op_recover)
