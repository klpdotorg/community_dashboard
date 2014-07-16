from django.shortcuts import render
from django.http import HttpResponse
from aksharaklp.fileuploadapp.models import TbDistrict,TbBlock,TbCluster,TbSchool
from django.core import serializers

# Create your views here.
def reports(request):
	districts=serializers.serialize("json",TbDistrict.objects.all(),fields=('id','district_name'))
	
	blocks=serializers.serialize("json",TbBlock.objects.all(),fields=('id','block_name','district'))
	
	clusters=serializers.serialize("json",TbCluster.objects.all(),fields=('id','cluster_name','block'))
	
	schools=serializers.serialize("json",TbSchool.objects.all(),fields=('id','school_name','cluster','klp_id'))
	
	locationData={'districts':districts,'blocks':blocks,'clusters':clusters,'schools':schools}
	
	return render(request, 'reports/reports.html', {'locationData':locationData})