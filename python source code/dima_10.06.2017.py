from nltk.corpus import stopwords 
from nltk.util import ngrams 
import os
import pandas as pd
import numpy as np
import re
from nltk.stem.api import StemmerI
from nltk.stem.regexp import RegexpStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.isri import ISRIStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.rslp import RSLPStemmer
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.csr import csr_matrix #need this if you want to save tf-idf matrix
def filter_pattern(arr_pattern, text):

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
arr_patterns = [pattern0, pattern1, pattern2, pattern3, pattern4, 
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
                
number_of_bug_descr = list()
list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags = list()

arr_time_created_for_all_projects = list()
arr_time_resolved_for_all_projects = list()

list_of_vectorized_bugs = list()
list_pos_im = list()
list_pos_xml = list()
list_pos_arch = list()
list_log_ldif_war = list()
col_attachments = list()
col_attachments_1 = list()
col_num_of_comments = list()
list_total_texts = list()
for i in [1,2,3]:
    str_path = "JBoss%d.csv" % i
    data = pd.read_csv(str_path)    
    
    cols=pd.Series(data.columns)
    for dup in data.columns.get_duplicates(): cols[data.columns.get_loc(dup)]=[dup+'.'+str(d_idx) if d_idx!=0 else dup for d_idx in range(data.columns.get_loc(dup).sum())]
    data.columns=cols
    print(data.columns)
    
    data.dropna(subset = ['Description'], inplace = True)
    time_created = list(data['Created'][1:])
    
    attachment = list(data['Attachment'][1:])
    col_attachments.append(attachment)
    attachment_1 = list(data['Attachment.1'][1:])
    col_attachments_1.append(attachment_1)
    col_num_comm = list(data['Custom field (Number of comments)'][1:])
    col_num_of_comments.append(col_num_comm)
    
    arr_time_created_for_all_projects = arr_time_created_for_all_projects + time_created
    time_resolved = list(data['Resolved'][1:])
    arr_time_resolved_for_all_projects = arr_time_resolved_for_all_projects + time_resolved
    
    data_description0 = data['Description'][1:]
    data_description0.to_frame()
    data_len = len(data_description0)
    number_of_bug_descr.append(data_len)
    zeros_df = pd.DataFrame(0, index=data_description0.index, columns=['HasStackTrace'])
    data_description = pd.concat([data_description0, zeros_df], axis=1)
    
    subset = data_description[['Description', 'HasStackTrace']]
    list_of_bugs_descriptions_and_stack_trace_flags = [list(x) for x in subset.values]
                                                       
    
    for k,item in enumerate(list_of_bugs_descriptions_and_stack_trace_flags):

        text = item[0]
        list_total_texts.append(text)
        list_of_bugs_descriptions_and_stack_trace_flags[k] = filter_pattern(arr_patterns, text) 
        
        
    list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags = list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags + list_of_bugs_descriptions_and_stack_trace_flags
    for num, item in enumerate(list_of_bugs_descriptions_and_stack_trace_flags): 
        list_of_vectorized_bugs.append([i, num, item[1], 0, 0, 0])
    str_for_print = 'Number of descriptions in %d project: ' % i
    print(str_for_print)
    print(len(list_of_bugs_descriptions_and_stack_trace_flags))


print('Number of all descriptions: ')
print(len(list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags))
print('Len of list_of_vectorized_bugs')
print(len(list_of_vectorized_bugs))
  
#stem function
def stem(tokens, stop_words):
    #different stemm algorithms
    stemming_algorithms = {
    "stemmer1" : SnowballStemmer("english"),
    "stemmer2" : StemmerI,
    "stemmer3" : RegexpStemmer,
    "stemmer4" : LancasterStemmer,
    "stemmer5" : ISRIStemmer,
    "stemmer6" : PorterStemmer,
    "stemmer7" : SnowballStemmer,
    "stemmer8" : WordNetLemmatizer,
    "stemmer9" : RSLPStemmer}
    tokens = [stemming_algorithms['stemmer1'].stem(token) for token in tokens if (token not in stop_words)] 
    return tokens 
    
#lemmatize function   
def lem(tokens, stop_words):
    lmtzr = WordNetLemmatizer()
    tokens = [lmtzr.lemmatize(token) for token in tokens if (token not in stop_words)] 
    return tokens

#return tokens without stop words
def get_tokens(file_text):
    #cleaning words, making lowercase and tokenization
    tokens = list()
    #this regex find all words without symbols and numbers (,:. in the end of word and * at the beggining/end is an exception)
    #* - is a header tag in Jira (*... ... ...*)
    pattern = re.compile(r'^\*?([a-zA-Z]{2,15})(?:|\.|\:|\,)\*?$')
    tokens = [pattern.findall(i)[0].lower() for i in file_text.split() if (len(pattern.findall(i))>0)]
    #deleting stop_words and linux command
    variants_of_stopwords = {
    '429': ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away', 'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes', 'been', 'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down', 'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods', 'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'herself', 'high', 'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into', 'is', 'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible', 'present', 'presented', 'presenting', 'presents', 'problem', 'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z'],
    '319': ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herse"', 'him', 'himse"', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itse"', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myse"', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves'],
    '667': ['a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', "can't", 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure', 't', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "'ve", 'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome', "we'll", 'went', 'were', 'werent', "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero'],
    '167': stopwords.words('english')
    }
    try:
        stop_words = variants_of_stopwords['319']
    except KeyError as e:
        raise ValueError('Undefined unit: {}'.format(e.args[1]))
    #call stem or lem function
    stem_or_lem = {
    "stem" : stem(tokens, stop_words), #CHECK IT
    "lem" : lem(tokens, stop_words)                
    }
    tokens = stem_or_lem["lem"]
    return tokens

#return bigrams
def get_bigrams(file_text):
    tokens = get_tokens(file_text)
    return list(ngrams(tokens,2))

#call tokenazation (and bigram) function with text of bug description as a parametr              
list_tokens_with_stack_trace_flag = [[get_tokens(x[0]),x[1]] for x in list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags ]
list_bigrams_with_stack_trace_flag = [[get_bigrams(x[0]),x[1]] for x in list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags ] 
                                       
#print('---------num of tokens-----------')
#print(len(list_tokens_with_stack_trace_flag))   
#print('---------num of bigrams-----------')                                   
#print(len(list_bigrams_with_stack_trace_flag))                                       
                                       
#Saving tokens in text file
thefile_words = open('words.txt', 'w', encoding='utf-8')
for item in list_tokens_with_stack_trace_flag:
    temp_str = ', '.join(item[0])
    thefile_words.write("%r\n" % temp_str)
    thefile_words.write("%s\n" % str(item[1]))
thefile_words.close()
#Saving bigrams in text file
thefile_bigrams = open('bigrams.txt', 'w', encoding='utf-8')
for item in list_bigrams_with_stack_trace_flag:
    my_str = ' '
    for x in item[0]:
        temp_str = ' / '.join(x)
        my_str = my_str + ' , ' + temp_str
    thefile_bigrams.write("%r\n" % my_str)
    thefile_bigrams.write("%s\n" % str(item[1]))
thefile_bigrams.close()

#Create list of only words from list with words and flag
corpus = list() 
for item in list_tokens_with_stack_trace_flag:
    temp_str = ' '.join(item[0])
    corpus.append(temp_str)


xls = pd.read_excel('JBoss_description_table_marked.xls')
target_steps_to_repr = list(xls['steps to reproduce'][1:])
target_exp_obs_beh = list(xls['expected/observed behavior'][1:])
print('length of step to reproduc vector: ', len(target_steps_to_repr))
print('length of observed behavior vector: ', len(target_exp_obs_beh))

    
from sklearn.cluster import KMeans
from sklearn import metrics

list_tokens_after_lem = list()
for item in list_tokens_with_stack_trace_flag:
    list_tokens_after_lem.append(item[0])

print('----------------------------')



attach_2122 = list()
attach_2122_1 = list()
num_comment_2122 = list()
for item in col_attachments:
    attach_2122 = attach_2122 + item
for item in col_attachments_1:
    attach_2122_1 = attach_2122_1 + item


list_pos_see_attached = list()
pattern_see = re.compile('\ssee\s|\sSee\s')
pattern_attached = re.compile('\sattached\s|\sAttached\s')
pattern_log_ldif_war = re.compile('\.log|\.ldif|\.war')
pattern_im = re.compile('\.bmp|\.cpt|\.gif|\.hdr|\.jpeg|\.jpg|\.jpe|\.jp2|\.pcx|\.pdf|\.pdn|\.png|\.psd|\.tga|\.tpic|\.tiff|\.tif|\.wdp|\.hdp|\.xpm')
pattern_arch = re.compile('\.7z|\.ace|\.arj|\.bz2|\.cab|\.cpio|\.deb|\.gz|\.jar|\.lzh|\.lzo|\.lzh|\.rar|\.rpm|\.tar|\.xz|\.zip|\.zoo')
pattern_xml = re.compile('\.xml')
for k,text in enumerate(list_total_texts):
    if pattern_im.search(text):
        list_pos_im.append(k)
    if pattern_arch.search(text):
        list_pos_arch.append(k)
    if pattern_xml.search(text):
        list_pos_xml.append(k)
    if pattern_log_ldif_war.search(text):
        list_log_ldif_war.append(k)
    if (pattern_see.search(text) or pattern_attached.search(text)):
        list_pos_see_attached.append(k)


def isnan(obj):
    return obj != obj

for i,item in enumerate(attach_2122):
    if isnan(item):
        attach_2122[i] = ''

for i,item in enumerate(attach_2122_1):
    if isnan(item):
        attach_2122_1[i] = ''
        
for k,attach in enumerate(attach_2122):
    if pattern_im.search(attach):
        list_pos_im.append(k)
    if pattern_arch.search(attach):
        list_pos_arch.append(k)
    if pattern_xml.search(attach):
        list_pos_xml.append(k)
    if pattern_log_ldif_war.search(attach):
        list_log_ldif_war.append(k)         

for k,attach in enumerate(attach_2122_1):
    if pattern_im.search(attach):
        list_pos_im.append(k)
    if pattern_arch.search(attach):
        list_pos_arch.append(k)
    if pattern_xml.search(attach):
        list_pos_xml.append(k)
    if pattern_log_ldif_war.search(attach):
        list_log_ldif_war.append(k)         
    

from collections import Counter
    
ftr_logs_arch_list = list()
for i in range(2122):
    if (i in list_pos_arch) or (i in list_log_ldif_war):
        ftr_logs_arch_list.append(1)
    else:
        ftr_logs_arch_list.append(0)
        
ftr_im_list = list()
for i in range(2122):
    if (i in list_pos_im):
        ftr_im_list.append(1)
    else:
        ftr_im_list.append(0)   
        
ftr_xml_list = list()
for i in range(2122):
    if (i in list_pos_xml):
        ftr_xml_list.append(1)
    else:
        ftr_xml_list.append(0)         

corpus_strings_tokens_after_lem = list()
for item in list_tokens_after_lem:
    corpus_strings_tokens_after_lem.append(' '.join(item))                
 

print("dict=================================")

ftr_stack_trace_list = list()
for item in list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags:
    ftr_stack_trace_list.append(item[1])
    
