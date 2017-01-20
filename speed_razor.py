#!/usr/bin/env python
import sys
import subprocess
import os
import datetime

nowms = datetime.datetime.now()
cfgfile_path = "/tmp/fastdpi_tariff"+str(nowms.microsecond)

args = {"user_ip":sys.argv[1],"rate":int(sys.argv[2]),"ceil":int(sys.argv[3]), "action":sys.argv[4],"cfg_file":cfgfile_path}



htb_params = {"inbound_max":args["ceil"],
"class0_in_min":args["rate"],"class1_in_min":args["rate"],"class2_in_min":args["rate"],"class3_in_min":args["rate"],"class4_in_min":args["rate"],"class5_in_min":args["rate"],"class6_in_min":args["rate"],"class7_in_min":args["rate"],
"class0_in_max":args["ceil"],"class1_in_max":args["ceil"],"class2_in_max":args["ceil"],"class3_in_max":args["ceil"],"class4_in_max":args["ceil"],"class5_in_max":args["ceil"],"class6_in_max":args["ceil"],"class7_in_max":args["ceil"],
"outbound_max": args["ceil"]*2,
"class0_out_min":args["rate"]*2,"class1_out_min":args["rate"]*2,"class2_out_min":args["rate"]*2,"class3_out_min":args["rate"]*2,"class4_out_min":args["rate"]*2,"class5_out_min":args["rate"]*2,"class6_out_min":args["rate"]*2,"class7_out_min":args["rate"]*2,
"class0_out_max":args["ceil"]*2,"class1_out_max":args["ceil"]*2,"class2_out_max":args["ceil"]*2,"class3_out_max":args["ceil"]*2,"class4_out_max":args["ceil"]*2,"class5_out_max":args["ceil"]*2,"class6_out_max":args["ceil"]*2,"class7_out_max":args["ceil"]*2}





htb_template = """
htb_inbound_root=rate %(inbound_max)skbit
htb_inbound_class0=rate %(class0_in_min)skbit ceil %(class0_in_max)skbit
htb_inbound_class1=rate %(class1_in_min)skbit ceil %(class0_in_max)skbit
htb_inbound_class2=rate %(class2_in_min)skbit ceil %(class0_in_max)skbit
htb_inbound_class3=rate %(class3_in_min)skbit ceil %(class0_in_max)skbit
htb_inbound_class4=rate %(class4_in_min)skbit ceil %(class0_in_max)skbit
htb_inbound_class5=rate %(class5_in_min)skbit ceil %(class0_in_max)skbit
htb_inbound_class6=rate %(class6_in_min)skbit ceil %(class0_in_max)skbit
htb_inbound_class7=rate %(class7_in_min)skbit ceil %(class0_in_max)skbit
htb_root=rate %(outbound_max)skbit
htb_class0=rate %(class0_out_min)skbit ceil %(class0_out_max)skbit
htb_class1=rate %(class1_out_min)skbit ceil %(class1_out_max)skbit
htb_class2=rate %(class2_out_min)skbit ceil %(class2_out_max)skbit
htb_class3=rate %(class3_out_min)skbit ceil %(class3_out_max)skbit
htb_class4=rate %(class4_out_min)skbit ceil %(class4_out_max)skbit
htb_class5=rate %(class5_out_min)skbit ceil %(class5_out_max)skbit
htb_class6=rate %(class6_out_min)skbit ceil %(class6_out_max)skbit
htb_class7=rate %(class7_out_min)skbit ceil %(class7_out_max)skbit
""" %htb_params

tariff_config = open(cfgfile_path, "w+")
tariff_config.write(htb_template)
tariff_config.close()

enable_command = ("fdpi_ctrl load --policing  %(cfg_file)s --ip %(user_ip)s" %args)
disable_command = ("fdpi_ctrl del --policing --ip %(user_ip)s" %args)

if args["action"] == 'on':
	subprocess.check_call(enable_command,shell=True)
elif args["action"] == 'off':
	subprocess.check_call(disable_command,shell=True)
elif args["action"]=='block':
	print( "Ambiguous action, script execution has stopped!" )

os.remove(cfgfile_path)

