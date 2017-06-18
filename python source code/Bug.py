# -*- coding: utf-8 -*-
import re
import os

class Bug(object):
    def __init__(self, 
                 idBug, 
                 idProject,  
                 rawBugDescription,
                 hasConfigFilesOrLogs,
                 hasImages):  
        self.idBug = idBug
        self.idProject = idProject
        self.idCluster = 0
        self.rawBugDescription = rawBugDescription
        self.processedBugDescription = ""
        self.hasSTR = 0
        self.hasEOB = 0
        self.hasConfigFilesOrLogs = hasConfigFilesOrLogs
        self.hasImages = hasImages
        self.hasStackTrace = 0
        self.hasJavaCode = 0
        Bug.arr_patterns = Bug.get_patterns()
        
    def __repr__(self):
        return "Bug(\n\tidBug = %s\n\tidProject = %s\n\tidCluster = %s\n)" % (self.idBug, self.idProject, self.idCluster)
        
    def preprocessing_text(self):
        self.processedBugDescription = self.rawBugDescription + "_processed"
        
    def filter_pattern(self, arr_pattern, text):  
        stack_trace_flag = 0
        temp_str = ' '
        cleaned_text = ' '
        cleaned_text = text
        temp_str = text

        pattern_a_lot_of_ERROR = re.compile('.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*')
        if pattern_a_lot_of_ERROR.search(temp_str):
            stack_trace_flag = 1
            temp_str = pattern_a_lot_of_ERROR.sub(' ', temp_str)
            cleaned_text = temp_str
                
        for i, pattern in enumerate(arr_pattern):
            if pattern.search(temp_str):
                stack_trace_flag = 1
                temp_str = pattern.sub(' ', temp_str)
                cleaned_text = temp_str
        
        cleaned_text = os.linesep.join([s for s in cleaned_text.splitlines() if s]) #ct
        temp_str = " ".join(temp_str.split())
        return [temp_str, stack_trace_flag]
    
    def get_patterns() :
        pattern0 = re.compile(r'({{.*?}})', re.DOTALL) #теперь работают верно OK
        pattern1 = re.compile(r'({code.*?{code})', re.DOTALL) #OK
        pattern2 = re.compile(r'({noformat.*?{noformat})', re.DOTALL)
        pattern3 = re.compile(r'({panel.*?{panel})', re.DOTALL)
        pattern4 = re.compile(r'({quote.*?{quote})', re.DOTALL)
        pattern5 = re.compile('\\nmysql>.* sec[)]', re.DOTALL) #for sql
        pattern6 = re.compile('Original Message.*\\n(>\\s)?Subject:.*\\n(>\\s)?Date:.*\\n(>\\s)?From:.*\\n(>\\s)?To:.*')
        pattern7 = re.compile('\\n(>\\s)?Service Level:.*\\n(>\\s)?Product:.*\\n(>\\s)?Response Time:.*\\n(>\\s)?Time of Expiration:.*\\n(>\\s)?Created:.*\\n(>\\s)?URL:.*\\n(>\\s)?Subject:.*')
        pattern8 = re.compile('[[(][0-9][0-9]:[0-9][0-9].*(?:(PM)|(AM)).*:')
        
        pattern9 = re.compile('\\n(>\\s)?Resolving.*\\n(>\\s)?Connecting.*\\n(>\\s)?HTTP.*\\n(>\\s)?(\\s)+HTTP.*\\n(>\\s)?(\\s)+Date:.*\\n(>\\s)?(\\s)+Server:.*(?:(\\n(>\\s)?(\\s)+Location:.*\\n(>\\s)?(\\s)+Content-Length:.*\\n(>\\s)?(\\s)+Keep-Alive:.*\\n(>\\s)?(\\s)+Connection:.*\\n(>\\s)?(\\s)+Content-Type:.*(\\n(>\\s)?(\\s)+Location:.*)?)|(\\n(>\\s)?(\\s)+X-Powered-By:.*\\n(>\\s)?(\\s)+Content-Type:.*\\n(>\\s)?(\\s)+(?:(Content-Language:)|(Content-Length:)).*(\\n(>\\s)?(\\s)+Set-Cookie:.*)?(\\n(>\\s)?(\\s)+Via:.*)?(\\n(>\\s)?(\\s)+Connection:.*)?))(.*Length:.*)?')
        pattern10 = re.compile('(?:(.*ALERT.*)|(?:(.*ERROR.*)|(?:.*ERROR.*|(?:.*INFO.*|(?:.*WARN.*|(?:.*CLOSE_WAIT.*|(?:.*BLOCKED.*|(?:.*DEBUG.*|.*WAITING.*))))))))') 
        pattern11 = re.compile('(?:(((\\n.*ERROR.*)+)?((.*ERROR.*\\n)+)?((.*[a-zA-Z]Exception.*\\n)+)?((.*[a-zA-Z]Error.*\\n)+)?((.*at .*[(].*(?:java|(?:Unknown Source|Native Method)).*[)].*)+))|((((?:((\\n.*ERROR.*)+)|((.*ERROR.*\\n)+)))+)((((.*[a-zA-Z]Exception.*\\n)+)))))')
        pattern12 = re.compile('.*(?:waiting|locked).*0x.*[(].*[)].*')
        pattern13 = re.compile('.*0x.*0x.*')
        pattern14 = re.compile('.*(?:(".*ActiveMQ.*")|(".*Thread-7.*")).*')
        pattern15 = re.compile('([a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+[(](?:.*java.*|(?:.*Native Method.*|.*No such file or directory.*))[)])')
        pattern16 = re.compile('.*[Cc]aused by.*java.*\\n(.*[Cc]aused by.*java.*\\n)+') 
        pattern17 = re.compile('.*at line.*\\n.*at line.*\\n((.*at line.*\\n)+)')
        pattern18 = re.compile('((.*[0-9][0-9]:[0-9][0-9]:[0-9][0-9].*[[]error[]].*client.*)+)')
        pattern19 = re.compile('.*java.*[(].*[)].*\\n.*java.*[(].*[)].*\\n')
        pattern20 = re.compile('.*[(].*".*".*=>.*".*".*[)].*')
        pattern21 = re.compile('failure description:.*[{].*[}]', re.DOTALL)
        #ok
        #pattern12 = re.compile('[\\s][{][\\s].*[\\s][}][\\s]', re.DOTALL)
        pattern22 = re.compile('\\n[{]\\r\\n.*\\r\\n[}]\\r', re.DOTALL) #12, 17 и 20 не конфликтуют?
        pattern23 = re.compile('[/][^\\s]*=[^\\s]*[/][^\\s]*=[^\\s]*')
        pattern24 = re.compile('[^\\s]+[.][^\\s"]+') #DOOOOOOOOOOOOOTTTTT
        pattern25 = re.compile('{{.*}}')                                #
        pattern26 = re.compile('[^\\s]+[/][^\\s]+')
        pattern27 = re.compile('.*Event.*receive.*from remote server.*\\nInternal Server Error.*')
        pattern28 = re.compile('<.*>\\s.*<[/].*>\\s', re.DOTALL)
        #pattern28 = re.compile('[\\w"-[.]]+(?:(=)|(==))[\\w"-[.]]+')
        pattern29 = re.compile('(?:({panel})|(?:({code[^\\s]*})|(?:({noformat})|({quote}))))')
        pattern30 = re.compile('[a-z]+[A-Z][a-z]+( )?[{].*[}]', re.DOTALL)
        pattern31 = re.compile('[A-Z][a-z]+[A-Z][a-z]+[(].*[)]')
        pattern32 = re.compile('{.*return.*}', re.DOTALL)
        pattern33 = re.compile('[^\\s]*@[^\\s]*')
        pattern34 = re.compile('[A-Z]+?[a-z]+[A-Z][a-z]+[^\\s]*')
        pattern35 = re.compile('[0-9]+.*has been deprecated')
        #pattern32 = re.compile('[[][0-9][0-9]:[0-9][0-9] (?:(PM)|(AM))[]].*:')
        pattern36 = re.compile('@[^\\s]*')
        pattern37 = re.compile('[.][a-z]+[^\\s]*') #changed 06/12 20.14 DOOOOOOOOOOOOOTTTTT
        pattern38 = re.compile('<[^\\s]*>')
        pattern39 = re.compile('<[[].*[]]>')
        pattern40 = re.compile('[[]disconnected.*[/][]]')
        pattern41 = re.compile('[-][-][a-z]*')
        pattern42 = re.compile('try.*{.*}')
        pattern43 = re.compile('catch.*{.*}')
        pattern44 = re.compile('{.*throw.*}')
        pattern45 = re.compile('check.*{.*}')
        pattern46 = re.compile('public void')
        pattern47 = re.compile('private void')
        pattern48 = re.compile('[[][[].*[]][]]')
        pattern49 = re.compile('<.*[/]>')
        pattern50 = re.compile('(?:a2p|ac|addgroup|adduser|agrep|alias|apropos|apt-cache|apt-get|aptitude|ar|arch|arp|as|aspell|at|awk|basename|bash|bc|bdiff|bfs|bg|biff|break|bs|bye|cal|calendar|cancel|cat|cc|cd|cfdisk|chdir|checkeq|checknr|chfn|chgrp|chkey|chmod|chown|chroot|chsh|cksum|clear|cmp|col|comm|compress|continue|cp|cpio|crontab|csh|csplit|ctags|cu|curl|cut|date|dc|dd|delgroup|deluser|depmod|deroff|df|dhclient|diff|dig|dircmp|dirname|dmesg|dos2unix|dpkg|dpost|du|echo|ed|edit|egrep|eject|elm|emacs|enable|env|eqn|ex|exit|expand|expr|fc|fdisk|fg|fgrep|file|find|findsmb|finger|fmt|fold|for|foreach|free|fsck|ftp|fuser|gawk|getfacl|gpasswd|gprof|grep|groupadd|groupdel|groupmod|gunzip|gview|gvim|gzip|halt|hash|hashstat|head|help|history|host|hostid|hostname|id|ifconfig|ifdown|ifquery|ifup|info|init|insmod|iostat|ip|isalist|iwconfig|jobs|join|keylogin|kill|killall|ksh|last|ld|ldd|less|lex|link|ln|lo|locate|login|logname|logout|losetup|lp|lpadmin|lpc|lpq|lpr|lprm|lpstat|ls|lsmod|lsof|lzcat|lzma|mach|mail|mailcompat|mailx|make|man|merge|mesg|mii-tool|mkdir|mkfs|mkswap|modinfo|modprobe|more|mount|mt|mv|myisamchk|mysql|mysqldump|nc|neqn|netstat|newalias|newform|newgrp|nice|niscat|nischmod|nischown|nischttl|nisdefaults|nisgrep|nismatch|nispasswd|nistbladm|nl|nmap|nohup|nroff|nslookup|od|on|onintr|optisa|pack|pagesize|parted|partprobe|passwd|paste|pax|pcat|perl|pg|pgrep|pico|pine|ping|pkill|poweroff|pr|printenv|printf|priocntl|ps|pstree|pvs|pwd|quit|rcp|readlink|reboot|red|rehash|rename|renice|repeat|replace|rgview rgvim|rlogin|rm|rmdir|rmmod|rn|route|rpcinfo|rsh|rsync|rview|rvim|s2p|sag|sar|scp|screen|script|sdiff|sed|sendmail|service|set|setenv|setfacl|sfdisk|sftp|sh|shred|shutdown|sleep|slogin|smbclient|sort|spell|split|startx|stat|stop|strftime|strip|stty|su|sudo|swapoff|swapon|sysklogd|tabs|tac|tail|talk|tar|tbl|tcopy|tcpdump|tcsh|tee|telinit|telnet|test|time|timex|todos|top|touch|tput|tr|traceroute|trap|tree|troff|tty|ul|umask|umount|unalias|uname|uncompress|unhash|uniq|unlink|unlzma|unpack|until|unxz|unzip|uptime|useradd|userdel|usermod|vacation|vgrind|vi|view|vim|vipw|visudo|vmstat|w|wait|wall|wc|wget|whatis|whereis|which|while|who|whoami|whois|write|X|Xorg|xargs|xfd|xhost|xinit|xlsfonts|xrdb|xset|xterm|xz|xzcat|yacc|yes|yppasswd|yum|zcat|zip|zipcloak|zipinfo|zipnote|zipsplit) -{1,2}\w+ \w*')
        #add regex for deleting linux comand:
        pattern51 = re.compile(r'\b(a2p|ac|addgroup|adduser|agrep|alias|apropos|apt-cache|apt-get|aptitude|ar|arch|arp|as|aspell|at|awk|basename|bash|bc|bdiff|bfs|bg|biff|break|bs|bye|cal|calendar|cat|cc|cd|cfdisk|chdir|checkeq|checknr|chfn|chgrp|chkey|chmod|chown|chroot|chsh|cksum|cmp|col|comm|compress|cp|cpio|crontab|csh|csplit|ctags|cu|curl|date|dc|dd|delgroup|deluser|depmod|deroff|df|dhclient|diff|dig|dircmp|dirname|dmesg|dos2unix|dpkg|dpost|du|echo|ed|egrep|eject|elm|emacs|env|eqn|ex|expr|fc|fdisk|fg|fgrep|findsmb|finger|fmt|foreach|fsck|ftp|fuser|gawk|getfacl|gpasswd|gprof|grep|groupadd|groupdel|groupmod|gunzip|gview|gvim|gzip|halt|hash|hashstat|hostid|ifconfig|ifdown|ifquery|ifup|init|insmod|iostat|ip|isalist|iwconfig|keylogin|kill|killall|ksh|last|ld|ldd|less|lex|link|ln|lo|logname|logout|losetup|lp|lpadmin|lpc|lpq|lpr|lprm|lpstat|ls|lsmod|lsof|lzcat|lzma|mach|mailcompat|mailx|mesg|miitool|mkdir|mkfs|mkswap|modinfo|modprobe|mount|mt|mv|myisamchk|mysqldump|nc|neqn|netstat|newalias|newform|newgrp|niscat|nischmod|nischown|nischttl|nisdefaults|nisgrep|nismatch|nispasswd|nistbladm|nl|nmap|nohup|nroff|nslookup|od|on|onintr|optisa|pack|pagesize|parted|partprobe|passwd|pax|pcat|perl|pg|pgrep|pico|pine|pkill|poweroff|pr|printenv|printf|priocntl|ps|pstree|pvs|pwd|rcp|readlink|red|rehash|renice|repeat|rgview|rgvim|rlogin|rm|rmdir|rmmod|rn|route|rpcinfo|rsh|rsync|rview|rvim|s2p|sag|sar|scp|sdiff|sed|sendmail|setenv|setfacl|sfdisk|sftp|sh|shred|slogin|smbclient|sort|spell|split|startx|stat|strftime|strip|stty|su|sudo|swapoff|swapon|sysklogd|tac|tar|tbl|tcopy|tcpdump|tcsh|tee|telinit|telnet|timex|todos|tput|tr|traceroute|trap|tree|troff|tty|ul|umask|umount|unalias|uname|uncompress|unhash|uniq|unlink|unlzma|unpack|until|unxz|unzip|uptime|useradd|userdel|usermod|vacation|vgrind|vi|vim|vipw|visudo|vmstat|w|wall|wc|wget|whatis|whereis|which|while|who|whoami|whois|X|Xorg|xargs|xfd|xhost|xinit|xlsfonts|xrdb|xset|xterm|xz|xzcat|yacc|yppasswd|yum|zcat|zip|zipcloak|zipinfo|zipnote|zipsplit)\b')
        pattern52 = re.compile('(?:https|http)://\w*\S*\d*', re.DOTALL)
        #pattern50 = re.compile(r'\(\d{2}:.*?\n', re.DOTALL)
        pattern53 = re.compile('[^\\s]*[0-9][^\\s]*')
        #pattern53_1 = re.compile('\\s[^a-zA-Z\\s]*[a-zA-Z]+[^a-zA-Z\\s]*.*\\s') #deleting all words with no-letters
        pattern54 = re.compile('[^a-zA-Z\\s]+') #varsion with deleting words like doesn't i'll IT REMOVES DOTS!!!
        pattern55 = re.compile('\\sPM\\s')
        pattern56 = re.compile('\\sAM\\s')
        
        #deleting java key-words
        pattern57 = re.compile('(?:(\\sabstract\\s)|(\\sassert\\s))')
        pattern58 = re.compile('(?:(\\sboolean\\s)|(\\sbreak\\s))')
        pattern59 = re.compile('(?:(\\sbyte\\s)|(\\scase\\s))')
        pattern60 = re.compile('(?:(\\scatch\\s)|(\\schar\\s))')
        pattern61 = re.compile('(?:(\\sclass\\s)|(\\sconst\\s))')
        pattern62 = re.compile('(?:(\\scontinue\\s)|(\\sdefault\\s))')
        pattern63 = re.compile('(?:(\\sdo\\s)|(\\sdouble\\s))')
        pattern64 = re.compile('(?:(\\selse\\s)|(\\senum\\s))')
        pattern65 = re.compile('(?:(\\sfor\\s)|(\\sfloat\\s))')
        pattern66 = re.compile('(?:(\\sgoto\\s)|(\\sif\\s))')
        pattern67 = re.compile('(?:(\\sinstanceof\\s)|(\\sint\\s))')
        pattern68 = re.compile('(?:(\\snew\\s)|(\\sprivate\\s))')
        pattern69 = re.compile('(?:(\\sprotected\\s)|(\\spublic\\s))')
        pattern70 = re.compile('(?:(\\sreturn\\s)|(\\sstatic\\s))')
        pattern71 = re.compile('(?:(\\sstrictfp\\s)|(\\sswitch\\s))')
        pattern72 = re.compile('(?:(\\sthis\\s)|(\\sthrow\\s))')
        pattern73 = re.compile('(?:(\\sthrows\\s)|(\\stransient\\s))')
        pattern74 = re.compile('(?:(\\stry\\s)|(\\svoid\\s))')
        pattern75 = re.compile('(?:(\\svolatile\\s)|(\\swhile\\s))')
        pattern76 = re.compile('(?:(\\strue\\s)|(\\sfalse\\s))')
        pattern77 = re.compile('\\snull\\s')
        
        pattern78 = re.compile('[a-zA-Z]+\'[a-zA-Z]+') #deleting words with ' symbol inside
        pattern79 = re.compile('\\s[a-zA-Z]\\s') #deleting words from one symbol
        pattern80 = re.compile('\\s[A-Z]+\\s') #deleting abbreviation
        pattern81 = re.compile('.*undefined.*\\n.*undefined.*\\n.*undefined.*\\n.*undefined.*\\n.*undefined.*\\n') #215 in project 2
        pattern82 = re.compile('relay.*undefined.*\\n.*transport.*\\n.*undefined.*\\n.*undefined') #215 in project 2
        pattern83 = re.compile('drwxr xr.*') #458 project 2
        pattern84 = re.compile('\\t\\t\\t\\t\\t\\soption.*\\n\\t\\t\\t\\t\\t\\soption.*\\n\\t\\t\\t\\t\\t\\soption.*\\n')
        pattern85 = re.compile('\\t\\smodule option.*\\n\\t\\smodule option.*\\n\\t\\smodule option.*\\n')
        pattern86 = re.compile('\\s\\sFailed to load module\\s\\s\\sextension.*\\n.*\\n\\s\\sFailed to load module\\s\\s\\sextension.*\\n.*\\n') #709 in project 2
        pattern87 = re.compile('\\sdoes\\s')
        pattern88 = re.compile('\\sdoesnt\\s')
        pattern89 = re.compile('\\sive\\s')
        pattern90 = re.compile('\\sdont\\s')
        pattern91 = re.compile('\\shes\\s')
        pattern92 = re.compile('\\sill\\s')
        pattern93 = re.compile('\\sdid\\s')
        pattern94 = re.compile('\\syoull\\s')
        pattern95 = re.compile('\\sdoesn\\s')
        pattern96 = re.compile('\\shaven\\s')
        pattern97 = re.compile('\\sdon\\s')
        pattern98 = re.compile('\\sisnt\\s')
        
        #нужно добавить шаблонов
        Bug.arr_patterns = [pattern0, pattern1, pattern2, pattern3, pattern4, 
                        pattern5, pattern6, pattern7, pattern8, pattern9, pattern10,
                        pattern11, pattern12, pattern13, pattern14,
                        pattern15, #dot is alive
                        pattern16, pattern17, pattern18, pattern19, pattern20, pattern21, #dot is alive
                        pattern22, pattern23, pattern24, pattern25, pattern26, pattern27, pattern28, #dot is alive
                        pattern29, pattern30, pattern31, pattern32, pattern33, pattern34, pattern35, #dot is alive
                        pattern36, pattern37, pattern38, pattern39, pattern40, pattern41, pattern42, #dot is alive
                        pattern43, pattern44, pattern45, pattern46, pattern47, pattern48, pattern49, #dot is alive
                        pattern50, pattern51, pattern52, #dot is alive
                        pattern53,
        #                pattern54 IT REMOVES DOTS
                        pattern55,
                        pattern56, pattern57, pattern58, pattern59, pattern60, pattern61, pattern62,
                        pattern63, pattern64, pattern65, pattern66, pattern67, pattern68, pattern69,
                        pattern70, pattern71, pattern72, pattern73, pattern74, pattern75, pattern76,
                        pattern77, pattern78, pattern79, pattern80, pattern81, pattern82, pattern83,
                        pattern84, pattern85, pattern86, pattern87, pattern88, pattern89,
                        pattern90, pattern91, pattern92, pattern93, pattern94, pattern95, pattern96,
                        pattern97, pattern98]              
                