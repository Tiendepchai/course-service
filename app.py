from flask import Flask
from routes import course_bp
from models import create_course_table

app = Flask(__name__)

# Tạo bảng nếu chưa có
create_course_table()

# Đăng ký blueprint
app.register_blueprint(course_bp)

if __name__ == '__main__':
    app.run(debug=True)
