from aksharaklp.fileuploadapp.models import *
from django.db import connection


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
	
def determine_weights():
	no_of_yes_query = 'SELECT  sum(tb_performance_feedback.parents_teachers) AS Parents_yes_total_t,   sum(tb_performance_feedback.parents_parents) AS Parents_yes_total_p,   sum(tb_performance_feedback.parents_community) AS Parents_yes_total_c,   sum(tb_performance_feedback.sdmc_teachers) AS sdmc_yes_total_t,   sum(tb_performance_feedback.sdmc_parents) AS sdmc_yes_total_p,   sum(tb_performance_feedback.sdmc_community) AS sdmc_yes_total_c,   sum(tb_performance_feedback.community_teachers) AS community_yes_total_t,   sum(tb_performance_feedback.community_parents) AS community_yes_total_p,   sum(tb_performance_feedback.community_community) AS community_yes_total_c,   sum(tb_performance_feedback.teachers_teachers) AS teachers_yes_total_t,   sum(tb_performance_feedback.teachers_parents) AS teachers_yes_total_p,   sum(tb_performance_feedback.teachers_community) AS teachers_yes_total_c FROM   public.tb_performance_feedback'
	no_of_count_query = 'SELECT  count(tb_performance_feedback.parents_teachers) AS Parents_response_count_t,   count(tb_performance_feedback.parents_parents) AS Parents_response_count_p,   count(tb_performance_feedback.parents_community) AS Parents_response_count_c,   count(tb_performance_feedback.sdmc_teachers) AS sdmc_response_count_t,   count(tb_performance_feedback.sdmc_parents) AS sdmc_response_count_p,   count(tb_performance_feedback.sdmc_community) AS sdmc_response_count_c,   count(tb_performance_feedback.community_teachers) AS community_response_count_t,   count(tb_performance_feedback.community_parents) AS community_response_count_p,   count(tb_performance_feedback.community_community) AS community_response_count_c,   count(tb_performance_feedback.teachers_teachers) AS teachers_response_count_t,   count(tb_performance_feedback.teachers_parents) AS teachers_response_count_p,   count(tb_performance_feedback.teachers_community) AS teachers_response_count_c FROM   public.tb_performance_feedback'
#calculate the total number of yes
	weights_cursor = connection.cursor()
	weights_cursor.execute(no_of_yes_query,)
	for yes_row  in weights_cursor:
		parents_yes_total_t = yes_row[0]
		parents_yes_total_p = yes_row[1]
		parents_yes_total_c = yes_row[2]
		sdmc_yes_total_t = yes_row[3]
		sdmc_yes_total_p = yes_row[4]
		sdmc_yes_total_c = yes_row[5]
		community_yes_total_t = yes_row[6]
		community_yes_total_p = yes_row[7]
		community_yes_total_c = yes_row[8]
		teachers_yes_total_t = yes_row[9]
		teachers_yes_total_p = yes_row[10]
		teachers_yes_total_c = yes_row[11]

	weights_cursor.fetchall()

#calculate the total number of yes
	weights_cursor.execute(no_of_count_query,)
	for count_row in weights_cursor:
		parents_agree_percent_t = round(parents_yes_total_t/count_row[0]*100,0)
		parents_agree_percent_p = round(parents_yes_total_p/count_row[1]*100,0)
		parents_agree_percent_c = round(parents_yes_total_c/count_row[2]*100,0)
		sdmc_agree_percent_t = round(sdmc_yes_total_t/count_row[3]*100,0)
		sdmc_agree_percent_p = round(sdmc_yes_total_p/count_row[4]*100,0)
		sdmc_agree_percent_c = round(sdmc_yes_total_c/count_row[5]*100,0)
		community_agree_percent_t = round(community_yes_total_t/count_row[6]*100,0)
		community_agree_percent_p = round(community_yes_total_p/count_row[7]*100,0)
		community_agree_percent_c = round(community_yes_total_c/count_row[8]*100,0)
		teachers_agree_percent_t = round(teachers_yes_total_t/count_row[9]*100,0)
		teachers_agree_percent_p = round(teachers_yes_total_p/count_row[10]*100,0)
		teachers_agree_percent_c = round(teachers_yes_total_c/count_row[11]*100,0)

	weights_cursor.fetchall()
	
	weights_cursor.close()
#calculate normalised percentages
	parents_total_agree_percent = parents_agree_percent_t+parents_agree_percent_p+parents_agree_percent_c
	parents_normal_agree_percent_t = round(parents_agree_percent_t/parents_total_agree_percent*100,0)
	parents_normal_agree_percent_p = round(parents_agree_percent_p/parents_total_agree_percent*100,0)
	parents_normal_agree_percent_c = round(parents_agree_percent_c/parents_total_agree_percent*100,0)

	sdmc_total_agree_percent = sdmc_agree_percent_t + sdmc_agree_percent_p + sdmc_agree_percent_c
	sdmc_normal_agree_percent_t = round(sdmc_agree_percent_t/sdmc_total_agree_percent*100,0)
	sdmc_normal_agree_percent_p = round(sdmc_agree_percent_p/sdmc_total_agree_percent*100,0)
	sdmc_normal_agree_percent_c = round(sdmc_agree_percent_c/sdmc_total_agree_percent*100,0)

	community_total_agree_percent = community_agree_percent_t + community_agree_percent_p + community_agree_percent_c
	community_normal_agree_percent_t = round(community_agree_percent_t/community_total_agree_percent*100,0)
	community_normal_agree_percent_p = round(community_agree_percent_p/community_total_agree_percent*100,0)
	community_normal_agree_percent_c = round(community_agree_percent_c/community_total_agree_percent*100,0)

	teacher_total_agree_percent = teachers_agree_percent_t + teachers_agree_percent_p + teachers_agree_percent_c
	teachers_normal_agree_percent_t = round(teachers_agree_percent_t/teacher_total_agree_percent*100,0)
	teachers_normal_agree_percent_p = round(teachers_agree_percent_p/teacher_total_agree_percent*100,0)
	teachers_normal_agree_percent_c = round(teachers_agree_percent_c/teacher_total_agree_percent*100,0)
