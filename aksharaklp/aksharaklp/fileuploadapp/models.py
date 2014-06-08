# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y-%m-%d')


class TbBlock(models.Model):
    id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=120, blank=True)
    district = models.ForeignKey('TbDistrict')
    class Meta:
        db_table = 'tb_block'
        unique_together = ("block_name", "district")

class TbCluster(models.Model):
    id = models.AutoField(primary_key=True)
    cluster_name = models.CharField(max_length=150, blank=True)
    block = models.ForeignKey(TbBlock)
    class Meta:
        db_table = 'tb_cluster'
        unique_together = ("cluster_name", "block")

class TbDistrict(models.Model):
    id = models.AutoField(primary_key=True)
    district_name = models.CharField(unique=True, max_length=50, blank=True)
    class Meta:
        db_table = 'tb_district'

class TbFc(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=120)
    class Meta:
        db_table = 'tb_fc'

class TbPerformanceFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    visit = models.ForeignKey('TbVisitDetails', blank=True, null=True)
    parents_teachers = models.SmallIntegerField(blank=True, null=True)
    parents_parents = models.SmallIntegerField(blank=True, null=True)
    parents_community = models.SmallIntegerField(blank=True, null=True)
    assumed_actual_parents = models.SmallIntegerField(blank=True, null=True)
    sdmc_teachers = models.SmallIntegerField(blank=True, null=True)
    sdmc_parents = models.SmallIntegerField(blank=True, null=True)
    sdmc_community = models.SmallIntegerField(blank=True, null=True)
    assumed_actual_sdmc = models.SmallIntegerField(blank=True, null=True)
    community_teachers = models.SmallIntegerField(blank=True, null=True)
    community_parents = models.SmallIntegerField(blank=True, null=True)
    community_community = models.SmallIntegerField(blank=True, null=True)
    assumed_actual_comm = models.SmallIntegerField(blank=True, null=True)
    teachers_teachers = models.SmallIntegerField(blank=True, null=True)
    teachers_parents = models.SmallIntegerField(blank=True, null=True)
    teachers_community = models.SmallIntegerField(blank=True, null=True)
    assumed_actual_teachers = models.SmallIntegerField(blank=True, null=True)
    addl_comments_fs = models.CharField(max_length=750, blank=True)
    class Meta:
        db_table = 'tb_performance_feedback'
        
class TbRequirementsFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    visit = models.ForeignKey('TbVisitDetails', blank=True, null=True)
    teacher_tlmsufficient = models.SmallIntegerField(blank=True, null=True)
    teacher_work_overload = models.SmallIntegerField(blank=True, null=True)
    teacher_need_training = models.SmallIntegerField(blank=True, null=True)
    teacher_relationship_hm = models.SmallIntegerField(blank=True, null=True)
    teacher_requirement = models.SmallIntegerField(blank=True, null=True)
    parents_good_school = models.SmallIntegerField(blank=True, null=True)
    parents_teachers_regular = models.SmallIntegerField(blank=True, null=True)
    parents_attention_to_children = models.SmallIntegerField(blank=True, null=True)
    parents_food_served = models.SmallIntegerField(blank=True, null=True)
    parent_requirement = models.SmallIntegerField(blank=True, null=True)
    community_qtm_to_teach = models.SmallIntegerField(blank=True, null=True)
    community_str = models.SmallIntegerField(blank=True, null=True)
    community_govt_involved = models.SmallIntegerField(blank=True, null=True)
    community_good_infra = models.SmallIntegerField(blank=True, null=True)
    community_requirement = models.SmallIntegerField(blank=True, null=True)
    teacher_addl_comments = models.CharField(max_length=750, blank=True)
    parents_addl_comments = models.CharField(max_length=750, blank=True)
    community_addl_comments = models.CharField(max_length=750, blank=True)
    class Meta:
        db_table = 'tb_requirements_feedback'

class TbSchool(models.Model):
    id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=500, blank=True)
    cluster = models.ForeignKey(TbCluster)
    klp_id = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    class Meta:        
        db_table = 'tb_school'
        unique_together = ("school_name","cluster")

class TbVisitDetails(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.SmallIntegerField(blank=True, null=True)
    day = models.SmallIntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    fc = models.ForeignKey(TbFc)
    other_visit = models.CharField(max_length=500, blank=True)
    school = models.ForeignKey(TbSchool)
    class Meta:
        db_table = 'tb_visit_details'
        unique_together = ("day", "month", "year", "fc", "school", "other_visit")

class TbWeightDetermination(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length=150, blank=True)
    total_yes_teachers = models.IntegerField(blank=True, null=True)
    total_yes_parents = models.IntegerField(blank=True, null=True)
    total_yes_community = models.IntegerField(blank=True, null=True)
    agreement_percent_teacher = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    agreement_percent_parents = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    agreement_percent_community = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    normalized_agreement_percent_t = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    normalized_agreement_percent_p = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    normalized_agreement_percent_c = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    final_weights = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'tb_weight_determination'

