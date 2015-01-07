from django.shortcuts import render
from django.http import HttpResponse,QueryDict
from aksharaklp.fileuploadapp.models import TbDistrict,TbBlock,TbCluster,TbSchool,TbVisitDetails
from django.core import serializers
import json
from django.db.models import F, Max
from django.db import connection
import sys
import traceback
import time

def main(request):
	districts=serializers.serialize("json",TbDistrict.objects.all(),fields=('id','district_name'))
	
	blocks=serializers.serialize("json",TbBlock.objects.all(),fields=('id','block_name','district'))
	
	clusters=serializers.serialize("json",TbCluster.objects.all(),fields=('id','cluster_name','block'))
	
	schools=serializers.serialize("json",TbSchool.objects.all(),fields=('id','school_name','cluster','klp_id'))
	
	locationData={'districts':districts,'blocks':blocks,'clusters':clusters,'schools':schools}
	
	date_=getMaxMinDates()
	fromDate=date_[0]
	toDate=date_[1]

	return render(request, 'reports/reports.html', {'locationData':locationData,'toDate':toDate,'fromDate':fromDate})

def getMaxMinDates():
	query=("SELECT min(to_date(nullif(year||'-'||month||'-'||day,''), 'YYYY-MM-DD'))," 
		"max(to_date(nullif(year||'-'||month||'-'||day,''), 'YYYY-MM-DD')) FROM tb_visit_details;")
	try:
		cursor = connection.cursor()
		cursor.execute(query)
		data=cursor.fetchone()
	except Exception:
		sys.stderr.write("----------------SQL ERROR-----------------------\n")
		traceback.print_exc()

	return data

def generateReport(request):
	response = HttpResponse()
	data=dict()
	data["perfData"]=fetchPerfData(request.GET)
	rows=fetchReqData(request.GET)
	data["reqData"]=rows['avgs']
	data["reqAvgsSplit"]=rows['splits']
	response.write(json.dumps(data))
	return response

