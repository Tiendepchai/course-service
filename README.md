# **2. Service Quản Lý Môn Học (Course Service)**  

Dịch vụ này sẽ quản lý thông tin về môn học với các tính năng chính:  
- **Tạo môn học mới**  
- **Lấy danh sách môn học**  
- **Lấy thông tin một môn học cụ thể**  
- **Cập nhật thông tin môn học**  
- **Xóa môn học**  

---

## **1. Cài đặt môi trường**
Tải thư mục dự án `course-service` và vào bên trong:
```sh
git clone https://github.com/Tiendepchai/course-service.git && cd course-service
```
Tạo môi trường ảo và cài đặt Flask:
```sh
pip install -r requirements
```

---

## **2. Xây dựng API**
### **File: `app.py`**
Chứa API Flask và khởi tạo database.
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate

app = Flask(__name__)

# Cấu hình database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/course_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from resources.course import CourseResource, CourseListResource
api.add_resource(CourseListResource, '/courses')
api.add_resource(CourseResource, '/courses/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
```

---

### **File: `models.py`**
Chứa model **Course**.
```python
from app import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    credit = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Course {self.name}>'
```

---

### **File: `schemas.py`**
Dùng **Marshmallow** để validate dữ liệu.
```python
from marshmallow import Schema, fields

class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    credit = fields.Int(required=True)
```

---

### **File: `resources/course.py`**
Chứa API xử lý CRUD môn học.
```python
from flask_restful import Resource
from flask import request
from models import Course, db
from schemas import CourseSchema

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

class CourseListResource(Resource):
    def get(self):
        courses = Course.query.all()
        return courses_schema.dump(courses), 200

    def post(self):
        data = request.get_json()
        errors = course_schema.validate(data)
        if errors:
            return {"message": "Invalid data", "errors": errors}, 400
        
        course = Course(**data)
        db.session.add(course)
        db.session.commit()
        return course_schema.dump(course), 201

class CourseResource(Resource):
    def get(self, id):
        course = Course.query.get_or_404(id)
        return course_schema.dump(course), 200

    def put(self, id):
        course = Course.query.get_or_404(id)
        data = request.get_json()
        errors = course_schema.validate(data)
        if errors:
            return {"message": "Invalid data", "errors": errors}, 400
        
        course.name = data['name']
        course.code = data['code']
        course.credit = data['credit']
        db.session.commit()
        return course_schema.dump(course), 200

    def delete(self, id):
        course = Course.query.get_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return {"message": "Course deleted"}, 204
```

---

## **3. Chạy Dịch Vụ**
### **Bước 1: Tạo Database**
Chạy MySQL hoặc PostgreSQL và tạo database:
```sql
CREATE DATABASE course_db;
```

### **Bước 2: Cấu hình Flask-Migrate**
Khởi tạo và chạy migration:
```sh
flask db init
flask db migrate -m "Create courses table"
flask db upgrade
```

### **Bước 3: Chạy API**
```sh
python app.py
```
API sẽ chạy tại `http://127.0.0.1:5000`.

---

## **4. Kiểm thử API với cURL hoặc Postman**
### **Tạo môn học**
```sh
curl -X POST "http://127.0.0.1:5000/courses" \
     -H "Content-Type: application/json" \
     -d '{"name": "Lập trình Python", "code": "PY101", "credit": 3}'
```

### **Lấy danh sách môn học**
```sh
curl -X GET "http://127.0.0.1:5000/courses"
```

### **Lấy một môn học**
```sh
curl -X GET "http://127.0.0.1:5000/courses/1"
```

### **Cập nhật môn học**
```sh
curl -X PUT "http://127.0.0.1:5000/courses/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "Lập trình Flask", "code": "FL101", "credit": 4}'
```

### **Xóa môn học**
```sh
curl -X DELETE "http://127.0.0.1:5000/courses/1"
```

---

## **5. Đóng gói với Docker**
### **File: `Dockerfile`**
```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### **File: `docker-compose.yml`**
```yaml
version: '3.10'
services:
  course_service:
    build: .
    ports:
      - "5001:5000"
    environment:
      - SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@db/course_db
    depends_on:
      - db

  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: course_db
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3307:3307"
```

### **Chạy Docker**
```sh
docker-compose up --build
```
