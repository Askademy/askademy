from collections import namedtuple


# Define a namedtuple to represent search results
SearchResult = namedtuple(
    "SearchResult", ["name", "location", "job_title", "profile_url"]
)

# Dummy data for testing
dummy_data = [
    SearchResult(
        name="John Smith",
        location="New York, NY",
        job_title="Software Engineer",
        profile_url="https://example.com/johnsmith",
    ),
    SearchResult(
        name="Jane Doe",
        location="San Francisco, CA",
        job_title="Product Manager",
        profile_url="https://example.com/janedoe",
    ),
    SearchResult(
        name="David Lee",
        location="Seattle, WA",
        job_title="Data Analyst",
        profile_url="https://example.com/davidlee",
    ),
    SearchResult(
        name="Amy Chen",
        location="Boston, MA",
        job_title="Marketing Specialist",
        profile_url="https://example.com/amychen",
    ),
    SearchResult(
        name="Mark Johnson",
        location="Chicago, IL",
        job_title="Sales Manager",
        profile_url="https://example.com/markjohnson",
    ),
    SearchResult(
        name="Karen Kim",
        location="Los Angeles, CA",
        job_title="Graphic Designer",
        profile_url="https://example.com/karenkim",
    ),
    SearchResult(
        name="Chris Taylor",
        location="Austin, TX",
        job_title="Software Developer",
        profile_url="https://example.com/christaylor",
    ),
    SearchResult(
        name="Julia Rodriguez",
        location="Miami, FL",
        job_title="Project Manager",
        profile_url="https://example.com/juliarodriguez",
    ),
    SearchResult(
        name="Michael Brown",
        location="Denver, CO",
        job_title="Business Analyst",
        profile_url="https://example.com/michaelbrown",
    ),
    SearchResult(
        name="Lisa Nguyen",
        location="Portland, OR",
        job_title="UX Designer",
        profile_url="https://example.com/lisanguyen",
    ),
]

grades = {
    1: "Nursery 1",
    2: "Nursery 2",
    3: "Kindergarten 1",
    4: "Kindergarten 2",
    5: "Primary 1",
    6: "Primary 2",
}

strands = [
    {
        "id": "strand-1",
        "name": "Strand 1",
        "substrands": [
            {
                "id": "substrand-1",
                "name": "Substrand 1",
                "topics": [
                    {
                        "id": "topic-1",
                        "name": "Topic 1",
                        "content": "This is the content for Topic 1",
                    },
                    {
                        "id": "topic-2",
                        "name": "Topic 2",
                        "content": "This is the content for Topic 2",
                    },
                ],
            },
            {
                "id": "substrand-2",
                "name": "Substrand 2",
                "topics": [
                    {
                        "id": "topic-3",
                        "name": "Topic 3",
                        "content": "This is the content for Topic 3",
                    },
                    {
                        "id": "topic-4",
                        "name": "Topic 4",
                        "content": "This is the content for Topic 4",
                    },
                ],
            },
        ],
    },
    {
        "id": "strand-2",
        "name": "Strand 2",
        "substrands": [
            {
                "id": "substrand-3",
                "name": "Substrand 3",
                "topics": [
                    {
                        "id": "topic-5",
                        "name": "Topic 5",
                        "content": "This is the content for Topic 5",
                    },
                    {
                        "id": "topic-6",
                        "name": "Topic 6",
                        "content": "This is the content for Topic 6",
                    },
                ],
            },
            {
                "id": "substrand-4",
                "name": "Substrand 4",
                "topics": [
                    {
                        "id": "topic-7",
                        "name": "Topic 7",
                        "content": "This is the content for Topic 7",
                    },
                    {
                        "id": "topic-8",
                        "name": "Topic 8",
                        "content": "This is the content for Topic 8",
                    },
                ],
            },
        ],
    },
]


curriculums = [
    {
        "subject": "Mathematics",
        "grade": 1,
    },
    {
        "subject": "English",
        "grade": 2,
    },
    {
        "subject": "Science",
        "grade": 1,
    },
    {
        "subject": "Social Studies",
        "grade": 3,
    },
    {
        "subject": "Art",
        "grade": 2,
    },
    {
        "subject": "History",
        "grade": 3,
    },
    {
        "subject": "Geography",
        "grade": 1,
    },
    {
        "subject": "Physical Education",
        "grade": 2,
    },
    {
        "subject": "Music",
        "grade": 1,
    },
    {
        "subject": "Foreign Language",
        "grade": 2,
    },
    {
        "subject": "Computer Science",
        "grade": 3,
    },
    {
        "subject": "Writing",
        "grade": 1,
    },
    {
        "subject": "Reading",
        "grade": 2,
    },
    {
        "subject": "Drama",
        "grade": 3,
    },
    {
        "subject": "Business",
        "grade": 1,
    },
    {
        "subject": "Engineering",
        "grade": 2,
    },
    {
        "subject": "Psychology",
        "grade": 3,
    },
    {
        "subject": "Philosophy",
        "grade": 1,
    },
    {
        "subject": "Marketing",
        "grade": 2,
    },
]



user = {
    "id": 2,
    "first_name": "Adwoa",
    "middle_name": "Yaa",
    "last_name": "Appiah",
    "nickname": "Adyaa",
    "full_name": "Adwoa Yaa Appiah",
    "email": "adwoa.appiah@gmail.com",
    "phone_number": "0241234567",
    "birthdate": "1995-06-15",
    "gender": "F",
    "bio": "Software developer",
    "friendship_status": None,
    "profile_picture": "http://127.0.0.1:8000/media/users/IMG_20210920_100458_312.jpg",
    "cover_picture": "http://127.0.0.1:8000/media/users/IMG_20210920_100458_312.jpg",
    "school": "University of Ghana",
    "education_history": ["St. Monica's Senior High School"],
    "subjects": ["Computer Science", "Mathematics"],
    "level": "Undergraduate",
    "points": 200,
    "url": "http://127.0.0.1:8000/api/users/2/",
    "date_joined": "2023-03-25T09:13:36.104947Z",
    "is_active": True,
    "last_login": "2023-03-27T06:56:39.442993Z",
}
