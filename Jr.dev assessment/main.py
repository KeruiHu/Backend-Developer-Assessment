import csv
import sys
import json

class student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.totalAverage = 0
        self.courses = []
        self.courseAverage = []
        self.total = 0
    def addcourse(self, curr_course):
        if not (curr_course in self.courses):
            self.courses.append(curr_course)
            self.courseAverage.append(0)
    def addmark(self,curr_course,mark):
        self.courseAverage[self.courses.index(curr_course)] += mark
        self.total += mark

    def calculatetotalAverage(self):
        self.totalAverage = self.total / len(self.courses)


class course:
    def __init__(self, id, name, teacher):
        self.id = id
        self.name = name
        self.teacher = teacher


class test:
    def __init__(self, id, weight,course_id):
        self.id = id
        self.weight = weight
        self.course_id = course_id

course_list = []
student_list = []
test_list = []

def test_data():
    for course_ele in course_list:
        total_weight = 0
        for test_ele in test_list:
            if course_ele.id == test_ele.course_id:
                total_weight += int(test_ele.weight)
        if total_weight != 100:
            return False
    return True

def writeinJSON(filename):
    data = {}
    data['students'] = []

    for curr_student in student_list:
        curr_student_info = {'id': int(curr_student.id), 'name': curr_student.name,
                            'totalAverage': round(curr_student.totalAverage,2), 'courses': []}
        for curr_course in curr_student.courses:
            curr_course_info = {'id': int(curr_course.id), 'name': curr_course.name, 'teacher': curr_course.teacher,
                        'courseAverage':round(curr_student.courseAverage[curr_student.courses.index(curr_course)],2)}
            curr_student_info['courses'].append(curr_course_info)
        data['students'].append(curr_student_info)

    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)

def writeerror(filename):
    data = {}
    data['error'] = "Invalid course weights"
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)

def main():
    with open(sys.argv[1], mode='r') as courses:
        csv_courses = csv.DictReader(courses)
        line_count = 0
        for row in csv_courses:
            if line_count == 0:
                line_count +=1
            course_list.append(course(row["id"],row["name"],row["teacher"]))
            line_count += 1

    with open(sys.argv[2], mode='r') as students:
        csv_students = csv.DictReader(students)
        line_count = 0
        for row in csv_students:
            if line_count == 0:
                line_count +=1
            student_list.append(student(row["id"],row["name"]))
            line_count += 1

    with open(sys.argv[3], mode='r') as tests:
        csv_tests = csv.DictReader(tests)
        line_count = 0
        for row in csv_tests:
            if line_count == 0:
                line_count +=1
            test_list.append(test(row["id"],row["weight"],row["course_id"]))
            line_count += 1

    with open(sys.argv[4], mode='r') as marks:
        csv_marks = csv.DictReader(marks)
        line_count = 0
        for row in csv_marks:
            if line_count == 0:
                line_count +=1
            for curr_test in test_list:
                if curr_test.id == row["test_id"]:
                    for curr_student in student_list:
                        if curr_student.id == row["student_id"]:
                            for curr_course in course_list:
                                if curr_course.id == curr_test.course_id:
                                    curr_student.addcourse(curr_course)
                                    curr_student.addmark(curr_course, int(row["mark"])*int(curr_test.weight)/100)

            line_count += 1

    for curr_student in student_list:
        curr_student.calculatetotalAverage()
    validation = test_data()
    if validation:
        writeinJSON(sys.argv[5])
    else:
        writeerror(sys.argv[5])

if __name__ == "__main__":
  main()