print("IMAGES")
print(len(ftr_im_list)) 
print(sum(ftr_im_list))
print('===============================')

       
mean_1 = np.mean(ftr_logs_arch_list)    
std_1 = np.std(ftr_logs_arch_list)
mean_2 = np.mean(ftr_im_list)    
std_2 = np.std(ftr_im_list)
mean_4 = np.mean(ftr_xml_list)    
std_4 = np.std(ftr_xml_list)    
mean_6 = np.mean(target_steps_to_repr)    
std_6 = np.std(target_steps_to_repr) 
mean_7 = np.mean(target_exp_obs_beh)    
std_7 = np.std(target_exp_obs_beh) 
mean_8 = np.mean(ftr_stack_trace_list)    
std_8 = np.std(ftr_stack_trace_list) 
    
print("-------------------NEW FEATURES------------------") 
list_of_vectorized_bugs_9 = list()
list_of_vectorized_bugs_9_unnorm = list()
list_of_vectorized_bugs_9_norm_quantw_comm_verbs = list()
for i in range(2122):
    list_of_vectorized_bugs_9.append([(ftr_logs_arch_list[i] - mean_1)/std_1,
                                     (ftr_im_list[i]-mean_2)/std_2,
                                    (ftr_xml_list[i]-mean_4)/std_4,
                                    (target_steps_to_repr[i]-mean_6)/std_6,
                                    (target_exp_obs_beh[i]-mean_7)/std_7,
                                    (ftr_stack_trace_list[i]-mean_8)/std_8 ]) 
    list_of_vectorized_bugs_9_unnorm.append([ftr_logs_arch_list[i],
                                    ftr_im_list[i],
                                    ftr_xml_list[i],
                                    target_steps_to_repr[i],
                                    target_exp_obs_beh[i],
                                    ftr_stack_trace_list[i] ])
    list_of_vectorized_bugs_9_norm_quantw_comm_verbs.append([ftr_logs_arch_list[i],
                                    ftr_im_list[i],
                                    ftr_xml_list[i],
                                    target_steps_to_repr[i],
                                    target_exp_obs_beh[i],
                                    ftr_stack_trace_list[i] ])
    

#АГГЛОМЕРАТИВНАЯ КЛАСТЕРИЗАЦИЯ (иерархическая?)    
from sklearn.cluster import AgglomerativeClustering    

AC_model = KMeans(n_clusters=14, random_state=7).fit(list_of_vectorized_bugs_9_norm_quantw_comm_verbs)
labels_9 = AC_model.labels_

myset_9 = set(labels_9)

#create description of bugs from different clusters
#with help of words with high tf-idf within this clusters
#START
corpus_90_all = list()
for item in list_tokens_after_lem:
    corpus_90_all.append(' '.join(item))  
    
corplist_vb_0 = list()
corplist_vb_1 = list()
corplist_vb_2 = list()
corplist_vb_3 = list()
corplist_vb_4 = list()
corplist_vb_5 = list()
corplist_vb_6 = list()
corplist_vb_7 = list()
corplist_vb_8 = list()
corplist_vb_9 = list()
corplist_vb_10 = list()
corplist_vb_11 = list()
corplist_vb_12 = list()
corplist_vb_13 = list()
corplist_vb_14 = list()
corplist_vb_15 = list()
for i,item in enumerate(labels_9):
    if item == 0:
        corplist_vb_0.append(corpus_90_all[i])
    if item == 1:
        corplist_vb_1.append(corpus_90_all[i])
    if item == 2:
        corplist_vb_2.append(corpus_90_all[i])    
    if item == 3:
        corplist_vb_3.append(corpus_90_all[i])    
    if item == 4:
        corplist_vb_4.append(corpus_90_all[i])    
    if item == 5:
        corplist_vb_5.append(corpus_90_all[i])    
    if item == 6:
        corplist_vb_6.append(corpus_90_all[i])    
    if item == 7:
        corplist_vb_7.append(corpus_90_all[i])    
    if item == 8:
        corplist_vb_8.append(corpus_90_all[i])    
    if item == 9:
        corplist_vb_9.append(corpus_90_all[i])    
    if item == 10:
        corplist_vb_10.append(corpus_90_all[i])    
    if item == 11:
        corplist_vb_11.append(corpus_90_all[i])    
    if item == 12:
        corplist_vb_12.append(corpus_90_all[i])
    if item == 13:
        corplist_vb_13.append(corpus_90_all[i])    
    if item == 14:
        corplist_vb_14.append(corpus_90_all[i])    
    if item == 15:
        corplist_vb_15.append(corpus_90_all[i])    
    
corplist = [corplist_vb_0, corplist_vb_1, corplist_vb_2, corplist_vb_3,
            corplist_vb_4, corplist_vb_5, corplist_vb_6, corplist_vb_7,
            corplist_vb_8, corplist_vb_9, corplist_vb_10, corplist_vb_11,
            corplist_vb_12, corplist_vb_13]    

freqcorplist_vb_0 = list()
freqcorplist_vb_1 = list()
freqcorplist_vb_2 = list()
freqcorplist_vb_3 = list()
freqcorplist_vb_4 = list()
freqcorplist_vb_5 = list()
freqcorplist_vb_6 = list()
freqcorplist_vb_7 = list()
freqcorplist_vb_8 = list()
freqcorplist_vb_9 = list()
freqcorplist_vb_10 = list()
freqcorplist_vb_11 = list()
freqcorplist_vb_12 = list()
freqcorplist_vb_13 = list()
freqcorplist_vb_14 = list()
freqcorplist_vb_15 = list()

list_of_lists_of_words_with_highest_tfidf = list()            
list_of_lists_of_words_with_highest_usual_frequensy = list()

for i,item in enumerate(labels_9):
    if item == 0:
        freqcorplist_vb_0.append(list_tokens_after_lem[i])
    if item == 1:
        freqcorplist_vb_1.append(list_tokens_after_lem[i])
    if item == 2:
        freqcorplist_vb_2.append(list_tokens_after_lem[i])    
    if item == 3:
        freqcorplist_vb_3.append(list_tokens_after_lem[i])    
    if item == 4:
        freqcorplist_vb_4.append(list_tokens_after_lem[i])    
    if item == 5:
        freqcorplist_vb_5.append(list_tokens_after_lem[i])    
    if item == 6:
        freqcorplist_vb_6.append(list_tokens_after_lem[i])    
    if item == 7:
        freqcorplist_vb_7.append(list_tokens_after_lem[i])    
    if item == 8:
        freqcorplist_vb_8.append(list_tokens_after_lem[i])    
    if item == 9:
        freqcorplist_vb_9.append(list_tokens_after_lem[i])    
    if item == 10:
        freqcorplist_vb_10.append(list_tokens_after_lem[i])    
    if item == 11:
        freqcorplist_vb_11.append(list_tokens_after_lem[i])    
    if item == 12:
        freqcorplist_vb_12.append(list_tokens_after_lem[i])
    if item == 13:
        freqcorplist_vb_13.append(list_tokens_after_lem[i])    
    if item == 14:
        freqcorplist_vb_14.append(list_tokens_after_lem[i])    
    if item == 15:
        freqcorplist_vb_15.append(list_tokens_after_lem[i])    

temp_freq_list = [freqcorplist_vb_0, freqcorplist_vb_1,freqcorplist_vb_2,
                  freqcorplist_vb_3,freqcorplist_vb_4,freqcorplist_vb_5,
                  freqcorplist_vb_6,freqcorplist_vb_7,freqcorplist_vb_8,
                  freqcorplist_vb_9,freqcorplist_vb_10,freqcorplist_vb_11,
                  freqcorplist_vb_12,freqcorplist_vb_13]        

for temp in temp_freq_list:                 
    list_of_lists_of_words_with_highest_usual_frequensy.append( [item for sublist in temp for item in sublist])
                
from collections import defaultdict        
from collections import Counter

for i,item in enumerate(list_of_lists_of_words_with_highest_usual_frequensy):
    list_of_lists_of_words_with_highest_usual_frequensy[i] = Counter(item)

for i,item in enumerate(list_of_lists_of_words_with_highest_usual_frequensy):        
    list_tuples_key_value0 = list()
    for key, value in item.items():
        list_tuples_key_value0.append( (key, value/len(item)) )
    list_tuples_key_value0.sort(key=lambda tup: tup[1])
    for k,v in enumerate(list_tuples_key_value0):
        list_tuples_key_value0[k] = v[0]

    list_of_lists_of_words_with_highest_usual_frequensy[i] = list_tuples_key_value0[-50:]    

            
for corpus_90 in corplist:    
    tf_90 = TfidfVectorizer(input=corpus_90, analyzer='word', ngram_range=(1,1),
                         min_df = 0, smooth_idf=True)
    tfidf_matrix_90 =  tf_90.fit_transform(corpus_90)
    feature_names_90 = tf_90.get_feature_names()
    
    dict_tfidf_90 = list()
    for doc in range(len(corpus_90)):
        feature_index_90 = tfidf_matrix_90[doc,:].nonzero()[1]
        tfidf_scores_90 = zip(feature_index_90, [tfidf_matrix_90[doc, x] for x in feature_index_90])
        temp_d_90 = dict()
        for w, s in [(feature_names_90[i], s) for (i, s) in tfidf_scores_90]:
            temp_d_90.update([(w,s)])
        dict_tfidf_90.append(temp_d_90)   
        
    intermediate = defaultdict(list)
    
    for subdict in dict_tfidf_90:
        for key, value in subdict.items():
            intermediate[key].append(value)
        
    list_tuples_key_value = list()
    for key, value in intermediate.items():
        list_tuples_key_value.append( (key, np.median(value)) )
    list_tuples_key_value.sort(key=lambda tup: tup[1])
    for k,v in enumerate(list_tuples_key_value):
        list_tuples_key_value[k] = v[0]
    list_of_lists_of_words_with_highest_tfidf.append(list_tuples_key_value[-50:]) 


#10) массив количества слов 2122 word_quantity_list       0
#11) бинарный массив 2122 логи/архивы ftr_logs_arch_list  1 
#12) бинарный массив 2122 изображения ftr_im_list         2
#13) массив кол-ва комментов 2122     num_comment_2122    3
#14) бинарный массив 2122 xml     ftr_xml_list            4
#15) массив долей глаголов 2122 ftr_VB_percentage_list    5
#16) бинарный массив STR 2122 target_steps_to_repr        6
#17) бинарный массив EOB 2122 target_exp_obs_beh          7
#18) бинарный массив ST 2122 ftr_stack_trace_list         8
#19) list_of_lists_of_words_with_highest_tfidf 14
#20) list_of_lists_of_words_with_highest_usual_frequensy 14
#21) binary_array_has_something 2122
 
binary_array_has_something = list()
for i in range(2122):
    binary_array_has_something.append(target_steps_to_repr[i]+target_exp_obs_beh[i])
                              
for i,item in enumerate(binary_array_has_something):
    if item > 1:
        binary_array_has_something[i] = 1
#print('binary_array_has_something')
#print(len(binary_array_has_something))
#print(binary_array_has_something)

from sklearn import tree
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest

