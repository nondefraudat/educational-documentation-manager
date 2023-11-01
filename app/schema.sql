DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Faculty;
DROP TABLE IF EXISTS Rank;
DROP TABLE IF EXISTS Position;
DROP TABLE IF EXISTS Degree;
DROP TABLE IF EXISTS Teacher;
DROP TABLE IF EXISTS TeacherUserRelation;
DROP TABLE IF EXISTS StudentGroup;
DROP TABLE IF EXISTS "Subject";
DROP TABLE IF EXISTS TeacherGroupSubjectRelation;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS SelectionAnswer;
DROP TABLE If EXISTS QuestionType;
DROP TABLE IF EXISTS TextAnswer;


CREATE TABLE User (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Login" TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL,
    Rights TEXT NOT NULL
);

CREATE TABLE Department (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE Faculty (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE Rank (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE Position (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE Degree (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE Teacher (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT NOT NULL,
    Surname TEXT NOT NULL,
    Patronymic TEXT NOT NULL,
    DepartmentId INTEGER NOT NULL,
    FacultyId INTEGER NOT NULL,
    RankId INTEGER NOT NULL,
    PositionId INTEGER NOT NULL,
    DegreeId INTEGER NOT NULL,
    FOREIGN KEY(DepartmentId) REFERENCES Department(Id),
    FOREIGN KEY(FacultyId) REFERENCES Faculty(Id),
    FOREIGN KEY(RankId) REFERENCES "Rank"(Id),
    FOREIGN KEY(PositionId) REFERENCES Position(Id),
    FOREIGN KEY(DegreeId) REFERENCES Degree(Id)
);

CREATE TABLE TeacherUserRelation (
    TeacherId INTEGER NOT NULL,
    UserId INTEGER NOT NULL,
    FOREIGN KEY(TeacherId) REFERENCES Teacher(Id),
    FOREIGN KEY(UserId) REFERENCES User(Id),
    PRIMARY KEY (TeacherId, UserId)
);

CREATE TABLE StudentGroup (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE Subject (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE TeacherGroupSubjectRelation (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Year INTEGER NOT NULL,
    TeacherId INTEGER NOT NULL,
    StudentGroupId INTEGER NOT NULL,
    SubjectId INTEGER NOT NULL,
    FOREIGN KEY(TeacherId) REFERENCES Teacher(Id),
    FOREIGN KEY(SubjectId) REFERENCES "Subject"(Id),
    FOREIGN KEY(StudentGroupId) REFERENCES StudentGroup(Id)
);

CREATE TABLE QuestionType (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT UNIQUE NOT NULL
);

CREATE TABLE Question (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Tag" TEXT UNIQUE NOT NULL
    QuestionTypeId TEXT UNIQUE NOT NULL
    "Value" TEXT UNIQUE NOT NULL
    QuestionTypeId REFERENCES QuestionType(Id)
);

CREATE TABLE SelectionAnswer (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestionId INTEGER NOT NULL,
    TeacherGroupSubjectRelationId INTEGER NOT NULL,
    "Value" TEXT NOT NULL,
    FOREIGN KEY(QuestionId) REFERENCES QuestionType(Id),
    FOREIGN KEY(TeacherGroupSubjectRelationId) REFERENCES TeacherGroupSubjectRelation(Id)
);

CREATE TABLE TextAnswer (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestionId INTEGER NOT NULL,
    TeacherGroupSubjectRelationId INTEGER NOT NULL,
    "Value" TEXT NOT NULL,
    FOREIGN KEY(QuestionId) REFERENCES QuestionType(Id),
    FOREIGN KEY(TeacherGroupSubjectRelationId) REFERENCES TeacherGroupSubjectRelation(Id)
);
