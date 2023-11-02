import json
from django.db import IntegrityError
from records.models import *

def load_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data

def create_grades(data):
    for grade in data:
        obj, _ = Grade.objects.get_or_create(name=grade['name'], code=grade['code'])

def create_subjects(data):
    for subject in data:
        obj, _ = Subject.objects.get_or_create(name=subject['name'], code=subject['code'])

def create_curriculums(data):
    for curriculum_data in data:
        grade = Grade.objects.get(code=curriculum_data['grade'])
        subject = Subject.objects.get(code=curriculum_data['subject'])
        Curriculum.objects.get_or_create(grade=grade, subject=subject)

def create_strands_and_substrands(data):
    for strand_data in data:
        subject = Subject.objects.get(code=strand_data["curriculums"][0].split(":")[0])
        strand = Strand.objects.create(number=strand_data['number'], name=strand_data['name'], subject=subject)
        for cul_annote in strand_data["curriculums"]:
            curriculum = Curriculum.objects.get(annotation=cul_annote)
            strand.curriculums.add(curriculum)
        strand.save()
        
        for substrand_data in strand_data['substrands']:
            substrand = Substrand.objects.create(number=substrand_data['number'], name=substrand_data['name'], strand=strand)
            for cul_annote in substrand_data["curriculums"]:
                curriculum = Curriculum.objects.get(annotation=cul_annote)
                substrand.curriculums.add(curriculum)
            strand.save()
        

def create_regions_and_districts(data):
    for region_data in data["regions"]:
        Region.objects.create(code=region_data['code'], name=region_data['region'])

    for district_data in data['districts']:
        region = Region.objects.get(code=district_data['region'])
        District.objects.create(id=district_data['id'], name=district_data['name'], region=region)


def create_dummy():
    # json_file_path = 'records/curriculums/curriculums.json'
    # data = load_data_from_json(json_file_path)

    # create_grades(data["grades"])
    # create_subjects((data["subjects"]))
    # create_curriculums(data["curriculums"])
    # create_strands_and_substrands(data["strands"])

    # json_file_path = 'records/locations/locations.json'
    # data = load_data_from_json(json_file_path)

    # create_regions_and_districts(data)


    pass


if __name__ == "__main__":
    create_dummy()