#DT-----------------------------------------------------------------------start
#tf12 = TfidfVectorizer(input=corpus_90_all, ngram_range=(1,1), smooth_idf=True, stop_words = 'english')
#tfidf_matrix123 =  tf12.fit_transform(corpus_90_all)
#tfidf_matrix12 = tfidf_matrix123.toarray()
#feature_names = tf12.get_feature_names()
#
#
##feature_names = tf12.get_feature_names()
##print(len(feature_names))
#
#ch2 = SelectKBest(chi2, k=1500) #try to change that
#X_train_12 = ch2.fit_transform(tfidf_matrix12, binary_array_has_something)
#
#print('X_train_12')
#print(np.array(X_train_12).shape)
#print(X_train_12)
#
#selected_features_numbers_of_col = list()
#for key in np.asarray(tf12.get_feature_names())[ch2.get_support()]:
#    selected_features_numbers_of_col.append((tf12.vocabulary_).get(key))
#
#
#clf12 = tree.DecisionTreeClassifier(max_depth = 10, random_state = 42)
#clf12.fit(X_train_12, binary_array_has_something)
##print(clf12)
# 
#predicted12 = clf12.predict(X_train_12)
## summarize the fit of the model
#print(metrics.classification_report(binary_array_has_something, predicted12))
#print(metrics.confusion_matrix(binary_array_has_something, predicted12))
#print('-----------------------------------')
#    
#
#import pydotplus
#selected_terms_names = list()     
#for item in selected_features_numbers_of_col:
#    selected_terms_names.append(feature_names[item])
#    
##print('WHAT HAPPENS==============================================')
##print('selected_terms_names')
##print(len(selected_terms_names))
##print(selected_terms_names)
#
##clf00 = tree.DecisionTreeClassifier(random_state = 42)
##clf00.fit([[1,2,3],[4,5,6],[7,8,9]], [0,1,0])
##dot_data00 = tree.export_graphviz(clf00, out_file=None,
##                                feature_names = ['one','two','three'],
##                                class_names = ["bad","good"],
##                                filled = True,rounded  = True)
##graph00 = pydotplus.graph_from_dot_data(dot_data00)
##print(dot_data00)
##print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\') 
##print(graph00.get_node_list())
##print(graph00.get_edge_list())
##graph00.write_pdf("F:\\mike\\hse\\sem_2\\exactpro\\clustering\\TREE_2.pdf")
#
#
#
#dot_data = tree.export_graphviz(clf12, out_file=None,
#                                feature_names = selected_terms_names,
#                                class_names = ["'zero'","'one'"],
#                                filled = True,rounded  = True)
#graph = pydotplus.graph_from_dot_data(dot_data)
#print(dot_data)
#print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\') 
##print(graph.get_node_list())
##print(graph.get_edge_list())
#graph.write_pdf("F:\\mike\\hse\\sem_2\\exactpro\\clustering\\TREE_3.pdf")
#DT-----------------------------------------------------------------------start


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




list_vb_0 = list()
list_vb_1 = list()
list_vb_2 = list()
list_vb_3 = list()
list_vb_4 = list()
list_vb_5 = list()
list_vb_6 = list()
list_vb_7 = list()
list_vb_8 = list()
list_vb_9 = list()
list_vb_10 = list()
list_vb_11 = list()
list_vb_12 = list()
list_vb_13 = list()
list_vb_14 = list()
list_vb_15 = list()
for i,item in enumerate(labels_9):
    if item == 0:
        list_vb_0.append(list_of_vectorized_bugs_9_unnorm[i])
    if item == 1:
        list_vb_1.append(list_of_vectorized_bugs_9_unnorm[i])
    if item == 2:
        list_vb_2.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 3:
        list_vb_3.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 4:
        list_vb_4.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 5:
        list_vb_5.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 6:
        list_vb_6.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 7:
        list_vb_7.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 8:
        list_vb_8.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 9:
        list_vb_9.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 10:
        list_vb_10.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 11:
        list_vb_11.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 12:
        list_vb_12.append(list_of_vectorized_bugs_9_unnorm[i])
    if item == 13:
        list_vb_13.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 14:
        list_vb_14.append(list_of_vectorized_bugs_9_unnorm[i])    
    if item == 15:
        list_vb_15.append(list_of_vectorized_bugs_9_unnorm[i])    

list_vb = [list_vb_0,list_vb_1,list_vb_2,list_vb_3,list_vb_4,list_vb_5,list_vb_6,list_vb_7,list_vb_8,list_vb_9,list_vb_10,list_vb_11,list_vb_12,list_vb_13]
#,list_vb_14]
#,list_vb_15]

#print('============bad 57=============')
#print('bad 57%')
#list_vb_1_temp = np.array(list_vb_1)
#print("logs zips number")
#print(sum(list_vb_1_temp[:,1]))
#print("image number")
#print(sum(list_vb_1_temp[:,2]))
#print("xml")
#print(sum(list_vb_1_temp[:,4]))
#print('=============bad 12===========')
#print('bad 12%')
#list_vb_3_temp = np.array(list_vb_3)
#print("logs zips number")
#print(sum(list_vb_3_temp[:,1]))
#print("image number")
#print(sum(list_vb_3_temp[:,2]))
#print("xml")
#print(sum(list_vb_3_temp[:,4]))
#print('===========================')

#for i,item in enumerate(list_vb):
#    if len(item) == 0:
#        print(i)
#        print("no bugs in this cluster")
#        continue
#    print("-------CLUSTER-----------")
#    print(i)  
#    for j in range(9):
#        print(j)
##        print(item)
##        print("median")
#        temp_item = np.array(item)
#        temp_AC = temp_item[:,j]
#        print(np.median(temp_AC))
#
#count_0 = 0
#count_1 = 0
#count_2 = 0
#count_3 = 0
#count_4 = 0        
#count_5 = 0
#count_6 = 0
#count_7 = 0
#count_8 = 0
#count_9 = 0
#count_10 = 0
#count_11 = 0
#count_12 = 0
#count_13 = 0
#count_14 = 0        
#count_15 = 0
#for i in labels_9:
#    if i == 0:
#        count_0 += 1
#    if i == 1:
#        count_1 += 1
#    if i == 2:
#        count_2 += 1
#    if i == 3:
#        count_3 += 1
#    if i == 4:
#        count_4 += 1
#    if i == 5:
#        count_5 += 1
#    if i == 6:
#        count_6 += 1
#    if i == 7:
#        count_7 += 1
#    if i == 8:
#        count_8 += 1
#    if i == 9:
#        count_9 += 1
#    if i == 10:
#        count_10 += 1
#    if i == 11:
#        count_11 += 1
#    if i == 12:
#        count_12 += 1
#    if i == 13:
#        count_13 += 1
#    if i == 14:
#        count_14 += 1
#    if i == 15:
#        count_15 += 1
##        
#print("0--")
#print(count_0)        
#print("1--")
#print(count_1)
#print("2--")
#print(count_2)        
#print("3--")
#print(count_3)
#print("4--")
#print(count_4)        
#print("5--")
#print(count_5)
#print("6--")
#print(count_6)        
#print("7--")
#print(count_7)
#print("8--")
#print(count_8)        
#print("9--")
#print(count_9)
#print("10--")
#print(count_10)        
#print("11--")
#print(count_11)
#print("12--")
#print(count_12)        
#print("13--")
#print(count_13)
#print("14--")
#print(count_14)        
#print("15--")
#print(count_15)
#
#print("------------------------")


#======================================================================================
#======================================================================================
#======================================================================================
#======================================================================================
#new clust with frequent terms from clusters
def contain_freq_words_from_clust(list_to_check, list_with_freq_words, conf_level):
    freq_counter = 0.0
    n = len(list_to_check)
    if n == 0:
        return False
    for item in list_to_check:
        if item in list_with_freq_words:
            freq_counter = freq_counter + 1
    if (freq_counter/n > conf_level):
        return True
    else:
        return False

def contain_zip_log_im_xml(list_to_check, list_of_chain_words):
    n = len(list_to_check)
    if n == 0:
        return False
    return set(list_to_check).issuperset(set(list_of_chain_words))

def contain_str_eob(list_to_check, list_of_chain_words):
    n = len(list_to_check)
    if n == 0:
        return False
    return set(list_to_check).issuperset(set(list_of_chain_words))        


list_contain_zlix_0 = list()
list_contain_zlix_1 = list()
list_contain_zlix_2 = list()
list_contain_zlix_3 = list()
list_contain_zlix_4 = list()
list_contain_zlix_5 = list()
list_contain_zlix_6 = list()
list_contain_zlix_7 = list()
list_contain_zlix_8 = list()
list_contain_zlix_9 = list()
list_contain_zlix_10 = list()
list_contain_zlix_11 = list()
list_contain_zlix_12 = list()
list_contain_zlix_13 = list()
list_contain_zlix_14 = list()
list_contain_zlix_15 = list()
list_contain_zlix_16 = list()
list_contain_zlix_17 = list()
list_contain_zlix_18 = list()
list_contain_zlix_19 = list()
list_contain_zlix_20 = list()
list_contain_zlix_21 = list()
list_contain_zlix_22 = list()
list_contain_zlix_23 = list()
list_contain_zlix_24 = list()
list_contain_zlix_25 = list()

pat_zlix_0 = ['attached','following','file','deployment','fails','similar',
              'receives','jconsole','start','logged']
pat_zlix_1 = ['attached','start']
pat_zlix_2 = ['attached','shot']
pat_zlix_3 = ['attached','configuration']
pat_zlix_4 = ['following','deployment']
pat_zlix_5 = ['following','dependency']
pat_zlix_6 = ['following','trying']
pat_zlix_7 = ['following','configuration']
pat_zlix_8 = ['following','producer']
pat_zlix_9 = ['following','directory']
pat_zlix_10 = ['following','library']
pat_zlix_11 = ['file','broker']
pat_zlix_12 = ['file','deploy']
pat_zlix_13 = ['file','element']
pat_zlix_14 = ['file','web']
pat_zlix_15 = ['file','server']
pat_zlix_16 = ['deployment','like']
pat_zlix_17 = ['deployment','archived']
pat_zlix_18 = ['deployment','according']
pat_zlix_19 = ['fails','intermittently']
pat_zlix_20 = ['fails','configuration']
pat_zlix_21 = ['fails','branch']
pat_zlix_22 = ['fails','client']
pat_zlix_23 = ['fails','test']
pat_zlix_24 = ['fails','directory']
pat_zlix_25 = ['logged']

