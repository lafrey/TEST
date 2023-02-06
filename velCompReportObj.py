####################################################
#  Object file for basic veloce compile log check  #
#                                                  #
#  This file parses the data in the compile DB     #
#  and stores it as an object in the               #
#  velCompReportObj class.                         #
####################################################

# Edited October 2022 by Nathan Windels (nathan.windels@siemens.com)

import os
import sys
import inspect
from os import path
from collections import defaultdict


class velCompReportObj:
    
	#general variables (init?)
	design_status = ""

	# config vars: parse_veloce_config()
	ADVISOR = False
	ADVISOR_TYPE = ""
	POWER_AWARE = False
	XWAVE = False
	AUTO_CUI = False
	PARALLEL_ENABLED = False
	POWER_ESTIMATION_ENABLED = False
	ASSERTIONS_ENABLED = False
	COVERAGE_ENABLED = False
	DFT_ENABLED = False
	FAULT_ENABLED = False
	design_type = ""
	Mm_factor = ""

	# velsyn data
	lut_flop_count = {}
	lut_flop_count["num_luts"] = {}
	lut_flop_count["num_ff"] = {}
	lut_flop_count["combo_synth_luts"] = {}
	lut_flop_count["synth_ff"] = {}
	lut_flop_count["mem_interface_luts"] = {}
	lut_flop_count["mem_bytes"] = {}

	# rtlc data

	curr_dir = ""
	existing_logs = []
	rtlc_tasks = []
	completed_tasks = []
	Delay_files = []
	four_state_mod = []
	rtlc_warning_info = set()
	velsyn_warning_info = []
	THP = False
	write_perm = True
	multi_driv = 0
	avb_count = 0
	lut_flops = ""
	rtlc_time = 0
	velsyn_time = 0
	velgs_time = 0
	velcomp_time = 0
	undriven_nets = 0
	arbitrary_loops = 0
	rtlc_warning_count = 0
	velsyn_warning_count = 0
	velsyn_error_code = ""
	hw_platform = ""
	
	TBX_HOME = ""
	VMW_HOME = ""
	VELOCE_VERSION = ""
	VPROBE_HOME = ""
	XL_VIP_HOME = ""
	VELSYN_HOSTINFO = ""
	memories_inferred = 0
	empty_Mod = 0
	list_emptyMod = []
	blackbox_Mod = 0
	path_max_depth = 0
	deadlogic_nets = 0
	deadlogic_modules = 0
	dumps = {}
	task_time = {}
	sorted_task_time = {}
	warning_repo = defaultdict(list)
	DEBUG_MODE = False
	my_classname = ""

	UCLOCK = ""
 
	# defining report files to analyze
	
	veloce_config_file = ""
	velcomp_log = ""
	velsyn_log = ""
	velgs_log = ""
	
	glob_dsyn_file =""
	emptyMod_list = ""
	compile_DBLinker_0 = ""
	velcomp_hlog = ""
	compile_rtlc_initial = ""
	rtlc_log = ""
	rtlc_log_short = ""
	precompile_env = ""
	velsyn_undriven_short = ""
	velsyn_undriven = ""
	emptyMod_list_short = ""
	velsyn_log_short = ""
	blackbox_list = ""
	static_clock_report = ""
	velsyn_report_short = ""
	velsyn_report_short_new = ""	
	velsyn_report_new = ""
	velsyn_report = ""
	reco_versions = []

	def __init__(self, curr_dir, debug_mode):
     
		if self.DEBUG_MODE: print("\n[DEBUG] " + self.my_classname + " - Intializing veloce object...")
		
		self.DEBUG_MODE = debug_mode
		self.my_classname = self.__class__.__name__
  
		if (os.path.exists(curr_dir) and os.access(curr_dir, os.W_OK)):
			self.curr_dir = curr_dir
			self.write_perm = True
		else: 
			self.curr_dir = os.environ['PWD']
			self.write_perm = False

		# recognized versions
		self.reco_versions.append("Veloce_v18.0.6")
		self.reco_versions.append("Veloce_v19.0.1")
		self.reco_versions.append("Veloce_v19.0.2")
		self.reco_versions.append("Veloce_v19.0.2_CedrosGLE")
		self.reco_versions.append("Veloce_v19.0.2_Cedros")
		self.reco_versions.append("Veloce_v20.0.1")
		self.reco_versions.append("Veloce_v20.1.3")
		self.reco_versions.append("Veloce_v21.0.2")
		self.reco_versions.append("Veloce_v22.0.1")
		self.reco_versions.append("Veloce_v22.0.2")
		self.reco_versions.append("Veloce_v23.0.0")

		self.veloce_config_file = self.curr_dir + "/veloce.config"

		self.velgs_log = self.curr_dir + "/veloce.log/compile_velgs_0.log"

		self.velsyn_report_short = "/veloce.med/velsyn.out/velsyn.report"
		self.velsyn_report = self.curr_dir + self.velsyn_report_short
		self.velsyn_report_short_new = "/veloce.log/velsyn/velsyn.report"
		self.velsyn_report_new = self.curr_dir + self.velsyn_report_short_new

		self.emptyMod_list_short = "/veloce.med/rtlc.out/emptyMod.list"
		self.emptyMod_list = self.curr_dir + self.emptyMod_list_short
		self.precompile_env = self.curr_dir + "/precompile_env.txt"
		self.velcomp_log = self.curr_dir + "/veloce.log/velcomp.log"
		self.velcomp_hlog = self.curr_dir + "/veloce.log/velcomp.hlog"
		
		self.velsyn_undriven_short = "/veloce.med/velsyn.undriven.log"
		self.velsyn_undriven = self.curr_dir + self.velsyn_undriven_short

		self.velsyn_log_short = "/veloce.log/compile_velsyn_0.log"
		self.velsyn_log = self.curr_dir + self.velsyn_log_short

		self.rtlc_log_short = "/veloce.log/compile_rtlc_0.log"
		self.rtlc_log = self.curr_dir + self.rtlc_log_short

		self.compile_rtlc_initial_short = "/veloce.log/compile_rtlc_initial_0.log"
		self.compile_rtlc_initial = self.curr_dir + self.compile_rtlc_initial_short

		self.glob_dsyn_file = self.curr_dir + "/veloce.med/design_level/glob_Dsyn_Usermem2LB.map.0"
		self.compile_DBLinker_0 = self.curr_dir + "/veloce.log/compile_DBLinker_0.log"
		self.blackbox_list = self.curr_dir + "/veloce.med/rtlc.out/blackbox.list"

		self.static_clock_report = self.curr_dir + "/veloce.log/Static_Clock_Report.log"


		# TASKS SHOULD BE PARSED FROM THE velcomp.log

		self.rtlc_tasks.append("compile_rtlc_design_check_0")
		self.rtlc_tasks.append("compile_rtlc_initial_0")
		self.rtlc_tasks.append("compile_transactor_analysis_initial_0")
		self.rtlc_tasks.append("compile_transactor_compile_initial_0")
		self.rtlc_tasks.append("compile_transactor_analysis_final_0")
		self.rtlc_tasks.append("compile_transactor_compile_final_0")
		self.rtlc_tasks.append("compile_velsyn_for_advisor_0")
		self.rtlc_tasks.append("compile_rtlc_advisor_0")
		self.rtlc_tasks.append("compile_rtlc_0")
		self.rtlc_tasks.append("compile_hvl_0")

		if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Current directory is: " + self.curr_dir)
		if self.DEBUG_MODE: print("\n[DEBUG] " + self.my_classname + " - Checking paths of critical files: ")

		if (os.path.exists(self.veloce_config_file)):
			self.existing_logs.append(self.veloce_config_file)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - veloce_config_file (" + self.veloce_config_file + ") does not exist.")

		if (os.path.exists(self.velgs_log)):
			self.existing_logs.append(self.velgs_log)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velgs_log (" + self.velgs_log + ") does not exist.")

		if (os.path.exists(self.velsyn_report)):
			self.existing_logs.append(self.velsyn_report)
		elif(os.path.exists(self.velsyn_report_new)):
			self.velsyn_report = self.velsyn_report_new
			self.velsyn_report_short = self.velsyn_report_short_new
			self.existing_logs.append(self.velsyn_report)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velsyn_report (" + self.velsyn_report_new + ") does not exist.")

		if (os.path.exists(self.emptyMod_list)):
			self.existing_logs.append(self.emptyMod_list)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - emptyMod_list (" + self.emptyMod_list + ") does not exist.")

		if (os.path.exists(self.precompile_env)):
			self.existing_logs.append(self.precompile_env)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - precompile_env (" + self.precompile_env + ") does not exist.")

		if (os.path.exists(self.velcomp_log)):
			self.existing_logs.append(self.velcomp_log)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velcomp_log (" + self.velcomp_log + ") does not exist.")

		if (os.path.exists(self.velcomp_hlog)):
			self.existing_logs.append(self.velcomp_hlog)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velcomp_hlog (" + self.velcomp_hlog + ") does not exist.")

		if (os.path.exists(self.velsyn_undriven)):
			self.existing_logs.append(self.velsyn_undriven)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velsyn_undrive (" + self.velsyn_undriven + ") does not exist.")

		if (os.path.exists(self.velsyn_log)):
			self.existing_logs.append(self.velsyn_log)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velsyn_log (" + self.velsyn_log + ") does not exist.")

		if (os.path.exists(self.glob_dsyn_file)):
			self.existing_logs.append(self.glob_dsyn_file)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - glob_dsyn_file (" + self.glob_dsyn_file + ") does not exist.")

		if (os.path.exists(self.compile_DBLinker_0)):
			self.existing_logs.append(self.compile_DBLinker_0)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - compile_DBLinker_0 (" + self.compile_DBLinker_0 + ") does not exist.")

		if (os.path.exists(self.blackbox_list)):
			self.existing_logs.append(self.blackbox_list)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - blackbox_list (" + self.blackbox_list + ") does not exist.")
		
		if (os.path.exists(self.static_clock_report)):
			self.existing_logs.append(self.static_clock_report)
		else:
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - static_clock_report (" + self.static_clock_report + ") does not exist.")

		# this used to be its own function, but it makes more sense in the init routine
		sanity = False
		check_file = False

		# print(self.existing_logs)

		if (self.velcomp_log in self.existing_logs) and (self.velsyn_log in self.existing_logs) and (self.velgs_log in self.existing_logs):
			sanity = True
			print("\n" + self.my_classname + " - All required files exist")
		else:
			print("\n" + self.my_classname + " - Could not find one or more of the following logs: " + self.velcomp_log + self.velsyn_log + self.velgs_log)

			# print("\n" + self.my_classname + " - Logs found are:\n")
			# for x in range(len(self.existing_logs)):
			# 	print(self.existing_logs[x])

		if sanity:
			velcomp_log_check = self.if_string_exist(self.velcomp_log, "Compilation finished successfully")
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velcomp log check okay = " + str(velcomp_log_check))
			if velcomp_log_check == False :
				print("" + self.my_classname + " - Did not find 'Compilation finished successfully' in velcomp log: " + self.velcomp_log)
			
			#print("TODO " + self.my_classname + ": velsyn_log - test if this solution works for projects dstributed to large machine!!")
			velsyn_log_check = self.if_string_exist(self.velsyn_log, "Task: exited with code: 0") or self.if_string_exist(self.velsyn_log, "velcomp: task exit code for this job: 0")
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velsyn log check okay = " + str(velsyn_log_check))
			if velsyn_log_check == False :
				print("" + self.my_classname + " - Did not find 'Task: exited with code: 0' in velsyn log: " + self.velsyn_log)
				
			velgs_log_check = self.if_string_exist(self.velgs_log, "Task: exited with code: 0") or self.if_string_exist(self.velgs_log, "velcomp: task exit code for this job: 0")
			if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - velgs log check okay = " + str(velgs_log_check))
			if velgs_log_check == False :
				print("" + self.my_classname + " - Did not find 'Task: exited with code: 0' in velgs log: " + self.velgs_log)
				
			check_file = velcomp_log_check and velsyn_log_check and velgs_log_check

		if sanity and check_file:
			#print "Design  has been compiled successfully"
			self.design_status == "success"
		else:
			#print "Design not compiled successfully. Please review the compilation log files"
			self.design_status == "fail"

	def populate_warning_repo(self):

		self.warning_repo["RTLC-5723"].extend(("Option -flatten_mod will be ignored if passed on this module", 0))
		self.warning_repo["RTLC-5640"].extend(("Module not encountered during partition", 0))
		self.warning_repo["TBXC-15494"].extend(("Clock generator is inactive on negedge with initial value 1", 0))
		self.warning_repo["TBXC-15443"].extend(("Unrolling for/repeat loop", 0))
		self.warning_repo["RTLC-5597"].extend(("Net is a potential RAM", 0))
		self.warning_repo["RTLC-5653"].extend(("Signal is a potential RAM", 0))
		self.warning_repo["RTLC-5685"].extend(("Memory cannot be inferred as forceSet/fault is applied", 0))
		self.warning_repo["RTLC-5404"].extend(("Module reading 'X' value either for assignment or comparison", 0))
		self.warning_repo["RTLC-5489"].extend(("File has '#' delay present. All delays will be ignored", 0))
		self.warning_repo["RTLC-5703"].extend(("Nonstatic initialization or assignment to a memory signal", 0))
		self.warning_repo["RTLC-5540"].extend(("Index value might be out of prefix index constraints", 0))
		self.warning_repo["RTLC-5586"].extend(("Net is a potential memory", 0))
		self.warning_repo["RTLC-5439"].extend(("Flip-Flop is always disabled", 0))
		self.warning_repo["RTLC-5500"].extend(("Zero or negative repetition multiplier replaced by 1'b0", 0))
		self.warning_repo["RTLC-5724"].extend(("Option -flatten_mod will be ignored if passed on this module", 0))
		self.warning_repo["RTLC-5490"].extend(("Inter-assignment delay ignored", 0))
		self.warning_repo["RTLC-5565"].extend(("Default Condition is not given for Unique case", 0))
		self.warning_repo["RTLC-1688"].extend(("Illegal output/inout port specification", 0))
		self.warning_repo["RTLC-5461"].extend(("Size mismatch of port in the instance", 0))
		self.warning_repo["RTLC-5662"].extend(("Signal is not part of the sensitivity list", 0))
		self.warning_repo["TBXC-1056"].extend(("Unknown command line option is ignored", 0))
		self.warning_repo["TBXC-15488"].extend(("Illegal  multiply assigned RTL signal", 0))
		self.warning_repo["RTLC-5385"].extend(("Invalid entry in tcl_force_file", 0))
		self.warning_repo["RTLC-5382"].extend(("Inter-assignment delay used in initila block will be ignored", 0))
		self.warning_repo["RTLC-5691"].extend(("User define DW component found", 0))
		self.warning_repo["TBXC-5540"].extend(("Index value might be out of prefix index constraints", 0))
		self.warning_repo["RTLC-5622"].extend(("UDP edge specifications will be ignored", 0))
		self.warning_repo["RTLC-5390"].extend(("Strengths pull1 and pull0 are treated as weak1 and weak0", 0))
		self.warning_repo["RTLC-5613"].extend(("UDP rows with 'X' entries will be ignored", 0))
		self.warning_repo["RTLC-5411"].extend(("Tri-stated net has non tri-state drivers", 0))
		self.warning_repo["RTLC-5357"].extend(("ForceSet intrumentation on memory will be ignored", 0))
		self.warning_repo["TBXC-5743"].extend(("Could not resolve net in the annotated nets file", 0))
		self.warning_repo["TBXC-5500"].extend(("Annotation applied on net which is connected to inout port", 0))
		self.warning_repo["TBXC-15501"].extend(("Expected a system task, not a function", 0))
		self.warning_repo["TBXC-5461"].extend(("Size mismatch in port for the instance", 0))
		self.warning_repo["RTLC-5782"].extend(("Module reading 4-state for assignment or comparison", 0))
		self.warning_repo["RTLC-5811"].extend(("Module empty", 0))
		self.warning_repo["RTLC-5601"].extend(("Bit/Part/Concatenation is out of range", 0))
		self.warning_repo["TBXC-15464"].extend(("Exported function call optimized as one way function call", 0))
		self.warning_repo["TBXC-15414"].extend(("Argument in $fdisplay larger thean supported width (64 bits)", 0))
		self.warning_repo["TBXC-5653"].extend(("Signal is a potential RAM", 0))
		self.warning_repo["TBXC-5784"].extend(("Signal not part of the sensitivity list still being read", 0))
		self.warning_repo["TBXC-5385"].extend(("Net mentioned in tcl_force_file not found", 0))
		self.warning_repo["RTLC-5356"].extend(("Non-synthesizable Clocking style", 0))
		self.warning_repo["RTLC-1073"].extend(("No connection to the output port", 0))
		self.warning_repo["RTLC-1034"].extend(("Too few connections for instance of module", 0))
		self.warning_repo["RTLC-1036"].extend(("Mismatch in port size and port connection size in instantiation", 0))
		self.warning_repo["RTLC-15456"].extend(("Argument to Exported Task/Function takes a default value", 0))
		self.warning_repo["RTLC-1033"].extend(("No connection to the input port", 0))
		self.warning_repo["RTLC-2029"].extend(("Inconsistent range in corresponding IO declaration", 0))
		self.warning_repo["RTLC-1995"].extend(("Invalid Index Found for Array Bit Select or Part Select", 0))
		self.warning_repo["RTLC-1035"].extend(("No connection to module port", 0))
		self.warning_repo["RTLC-5594"].extend(("Division/remainder of large vectors lead to large critical path", 0))
		self.warning_repo["TBXC-5640"].extend(("Encountered module was not encountered during partitioning", 0))
		self.warning_repo["RTLC-5387"].extend(("Constant driver on port for the instance is removed", 0))
		self.warning_repo["RTLC-5783"].extend(("The signal has multiple drivers", 0))
		self.warning_repo["TBXC-15463"].extend(("Event found in a sensitivity list will be ignored", 0))
		self.warning_repo["RTLC-5786"].extend(("Delays and Strengths associated with gate instances are ignored", 0))
		self.warning_repo["RTLC-2429"].extend(("Enum can only be assigned to same enum type or enum member", 0))
		self.warning_repo["RTLC-1047"].extend(("Replication operator with Zero or negative multiplier",0))
		self.warning_repo["RTLC-5373"].extend(("Strength supply1 and supply0 are treated as strong1 and strong0", 0))
		self.warning_repo["RTLC-5628"].extend(("Clocks forming a part of the asynchronous logic", 0))
		self.warning_repo["TBXC-5514"].extend(("Ignoring always/initial block since it has no useful statements", 0))
		self.warning_repo["TBXC-1688"].extend(("Illegal output/inout port specification for the instance", 0))
		self.warning_repo["TBXC-5812"].extend(("Intra-assignment delays ignored", 0))
		self.warning_repo["TBXC-5703"].extend(("Ignoring nonstatic initialization/assignment to a memory signal", 0))
		self.warning_repo["RTLC-5458"].extend(("Net/Signal modelled as either bufif0/bufif1", 0))
		self.warning_repo["RTLC-5863"].extend(("Initial value ignored possibly because a latch is inferred", 0))
		self.warning_repo["RTLC-5616"].extend(("UDP row ignored since all inputs are don't care", 0))
		self.warning_repo["RTLC-1452"].extend(("Invalid Instance Rule", 0))
		self.warning_repo["RTLC-1006"].extend(("Null port declaration", 0))
		self.warning_repo["TBXC-5601"].extend(("Bit/Part/Concatenation is out of Range", 0))
		self.warning_repo["ADVISOR"].extend(("Advisor warning", 0))


	def get_num(self, str_line):

		for i in str_line.split():
			if i.isdigit() or self.is_float(i):
				return i

	def is_float(self, a_string):
		try:
			float(a_string)
			return True
		except ValueError:
			return False

	def if_string_exist(self, filename, str_v):
		
		fp = open(filename, "r")
		file_lines = fp.readlines()
		fp.close()
		found = False
		for ii in reversed(range(len(file_lines))):
			# print(ii, file_lines[ii])
			line = file_lines[ii]
			if (str_v in line):
				found =1
				break

		return found
	
	def parse_velsyn_log(self):

		if self.velsyn_log in self.existing_logs:
			
			for line in reversed(list(open(self.velsyn_log))):
				if "velcomp: task exit code for this job" in line or "Task: exited with code" in line:
					self.velsyn_error_code = line.split(":")[2]
					print("testing: " + self.velsyn_error_code)
			
			fp = open(self.velsyn_log, "r")

			self.fw = 0
		
			self.VMW_HOME = fp.readlines()[0].split()[0][0:-11]
			self.VELOCE_VERSION = self.VMW_HOME.split('/')[-1]

			fp.seek(0)


			#-dis_resolve_all_multidriver
			for line in fp:
				if self.PARALLEL_ENABLED == True:
					if "THP" in line:
						self.THP = True
				if "multiple drivers" in line or "multiply driven" in line:
					self.multi_driv = self.multi_driv + 1
				if "HostInfo: Linux" in line:
					self.VELSYN_HOSTINFO = line.split()[2]
					
			fp.close()
		else:
			print("\n\n" + self.my_classname + " - Velsyn log file doesn\'t exist")

		self.velsyn_report_info()
		self.get_undriven_nets()
		self.get_info_from_dump()


	def parse_velgs_log(self):
		line_v = 0
		str_v = ""
		if (self.velgs_log in self.existing_logs):
			fp = open(self.velgs_log, "r")
			for line in fp:
				for word in line.split():
					if word == "Frequency":
						line_v = line
			str_v = ""
			str_v += self.get_num(line_v)
			str_v += " KHz"
			fp.close()
		else:
			str_v = "\nCould not find velgs.log file and hence cannot provide Uclock frequency. Please review the veloce.log diectory"

		self.UCLOCK = str_v



	def get_blackbox(self):

		if self.blackbox_list in self.existing_logs:
			fp = open(self.blackbox_list, "r")
			for line in fp:
				self.blackbox_Mod = self.blackbox_Mod + 1

			fp.close()
		else:
			self.blackbox_Mod = 0

	def info_from_warning(self, line, task):
		# it appears that he had some bigger plans for this function...

		#self.wf = 0
		#prev_word = ""

		warning = line.split()[0].rstrip()

		# Nathan simplified the logic - no need for a loop.  Leaving old code in there just in case it becomes apparent that there was another purpose for it.
		if ("Warning" == warning) or ("SimWarn" == warning):
			word = line.split()[1].rstrip("]:").strip("[")
			if word in self.warning_repo:
				self.warning_repo[word][1] = str(int(self.warning_repo[word][1]) + 1)

				if (len(self.warning_repo[word]) < 3):
					self.warning_repo[word].append(warning)
				#print(self.warning_repo[word])
			else: 
				if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Warning not found in warning repo: " + word)
				self.warning_repo[word].extend(("note: warning added by summary script", 0))


	def get_dump_info(self, line):
		lc = 0
		#line_v = line
		fw = 0
		sw = 0
		fv = ""
		sv = ""
		#global dumps
		for word in line.split():
			lc = lc + 1
			if sw == 1:
				sv = word
				if self.VELOCE_VERSION == "Veloce_v20.0.1":
					self.dumps[fv] = "/veloce.log/velsyn/" + sv
				else:
					self.dumps[fv] = "/veloce.med/" + sv
				fw = 0
				sw = 0
			if fw == 1:
				fv = word
				sw = 1
			if word == "-Dump":
				fw = 1
			
		
	def get_info_from_dump(self):

		if "p0" in self.dumps:
			#print "\nAnalyzing p0 dump file\n"
			if (os.path.exists(self.curr_dir + self.dumps["p0"])):
				fp = open(self.curr_dir + self.dumps["p0"], "r")
				
				if self.write_perm:
					fp_m = open(self.curr_dir + "/deadmodules.list", "w")
					fp_n = open(self.curr_dir + "/deadnets.list", "w")
				else:
					fp_m = open("deadmodules.list", "w")
					fp_n = open("deadnets.list", "w")

				lines_seen = set()

				for line in fp:
					if ("rtlc" not in line) and ("VCC" not in line) and ("CONST" not in line) and ("Const" not in line) and ("VMW" not in line) and ("GND" not in line) and ("mctcore" not in line):
						if line not in lines_seen:
							lines_seen.add(line)
							if "dead module" in line:
								self.deadlogic_modules = self.deadlogic_modules + 1
								fp_m.write(line)
							if "dead net" in line:
								self.deadlogic_nets = self.deadlogic_nets + 1
								fp_n.write(line)
					
				fp_m.close()
				fp_n.close()
				fp.close()

			else:
				self.deadlogic_nets = -1
				self.deadlogic_modules = -1

		else:
			self.deadlogic_nets = -2
			self.deadlogic_modules = -2

		if "c1" in self.dumps:
			if (os.path.exists(self.curr_dir + self.dumps["c1"])):
				fp = open(self.curr_dir + self.dumps["c1"], "r")
				for line in fp:
					if "arbitrary manner" in line:
						self.arbitrary_loops += 1

				fp.close()

			else:
				self.arbitrary_loops = -1
		else:
			self.arbitrary_loops = -2	

		for item in self.dumps.keys():
			
			#if item == "c0":
				#print "\nValue of c0 key is: ", self.dumps[item]
			#if item == "c1":
				#print "\nValue of c1 key is: ", self.dumps[item]
			#if item == "m9":
				#print "\nValue of m9 key is: ", self.dumps[item]
			#if item == "p3":
				#print "\nValue of p3 key is: ", self.dumps[item]
			if item[0] == "e":
				#print "\nValue of e  key is: ", self.dumps[item]
				if (os.path.exists(self.curr_dir + self.dumps[item])):
					#print "\nYes, the dump file exists"
					fp = open(self.curr_dir + self.dumps[item], "r")
					for line in fp:
						if "Path with depth" in line:
							self.path_max_depth = (self.get_num(line))
							break
					fp.close()
				else:
					self.path_max_depth = 0
			#if item[0] == "E":
				#print "\nValue of E  key is: ", self.dumps[item]
			#if item[0] == "P":
				#print "\nValue of P  key is: ", self.dumps[item]


			
	def velsyn_report_info(self):
		is_before_dead = False
		is_after_dead = False
		
		if self.velsyn_report in self.existing_logs:
			fp = open(self.velsyn_report, "r")
			for line in fp:
				if "MED Hardware Platform" in line:
					self.hw_platform = line.split(":")[1].strip()
					#print "MED HW Platform is: ", hw_platform
				if "Before Dead Logic Elimination" in line:
					is_before_dead = True
				if "After Dead Logic Elimination" in line:
					is_before_dead = False
					is_after_dead = True
				if "Total Available Memory Bytes" in line:
					is_after_dead = False
				if "NUMBER OF USED ARRAY BOARDS IN DESIGN" in line:
					self.avb_count = self.get_num(line)
				if "Total Velsyn compile time" in line:
					self.velsyn_time = self.get_num(line)
				if "-Dump" in line:
					self.get_dump_info(line)

				if is_before_dead:
					if "Number of LUTs" in line:
						self.lut_flop_count["num_luts"]["description"] = "Number of LUTs"
						self.lut_flop_count["num_luts"]["before_dead"] = line.split()[3].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - " + self.lut_flop_count["num_luts"]["description"] + ": " + self.lut_flop_count["num_luts"]["before_dead"])
						
					if "Number of flip-flops" in line:
						self.lut_flop_count["num_ff"]["description"] = "Number of flip-flops"
						self.lut_flop_count["num_ff"]["before_dead"] = line.split()[3].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Number of flip-flops: " + self.lut_flop_count["num_ff"]["before_dead"])
					
					# if "Memory Interface LUTs" in line:
					# 	self.lut_flop_count["mem_interface_luts"]["description"] = "Memory Interface LUTs"
					# 	self.lut_flop_count["mem_interface_luts"]["before_dead"] = line.split()[3].strip()
					# 	if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Memory Interface LUTs: " + self.lut_flop_count["mem_interface_luts"]["before_dead"])

					if "Combinatorial synthesis LUTs" in line: 
						self.lut_flop_count["combo_synth_luts"]["description"] = "Combinatorial synthesis LUTs"
						self.lut_flop_count["combo_synth_luts"]["before_dead"] = line.split()[3].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Combinatorial synthesis LUTs: " + self.lut_flop_count["combo_synth_luts"]["before_dead"])
					
					if "Synthesis flip-flops" in line:
						self.lut_flop_count["synth_ff"]["description"] = "Synthesis flip-flops"
						self.lut_flop_count["synth_ff"]["before_dead"] = line.split()[2].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Synthesis flip-flops: " + self.lut_flop_count["synth_ff"]["before_dead"])
					
					if "Memory Bytes" in line:
						self.lut_flop_count["mem_bytes"]["description"] = "Memory Bytes"
						self.lut_flop_count["mem_bytes"]["before_dead"] = line.split()[2].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Memory Bytes: " + self.lut_flop_count["mem_bytes"]["before_dead"])

				if is_after_dead:
					if "Number of LUTs" in line:
						self.lut_flop_count["num_luts"]["description"] = "Number of LUTs"
						self.lut_flop_count["num_luts"]["after_dead"] = line.split()[3].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - " + self.lut_flop_count["num_luts"]["description"] + ": " + self.lut_flop_count["num_luts"]["after_dead"])
						
					if "Number of flip-flops" in line:
						self.lut_flop_count["num_ff"]["description"] = "Number of flip-flops"
						self.lut_flop_count["num_ff"]["after_dead"] = line.split()[3].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Number of flip-flops: " + self.lut_flop_count["num_ff"]["after_dead"])
					
					if "Memory Interface LUTs" in line:
						self.lut_flop_count["mem_interface_luts"]["description"] = "Memory Interface LUTs"
						self.lut_flop_count["mem_interface_luts"]["before_dead"] = 0
						self.lut_flop_count["mem_interface_luts"]["after_dead"] = line.split()[3].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Memory Interface LUTs: " + self.lut_flop_count["mem_interface_luts"]["after_dead"])

					if "Combinatorial synthesis LUTs" in line: 
						self.lut_flop_count["combo_synth_luts"]["description"] = "Combinatorial synthesis LUTs"
						self.lut_flop_count["combo_synth_luts"]["after_dead"] = line.split()[3].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Combinatorial synthesis LUTs: " + self.lut_flop_count["combo_synth_luts"]["after_dead"])
					
					if "Synthesis flip-flops" in line:
						self.lut_flop_count["synth_ff"]["description"] = "Synthesis flip-flops"
						self.lut_flop_count["synth_ff"]["after_dead"] = line.split()[2].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Synthesis flip-flops: " + self.lut_flop_count["synth_ff"]["after_dead"])
					
					if "Memory Bytes" in line:
						self.lut_flop_count["mem_bytes"]["description"] = "Memory Bytes"
						self.lut_flop_count["mem_bytes"]["after_dead"] = line.split()[2].strip()
						if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Memory Bytes: " + self.lut_flop_count["mem_bytes"]["after_dead"])
		
			fp.seek(0)

			if self.avb_count == 0:
				for line in fp:
					if "NUMBER OF MACROS IN DESIGN" in line:
						lf = int(self.get_num(line))
						if self.design_type == "Veloce2":
							if (lf > 16):
								if (lf % 16) == 0:
									self.avb_count = (lf/16)
									#print "self.avb_count_1: ", self.avb_count
								else:
									self.avb_count = (lf/16) + 1
									#print "self.avb_count_2: ", self.avb_count
							else:
								self.avb_count = 1
								#print "self.avb_count_3: ", self.avb_count
						elif self.design_type == "Strato":
							if (lf > 64):
								if (lf % 64) == 0:
									self.avb_count = (lf/64)
								else:
									self.avb_count = (lf/64) + 1
							else:
								self.avb_count = 1
						else:
							self.avb_count = -1
								

			fp.close()
		else:
			self.avb_count = "\nCould not determine size of the design. Please review velsyn.report file for more info"
			self.lut_flops = "\nCould not determine lut and flop information"

		self.get_info_from_dump()


	def parse_veloce_config(self):

		if (self.veloce_config_file in self.existing_logs):
			fp = open(self.veloce_config_file, "r")

			for line in fp:
				if line[0] != "#":
					if "-xwave_siglist" in line:
						self.XWAVE = True
					if "-rtlc_opt_flow" in line:
						self.ADVISOR = True	
						lc = 0
						for word in line.split():
							if lc == 1:
								self.ADVISOR_TYPE = word
								lc = 0
							if word == "-rtlc_opt_flow":
								lc = 1
					if "-upf_file" in line:
						self.POWER_AWARE = True
					if "-parallel" in line:
						self.PARALLEL_ENABLED = True
					if "-platform" in line:
						if "StratoM" in line:
							self.design_type = "Strato"
						if "D2" in line:
							self.design_type = "Veloce2"
					if "-useAutoCUiFlow" in line:
						self.AUTO_CUI = True
					if "-Mm" in line:
						wf = 0
						for word in line.split():
							if wf == 1:
								self.Mm_factor = word
								wf = 0
							if word == "-Mm":
								wf = 1
					if "-enable_fcov_support" in line:
						self.COVERAGE_ENABLED = True
					if "-assertcomp" in line:
						self.ASSERTIONS_ENABLED = True
					if "-pwr_inst" in line or "-pwr_inst_list" in line:
						self.POWER_ESTIMATION_ENABLED = True
					if "-FAfi" in line:
						self.FAULT_ENABLED = True
					if "-dft_stimulate_dut_ports" in line or "-dft_stil_file" in line or "-dft_pattern_file_list" in line:
						self.DFT_ENABLED = True

			fp.close()
		else:
			print("\n\nCould not find veloce.config in this directory\n\n")

		

	def get_undriven_nets(self):

		if self.velsyn_undriven in self.existing_logs:
			fp = open(self.velsyn_undriven, "r")
			for line in fp:
				if ("rtlc" in line) or ("mctcore" in line):
					#print "\n\nLine content is: ", line
					continue
				else:
					self.undriven_nets += 1
			fp.close()
		else:
			self.undriven_nets= -1



	def parse_glob_dsyn_file(self):
		
		wf = 0
		wfi = 0
		LSB = ""
		MSB = ""
		BAddr = ""
		EAddr = ""
		str_v = ""
		memories_inferred = 0

		if self.write_perm:
			fp_m = open(self.curr_dir + "/inferred_mems.list", "w")	
		else:
			fp_m = open("/inferred_mems.list", "w")

		if self.glob_dsyn_file in self.existing_logs:
			fp = open(self.glob_dsyn_file, "r")
			
			for line in fp:
				if "INST" in line:
					if ("rtlc" not in line) and ("mctcore" not in line):
						memories_inferred = memories_inferred + 1
						str_v = line[6:]
						wf = 1
						#fp_m.write(line[6:])
				if wf:
					if "LSBit" in line:
						LSB = self.get_num(line)
					if "MSBit" in line:
						MSB = self.get_num(line)
					if "BeginAddress" in line:
						BAddr = self.get_num(line)
					if "EndAddress" in line:
						EAddr = self.get_num(line)
						wf = 0
						str_v = str_v.rstrip("\n")+"["+EAddr+":"+BAddr +"]"+"["+MSB+":"+LSB+"]"
						fp_m.write(str_v)
						fp_m.write("\n")

			fp.close()

		fp_m.close()
		#print "\nMemories inferred from glob dsyn: ", memories_inferred

		return memories_inferred
	


	def parse_dissolve_memattr(self):

		wf = 0
		wfi = 0
		str_v = ""
		memories_inferred = 0

		if self.write_perm:
			fp_m = open(self.curr_dir + "/inferred_mems.list", "w")	
		else:
			fp_m = open("/inferred_mems.list", "w")

		if (self.ADVISOR == True):
			if (os.path.exists(self.curr_dir + "/veloce.med/ADVISOR/dissolve_memattr.list")):
				m_count = 0
				fp = open(self.curr_dir + "/veloce.med/ADVISOR/dissolve_memattr.list", "r")
				for line in fp:
					if wfi:
						wfi = 0
						str_v +=  "." + line
						if ("rtlc" not in str_v) and ("mctcore" not in str_v):
							fp_m.write(str_v)
						str_v = ""
					if wf:
						str_v = line
						str_v = str_v.rstrip("\n")
						wf = 0
						wfi = 1
					if "module" in line:
						wf = 1
						m_count = m_count + 1

				memories_inferred = memories_inferred + m_count
				#print "\nMemories inferred from glob dsyn and mem attribs file: ", memories_inferred
				fp.close()

		fp_m.close()
		
		return memories_inferred

	def parse_inferred_memories(self):
		self.memories_inferred = self.parse_dissolve_memattr() + self.parse_glob_dsyn_file()

	def parse_emptyMod(self):

		if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Function (get_empty_mod) called from: " + sys._getframe().f_back.f_code.co_name)

		if (os.path.exists(self.emptyMod_list)):
			fp = open(self.emptyMod_list, "r")
			for line in fp:
				if "Master Name" in line:
					self.empty_Mod = self.empty_Mod + 1
					self.list_emptyMod.append(line.split()[-1])
			
			fp.close()


	def get_time(self, line):
		"""	Gets the time from 'Started task' or 'Complete task' line in velcomp.log

			Creates a dictionary task_time[task name] = time 
  		"""	
		lc = 0
		for word in line.split():
			if lc == 1:
				self.task_time[word] = self.get_num(line)
				# if self.DEBUG_MODE: print ("[DEBUG] " + self.my_classname + " - get_time: " + word + " = " + self.task_time[word])
				lc = 0
			if "task:" == word:
				lc = 1



	def get_rtlc_time(self):

		for task in self.rtlc_tasks:
			if task in self.sorted_task_time.keys():
				#print "\nTask name: ", sorted_task_time[task]
				self.rtlc_time = self.rtlc_time + int(self.sorted_task_time[task])
				
		print ("\nRTLC time is: " + str(self.rtlc_time))
		

	def get_started_tasks(self, task):

		if self.compile_DBLinker_0 not in self.existing_logs:
			self.velcomp_time = -1

		fp = open(task, "r")
		
		for line in fp:
			if "Completed task" in line and "partition" not in line:
				self.completed_tasks.append(line)
				self.get_time(line)

			#if velcomp_time != -1:
			#	if "-start_task velsyn" in line:
			#		print "\nStarted task: ", line
			#	if "-start_task rtlc" in line:
			#		print "\nStarted task: ", line

		fp.close()

	def get_completed_tasks(self, task):

		if self.compile_DBLinker_0 not in self.existing_logs:
			self.velcomp_time = -1

		fp = open(task, "r")
		
		for line in fp:
			if "Completed task" in line and "partition" not in line:
				self.completed_tasks.append(line)
				self.get_time(line)

			#if velcomp_time != -1:
			#	if "-start_task velsyn" in line:
			#		print "\nStarted task: ", line
			#	if "-start_task rtlc" in line:
			#		print "\nStarted task: ", line

		fp.close()



	def parse_velcomp_log(self):

		# populates task_time from velcomp_log_0
		if self.velcomp_hlog not in self.existing_logs:
			self.get_completed_tasks(self.velcomp_log)
		else:
			self.get_completed_tasks(self.velcomp_hlog)
			self.get_completed_tasks(self.velcomp_log)

		for key,value in self.task_time.items():
			if key not in self.sorted_task_time.keys():
				self.sorted_task_time[key] = value

		for task in self.rtlc_tasks:
			if task in self.sorted_task_time.keys():
				#print "\nTask name: ", sorted_task_time[task]
				self.rtlc_time = self.rtlc_time + int(self.sorted_task_time[task])

		if "compile_velsyn_0" in self.sorted_task_time:
			self.velsyn_time = self.sorted_task_time["compile_velsyn_0"]

		if "compile_velgs_0" in self.sorted_task_time:
			self.velgs_time = self.sorted_task_time["compile_velgs_0"]



	def parse_compile_rtlc_initial(self):
		
		if self.DEBUG_MODE: print("[DEBUG] " + self.my_classname + " - Function (info_from_rtlc) called from: " + sys._getframe().f_back.f_code.co_name)

		if os.path.exists(self.compile_rtlc_initial):
			fp = open(self.compile_rtlc_initial)
			for line in fp:
				if ("Warning" in line) or ("SimWarn" in line):
					self.rtlc_warning_info.add(line)
					self.info_from_warning(line, "rtlc")
					#if line not in rtlc_warning_info:
						#m_count += 1
						#info_from_warning(line,"rtlc")

			#print "Additional warning count: ", m_count
			fp.close()

	def parse_rtlc_log(self):

		wf = 0
		wf1 = 0

		#need to check if rtlc_warning_info is empty
		if self.DEBUG_MODE: print("\n[DEBUG] " + self.my_classname + " - Generating info from RTLC task log files:")

		if os.path.exists(self.rtlc_log):
			if self.DEBUG_MODE: print("\n[DEBUG] " + self.my_classname + " - " + self.rtlc_log_short + " file exists")

			fp = open(self.rtlc_log)
			if self.DEBUG_MODE: print("\n[DEBUG] " + self.my_classname + " - Analyzing " + self.rtlc_log_short + " for details:")

			for line in fp:
				if "All delays will be ignored" in line:
					for word in line.split():
						if wf == 1:
							if word[:-1] not in self.Delay_files:
								self.Delay_files.append(word[:-1])
							wf = 0
						if word == "File":
							wf = 1

				if ("Warning" in line) or ("SimWarn" in line):
					if line not in self.rtlc_warning_info:
						# is this being added to simply just to compare if the warning already exists?
						self.rtlc_warning_info.add(line)
						self.info_from_warning(line, "rtlc")
					#rtlc_warning_info.append(line)
					#info_from_warning(line,"rtlc")

				if "Reading 4-state value" in line:
					for word in line.split():
						if wf1 == 1:
							wf1 = 0
							if word not in self.four_state_mod:
								#print "Four state word is: ", word
								self.four_state_mod.append(word)
						if word == "Module":
								wf1 = 1

			fp.seek(0)
			for word in fp.readlines()[1].split():
				if "TBX_HOME=" in word:
					self.TBX_HOME = word[9:]
					if self.DEBUG_MODE: print("\n[DEBUG] " + self.my_classname + " - TBX_HOME is: " + self.TBX_HOME + "\n")
			fp.close()
		else:
			if self.DEBUG_MODE: print("\ncompile_rtlc_0.log file does not exist. Cannot perform certain operartions.")

	def parse_all(self):
		self.config_file_info()
		self.populate_warning_repo()
		self.parse_velcomp_log()
		self.parse_compile_rtlc_initial()
		self.parse_rtlc_log()
		self.parse_emptyMod()
		self.parse_inferred_memories()
		self.parse_velsyn_log()
		self.parse_velgs_log()
		# self.parse_static_clock_report()


	def parse_static_clock_report(self):
    
		state = "start"
		clock_id = "0"
		# static_clock_dict["static_clock_report"] = {}
		# static_clock_dict["static_clock_report"]["clock"] = {}
		global static_clock_dict
		
		with open(veloce.static_clock_report, "r") as a_file:
			for line in a_file:
				if "Unit of delay periods" in line:
					static_clock_dict["unit_of_delay"] = line.split("=")[1].strip()
				if "CLOCK REPORT" in line:
					state = "clock_report"
				if "Clock Source Information" in line:
					state = "clock_source"
				if state == "clock_report":
					line_split = line.split()
					if len(line_split) < 1:
						continue
					try:
						int(line_split[0])
						#print("I got here! " + line_split[0])
						#if isinstance(int(line_split[0]), int):
						static_clock_dict["clock"][line_split[0]] = {}
						static_clock_dict["clock"][line_split[0]]["inactive_edge"] = line_split[1]
						static_clock_dict["clock"][line_split[0]]["phase_delay"] = line_split[2]
						static_clock_dict["clock"][line_split[0]]["posedge_delay"] = line_split[3]
						static_clock_dict["clock"][line_split[0]]["negedge_delay"] = line_split[4]
						static_clock_dict["clock"][line_split[0]]["percentage_of_uclock"] = {}
						static_clock_dict["clock"][line_split[0]]["percentage_of_uclock"]["auto_cfr"] = line_split[5]
						static_clock_dict["clock"][line_split[0]]["percentage_of_uclock"]["not_auto_cfr"] = line_split[6]
					except:
						blah = 0
					
				if state == "clock_source":
					line_split = line.split()
					if "Clock Name" in line:
						clock_id = line_split[0].strip('()')
						static_clock_dict["clock"][clock_id]["clock_name"] = line_split[4]
					elif "Module" in line:
						static_clock_dict["clock"][clock_id]["module"] = line_split[2]
					elif "File Name" in line:
						static_clock_dict["clock"][clock_id]["file_name"] = line_split[3]
					elif "Line No" in line:
						static_clock_dict["clock"][clock_id]["line_no"] = line_split[3]

