# **Service quản lý môn học (course service)**  

Dịch vụ này sẽ quản lý thông tin môn học với các tính năng chính:  
- **Tạo môn học mới**  
- **Lấy danh sách môn học**  
- **Lấy thông tin một môn học cụ thể**  
- **Cập nhật thông tin môn học**  
- **Xóa môn học**  

## **Công nghệ sử dụng**
- **Flask**: Xây dựng API RESTful  
- **mysql-connector-python**: Để làm việc với database  
- **MySQL hoặc PostgreSQL**: Lưu trữ dữ liệu  
- **Docker**: Đóng gói service  

## **Cấu trúc thư mục**
```
course_service/
│── app.py                  # Main Flask App
│── config.py               # Cấu hình MySQL
│── database.py             # Kết nối MySQL
│── models.py               # Định nghĩa bảng course
│── routes.py               # Xử lý API endpoints
│── requirements.txt        # Thư viện cần thiết
│── .gitignore              # Lọc các file môi trường
│── Dockerfile              # (Nếu deploy bằng Docker)
└── .env                    # Config biến môi trường
```
---

## **1. Cài đặt môi trường**  
Trước tiên, hãy tải về thư mục dự án:  
```sh
git clone https://github.com/Tiendepchai/course-service.git
```
Tạo một môi trường ảo và cài đặt Flask:  
```sh
pip install -r requirements.txt
```

---

## **2. Chạy Dịch Vụ**
### **Bước 1: Tạo Database**
Chạy MySQL và tạo database:
```sh
sudo -u root
```
```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password'; 
GRANT ALL PRIVILEGES ON course_db.* TO 'admin'@'localhost';
CREATE DATABASE course_db;
```

### **Bước 2: Chạy API**
```sh
python app.py
```
API sẽ chạy tại `http://127.0.0.1:5000`.

---

## **3. Kiểm thử API với cURL hoặc Postman**
#### **Tạo môn học mới**
```sh
curl -X POST http://127.0.0.1:5000/courses -H "Content-Type: application/json" -d '{\
  "name": "Calculus 1",\
  "description": "Mathematics"\
}'
```

#### **Lấy danh sách môn học**
```sh
curl http://127.0.0.1:5000/courses
```

#### **Lấy thông tin môn học theo ID**
```sh
curl http://127.0.0.1:5000/courses/1
```

#### **Cập nhật môn học**
```sh
curl -X PUT http://127.0.0.1:5000/courses -H "Content-Type: application/json" -d '{\
  "name": "Probability and statistics",\
  "description": "Mathematics"\
}'
```

#### **Xóa môn học**
```sh
curl -X DELETE http://127.0.0.1:5000/courses/1
```

---

## **4. Đóng gói với Docker**
### **File: `Dockerfile`**
```dockerfile
# Sử dụng image chính thức của Python
FROM python:3.10

# Đặt thư mục làm thư mục làm việc
WORKDIR /app

# Copy toàn bộ project vào container
COPY . .

# Cài đặt thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Chạy ứng dụng Flask
CMD ["python", "app.py"]

```

### **File: `docker-compose.yml`**
```yaml
version: '3.10'
services:
  mysql_db:
    image: mysql
    container_name: mysql_course_service
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: course_db
      MYSQL_USER: admin
      MYSQL_PASSWORD: password
    ports:
      - "3307:3307"
    volumes:
      - mysql_data:/var/lib/mysql

  course_service:
    build: .
    container_name: course_service
    restart: always
    depends_on:
      - mysql_db
    ports:
      - "5050:5050"
    environment:
      DB_HOST: localhost
      DB_USER: admin
      DB_PASSWORD: password
      DB_NAME: course_db

volumes:
  mysql_data:

```

### **Chạy Docker**
```sh
docker-compose up --build
```
---
