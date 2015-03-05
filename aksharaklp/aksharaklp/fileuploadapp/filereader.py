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
				district,dist_created = TbDistrict.objects.get_or_create(district_name = line[5].strip());  #";" is used within loops to bunch together statements
				fc_new, fc_created = TbFc.objects.get_or_create(name = line[4].strip());
				block_new, block_created = TbBlock.objects.get_or_create(block_name= line[6].strip(), district = district);
				cluster_new, cluster_created = TbCluster.objects.get_or_create(cluster_name = line[7].strip(), block = block_new);
				school_new, school_created = TbSchool.objects.get_or_create(school_name = line[9].strip(), cluster=cluster_new, klp_id= line[8].strip());
				visit_new = TbVisitDetails(month = line[2].strip(), day = line[1].strip(), year = line[3].strip(), fc = fc_new, other_visit = line[10].strip(), school = school_new);
				visit_new.save();
				performance_feedback, pf_created = TbPerformanceFeedback.objects.get_or_create(visit = visit_new, parents_teachers = check_answer(line[13].strip()), parents_parents = check_answer(line[14].strip()), parents_community = check_answer(line[15].strip()), sdmc_teachers = check_answer(line[16].strip()), sdmc_parents = check_answer(line[17].strip()), sdmc_community = check_answer(line[18].strip()), community_teachers = check_answer(line[19].strip()), community_parents = check_answer(line[20].strip()), community_community = check_answer(line[21].strip()), teachers_teachers = check_answer(line[22].strip()), teachers_parents = check_answer(line[23].strip()), teachers_community = check_answer(line[24].strip()), addl_comments_fs = line[25].strip());
				requirement_feedback = TbRequirementsFeedback.objects.get_or_create(visit = visit_new, teacher_tlmsufficient = check_answer(line[26].strip()), teacher_work_overload = check_answer(line[27].strip()), teacher_need_training = check_answer(line[28].strip()), teacher_relationship_hm = check_answer(line[29].strip()), parents_good_school = check_answer(line[31].strip()), parents_teachers_regular = check_answer(line[32].strip()), parents_attention_to_children = check_answer(line[33].strip()), parents_food_served = check_answer(line[34].strip()), community_qtm_to_teach = check_answer(line[36].strip()), community_str = check_answer(line[37].strip()), community_govt_involved = check_answer(line[38].strip()), community_good_infra = check_answer(line[39].strip()), teacher_addl_comments = line[30].strip(), parents_addl_comments = line[35].strip(), community_addl_comments = line[40].strip())
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