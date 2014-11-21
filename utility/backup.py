'''
backup.py

This file contain tools for backing up the server's database and to recover it.
'''

from django.core import serializers
from studies.models import *
from custom_auth.models import *

def backup(to_folder, file_type='xml'):
    """
    Back up the database to the folder specificed in to_folder. The database
    will be backed up into 6 different files which represents the models in
    Tangra.
    
    - to_folder: the folder where the backup will be stored in.
    - file_type: the types of the files. The default is 'xml.'
    """
    
    user_data = serializers.serialize(file_type, User.objects.all())
    study_data = serializers.serialize(file_type, Study.objects.all())
    stage_data = serializers.serialize(file_type, Stage.objects.all())
    group_data = serializers.serialize(file_type, Group.objects.all())
    group_stage_data = serializers.serialize(file_type, GroupStage.objects.all())
    user_stage_data = serializers.serialize(file_type, UserStage.objects.all())
    
    f = open(to_folder + '/users.' + file_type, 'w')
    f.write(user_data)
    f.close()
    
    f = open(to_folder + '/studies.' + file_type, 'w')
    f.write(study_data)
    f.close()
    
    f = open(to_folder + '/groups.' + file_type, 'w')
    f.write(group_data)
    f.close()
    
    f = open(to_folder + '/group_strages.' + file_type, 'w')
    f.write(group_stage_data)
    f.close()
    
    f = open(to_folder + '/user_stage_data.' + file_type, 'w')
    f.write(user_stage_data)
    f.close()
    

def recover(from_folder, file_type='xml'):
    """
    Recover the back up from from_folder. The files must be back up generated
    from backup function. To use the recover function, the database must be
    blank. This means that the old database must have been removed and migrate
    command has been run on the server. Otherwise, corruptions in the server
    may occur.
        
    - to_folder: the folder where the backup will be recovered.
    - file_type: the types of the files. The default is 'xml.' If you have
      performed back up in other file types such as 'json', you must change
      the argument.
    """    

    f = open(from_folder + '/users.' + file_type, 'r')
    user_data = f.read()
    f.close()
        
    f = open(from_folder + '/studies.' + file_type, 'r')
    study_data = f.read()
    f.close()
        
    f = open(from_folder + '/groups.' + file_type, 'r')
    group_data = f.read()
    f.close()
        
    f = open(from_folder + '/group_strages.' + file_type, 'r')
    group_stage_data = f.read()
    f.close()
        
    f = open(from_folder + '/user_stage_data.' + file_type, 'r')
    user_stage_data = f.read()
    f.close()    
    
    for d in serializers.deserialize(file_type, user_data):
        d.save()
        
    for d in serializers.deserialize(file_type, study_data):
        d.save()
        
    for d in serializers.deserialize(file_type, group_data):
        d.save()
        
    for d in serializers.deserialize(file_type, group_stage_data):
        d.save()
        
    for d in serializers.deserialize(file_type, user_stage_data):
        d.save()

        