#calculate the final weights
	parents_final_weights_t = round(parents_yes_total_t*parents_normal_agree_percent_t/100,0)
	parents_final_weights_p = round(parents_yes_total_p*parents_normal_agree_percent_p/100,0)
	parents_final_weights_c = round(parents_yes_total_c*parents_normal_agree_percent_c/100,0)

	sdmc_final_weights_t = round(sdmc_yes_total_t*sdmc_normal_agree_percent_t/100,0)
	sdmc_final_weights_p = round(sdmc_yes_total_p*sdmc_normal_agree_percent_p/100,0)
	sdmc_final_weights_c = round(sdmc_yes_total_c*sdmc_normal_agree_percent_c/100,0)

	community_final_weights_t = round(community_yes_total_t*community_normal_agree_percent_t/100,0)
	community_final_weights_p = round(community_yes_total_p*community_normal_agree_percent_p/100,0)
	community_final_weights_c = round(community_yes_total_c*community_normal_agree_percent_c/100,0)

	teachers_final_weights_t = round(teachers_yes_total_t*teachers_normal_agree_percent_t/100,0)
	teachers_final_weights_p = round(teachers_yes_total_t*teachers_normal_agree_percent_t/100,0)
	teachers_final_weights_c = round(teachers_yes_total_t*teachers_normal_agree_percent_t/100,0)

	#save in table
	weights_rows = TbWeightDetermination.objects.order_by('id')
	
	for weight_row in weights_rows:
		if weight_row.id == 1:
			weight_row.total_yes_teachers = parents_yes_total_t
			weight_row.total_yes_parents = parents_yes_total_p
			weight_row.total_yes_community = parents_yes_total_c
			weight_row.agreement_percent_teacher = parents_agree_percent_t
			weight_row.agreement_percent_parents = parents_agree_percent_p
			weight_row.agreement_percent_community = parents_agree_percent_c
			weight_row.normalized_agreement_percent_t = parents_normal_agree_percent_t
			weight_row.normalized_agreement_percent_p = parents_normal_agree_percent_p
			weight_row.normalized_agreement_percent_c = parents_normal_agree_percent_c
			weight_row.final_weights_t = parents_final_weights_t
			weight_row.final_weights_p = parents_final_weights_p
			weight_row.final_weights_c = parents_final_weights_c
		
		if weight_row.id == 2:
			weight_row.total_yes_teachers = sdmc_yes_total_t
			weight_row.total_yes_parents = sdmc_yes_total_p
			weight_row.total_yes_community = sdmc_yes_total_c
			weight_row.agreement_percent_teacher = sdmc_agree_percent_t
			weight_row.agreement_percent_parents = sdmc_agree_percent_p
			weight_row.agreement_percent_community = sdmc_agree_percent_c
			weight_row.normalized_agreement_percent_t = sdmc_normal_agree_percent_t
			weight_row.normalized_agreement_percent_p = sdmc_normal_agree_percent_p
			weight_row.normalized_agreement_percent_c = sdmc_normal_agree_percent_c
			weight_row.final_weights_t = sdmc_final_weights_t
			weight_row.final_weights_p = sdmc_final_weights_p
			weight_row.final_weights_c = sdmc_final_weights_c
			
		if weight_row.id == 3:
			weight_row.total_yes_teachers = community_yes_total_t
			weight_row.total_yes_parents = community_yes_total_p
			weight_row.total_yes_community = community_yes_total_c
			weight_row.agreement_percent_teacher = community_agree_percent_t
			weight_row.agreement_percent_parents = community_agree_percent_p
			weight_row.agreement_percent_community = community_agree_percent_c
			weight_row.normalized_agreement_percent_t = community_normal_agree_percent_t
			weight_row.normalized_agreement_percent_p = community_normal_agree_percent_p
			weight_row.normalized_agreement_percent_c = community_normal_agree_percent_c
			weight_row.final_weights_t = community_final_weights_t
			weight_row.final_weights_p = community_final_weights_p
			weight_row.final_weights_c = community_final_weights_c
	
		if weight_row.id == 4:
			weight_row.total_yes_teachers = teachers_yes_total_t
			weight_row.total_yes_parents = teachers_yes_total_p
			weight_row.total_yes_community = teachers_yes_total_c
			weight_row.agreement_percent_teacher = teachers_agree_percent_t
			weight_row.agreement_percent_parents = teachers_agree_percent_p
			weight_row.agreement_percent_community = teachers_agree_percent_c
			weight_row.normalized_agreement_percent_t = teachers_normal_agree_percent_t
			weight_row.normalized_agreement_percent_p = teachers_normal_agree_percent_p
			weight_row.normalized_agreement_percent_c = teachers_normal_agree_percent_c
			weight_row.final_weights_t = teachers_final_weights_t
			weight_row.final_weights_p = teachers_final_weights_p
			weight_row.final_weights_c = teachers_final_weights_c
			
		weight_row.save(update_fields = ["total_yes_teachers", "total_yes_parents", "total_yes_community","agreement_percent_teacher", "agreement_percent_parents", "agreement_percent_community","normalized_agreement_percent_t", "normalized_agreement_percent_p", "normalized_agreement_percent_c","final_weights_t", "final_weights_p", "final_weights_c"])
 	
	
	return True

def check_None(str):
	if (str == None):
		return 0
	else:
		return str