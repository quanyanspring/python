class myData:

    def __init__(self):
        self._name = None
        self._age = None
        self._city = None

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def city(self):
        return self._city

    @name.setter
    def name(self, value):
        self._name = value

    @age.setter
    def age(self, value):
        self._age = value

    @city.setter
    def city(self, value):
        self._city = value


my_data = myData()

my_data.age = 10
my_data.name = "wlq"
my_data.city = "beijing"

print(my_data.name)
print(my_data.age)
print(my_data.city)

