from django.db.utils import IntegrityError
from records.models import *
import json

json_data = None

# Load curriculums data from json file

def curriculums_to_database():
    # Create subejects and curriculums
    with open("records/curriculums/curriculums.json", "r") as f:
        json_data = json.load(f)
        
    for sb in json_data["subjects"]:
        try:
            sub = Subject.objects.create(name=sb["name"])
            for grd in json_data["grades"]:
                Curriculum.objects.create(subject=sub, grade=grd)
        except IntegrityError:
            pass

    for strand in json_data["strands"]:
        st = Strand.objects.create(
            name=strand["name"].upper(),
            number=strand["number"],
        )

        for substrand in strand["substrands"]:
            sbtr = Substrand.objects.create(
                strand=st,
                name=substrand["name"],
                number=int(substrand["id"].split(".")[-1]),
            )
            sbtr.curriculum.set(substrand["curriculum"])



