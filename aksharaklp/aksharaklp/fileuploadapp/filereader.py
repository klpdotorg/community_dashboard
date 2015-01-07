# File reader module
import csv
import sys
import traceback

from aksharaklp.fileuploadapp.models import *
""""Defines the method which will accept a file path and convert the csv into lines using a comma as a split.
 	This method deletes the first line as it assumes that line would be the column header"""
def read_file(filePath):
	
	with open(filePath, 'r') as datafile:
		#data = datafile.readlines()
		sniffer = csv.Sniffer()
		dialect = sniffer.sniff(datafile.read(1024))
		
		#datafile.seek(0)
		reader = csv.reader(datafile, dialect)
		if sniffer.has_header(datafile.read(1024)):
			next(reader, None)  # skips the column header
			
		print("Start Insertion ===>");
		for line in reader: #iterating over the lines in the data
			try:
				district,dist_created = TbDistrict.objects.get_or_create(district_name = line[5]);  #";" is used within loops to bunch together statements
				fc_new, fc_created = TbFc.objects.get_or_create(name = line[4]);
				block_new, block_created = TbBlock.objects.get_or_create(block_name= line[6], district = district);
				cluster_new, cluster_created = TbCluster.objects.get_or_create(cluster_name = line[7], block = block_new);
				school_new, school_created = TbSchool.objects.get_or_create(school_name = line[9], cluster=cluster_new, klp_id= line[8]);
				visit_new = TbVisitDetails(month = line[2], day = line[1], year = line[3], fc = fc_new, other_visit = line[10], school = school_new);
				visit_new.save();
				performance_feedback, pf_created = TbPerformanceFeedback.objects.get_or_create(visit = visit_new, parents_teachers = check_answer(line[13]), parents_parents = check_answer(line[14]), parents_community = check_answer(line[15]), sdmc_teachers = check_answer(line[16]), sdmc_parents = check_answer(line[17]), sdmc_community = check_answer(line[18]), community_teachers = check_answer(line[19]), community_parents = check_answer(line[20]), community_community = check_answer(line[21]), teachers_teachers = check_answer(line[22]), teachers_parents = check_answer(line[23]), teachers_community = check_answer(line[24]), addl_comments_fs = line[25]);
				requirement_feedback = TbRequirementsFeedback.objects.get_or_create(visit = visit_new, teacher_tlmsufficient = check_answer(line[26]), teacher_work_overload = check_answer(line[27]), teacher_need_training = check_answer(line[28]), teacher_relationship_hm = check_answer(line[29]), parents_good_school = check_answer(line[31]), parents_teachers_regular = check_answer(line[32]), parents_attention_to_children = check_answer(line[33]), parents_food_served = check_answer(line[34]), community_qtm_to_teach = check_answer(line[36]), community_str = check_answer(line[37]), community_govt_involved = check_answer(line[38]), community_good_infra = check_answer(line[39]), teacher_addl_comments = line[30], parents_addl_comments = line[35], community_addl_comments = line[40])
				#break
			except:
				sys.stderr.write("----------------SQL ERROR-----------------------\n")
				traceback.print_exc()

		

def check_answer(str):
	if str.lower() == 'yes':
		return 1
	if str.lower() == 'no':
		return 0
	else:
		return 