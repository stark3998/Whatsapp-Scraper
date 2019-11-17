from aap_whatsapp.model.message import User


def create_user(name="", number=None):
    if name or number:
        ob = User(name=name, number=number)
        x=ob.save()
        return ob