def fetchPerfData(queryDict):
	where=""
	groupBy=""
	parameters={}

	district=queryDict['district']
	block=queryDict['block']
	cluster=queryDict['cluster']
	school=queryDict['school']
	fromMonth=queryDict['fromMonth']
	fromYear=queryDict['fromYear']
	toMonth=queryDict['toMonth']
	toYear=queryDict['toYear']

	parameters['fromMonth']=fromMonth
	parameters['fromYear']=fromYear
	parameters['toYear']=toYear
	parameters['toMonth']=toMonth

	if district=='0':
		#all districts
		groupBy="GROUP BY date_"
		where=""
	elif block=='0':
		groupBy="GROUP BY date_, district.id"
		where="AND district.id = %(district)s"
		parameters['district'] = district
	elif cluster=='0':
		groupBy="GROUP BY date_, block.id"
		where="AND block.id = %(block)s"
		parameters['block'] = block
		#all clusters in district 
		#group by district where district
	elif school=='0':
		groupBy="GROUP BY date_, cluster.id"
		where="AND cluster.id = %(cluster)s"
		parameters['cluster'] = cluster
	else:
		groupBy="GROUP BY date_, school.id"
		where="AND school.id = %(school)s"
		parameters['school'] = school

	query=("SELECT to_date('01-'|| visit.month || '-' || visit.year, 'DD-MM-YYYY') date_,"
	"(sum(perform.parents_teachers)::float/count(perform.parents_teachers)::float) * (select normalized_agreement_percent_t from tb_weight_determination wgt_dtm where id=1) +"
	"(sum(perform.parents_parents)::float/count(perform.parents_parents)::float) *(select normalized_agreement_percent_p from tb_weight_determination wgt_dtm where id=1) +"
	"(sum(perform.parents_community)::float/count(perform.parents_community)::float) * (select normalized_agreement_percent_c from tb_weight_determination wgt_dtm where id=1) Parents,"
	
	"(sum(perform.sdmc_teachers)::float/count(perform.sdmc_teachers)::float) * (select normalized_agreement_percent_t from tb_weight_determination wgt_dtm where id=2) +"
	"(sum(perform.sdmc_parents)::float/count(perform.sdmc_parents)::float) *(select normalized_agreement_percent_p from tb_weight_determination wgt_dtm where id=2) +"
	"(sum(perform.sdmc_community)::float/count(perform.sdmc_community)::float) * (select normalized_agreement_percent_c from tb_weight_determination wgt_dtm where id=2) SDMC,"
	
	"(sum(perform.community_teachers)::float/count(perform.community_teachers)::float) * (select normalized_agreement_percent_t from tb_weight_determination wgt_dtm where id=3) +"
	"(sum(perform.community_parents)::float/count(perform.community_parents)::float) *(select normalized_agreement_percent_p from tb_weight_determination wgt_dtm where id=3) +"
	"(sum(perform.community_community)::float/count(perform.community_community)::float) * (select normalized_agreement_percent_c from tb_weight_determination wgt_dtm where id=3) Community,"
	
	"(sum(perform.teachers_teachers)::float/count(perform.teachers_teachers)::float) * (select normalized_agreement_percent_t from tb_weight_determination wgt_dtm where id=4) +"
	"(sum(perform.teachers_parents)::float/count(perform.teachers_parents)::float) *(select normalized_agreement_percent_p from tb_weight_determination wgt_dtm where id=4) +"
	"(sum(perform.teachers_community)::float/count(perform.teachers_community)::float) * (select normalized_agreement_percent_c from tb_weight_determination wgt_dtm where id=4) Teachers"
	
	" FROM"
	
	" public.tb_visit_details visit,"
	" public.tb_school school, "
	" public.tb_cluster cluster, "
	" public.tb_block block, "
	" public.tb_district district,"
	" public.tb_performance_feedback perform"
	
	" WHERE"

	" visit.school_id = school.id AND"
	" school.cluster_id = cluster.id AND"
	" cluster.block_id = block.id AND"
	" block.district_id = district.id AND"
	" perform.visit_id = visit.id AND"
	" to_date('01 '||visit.month||' '||visit.year, 'DD MM YYYY') BETWEEN to_date('01 '|| %(fromMonth)s||' ' || %(fromYear)s, 'DD MM YYYY')"
	" AND to_date('01 '|| %(toMonth)s ||' '|| %(toYear)s, 'DD MM YYYY')")

	query = query+" "+where+" "+groupBy+" ORDER BY date_;"
	rows="date,Parents,SDMC,Community,Teachers"
	try:
		cursor = connection.cursor()
		cursor.execute(query,parameters)
		for row in cursor:
			rows=rows+"\n"+row[0].strftime("%m-%Y")+","+'%.5f' % row[1]+","+'%.5f' % row[2]+","+'%.5f' % row[3]+","+'%.5f' % row[4]
		connection.close()
	except Exception:
		sys.stderr.write("----------------SQL ERROR-----------------------\n")
		connection.close()
		traceback.print_exc()

	return rows

