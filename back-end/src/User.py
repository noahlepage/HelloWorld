import uuid


class User :

    user_counter = 0



    def __init__(self, name="User") :

        self.name = name + user_counter

        user_counter += 1

        self.UserId = uuid.uuid4()


        