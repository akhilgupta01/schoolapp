class Student:
    def __init__(self, attributes:dict):
        self.attributes = attributes
        self.roll_no = attributes["Roll No"]
        self.name = attributes["Name"]
        self.last_name = attributes["Surname"]
        self.section = attributes["Section"]
        self.new_section = attributes["Target Section"]
        self.rte = attributes["RTE"]
        self.gender = attributes["Gender"]
        self.house = attributes["House"]
        self.percentage = attributes["Percentage"]
        self.percentage_group = attributes["AcademicBand"]
    
    def to_dict(self):
        return self.attributes

    def get_attr(self, name):
        return self.attributes[name]
    
    def set_attr(self, attr_name, value):
        self.attributes[attr_name] = value

    def __str__(self):
        return f"{self.roll_no};{self.name};{self.last_name};{self.section};{self.rte};{self.gender};{self.house};{self.percentage};{self.percentage_group}; {self.new_section}"
