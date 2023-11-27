from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    
    @Field.value.setter
    def validate(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Phone should be 10 symbols')
        else:
            return value
        
        


class Record:
    def __init__(self, name, birthday):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        try:
            for phone in self.phones:
                if phone.value == phone_number:
                    return phone
        except Exception:
            raise ValueError("Phone not found")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.validate(new_phone)
                phone.value = new_phone
                return
        raise ValueError("Phone not found")
    
    def days_to_birthday(self, value):
        today = datetime.now().date()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()

        days_remaining = (next_birthday - today).days
        return days_remaining
       
        

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone not found")
        


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 5

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name, None)
            

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]


    def __iter__(self):
        self.current_page = 0
        self.contacts = list(self.data.values())
        return self

    def __next__(self):
        start_idx = self.current_page * self.page_size
        end_idx = (self.current_page + 1) * self.page_size
        current_contacts = self.contacts[start_idx:end_idx]

        if not current_contacts:
            raise StopIteration

        self.current_page += 1
        return current_contacts
        
    def iterator(self):
        return self.__iter__()


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        self.__value = datetime.strptime(value, '%Y.%m.%d').date()
    
      
address_book = AddressBook()
for page in address_book:
    for contact in page:
        print(contact)
    print("===")