for i in range(2122):
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_0):
        list_contain_zlix_0.append(1)
    else:
        list_contain_zlix_0.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_1):
        list_contain_zlix_1.append(1)
    else:
        list_contain_zlix_1.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_2):
        list_contain_zlix_2.append(1)
    else:
        list_contain_zlix_2.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_3):
        list_contain_zlix_3.append(1)
    else:
        list_contain_zlix_3.append(0)        
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_4):
        list_contain_zlix_4.append(1)
    else:
        list_contain_zlix_4.append(0)       
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_5):
        list_contain_zlix_5.append(1)
    else:
        list_contain_zlix_5.append(0)       
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_6):
        list_contain_zlix_6.append(1)
    else:
        list_contain_zlix_6.append(0)       
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_7):
        list_contain_zlix_7.append(1)
    else:
        list_contain_zlix_7.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_8):
        list_contain_zlix_8.append(1)
    else:
        list_contain_zlix_8.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_9):
        list_contain_zlix_9.append(1)
    else:
        list_contain_zlix_9.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_10):
        list_contain_zlix_10.append(1)
    else:
        list_contain_zlix_10.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_11):
        list_contain_zlix_11.append(1)
    else:
        list_contain_zlix_11.append(0)    
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_12):
        list_contain_zlix_12.append(1)
    else:
        list_contain_zlix_12.append(0)    
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_13):
        list_contain_zlix_13.append(1)
    else:
        list_contain_zlix_13.append(0)    
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_14):
        list_contain_zlix_14.append(1)
    else:
        list_contain_zlix_14.append(0)       
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_15):
        list_contain_zlix_15.append(1)
    else:
        list_contain_zlix_15.append(0)       
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_16):
        list_contain_zlix_16.append(1)
    else:
        list_contain_zlix_16.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_17):
        list_contain_zlix_17.append(1)
    else:
        list_contain_zlix_17.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_18):
        list_contain_zlix_18.append(1)
    else:
        list_contain_zlix_18.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_19):
        list_contain_zlix_19.append(1)
    else:
        list_contain_zlix_19.append(0)
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_20):
        list_contain_zlix_20.append(1)
    else:
        list_contain_zlix_20.append(0)    
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_21):
        list_contain_zlix_21.append(1)
    else:
        list_contain_zlix_21.append(0)    
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_22):
        list_contain_zlix_22.append(1)
    else:
        list_contain_zlix_22.append(0)  
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_23):
        list_contain_zlix_23.append(1)
    else:
        list_contain_zlix_23.append(0)    
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_24):
        list_contain_zlix_24.append(1)
    else:
        list_contain_zlix_24.append(0)    
    if contain_zip_log_im_xml(list_tokens_after_lem[i],pat_zlix_25):
        list_contain_zlix_25.append(1)
    else:
        list_contain_zlix_25.append(0)


list_contain_str_eob_0 = list()        
list_contain_str_eob_1 = list()
list_contain_str_eob_2 = list()        
list_contain_str_eob_3 = list()        
list_contain_str_eob_4 = list()
list_contain_str_eob_5 = list()
list_contain_str_eob_6 = list()
list_contain_str_eob_7 = list()
list_contain_str_eob_8 = list()        
list_contain_str_eob_9 = list()        
list_contain_str_eob_10 = list()
list_contain_str_eob_11 = list()
list_contain_str_eob_12 = list()
list_contain_str_eob_13 = list()
list_contain_str_eob_14 = list()        
list_contain_str_eob_15 = list()
list_contain_str_eob_16 = list() 

pat_str_eob_0 = ['reproduce','expected','click','start','usecase','websphere',
                 'topic','choose','increase','owner']
pat_str_eob_1 = ['reproduce','step']                 
pat_str_eob_2 = ['reproduce','step','result']
pat_str_eob_3 = ['reproduce','directory']
pat_str_eob_4 = ['reproduce','command','using']
pat_str_eob_5 = ['reproduce','login']
pat_str_eob_6 = ['reproduce','restart']
pat_str_eob_7 = ['reproduce','click']
pat_str_eob_8 = ['expected','actual']
pat_str_eob_9 = ['start','stop']
pat_str_eob_10 = ['start','problem']
pat_str_eob_11 = ['start','note']
pat_str_eob_12 = ['start','connect','command']
pat_str_eob_13 = ['choose','jboss']
pat_str_eob_14 = ['choose','qa']
pat_str_eob_15 = ['increase','store']
pat_str_eob_16 = ['reproduce','following','expected','start','click','file'] #common for both str_eob and zlix


for i in range(2122):
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_0):
        list_contain_str_eob_0.append(1)
    else:
        list_contain_str_eob_0.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_1):
        list_contain_str_eob_1.append(1)
    else:
        list_contain_str_eob_1.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_2):
        list_contain_str_eob_2.append(1)
    else:
        list_contain_str_eob_2.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_3):
        list_contain_str_eob_3.append(1)
    else:
        list_contain_str_eob_3.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_4):
        list_contain_str_eob_4.append(1)
    else:
        list_contain_str_eob_4.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_5):
        list_contain_str_eob_5.append(1)
    else:
        list_contain_str_eob_5.append(0)    
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_6):
        list_contain_str_eob_6.append(1)
    else:
        list_contain_str_eob_6.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_7):
        list_contain_str_eob_7.append(1)
    else:
        list_contain_str_eob_7.append(0)    
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_8):
        list_contain_str_eob_8.append(1)
    else:
        list_contain_str_eob_8.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_9):
        list_contain_str_eob_9.append(1)
    else:
        list_contain_str_eob_9.append(0)    
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_10):
        list_contain_str_eob_10.append(1)
    else:
        list_contain_str_eob_10.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_11):
        list_contain_str_eob_11.append(1)
    else:
        list_contain_str_eob_11.append(0)    
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_12):
        list_contain_str_eob_12.append(1)
    else:
        list_contain_str_eob_12.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_13):
        list_contain_str_eob_13.append(1)
    else:
        list_contain_str_eob_13.append(0)    
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_14):
        list_contain_str_eob_14.append(1)
    else:
        list_contain_str_eob_14.append(0)
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_15):
        list_contain_str_eob_15.append(1)
    else:
        list_contain_str_eob_15.append(0)    
    if contain_str_eob(list_tokens_after_lem[i],pat_str_eob_16):
        list_contain_str_eob_16.append(1)
    else:
        list_contain_str_eob_16.append(0)    
        
        
        
        
list_contain_freq_words_from_clust_0 = list()
list_contain_freq_words_from_clust_1 = list()
list_contain_freq_words_from_clust_2 = list()
list_contain_freq_words_from_clust_3 = list()
list_contain_freq_words_from_clust_4 = list()
list_contain_freq_words_from_clust_5 = list()
list_contain_freq_words_from_clust_6 = list()
list_contain_freq_words_from_clust_7 = list()
list_contain_freq_words_from_clust_8 = list()
list_contain_freq_words_from_clust_9 = list()
list_contain_freq_words_from_clust_10 = list()
list_contain_freq_words_from_clust_11 = list()
list_contain_freq_words_from_clust_12 = list()
list_contain_freq_words_from_clust_13 = list()

perc_temp = 0.1
for i in range(2122):
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[0],perc_temp):
        list_contain_freq_words_from_clust_0.append(1)
    else:
        list_contain_freq_words_from_clust_0.append(0)
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[1],perc_temp):
        list_contain_freq_words_from_clust_1.append(1)
    else:
        list_contain_freq_words_from_clust_1.append(0)
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[2],perc_temp):
        list_contain_freq_words_from_clust_2.append(1)
    else:
        list_contain_freq_words_from_clust_2.append(0)
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[3],perc_temp):
        list_contain_freq_words_from_clust_3.append(1)
    else:
        list_contain_freq_words_from_clust_3.append(0)        
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[4],perc_temp):
        list_contain_freq_words_from_clust_4.append(1)
    else:
        list_contain_freq_words_from_clust_4.append(0)       
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[5],perc_temp):
        list_contain_freq_words_from_clust_5.append(1)
    else:
        list_contain_freq_words_from_clust_5.append(0)       
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[6],perc_temp):
        list_contain_freq_words_from_clust_6.append(1)
    else:
        list_contain_freq_words_from_clust_6.append(0)       
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[7],perc_temp):
        list_contain_freq_words_from_clust_7.append(1)
    else:
        list_contain_freq_words_from_clust_7.append(0)
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[8],perc_temp):
        list_contain_freq_words_from_clust_8.append(1)
    else:
        list_contain_freq_words_from_clust_8.append(0)
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[9],perc_temp):
        list_contain_freq_words_from_clust_9.append(1)
    else:
        list_contain_freq_words_from_clust_9.append(0)
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[10],perc_temp):
        list_contain_freq_words_from_clust_10.append(1)
    else:
        list_contain_freq_words_from_clust_10.append(0)
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[11],perc_temp):
        list_contain_freq_words_from_clust_11.append(1)
    else:
        list_contain_freq_words_from_clust_11.append(0)    
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[12],perc_temp):
        list_contain_freq_words_from_clust_12.append(1)
    else:
        list_contain_freq_words_from_clust_12.append(0)    
    if contain_freq_words_from_clust(list_tokens_after_lem[i],
                                        list_of_lists_of_words_with_highest_tfidf[13],perc_temp):
        list_contain_freq_words_from_clust_13.append(1)
    else:
        list_contain_freq_words_from_clust_13.append(0)    

java_code_vector = [] 
file = open('java_code.txt') 
for line in file:
    java_code_vector.append(int(line))

#print('JAVA CODE')
#print(java_code_vector)
        
list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW = list()
list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print = list()
for i in range(2122):
    list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW.append([ftr_logs_arch_list[i],
                                    ftr_im_list[i],
                                    ftr_xml_list[i],
                                    target_steps_to_repr[i],
                                    target_exp_obs_beh[i],
                                    ftr_stack_trace_list[i],
                                    java_code_vector[i],
                                    list_contain_freq_words_from_clust_0[i],
                                    list_contain_freq_words_from_clust_2[i],
                                    list_contain_freq_words_from_clust_3[i],
                                    list_contain_freq_words_from_clust_5[i],
                                    list_contain_freq_words_from_clust_6[i],
                                    list_contain_freq_words_from_clust_7[i],
                                    list_contain_freq_words_from_clust_8[i],
                                    list_contain_freq_words_from_clust_9[i],
                                    list_contain_freq_words_from_clust_10[i],
                                    list_contain_freq_words_from_clust_11[i],
                                    list_contain_freq_words_from_clust_12[i],
                                    list_contain_freq_words_from_clust_13[i],
                                    list_contain_zlix_0[i],
                                    list_contain_zlix_1[i],
                                    list_contain_zlix_2[i],
                                    list_contain_zlix_3[i],
                                    list_contain_zlix_4[i],
                                    list_contain_zlix_5[i],
                                    list_contain_zlix_6[i],
                                    list_contain_zlix_7[i],
                                    list_contain_zlix_8[i],
                                    list_contain_zlix_9[i],
                                    list_contain_zlix_10[i],
                                    list_contain_zlix_11[i],
                                    list_contain_zlix_12[i],
                                    list_contain_zlix_13[i],
                                    list_contain_zlix_14[i],
                                    list_contain_zlix_15[i],
                                    list_contain_zlix_16[i],
                                    list_contain_zlix_17[i],
                                    list_contain_zlix_18[i],
                                    list_contain_zlix_19[i],
                                    list_contain_zlix_20[i],
                                    list_contain_zlix_21[i],
                                    list_contain_zlix_22[i],
                                    list_contain_zlix_23[i],
                                    list_contain_zlix_24[i],
                                    list_contain_zlix_25[i],
                                    list_contain_str_eob_0[i],        
                                    list_contain_str_eob_1[i],
                                    list_contain_str_eob_2[i],        
                                    list_contain_str_eob_3[i],        
                                    list_contain_str_eob_4[i],
                                    list_contain_str_eob_5[i],
                                    list_contain_str_eob_6[i],
                                    list_contain_str_eob_7[i],
                                    list_contain_str_eob_8[i],        
                                    list_contain_str_eob_9[i],        
                                    list_contain_str_eob_10[i],
                                    list_contain_str_eob_11[i],
                                    list_contain_str_eob_12[i],
                                    list_contain_str_eob_13[i],
                                    list_contain_str_eob_14[i],        
                                    list_contain_str_eob_15[i],
                                    list_contain_str_eob_16[i] 
                                    ])
    list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print.append([ ftr_logs_arch_list[i],
                                    ftr_im_list[i],
                                    ftr_xml_list[i],
                                    target_steps_to_repr[i],
                                    target_exp_obs_beh[i],
                                    ftr_stack_trace_list[i],
                                    java_code_vector[i],
                                    list_contain_freq_words_from_clust_0[i],
                                    list_contain_freq_words_from_clust_2[i],
                                    list_contain_freq_words_from_clust_3[i],
                                    list_contain_freq_words_from_clust_5[i],
                                    list_contain_freq_words_from_clust_6[i],
                                    list_contain_freq_words_from_clust_7[i],
                                    list_contain_freq_words_from_clust_8[i],
                                    list_contain_freq_words_from_clust_9[i],
                                    list_contain_freq_words_from_clust_10[i],
                                    list_contain_freq_words_from_clust_11[i],
                                    list_contain_freq_words_from_clust_12[i],
                                    list_contain_freq_words_from_clust_13[i],
                                    list_contain_zlix_0[i],
                                    list_contain_zlix_1[i],
                                    list_contain_zlix_2[i],
                                    list_contain_zlix_3[i],
                                    list_contain_zlix_4[i],
                                    list_contain_zlix_5[i],
                                    list_contain_zlix_6[i],
                                    list_contain_zlix_7[i],
                                    list_contain_zlix_8[i],
                                    list_contain_zlix_9[i],
                                    list_contain_zlix_10[i],
                                    list_contain_zlix_11[i],
                                    list_contain_zlix_12[i],
                                    list_contain_zlix_13[i],
                                    list_contain_zlix_14[i],
                                    list_contain_zlix_15[i],
                                    list_contain_zlix_16[i],
                                    list_contain_zlix_17[i],
                                    list_contain_zlix_18[i],
                                    list_contain_zlix_19[i],
                                    list_contain_zlix_20[i],
                                    list_contain_zlix_21[i],
                                    list_contain_zlix_22[i],
                                    list_contain_zlix_23[i],
                                    list_contain_zlix_24[i],
                                    list_contain_zlix_25[i],
                                    list_contain_str_eob_0[i],        
                                    list_contain_str_eob_1[i],
                                    list_contain_str_eob_2[i],        
                                    list_contain_str_eob_3[i],        
                                    list_contain_str_eob_4[i],
                                    list_contain_str_eob_5[i],
                                    list_contain_str_eob_6[i],
                                    list_contain_str_eob_7[i],
                                    list_contain_str_eob_8[i],        
                                    list_contain_str_eob_9[i],        
                                    list_contain_str_eob_10[i],
                                    list_contain_str_eob_11[i],
                                    list_contain_str_eob_12[i],
                                    list_contain_str_eob_13[i],
                                    list_contain_str_eob_14[i],        
                                    list_contain_str_eob_15[i],
                                    list_contain_str_eob_16[i]
                                    ])