def fetchReqData(queryDict):
	where=""
	groupBy=""
	parameters={}

	district=queryDict['district']
	block=queryDict['block']
	cluster=queryDict['cluster']
	school=queryDict['school']
	fromMonth=queryDict['fromMonth']
	fromYear=queryDict['fromYear']
	toMonth=queryDict['toMonth']
	toYear=queryDict['toYear']

	parameters['fromMonth']=fromMonth
	parameters['fromYear']=fromYear
	parameters['toYear']=toYear
	parameters['toMonth']=toMonth

	if district=='0':
		#all districts
		groupBy="GROUP BY date_"
		where=""
	elif block=='0':
		groupBy="GROUP BY date_, district.id"
		where="AND district.id = %(district)s"
		parameters['district'] = district
	elif cluster=='0':
		groupBy="GROUP BY date_, block.id"
		where="AND block.id = %(block)s"
		parameters['block'] = block
		#all clusters in district 
		#group by district where district
	elif school=='0':
		groupBy="GROUP BY date_, cluster.id"
		where="AND cluster.id = %(cluster)s"
		parameters['cluster'] = cluster
	else:
		groupBy="GROUP BY date_, school.id"
		where="AND school.id = %(school)s"
		parameters['school'] = school

	query=("SELECT *,(t1+t2+t3+t4)/4 AS avg_t,(p1+p2+p3+p4)/4 AS avg_p,(c1+c2+c3+c4)/4 AS avg_c FROM "
	"(SELECT to_date('01-'|| visit.month || '-' || visit.year, 'DD-MM-YYYY') date_,"
	  
	"(sum(case when require.teacher_tlmsufficient=1 then 1 else 0 end)::float)/(case when count(teacher_tlmsufficient)=0 then 1 else count(teacher_tlmsufficient) end)::float t1,"
	"(sum(case when require.teacher_work_overload=0 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float t2,"
	"(sum(case when require.teacher_need_training=0 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float t3,"
	"(sum(case when require.teacher_relationship_hm=1 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float t4,"

	"(sum(case when require.parents_good_school=1 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float p1,"
	"(sum(case when require.parents_teachers_regular=0 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float p2,"
	"(sum(case when require.parents_attention_to_children=0 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float p3,"
	"(sum(case when require.parents_food_served=1 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float p4,"
	  
	"(sum(case when require.community_qtm_to_teach=1 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float c1,"
	"(sum(case when require.community_str=0 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float c2,"
	"(sum(case when require.community_govt_involved=0 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float c3,"
	"(sum(case when require.community_good_infra=1 then 1 else 0 end)::float)/(case when count(teacher_work_overload)=0 then 1 else count(teacher_work_overload) end)::float c4"

	" FROM" 
	  
	" public.tb_visit_details visit,"
	" public.tb_school school,"
	" public.tb_cluster cluster," 
	" public.tb_block block,"
	" public.tb_district district,"
	" public.tb_requirements_feedback require"
	  
	" WHERE"
	" visit.school_id = school.id AND"
	" school.cluster_id = cluster.id AND"
	" cluster.block_id = block.id AND"
	" block.district_id = district.id AND"
	" require.visit_id = visit.id AND"
	" to_date('01 '||visit.month||' '||visit.year, 'DD MM YYYY') BETWEEN to_date('01 '|| %(fromMonth)s || ' '|| %(fromYear)s, 'DD MM YYYY')"
	" AND to_date('01 '|| %(toMonth)s ||' '|| %(toYear)s, 'DD MM YYYY')")
	
	query = query+" "+where+" "+groupBy+" ORDER BY date_) x;"
	
	avgs="date,Teachers,Parents,Community"	
	splits="date,splitOf,split1,split2,split3,split4"

	try:
		cursor = connection.cursor()
		cursor.execute(query,parameters)
		for row in cursor:
			splits=splits+"\n"+row[0].strftime("%m-%Y")+","+"Teachers"+","+'%.5f' % row[1]+","+'%.5f' % row[2]+","+'%.5f' % row[3]+","+'%.5f' % row[4]
			splits=splits+"\n"+row[0].strftime("%m-%Y")+","+"Parents"+","+'%.5f' % row[5]+","+'%.5f' % row[6]+","+'%.5f' % row[7]+","+'%.5f' % row[8]
			splits=splits+"\n"+row[0].strftime("%m-%Y")+","+"Community"+","+'%.5f' % row[9]+","+'%.5f' % row[10]+","+'%.5f' % row[11]+","+'%.5f' % row[12]
			avgs=avgs+"\n" +row[0].strftime("%m-%Y")+","+'%.5f' % row[13]+","+'%.5f' % row[14]+","+'%.5f' % row[15]  
	except Exception:
		sys.stderr.write("\n----------------SQL ERROR-----------------------\n")
		traceback.print_exc()

	rows=dict()
	rows['avgs']=avgs
	rows['splits']=splits
	return rows