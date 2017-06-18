# -*- coding: utf-8 -*-     
import Bts_plug_in_system
#import Bug

system = Bts_plug_in_system.Bts_plug_in_system()

#    определяем, кто перед нами
role = system.who_are_you()

while True:
#    запускаем действие актора
    call_func_name = system.choose_the_action()
    getattr(system, call_func_name)()

#    запрашиваем, что делать дальше    
    if system.continue_or_save_or_exit():
        break