AC_model = KMeans(n_clusters=18, random_state=7).fit(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW)
labels_12 = AC_model.labels_

print("Siluette index")
print(metrics.silhouette_score(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW,
                               labels_12, metric = 'euclidean'))

myset_12 = set(labels_12)
print("myset_12")
print(myset_12)
#print("labels_12")
#print(len(labels_12))
#print(labels_12)

list_vb_0 = list()
list_vb_1 = list()
list_vb_2 = list()
list_vb_3 = list()
list_vb_4 = list()
list_vb_5 = list()
list_vb_6 = list()
list_vb_7 = list()
list_vb_8 = list()
list_vb_9 = list()
list_vb_10 = list()
list_vb_11 = list()
list_vb_12 = list()
list_vb_13 = list()
list_vb_14 = list()
list_vb_15 = list()
list_vb_16 = list()
list_vb_17 = list()
list_vb_18 = list()
list_vb_19 = list()

for i,item in enumerate(labels_12):
    if item == 0:
        list_vb_0.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])
    if item == 1:
        list_vb_1.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])
    if item == 2:
        list_vb_2.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 3:
        list_vb_3.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 4:
        list_vb_4.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 5:
        list_vb_5.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 6:
        list_vb_6.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 7:
        list_vb_7.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 8:
        list_vb_8.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 9:
        list_vb_9.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 10:
        list_vb_10.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 11:
        list_vb_11.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 12:
        list_vb_12.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])
    if item == 13:
        list_vb_13.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 14:
        list_vb_14.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 15:
        list_vb_15.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 16:
        list_vb_16.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 17:
        list_vb_17.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])
    if item == 18:
        list_vb_18.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
    if item == 19:
        list_vb_19.append(list_of_vectorized_bugs_9_norm_quantw_comm_verbs_NEW_for_print[i])    
                
        
list_vb = [list_vb_0,list_vb_1,list_vb_2,list_vb_3,list_vb_4,list_vb_5,list_vb_6,list_vb_7,list_vb_8,list_vb_9,list_vb_10,
           list_vb_11,list_vb_12,list_vb_13,list_vb_14,list_vb_15,list_vb_16,
           list_vb_17,list_vb_18,list_vb_19]
#,list_vb_14]
#,list_vb_15]

#print('============bad 57=============')
#print('bad 57%')
#list_vb_1_temp = np.array(list_vb_1)
#print("logs zips number")
#print(sum(list_vb_1_temp[:,1]))
#print("image number")
#print(sum(list_vb_1_temp[:,2]))
#print("xml")
#print(sum(list_vb_1_temp[:,4]))
#print('=============bad 12===========')
#print('bad 12%')
#list_vb_3_temp = np.array(list_vb_3)
#print("logs zips number")
#print(sum(list_vb_3_temp[:,1]))
#print("image number")
#print(sum(list_vb_3_temp[:,2]))
#print("xml")
#print(sum(list_vb_3_temp[:,4]))
#print('===========================')


count_0 = 0
count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0        
count_5 = 0
count_6 = 0
count_7 = 0
count_8 = 0
count_9 = 0
count_10 = 0
count_11 = 0
count_12 = 0
count_13 = 0
count_14 = 0        
count_15 = 0
count_16 = 0
count_17 = 0
count_18 = 0
count_19 = 0
for i in labels_12:
    if i == 0:
        count_0 += 1
    if i == 1:
        count_1 += 1
    if i == 2:
        count_2 += 1
    if i == 3:
        count_3 += 1
    if i == 4:
        count_4 += 1
    if i == 5:
        count_5 += 1
    if i == 6:
        count_6 += 1
    if i == 7:
        count_7 += 1
    if i == 8:
        count_8 += 1
    if i == 9:
        count_9 += 1
    if i == 10:
        count_10 += 1
    if i == 11:
        count_11 += 1
    if i == 12:
        count_12 += 1
    if i == 13:
        count_13 += 1
    if i == 14:
        count_14 += 1
    if i == 15:
        count_15 += 1
    if i == 16:
        count_16 += 1
    if i == 17:
        count_17 += 1
    if i == 18:
        count_18 += 1
    if i == 19:
        count_19 += 1
  
        
        
#        
print("0--")
print(count_0)        
print("1--")
print(count_1)
print("2--")
print(count_2)        
print("3--")
print(count_3)
print("4--")
print(count_4)        
print("5--")
print(count_5)
print("6--")
print(count_6)        
print("7--")
print(count_7)
print("8--")
print(count_8)        
print("9--")
print(count_9)
print("10--")
print(count_10)        
print("11--")
print(count_11)
print("12--")
print(count_12)        
print("13--")
print(count_13)
print("14--")
print(count_14)        
print("15--")
print(count_15)
print("16--")
print(count_16)
print("17--")
print(count_17)        
print("18--")
print(count_18)
print("19--")
print(count_19)        

print("------------------------")
















#for i in labels_9:
#    print(i)
        
#set_im_BAD =  set_list_of_pos_69_percent_HAS_NOTHING_BUGS.intersection(set_list_pos_im)
#set_arch_BAD = set_list_of_pos_69_percent_HAS_NOTHING_BUGS.intersection(set_list_pos_arch)
#set_log_ldif_war_BAD =  set_list_of_pos_69_percent_HAS_NOTHING_BUGS.intersection(set_list_log_ldif_war) 
#set_xml_BAD = set_list_of_pos_69_percent_HAS_NOTHING_BUGS.intersection(set_list_pos_xml)
#set_see_attached_BAD = set_list_of_pos_69_percent_HAS_NOTHING_BUGS.intersection(set_list_pos_see_attached)
#set_UNION_HAS_AT_LEAST_ONE_BAD = set_im_BAD.union(set_arch_BAD)
#set_UNION_HAS_AT_LEAST_ONE_BAD = set_UNION_HAS_AT_LEAST_ONE_BAD.union(set_log_ldif_war_BAD)
#set_UNION_HAS_AT_LEAST_ONE_BAD = set_UNION_HAS_AT_LEAST_ONE_BAD.union(set_xml_BAD)
#set_UNION_HAS_AT_LEAST_ONE_BAD = set_UNION_HAS_AT_LEAST_ONE_BAD.union(set_see_attached_BAD) #final
#
#
#set_im_GOOD =  set_list_of_pos_HAS_SOMETHING_BUGS.intersection(set_list_pos_im)
#set_arch_GOOD = set_list_of_pos_HAS_SOMETHING_BUGS.intersection(set_list_pos_arch)
#set_log_ldif_war_GOOD =  set_list_of_pos_HAS_SOMETHING_BUGS.intersection(set_list_log_ldif_war) 
#set_xml_GOOD = set_list_of_pos_HAS_SOMETHING_BUGS.intersection(set_list_pos_xml)
#set_see_attached_GOOD = set_list_of_pos_HAS_SOMETHING_BUGS.intersection(set_list_pos_see_attached)
#set_UNION_HAS_AT_LEAST_ONE_GOOD = set_im_GOOD.union(set_arch_GOOD)
#set_UNION_HAS_AT_LEAST_ONE_GOOD = set_UNION_HAS_AT_LEAST_ONE_GOOD.union(set_log_ldif_war_GOOD)
#set_UNION_HAS_AT_LEAST_ONE_GOOD = set_UNION_HAS_AT_LEAST_ONE_GOOD.union(set_xml_GOOD)
#set_UNION_HAS_AT_LEAST_ONE_GOOD = set_UNION_HAS_AT_LEAST_ONE_GOOD.union(set_see_attached_GOOD) #final
#
#
#
#print('Length BAD BUGS')
#print(len(set_list_of_pos_69_percent_HAS_NOTHING_BUGS))
#print('Length set_im_BAD')
#print(len(set_im_BAD))
#print('Length set_arch_BAD')
#print(len(set_arch_BAD))
#print('Length set_log_ldif_war_BAD')
#print(len(set_log_ldif_war_BAD))
#print('Length set_xml_BAD')
#print(len(set_xml_BAD))
#print('At least one good in BAD')
#print(len(set_UNION_HAS_AT_LEAST_ONE_BAD))
#
#print('Length GOOD BUGS')
#print(len(set_list_of_pos_HAS_SOMETHING_BUGS))
#print('Length set_im_GOOD')
#print(len(set_im_GOOD))
#print('Length set_arch_GOOD')
#print(len(set_arch_GOOD))
#print('Length set_log_ldif_war_GOOD')
#print(len(set_log_ldif_war_GOOD))
#print('Length set_xml_GOOD')
#print(len(set_xml_GOOD))
#print('At least one good in GOOD')
#print(len(set_UNION_HAS_AT_LEAST_ONE_GOOD))


#print(list_pos_im)
#print(list_pos_arch)
#print(list_pos_xml)
#print(pos_attached_BAD)
#print(pos_see_BAD)
#print(pos_attached_GOOD)
#print(pos_see_GOOD)

