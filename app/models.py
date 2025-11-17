from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON, DateTime, text, func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'student' or 'instructor'
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Relationships
    courses = relationship("Course", back_populates="instructor")
    enrollments = relationship("Enrollment", back_populates="user")
    progress_records = relationship("Progress", back_populates="user")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Relationships
    instructor = relationship("User", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    quizzes = relationship("Quiz", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    video_url = Column(String)
    order = Column(Integer, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="lessons")
    progress_records = relationship("Progress", back_populates="lesson")


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    correct_option = Column(String, nullable=False)

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    progress = Column(Integer, default=0)  # 0-100%
    enrolled_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress_records")
    lesson = relationship("Lesson", back_populates="progress_records")
