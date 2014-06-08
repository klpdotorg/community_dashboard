from aksharaklp.fileuploadapp.models import *

def analyze_data():
	performance_analysis = analyze_performance() 
	requirement_analysis = analyze_requirement()
	weight_determination = determine_weights()
	return "success"

def analyze_performance():
	performances = TbPerformanceFeedback.objects.filter(assumed_actual_parents = None , assumed_actual_sdmc = None, assumed_actual_comm = None, assumed_actual_teachers = None)
	for performance in performances:
		if(check_None(performance.parents_teachers) + check_None(performance.parents_parents) + check_None(performance.parents_community) > 1):
	 		performance.assumed_actual_parents = 1;
		else:
	 		performance.assumed_actual_parents = 0;
		if(check_None(performance.sdmc_teachers) + check_None(performance.sdmc_parents) + check_None(performance.sdmc_community) > 1):
	 		performance.assumed_actual_sdmc = 1;
		else:
	 		performance.assumed_actual_sdmc = 0;
		if(check_None(performance.community_teachers) + check_None(performance.community_parents) + check_None(performance.community_community) > 1):
	 		performance.assumed_actual_comm = 1;
		else: 
	 		performance.assumed_actual_comm = 0;
		if(check_None(performance.teachers_teachers) + check_None(performance.teachers_parents) + check_None(performance.teachers_community) > 1):
	 		performance.assumed_actual_teachers = 1;
		else:
	 		performance.assumed_actual_teachers = 0;
		performance.save(update_fields = ["assumed_actual_parents", "assumed_actual_sdmc", "assumed_actual_comm", "assumed_actual_teachers"])
	return True

def analyze_requirement():
	requirements = TbRequirementsFeedback.objects.filter(teacher_requirement = None, parent_requirement = None, community_requirement = None)
	for requirement in requirements:
		if(requirement.teacher_tlmsufficient == 1 and requirement.teacher_work_overload == 0 and requirement.teacher_need_training == 0 and requirement.teacher_relationship_hm == 1):
			requirement.teacher_requirement = 1;
		else:
			requirement.teacher_requirement = 0;
		if(requirement.parents_good_school == 1 and requirement.parents_teachers_regular == 1 and requirement.parents_attention_to_children == 1 and requirement.parents_food_served == 0):
			requirement.parent_requirement = 1;
		else:
			requirement.parent_requirement = 0;
		if(requirement.community_qtm_to_teach == 1 and requirement.community_str == 0 and requirement.community_govt_involved == 1 and requirement.community_good_infra == 1):
			requirement.community_requirement = 1;
		else:
			requirement.community_requirement = 0;
		requirement.save(update_fields = ["teacher_requirement", "parent_requirement", "community_requirement"])
	return True

def check_None(str):
	if (str == None):
		return 0
	else:
		return str