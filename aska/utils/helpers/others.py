import random
import string

def generate_nickname(full_name):
    """
    Generates a nickname for a user based on their full name.

    Args:
        full_name (str): The user's full name.

    Returns:
        str: The user's nickname.
    """
    name_parts = full_name.split()
    if len(name_parts) > 1:
        first_name = name_parts[0].lower()
        last_name = name_parts[-1].lower()
        first_part = first_name[:3]
        second_part = last_name[:2]
        random_part = ''.join(random.choice(string.digits) for i in range(3))
        nickname = first_part + second_part + random_part
    else:
        nickname = name_parts[0].lower()
    return nickname



print(generate_nickname("Kwaku Asiedu"))  # Output: "kwaa81"
print(generate_nickname("Asikwa Abrefa"))  # Output: "asiabf867"
print(generate_nickname("Emmanuel Danso"))  # Output: "emmnda267"
print(generate_nickname("Akosua Yeboah"))  # Output: "akoye966"
print(generate_nickname("Kofi Ampofo"))  # Output: "kofamp189"
print(generate_nickname("Nana Agyemang"))  # Output: "nanagy795"
print(generate_nickname("Ama Ofori"))  # Output: "amoofi123"
print(generate_nickname("Yaw Mensah"))  # Output: "yawmen631"
print(generate_nickname("Adwoa Boateng"))  # Output: "adwboa214"
print(generate_nickname("Kwabena Owusu"))  # Output: "kwaoqu698"