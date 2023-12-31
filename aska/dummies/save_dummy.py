import json
from curriculums.models import Curriculum, Grade, Subject, Substrand, Strand
from locations.models import Region, District
from schools.models import School
from users.models import CustomUser

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
        subject = Subject.objects.get(code=strand_data["annotation"].split(":")[0])
        strand, created = Strand.objects.get_or_create(number=strand_data['number'], name=strand_data['name'], subject=subject)
        if created:
            for cul_annote in strand_data["curriculums"]:
                curriculum = Curriculum.objects.get(annotation=cul_annote)
                strand.curriculums.add(curriculum)
            strand.save()
        
        for substrand_data in strand_data['substrands']:
            substrand, created = Substrand.objects.get_or_create(number=substrand_data['number'], name=substrand_data['name'], strand=strand)
            if created:
                for cul_annote in substrand_data["curriculums"]:
                    curriculum = Curriculum.objects.get(annotation=cul_annote)
                    substrand.curriculums.add(curriculum)
                strand.save()
        

def create_regions_and_districts(data):
    for region_data in data["regions"]:
        Region.objects.get_or_create(
            code=region_data['code'], 
            name=region_data['name'], 
            capital=region_data["capital"]
        )

    for district_data in data['districts']:
        region = Region.objects.get(code=district_data['region'])
        District.objects.get_or_create(
            name=district_data['name'],
            region=region,
            capital=district_data["capital"]
        )


def save_schools_to_database(data):
    district = District.objects.get(name="Upper Denkyira West District")
    for school in data["schools"]:
        school = School.objects.get_or_create(
            name=school["name"],
            code=school["code"],
            owner=school["owner"],
            email=school["email"],
            gender=school["gender"],
            district=district,
            town=school["town"],
            digital_address=school["digital_address"],
            location=school["location"],
            description=school["description"],
            date_established=school["date_established"],
            visible=school["visible"],
            logo=school["logo"]
        )


def store_users(user_data):
    for data in user_data["users"]:
        subjects_data = data.pop("subjects", [])  # Extract subjects data before creating the user
        data.pop("profile_picture")
        data.pop("cover_picture")
        user, _ = CustomUser.objects.get_or_create(**data)

        # Add subjects to the user
        for subject_code in subjects_data:
            subject = Subject.objects.get(code=subject_code)
            user.subjects.add(subject)



def create_dummy():
    # json_file_path = 'curriculums/data.json'
    # data = load_data_from_json(json_file_path)

    # create_grades(data["grades"])
    # create_subjects((data["subjects"]))
    # create_curriculums(data["curriculums"])
    # create_strands_and_substrands(data["strands"])

    # json_file_path = 'locations/data.json'
    # data = load_data_from_json(json_file_path)
    # create_regions_and_districts(data)


    # json_file_path = 'schools/data.json'
    # data = load_data_from_json(json_file_path)
    # save_schools_to_database(data)


    json_file_path = 'users/data.json'
    data = load_data_from_json(json_file_path)
    store_users(data)
    pass


if __name__ == "__main__":
    create_dummy()