#print('--------------------------BAD----------------------')
#print(sorted_toks_BAD)
#print('--------------------------GOOD----------------------')
#print(sorted_toks_GOOD)  

#corpus_BAD = list()
#for item in list_tokens_after_lem_HAS_NOTHING_BUGS:
#    corpus_BAD.append(' '.join(item))                
#corpus_GOOD = list()
#for item in list_tokens_after_lem_HAS_SOMETHING_BUGS:
#    corpus_GOOD.append(' '.join(item))
#    
#tf = TfidfVectorizer(input=corpus_BAD, analyzer='word', ngram_range=(1,1),
#                     min_df = 0, smooth_idf=True)
#print(corpus_BAD)
#tfidf_matrix =  tf.fit_transform(corpus_BAD)
#feature_names = tf.get_feature_names()
#doc = 0
#feature_index = tfidf_matrix[doc,:].nonzero()[1]
#tfidf_scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])
#print('-----------------------------------BAD TFIDF-------------------------')
#for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
#    print((w,s))
#
#tf = TfidfVectorizer(input=corpus_GOOD, analyzer='word', ngram_range=(1,1),
#                     min_df = 0, smooth_idf=True)
#tfidf_matrix =  tf.fit_transform(corpus_GOOD)
#feature_names = tf.get_feature_names()
#doc = 0
#feature_index = tfidf_matrix[doc,:].nonzero()[1]
#tfidf_scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])
#print()
#print()
#print('-----------------------------------GOOD TFIDF-------------------------')
#for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
#    print((w,s))

#print('Median BAD BUGS')
#print(np.median(list_lens_HAS_NOTHING_BUGS))
#print('Mean BAD BUGS')
#print(np.mean(list_lens_HAS_NOTHING_BUGS))
#print('Std BAD BUGS')
#print(np.std(list_lens_HAS_NOTHING_BUGS))
#diff_for_bins = (max(list_lens_HAS_NOTHING_BUGS) - min(list_lens_HAS_NOTHING_BUGS))/40
#temp_min = min(list_lens_HAS_NOTHING_BUGS)
#temp_max = max(list_lens_HAS_NOTHING_BUGS)
#pd.Series(list_lens_HAS_NOTHING_BUGS).plot(title = 'Bad bugs lengths distribution', kind='hist',
#          bins=[temp_min,temp_min+diff_for_bins,temp_min+2*diff_for_bins,
#          temp_min+3*diff_for_bins, temp_min+4*diff_for_bins,
#          temp_min+5*diff_for_bins,temp_min+6*diff_for_bins,temp_min+7*diff_for_bins,
#          temp_min+8*diff_for_bins,temp_min+9*diff_for_bins,
#          temp_min+10*diff_for_bins, temp_min+11*diff_for_bins,
#          temp_min+12*diff_for_bins,temp_min+13*diff_for_bins,
#          temp_min+14*diff_for_bins, temp_min+15*diff_for_bins,
#          temp_min+16*diff_for_bins, temp_min+17*diff_for_bins, temp_min+18*diff_for_bins,
#          temp_min+19*diff_for_bins,
#          temp_min+20*diff_for_bins, temp_min+21*diff_for_bins,
#          temp_min+22*diff_for_bins,temp_min+23*diff_for_bins,temp_min+24*diff_for_bins,
#          temp_min+25*diff_for_bins,temp_min+26*diff_for_bins,
#          temp_min+27*diff_for_bins, temp_min+28*diff_for_bins,
#          temp_min+29*diff_for_bins,temp_min+30*diff_for_bins,
#          temp_min+31*diff_for_bins, temp_min+32*diff_for_bins,
#          temp_min+33*diff_for_bins, temp_min+34*diff_for_bins, temp_min+35*diff_for_bins,
#          temp_min+36*diff_for_bins, temp_min+37*diff_for_bins, temp_min+38*diff_for_bins, temp_max])

#print('Median GOOD BUGS')
#print(np.median(list_lens_HAS_SOMETHING_BUGS))
#print('Mean GOOD BUGS')
#print(np.mean(list_lens_HAS_SOMETHING_BUGS))
#print('Std GOOD BUGS')
#print(np.std(list_lens_HAS_SOMETHING_BUGS))
#diff_for_bins = (max(list_lens_HAS_SOMETHING_BUGS) - min(list_lens_HAS_SOMETHING_BUGS))/50
#temp_min = min(list_lens_HAS_SOMETHING_BUGS)
#temp_max = max(list_lens_HAS_SOMETHING_BUGS)
#pd.Series(list_lens_HAS_SOMETHING_BUGS).plot(title = 'Good bugs lengths distribution', kind='hist',
#          bins=[temp_min,temp_min+diff_for_bins,temp_min+2*diff_for_bins,
#          temp_min+3*diff_for_bins, temp_min+4*diff_for_bins,
#          temp_min+5*diff_for_bins,temp_min+6*diff_for_bins,temp_min+7*diff_for_bins,
#          temp_min+8*diff_for_bins,temp_min+9*diff_for_bins,
#          temp_min+10*diff_for_bins, temp_min+11*diff_for_bins,
#          temp_min+12*diff_for_bins,temp_min+13*diff_for_bins,
#          temp_min+14*diff_for_bins, temp_min+15*diff_for_bins,
#          temp_min+16*diff_for_bins, temp_min+17*diff_for_bins, temp_min+18*diff_for_bins,
#          temp_min+19*diff_for_bins,
#          temp_min+20*diff_for_bins, temp_min+21*diff_for_bins,
#          temp_min+22*diff_for_bins,temp_min+23*diff_for_bins,temp_min+24*diff_for_bins,
#          temp_min+25*diff_for_bins,temp_min+26*diff_for_bins,
#          temp_min+27*diff_for_bins, temp_min+28*diff_for_bins,
#          temp_min+29*diff_for_bins,temp_min+30*diff_for_bins,
#          temp_min+31*diff_for_bins, temp_min+32*diff_for_bins,
#          temp_min+33*diff_for_bins, temp_min+34*diff_for_bins, temp_min+35*diff_for_bins,
#          temp_min+36*diff_for_bins, temp_min+37*diff_for_bins, temp_min+38*diff_for_bins, 
#          temp_min+39*diff_for_bins, temp_min+40*diff_for_bins, temp_min+41*diff_for_bins,
#          temp_min+42*diff_for_bins, temp_min+43*diff_for_bins, temp_min+44*diff_for_bins,
#          temp_min+45*diff_for_bins, temp_min+46*diff_for_bins, temp_min+47*diff_for_bins,
#          temp_min+48*diff_for_bins, temp_max])
##--------------------------------------------------------------------------
#list_VB_0 = list()
#list_VB_1 = list()
#list_VB_2 = list()
#list_VB_3 = list()
#list_VB_4 = list()
#list_VB_5 = list()
#list_VB_6 = list()
#list_VB_7 = list()
#for item_label, item_VB in zip(labels, list_of_VB):
#    if item_label == 0:
#        list_VB_0.append(item_VB)
#    if item_label == 1:
#        list_VB_1.append(item_VB)
#    if item_label == 2:
#        list_VB_2.append(item_VB)
#    if item_label == 3:
#        list_VB_3.append(item_VB)
#    if item_label == 4:
#        list_VB_4.append(item_VB)
#    if item_label == 5:
#        list_VB_5.append(item_VB)
#    if item_label == 6:
#        list_VB_6.append(item_VB)
##    if item_label == 7:
##        list_VB_7.append(item_VB)



