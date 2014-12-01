# extract.py #

# The main purpose of this file is to contains the functions for extracting
# a file.

import xml.etree.ElementTree as ET
from custom_auth.models import User
from studies.models import *
    

# Parser objects and variables.

class InvalidXMLError(Exception):
    
    def __init__(self, xml_file):
        self.msg = xml_file + " is invalid."
        
    def __str__(self):
        return self.msg
    

def update_users(xml_file):
    extract_data = extract_users(xml_file)

    for d in extract_data:
        if len(User.objects.filter(username=d['name'])) == 0:
            User.objects.create_user(d['name'], d['email'], d['password'])
    

def update_study(xml_file):
    extract_data = extract_study(xml_file)

    # Get the investigators
    investigators = []
    for i in extract_data['investigators']:
        investigators.append(User.objects.get(username=i))
        
    #print investigators
    if len(Study.objects.filter(name=extract_data['name'])) > 0:
        raise Exception('Study already exists!')
    
    # Update the study.
    new_study = Study.objects.create(name=extract_data['name'],
                    api_name=extract_data['api_name'],
                    description=extract_data['description'],
                    consent=extract_data['consent'],
                    instructions=extract_data['instructions'],
                    eligibility=extract_data['eligibility'],
                    reward=extract_data['reward'],
                    start_date=extract_data['start_date'],
                    end_date=extract_data['end_date'])
    
    new_study.investigators.add(*investigators)
    new_study.save()
    
    # Create each stage.
    stages = {}
    for k in extract_data['stages']:
        stages[k] = Stage.objects.create(study=new_study,
                        name=extract_data['stages'][k]['name'],
                        description=extract_data['stages'][k]['description'],
                        instructions=extract_data['stages'][k]['instructions'],
                        url=extract_data['url'][k]['url'])
    
    # Create each group.
    groups = []
    for g in extract_data['groups']:
        groups[g] = Stage.objects.create(name=g['name'],
                                         study=new_study)
        
        # Get the associated users.
        users = []
        
        for u in g['users']:
            users.append(User.objects.get(username=u))
        
        # We cannot do anything for the user right now.
            
        

def extract_users(xml_file):
    '''
    Extract user data from a particular xml_file.
    
    Arguments:
    - xml_file: the file with the user data.
    '''
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ret = []
    
    # Appending each child into the return function.
    for user in root:

        # Check for integrity
        if user.tag != 'user':
            raise InvalidXMLError(xml_file)
        
        if 'name' in user.attrib and 'password' in user.attrib and 'email' in user.attrib \
           and len(user.attrib) == 3 and len(user) == 0:
            ret.append(user.attrib)
        else:
            raise InvalidXMLError(xml_file)
        
    return ret

def extract_study_boilerplate(field_name, root, xml_file):
    '''
    This function contains the generic code for extracing Name, API Name,
    Informed Consent, Instructions and Eligibility from the XML file.
    '''
    
    f = root.findall(field_name)
    
    # Testing out the schema.
    if len(f) > 1:
        raise InvalidXMLError(xml_file)
    elif len(f[0].attrib) > 0:
        raise InvalidXMLError(xml_file)
    else:
        return f[0].text


def extract_study(xml_file):
    '''
    Extract study data from a particular xml_file.
    
    Arguments:
    - xml_file: the file with the user data.
    '''
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Schema check!
    if root.tag != 'study':
        raise InvalidXMLError(xml_file)
    
    ret = {}
    
    # Adding the very first members of the XML files and add it into the
    # extract dictionary.
    for f in ['name', 'api_name', 'description', 'consent', 'instructions', 'eligibility',
              'reward', 'start_date', 'end_date']:
        ret[f] = extract_study_boilerplate(f, root, xml_file)

    # Then format the description, instructions, eligibility and reward.
    for f in ['description', 'instructions', 'consent', 'eligibility', 'reward']:
        ret[f] = ' '.join(ret[f].split())
    
    # Attempt to extract all of the investigators from the file.
    investigators = []
    
    investigators_tmp = root.findall('investigators')
    
    if len(investigators_tmp) > 1:
        raise InvalidXMLError(xml_file)
    
    investigators_itr = investigators_tmp[0]
    
    for i in investigators_itr:
        if i.tag == 'user' and len(i.attrib) == 1 and 'name' in i.attrib:
            investigators.append(i.attrib['name'])
        else:
            raise InvalidXMLError(xml_file)

    #Attempt to extract all of the stages.
    stages = {}
    
    stages_tmp = root.findall('stages')
    
    if len(stages_tmp) > 1:
        raise InvalidXMLError(xml_file)
    
    stages_itr = stages_tmp[0]
    
    for s in stages_itr:
        try:
            stage_info = {}
            stage_info['name'] = s.find('name').text
            stage_info['description'] = ' '.join(s.find('description').text.split())
            stage_info['instructions'] = ' '.join(s.find('instructions').text.split())
            stage_info['url'] = s.find('url').text
            
            stage_num = int(s.attrib['number'])
            stages[stage_num] = stage_info
        except:
            raise InvalidXMLError(xml_file)

    ret['stages'] = stages
    
    #Attempt to extract all of the groups.
    groups = []
    
    groups_tmp = root.findall('groups')
    
    if len(groups_tmp) > 1:
        raise InvalidXMLError(xml_file)
    
    groups_itr = groups_tmp[0]
    
    for g in groups_itr:
        try:
            group_info = {}
            group_info['name'] = g.find('name').text
            group_info['users'] = []
            
            group_users = g.find('users')
            for u in group_users:
                if u.attrib['name'] not in investigators:
                    group_info['users'].append(u.attrib['name'])
                else:
                    raise InvalidXMLError(xml_file)

            group_info['stage_orders'] = []
            
            group_orders = g.find('stage_orders')
            for o in group_orders:
                group_info['stage_orders'].append(int(o.text))

            groups.append(group_info)
        except:
            raise InvalidXMLError(xml_file)
                
    ret['investigators'] = investigators
    ret['groups'] = groups
    
    return ret