#def percent_of_zeros_and_ones(my_list):
#    temp_len = len(my_list)
#    temp_counter_0 = 0
#    temp_counter_1 = 0
#    for item in my_list:
#        if(item == 0):
#            temp_counter_0 = temp_counter_0 + 1
#        if(item == 1):
#            temp_counter_1 = temp_counter_1 + 1
#    return [temp_counter_0 / temp_len, temp_counter_1 / temp_len]
##            
#def percent_of_40_4060_60(my_list):
#    temp_len = len(my_list)
#    temp_counter_0 = 0
#    temp_counter_1 = 0
#    temp_counter_2 = 0
#    for item in my_list:
#        if(item <= 0.4):
#            temp_counter_0 = temp_counter_0 + 1
#        if ((item > 0.4) and (item < 0.6)):
#            temp_counter_1 = temp_counter_1 + 1
#        if item >= 0.6:
#            temp_counter_2 = temp_counter_2 + 1
###    print('temp_counter_0')
###    print(temp_counter_0)
###    print('temp_counter_1')
###    print(temp_counter_1)
###    print('temp_counter_2')
###    print(temp_counter_2)
###    print('temp_len')
###    print(temp_len)
#    return [temp_counter_0 / temp_len, temp_counter_1 / temp_len, temp_counter_2 / temp_len]
##            
###---------------------------------------------------------------------------        
#print('---------------------------------------------------------------------')
#print('Cluster 0 info')
#print('Length cluster 0')
#print(len(list_VB_0))
#print('Percentage of cluster 0 in all bugs')
#print(len(list_VB_0) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_0:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
##-----------------------------------------------------------------------
#print('---------------------------------------------------------------------')
#print('Cluster 1 info')
#print('Length cluster 1')
#print(len(list_VB_1))
#print('Percentage of cluster 1 in all bugs')
#print(len(list_VB_1) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_1:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
#print('---------------------------------------------------------------------')
#print('Cluster 2 info')
#print('Length cluster 2')
#print(len(list_VB_2))
#print('Percentage of cluster 2 in all bugs')
#print(len(list_VB_2) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_2:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
#print('---------------------------------------------------------------------')
#print('Cluster 3 info')
#print('Length cluster 3')
#print(len(list_VB_3))
#print('Percentage of cluster 3 in all bugs')
#print(len(list_VB_3) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_3:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
#print('---------------------------------------------------------------------')
#print('Cluster 4 info')
#print('Length cluster 4')
#print(len(list_VB_4))
#print('Percentage of cluster 4 in all bugs')
#print(len(list_VB_4) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_4:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
#print('---------------------------------------------------------------------')
#print('Cluster 5 info')
#print('Length cluster 5')
#print(len(list_VB_5))
#print('Percentage of cluster 5 in all bugs')
#print(len(list_VB_5) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_5:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
#print('---------------------------------------------------------------------')
#print('Cluster 6 info')
#print('Length cluster 6')
#print(len(list_VB_6))
#print('Percentage of cluster 6 in all bugs')
#print(len(list_VB_6) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_6:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
#print('---------------------------------------------------------------------')
#print('Cluster 7 info')
#print('Length cluster 7')
#print(len(list_VB_7))
#print('Percentage of cluster 7 in all bugs')
#print(len(list_VB_7) / 2122)
#temp_ST_list = list()
#temp_RB_list = list()
#temp_STR_list = list()
#temp_EOB_list = list()
#for item in list_VB_7:
#    temp_ST_list.append(item[0])
#    temp_RB_list.append(item[1])
#    temp_STR_list.append(item[2])
#    temp_EOB_list.append(item[3])
#
#print('Stack trace percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_ST_list)[0])
#print(percent_of_zeros_and_ones(temp_ST_list)[1])  
#print('Stack trace mean')
#print(np.mean(temp_ST_list))        
#print('Stack trace median')
#print(np.median(temp_ST_list))
#print('Stack trace std')
#print(np.std(temp_ST_list))
#
#print('Readability percent of <40 / 40-60 / >60')
#print(percent_of_40_4060_60(temp_RB_list)[0])
#print(percent_of_40_4060_60(temp_RB_list)[1])
#print(percent_of_40_4060_60(temp_RB_list)[2])    
#print('Readability mean')
#print(np.mean(temp_RB_list))        
#print('Readability median')
#print(np.median(temp_RB_list))
#print('Readability std')
#print(np.std(temp_RB_list))
#
#print('STR percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_STR_list)[0])
#print(percent_of_zeros_and_ones(temp_STR_list)[1])  
#print('STR mean')
#print(np.mean(temp_STR_list))        
#print('STR median')
#print(np.median(temp_STR_list))
#print('STR std')
#print(np.std(temp_STR_list))
#
#print('EOB percent of zeros / ones')
#print(percent_of_zeros_and_ones(temp_EOB_list)[0])
#print(percent_of_zeros_and_ones(temp_EOB_list)[1])  
#print('EOB mean')
#print(np.mean(temp_EOB_list))        
#print('EOB median')
#print(np.median(temp_EOB_list))
#print('EOB std')
#print(np.std(temp_EOB_list))
#print('---------------------------------------------------------------------')
#
#
##START FEATURE SELECTION
#from sklearn.feature_selection import mutual_info_classif
#from scipy.stats import norm
#        
##Second method - INFORMATION GAIN
#def information_gain(X, y):
#
#    def _calIg():
#        entropy_x_set = 0
#        entropy_x_not_set = 0
#        for c in classCnt:
#            probs = classCnt[c] / float(featureTot)
#            entropy_x_set = entropy_x_set - probs * np.log(probs)
#            probs = (classTotCnt[c] - classCnt[c]) / float(tot - featureTot)
#            entropy_x_not_set = entropy_x_not_set - probs * np.log(probs)
#        for c in classTotCnt:
#            if c not in classCnt:
#                probs = classTotCnt[c] / float(tot - featureTot)
#                entropy_x_not_set = entropy_x_not_set - probs * np.log(probs)
#        return entropy_before - ((featureTot / float(tot)) * entropy_x_set
#                             +  ((tot - featureTot) / float(tot)) * entropy_x_not_set)
#        
#    tot = X.shape[0]
#    classTotCnt = {}
#    entropy_before = 0
#    for i in y:
#        if i not in classTotCnt:
#            classTotCnt[i] = 1
#        else:
#            classTotCnt[i] = classTotCnt[i] + 1
#    for c in classTotCnt:
#        probs = classTotCnt[c] / float(tot)
#        entropy_before = entropy_before - probs * np.log(probs)
#    nz = X.T.nonzero()
#    pre = 0
#    classCnt = {}
#    featureTot = 0
#    information_gain = []
#    for i in range(0, len(nz[0])):
#        if (i != 0 and nz[0][i] != pre):
#            for notappear in range(pre+1, nz[0][i]):
#                information_gain.append(0)
#            ig = _calIg()
#            information_gain.append(ig)
#            pre = nz[0][i]
#            classCnt = {}
#            featureTot = 0
#        featureTot = featureTot + 1
#        yclass = y[nz[1][i]]
#        if yclass not in classCnt:
#            classCnt[yclass] = 1
#        else:
#            classCnt[yclass] = classCnt[yclass] + 1
#    ig = _calIg()
#    information_gain.append(ig)
#    return np.asarray(information_gain)
#    
#def bns_count(word, data, category):
#    tp = np.sum([word in data[i] for i in range(0, len(data)) if category[i] == 1])
#    fp = np.sum([word in data[i] for i in range(0, len(data)) if category[i] == 0])
#    pos = np.sum(category)
#    neg = len(data) - pos
#    tpr = 1.0 * tp / pos
#    fpr = 1.0 * fp / neg
#    temp = np.abs(norm.ppf(tpr) - norm.ppf(fpr))
#    if np.isinf(temp):
#        temp = 0
#        return temp
#    return temp
#
#def bns(param1, param2):
#    vector_bns_importances = list()
#    for term in feature_names_tokens:
#        vector_bns_importances.append(bns_count(term, corpus, param2))
#    return vector_bns_importances         
#
#def feature_selection(classification_vector,classification_algoritm, i):
#    
#    if i==1:
#        k = round(tfidf_matrix_main_tokens_dense_TOK.shape[1])
#        method_names = {
#        bns: ['bns_tokens', 0.1],
#        mutual_info_classif: ['mutual classif tokens', 0.005],
#        information_gain: ['information gain tokens', 0.0005]
#        }
#    else:
#        k = round(0.02*tfidf_matrix_main_tokens_dense_BIGR.shape[1])
#        method_names = {
#        bns: ['bns_bigrams', 0.1],
#        mutual_info_classif: ['mutual classif bigrams', 0.005],
#        information_gain: ['information gain bigrams', 0.003]
#        }
#    #Vector names in string format
#    if classification_vector == target_steps_to_repr:
#        name_of_vector='steps to reproduce'
#    else:
#        name_of_vector='observed bahavior'   
#        
#    print('best tokens %s %s' % (method_names[classification_algoritm][0], name_of_vector))
#    ###############  tfidf_matrix_main_tokens???????????????
#    top_ranked_features = sorted(enumerate(classification_algoritm(tfidf_matrix_main_tokens, classification_vector)), key=lambda x:x[1], reverse=True)[:k]
#    top_ranked_features_indices = list()
#    top_ranked_features_values = list()
#    final_list_with_features = list()
#    for item in top_ranked_features:
#        if item[1] >= method_names[classification_algoritm][1]:
#            top_ranked_features_indices.append(item[0])
#            top_ranked_features_values.append(item[1])
#    #Saving result of feature selection  
#    thefile_words = open('%s %s features.txt' % (method_names[classification_algoritm][0], name_of_vector), 'w', encoding='utf-8')
#    for i in range(len(top_ranked_features_values)):
#        thefile_words.write("%r, %r\n" % (tf_main_tokens.get_feature_names()[top_ranked_features_indices[i]], top_ranked_features_values[i]))
#        final_list_with_features.append(tf_main_tokens.get_feature_names()[top_ranked_features_indices[i]])
#    thefile_words.close()
#    #Plotting histograms
#    #if classification_algoritm == information_gain:
#    #    plt.hist(top_ranked_features_values, bins=20, range=[0,0.01])
#    #else:
#    plt.hist(top_ranked_features_values, bins=20)
#    plt.title("Histogram")
#    plt.xlabel("Value")
#    plt.ylabel("Frequency")
#    plt.show() #Показать график  
#    return top_ranked_features_indices
#    
##Run different types of feature selections
##list_with_features = list()
#tfidf_matrix_main_tokens_dense_TOK = 1
#tfidf_matrix_main_tokens_dense_BIGR = 1
#
#X_tf_idf_dense_BNS_STR_BIGR = 1
#X_tf_idf_dense_BNS_EOB_BIGR = 1
#X_tf_idf_dense_MIC_STR_BIGR = 1
#X_tf_idf_dense_MIC_EOB_BIGR = 1
#X_tf_idf_dense_IG_STR_BIGR = 1
#X_tf_idf_dense_IG_EOB_BIGR = 1
#
#X_tf_idf_dense_BNS_STR_TOK = 1
#X_tf_idf_dense_BNS_EOB_TOK = 1
#X_tf_idf_dense_MIC_STR_TOK = 1
#X_tf_idf_dense_MIC_EOB_TOK = 1
#X_tf_idf_dense_IG_STR_TOK = 1
#X_tf_idf_dense_IG_EOB_TOK = 1
#
#for i in [1,2]:
#    tf_main_tokens = TfidfVectorizer(input=corpus, ngram_range=(i,i), smooth_idf=True) #adding 1 to all term frequencies
#    tfidf_matrix_main_tokens =  tf_main_tokens.fit_transform(corpus)
#    feature_names_tokens = tf_main_tokens.get_feature_names()
#    print('NUMBER OF TOKENS FEATURE NAMES:', len(feature_names_tokens))
#    if i == 1:
#        tfidf_matrix_main_tokens_dense_TOK = tfidf_matrix_main_tokens.toarray()
#    if i == 2:
#        tfidf_matrix_main_tokens_dense_BIGR = tfidf_matrix_main_tokens.toarray()
#    for y_target in [target_steps_to_repr, target_exp_obs_beh]: 
#        if i==2:
#            for method_target in [bns, mutual_info_classif, information_gain]:
#                if (method_target == bns) and (y_target == target_steps_to_repr):
#                    selected_features_nums_BNS_STR_BIGR = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_BNS_STR_BIGR))
#                    X_tf_idf_dense_BNS_STR_BIGR = tfidf_matrix_main_tokens_dense_BIGR[:,selected_features_nums_BNS_STR_BIGR]
#                if (method_target == bns) and (y_target == target_exp_obs_beh):
#                    selected_features_nums_BNS_EOB_BIGR = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_BNS_EOB_BIGR))
#                    X_tf_idf_dense_BNS_EOB_BIGR = tfidf_matrix_main_tokens_dense_BIGR[:,selected_features_nums_BNS_EOB_BIGR]
#                if (method_target == mutual_info_classif) and (y_target == target_steps_to_repr):
#                    selected_features_nums_MIC_STR_BIGR = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_MIC_STR_BIGR))
#                    X_tf_idf_dense_MIC_STR_BIGR = tfidf_matrix_main_tokens_dense_BIGR[:,selected_features_nums_MIC_STR_BIGR]
#                if (method_target == mutual_info_classif) and (y_target == target_exp_obs_beh):
#                    selected_features_nums_MIC_EOB_BIGR = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_MIC_EOB_BIGR))
#                    X_tf_idf_dense_MIC_EOB_BIGR = tfidf_matrix_main_tokens_dense_BIGR[:,selected_features_nums_MIC_EOB_BIGR]
#                if (method_target == information_gain) and (y_target == target_steps_to_repr):
#                    selected_features_nums_IG_STR_BIGR = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_IG_STR_BIGR))
#                    X_tf_idf_dense_IG_STR_BIGR = tfidf_matrix_main_tokens_dense_BIGR[:,selected_features_nums_IG_STR_BIGR]
#                if (method_target == information_gain) and (y_target == target_exp_obs_beh):
#                    selected_features_nums_IG_EOB_BIGR = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_IG_EOB_BIGR))
#                    X_tf_idf_dense_IG_EOB_BIGR = tfidf_matrix_main_tokens_dense_BIGR[:,selected_features_nums_IG_EOB_BIGR]
##                list_with_features.append(feature_selection(y_target, method_target, i))
#        else:
#            for method_target in [bns, mutual_info_classif, information_gain]:
##                list_with_features.append(feature_selection(y_target, method_target, i))
#                if (method_target == bns) and (y_target == target_steps_to_repr):
#                    selected_features_nums_BNS_STR_TOK = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_BNS_STR_TOK))
#                    X_tf_idf_dense_BNS_STR_TOK = tfidf_matrix_main_tokens_dense_TOK[:,selected_features_nums_BNS_STR_TOK]
#                if (method_target == bns) and (y_target == target_exp_obs_beh):
#                    selected_features_nums_BNS_EOB_TOK = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_BNS_EOB_TOK))
#                    X_tf_idf_dense_BNS_EOB_TOK = tfidf_matrix_main_tokens_dense_TOK[:,selected_features_nums_BNS_EOB_TOK]
#                if (method_target == mutual_info_classif) and (y_target == target_steps_to_repr):
#                    selected_features_nums_MIC_STR_TOK = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_MIC_STR_TOK))
#                    X_tf_idf_dense_MIC_STR_TOK = tfidf_matrix_main_tokens_dense_TOK[:,selected_features_nums_MIC_STR_TOK]
#                if (method_target == mutual_info_classif) and (y_target == target_exp_obs_beh):
#                    selected_features_nums_MIC_EOB_TOK = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_MIC_EOB_TOK))
#                    X_tf_idf_dense_MIC_EOB_TOK = tfidf_matrix_main_tokens_dense_TOK[:,selected_features_nums_MIC_EOB_TOK]
#                if (method_target == information_gain) and (y_target == target_steps_to_repr):
#                    selected_features_nums_IG_STR_TOK = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_IG_STR_TOK))
#                    X_tf_idf_dense_IG_STR_TOK = tfidf_matrix_main_tokens_dense_TOK[:,selected_features_nums_IG_STR_TOK]
#                if (method_target == information_gain) and (y_target == target_exp_obs_beh):
#                    selected_features_nums_IG_EOB_TOK = feature_selection(y_target, method_target, i)
#                    print(len(selected_features_nums_IG_EOB_TOK))
#                    X_tf_idf_dense_IG_EOB_TOK = tfidf_matrix_main_tokens_dense_TOK[:,selected_features_nums_IG_EOB_TOK]
#
#from sklearn.model_selection import train_test_split
#    
#X_train_BNS_STR_BIGR, X_test_BNS_STR_BIGR, y_train_BNS_STR_BIGR, y_test_BNS_STR_BIGR = train_test_split(X_tf_idf_dense_BNS_STR_BIGR,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_BNS_EOB_BIGR, X_test_BNS_EOB_BIGR, y_train_BNS_EOB_BIGR, y_test_BNS_EOB_BIGR = train_test_split(X_tf_idf_dense_BNS_EOB_BIGR,
#                                                                                                        target_exp_obs_beh,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_MIC_STR_BIGR, X_test_MIC_STR_BIGR, y_train_MIC_STR_BIGR, y_test_MIC_STR_BIGR = train_test_split(X_tf_idf_dense_MIC_STR_BIGR,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#        
#X_train_MIC_EOB_BIGR, X_test_MIC_EOB_BIGR, y_train_MIC_EOB_BIGR, y_test_MIC_EOB_BIGR = train_test_split(X_tf_idf_dense_MIC_EOB_BIGR,
#                                                                                                        target_exp_obs_beh,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_IG_STR_BIGR, X_test_IG_STR_BIGR, y_train_IG_STR_BIGR, y_test_IG_STR_BIGR = train_test_split(X_tf_idf_dense_IG_STR_BIGR,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_IG_EOB_BIGR, X_test_IG_EOB_BIGR, y_train_IG_EOB_BIGR, y_test_IG_EOB_BIGR = train_test_split(X_tf_idf_dense_IG_EOB_BIGR,
#                                                                                                        target_exp_obs_beh,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_BNS_STR_TOK, X_test_BNS_STR_TOK, y_train_BNS_STR_TOK, y_test_BNS_STR_TOK = train_test_split(X_tf_idf_dense_BNS_STR_TOK,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_BNS_EOB_TOK, X_test_BNS_EOB_TOK, y_train_BNS_EOB_TOK, y_test_BNS_EOB_TOK = train_test_split(X_tf_idf_dense_BNS_EOB_TOK,
#                                                                                                        target_exp_obs_beh,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_MIC_STR_TOK, X_test_MIC_STR_TOK, y_train_MIC_STR_TOK, y_test_MIC_STR_TOK = train_test_split(X_tf_idf_dense_MIC_STR_TOK,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#        
#X_train_MIC_EOB_TOK, X_test_MIC_EOB_TOK, y_train_MIC_EOB_TOK, y_test_MIC_EOB_TOK = train_test_split(X_tf_idf_dense_MIC_EOB_TOK,
#                                                                                                        target_exp_obs_beh,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_IG_STR_TOK, X_test_IG_STR_TOK, y_train_IG_STR_TOK, y_test_IG_STR_TOK = train_test_split(X_tf_idf_dense_IG_STR_TOK,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#
#X_train_IG_EOB_TOK, X_test_IG_EOB_TOK, y_train_IG_EOB_TOK, y_test_IG_EOB_TOK = train_test_split(X_tf_idf_dense_IG_EOB_TOK,
#                                                                                                        target_exp_obs_beh,
#                                                                                           test_size=0.33, random_state=42)
#
#from sklearn import metrics
#from sklearn.model_selection import cross_val_score
#from sklearn.linear_model import LogisticRegression
#from sklearn.svm import SVC
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.naive_bayes import GaussianNB
#from sklearn.naive_bayes import MultinomialNB
#
##matrices obj-features without feature selection
#X_train_STR_BIGR, X_test_STR_BIGR, y_train_STR_BIGR, y_test_STR_BIGR = train_test_split(tfidf_matrix_main_tokens_dense_BIGR,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#X_train_STR_TOK, X_test_STR_TOK, y_train_STR_TOK, y_test_STR_TOK = train_test_split(tfidf_matrix_main_tokens_dense_TOK,
#                                                                                                        target_steps_to_repr,
#                                                                                                        test_size=0.33, random_state=42)
#X_train_EOB_BIGR, X_test_EOB_BIGR, y_train_EOB_BIGR, y_test_EOB_BIGR = train_test_split(tfidf_matrix_main_tokens_dense_BIGR,
#                                                                                                        target_exp_obs_beh,
#                                                                                                        test_size=0.33, random_state=42)
#X_train_EOB_TOK, X_test_EOB_TOK, y_train_EOB_TOK, y_test_EOB_TOK = train_test_split(tfidf_matrix_main_tokens_dense_TOK,
#                                                                                                        target_exp_obs_beh,
#                                                                                                        test_size=0.33, random_state=42)
#
#log_reg_model = LogisticRegression()
#svc_model = SVC()
#random_forest_model = RandomForestClassifier()
#gaussianNB_model = GaussianNB()
#multinomialNB_model = MultinomialNB()
#
#for model_arr in [['RandomForestClassifier ',random_forest_model]]:
#    model = model_arr[1]
#    model_str = model_arr[0] + 'STR_BIGR'
#    print(model_str)
#    model.fit(X_train_STR_BIGR, y_train_STR_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_BIGR,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_BIGR,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_BIGR,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_STR_BIGR
#    predicted = model.predict(X_test_STR_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#
#    model = model_arr[1]
#    model_str = model_arr[0] + 'STR_TOK'
#    print(model_str)
#    model.fit(X_train_STR_TOK, y_train_STR_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_TOK,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_TOK,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_TOK,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_STR_TOK
#    predicted = model.predict(X_test_STR_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    model = model_arr[1]
#    model_str = model_arr[0] + 'EOB_BIGR'
#    print(model_str)
#    model.fit(X_train_EOB_BIGR, y_train_EOB_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_EOB_BIGR
#    predicted = model.predict(X_test_EOB_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#
#    model = model_arr[1]
#    model_str = model_arr[0] + 'EOB_TOK'
#    print(model_str)
#    model.fit(X_train_EOB_TOK, y_train_EOB_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_TOK,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_TOK,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, tfidf_matrix_main_tokens_dense_TOK,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#
#    print(model)
#    # make predictions
#    expected = y_test_EOB_TOK
#    predicted = model.predict(X_test_EOB_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#
##it's turned off now with 705 break 
#for model_arr in [['multinomialNB_model ',multinomialNB_model]]:
#    break 
#    model = model_arr[1]
#    model_str = model_arr[0] + 'BNS_STR_BIGR'
#    print(model_str)
#    model.fit(X_train_BNS_STR_BIGR, y_train_BNS_STR_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_BNS_STR_BIGR
#    predicted = model.predict(X_test_BNS_STR_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'BNS_EOB_BIGR'
#    print(model_str)
#    
#    model.fit(X_train_BNS_EOB_BIGR, y_train_BNS_EOB_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_BNS_EOB_BIGR
#    predicted = model.predict(X_test_BNS_EOB_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'MIC_STR_BIGR'
#    print(model_str)
#    
#    model.fit(X_train_MIC_STR_BIGR, y_train_MIC_STR_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_MIC_STR_BIGR
#    predicted = model.predict(X_test_MIC_STR_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'MIC_EOB_BIGR'
#    print(model_str)
#    
#    model.fit(X_train_MIC_EOB_BIGR, y_train_MIC_EOB_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_MIC_EOB_BIGR
#    predicted = model.predict(X_test_MIC_EOB_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'IG_STR_BIGR'
#    print(model_str)
#    
#    model.fit(X_train_IG_STR_BIGR, y_train_IG_STR_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_STR_BIGR,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_IG_STR_BIGR
#    predicted = model.predict(X_test_IG_STR_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'IG_EOB_BIGR'
#    print(model_str)
#    
#    model.fit(X_train_IG_EOB_BIGR, y_train_IG_EOB_BIGR)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_EOB_BIGR,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_IG_EOB_BIGR
#    predicted = model.predict(X_test_IG_EOB_BIGR)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'BNS_STR_TOK'
#    print(model_str)
#    
#    model.fit(X_train_BNS_STR_TOK, y_train_BNS_STR_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_BNS_STR_TOK
#    predicted = model.predict(X_test_BNS_STR_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'BNS_EOB_TOK'
#    print(model_str)
#    
#    model.fit(X_train_BNS_EOB_TOK, y_train_BNS_EOB_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_BNS_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_BNS_EOB_TOK
#    predicted = model.predict(X_test_BNS_EOB_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'MIC_STR_TOK'
#    print(model_str)
#    
#    model.fit(X_train_MIC_STR_TOK, y_train_MIC_STR_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_MIC_STR_TOK
#    predicted = model.predict(X_test_MIC_STR_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'MIC_EOB_TOK'
#    print(model_str)
#    
#    model.fit(X_train_MIC_EOB_TOK, y_train_MIC_EOB_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_MIC_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_MIC_EOB_TOK
#    predicted = model.predict(X_test_MIC_EOB_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'IG_STR_TOK'
#    print(model_str)
#    
#    model.fit(X_train_IG_STR_TOK, y_train_IG_STR_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_STR_TOK,
#                             target_steps_to_repr, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_IG_STR_TOK
#    predicted = model.predict(X_test_IG_STR_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')
#    
#    model = model_arr[1]
#    model_str = model_arr[0] + 'IG_EOB_TOK'
#    print(model_str)
#    
#    model.fit(X_train_IG_EOB_TOK, y_train_IG_EOB_TOK)
#    
#    print('Cross validation precision score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='precision')
#    print(scores.mean())
#    print('Cross validation recall score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='recall')
#    print(scores.mean())
#    print('Cross validation f1-score (cv=4)')
#    scores = cross_val_score(model, X_tf_idf_dense_IG_EOB_TOK,
#                             target_exp_obs_beh, cv=4,scoring='f1')
#    print(scores.mean())
#    
#    print('Hold-out scores (70% train, 30% test):')
#    print(model)
#    # make predictions
#    expected = y_test_IG_EOB_TOK
#    predicted = model.predict(X_test_IG_EOB_TOK)
#    # summarize the fit of the model
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))
#    print('-----------------------------------')