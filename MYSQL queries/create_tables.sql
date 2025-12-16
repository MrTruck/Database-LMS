USE lms_database;

-- ===============================
-- USER (Base account)
-- ===============================
CREATE TABLE `user` (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fullName VARCHAR(100) NOT NULL,
    role ENUM('student', 'instructor') NOT NULL
);

-- ===============================
-- STUDENT (Profile)
-- ===============================
CREATE TABLE Student (
    studentID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    studentName VARCHAR(100) NOT NULL,
    majorName VARCHAR(100),
    semester INT,

    FOREIGN KEY (userID) REFERENCES User(userID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ===============================
-- INSTRUCTOR (Profile)
-- ===============================
CREATE TABLE Instructor (
    instructorID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    instructorName VARCHAR(100) NOT NULL,
    department VARCHAR(100),

    FOREIGN KEY (userID) REFERENCES User(userID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ===============================
-- COURSE
-- ===============================
CREATE TABLE Course (
    courseID INT AUTO_INCREMENT PRIMARY KEY,
    courseName VARCHAR(100) NOT NULL,
    instructorID INT NOT NULL,
    userID INT NOT NULL,

    FOREIGN KEY (instructorID) REFERENCES Instructor(instructorID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (userID) REFERENCES User(userID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ===============================
-- ENROLLMENT (many-to-many)
-- ===============================
CREATE TABLE Enrollment (
    enrollmentID INT AUTO_INCREMENT PRIMARY KEY,
    courseID INT NOT NULL,
    studentID INT NOT NULL,
    enrollmentDate DATE DEFAULT (CURRENT_DATE),
    
    CONSTRAINT fk_enrollment_course
        FOREIGN KEY (courseID) REFERENCES Course(courseID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_enrollment_student
        FOREIGN KEY (studentID) REFERENCES Student(studentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- ===============================
-- SESSION (Course Content)
-- ===============================
CREATE TABLE Session (
    sessionID INT AUTO_INCREMENT PRIMARY KEY,
    courseID INT NOT NULL,
    sessionTitle VARCHAR(200) NOT NULL,
    sessionDate DATE NOT NULL,
    contentLink TEXT,

    FOREIGN KEY (courseID) REFERENCES Course(courseID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TRIGGER IF EXISTS create_student_after_user;
DROP TRIGGER IF EXISTS create_instructor_after_user;

DELIMITER $$

CREATE TRIGGER create_student_after_user
AFTER INSERT ON user
FOR EACH ROW
BEGIN
    IF NEW.role = 'student' THEN
        INSERT INTO Student (userID, studentName)
        VALUES (NEW.userID, NEW.fullName);
    END IF;
END$$

CREATE TRIGGER create_instructor_after_user
AFTER INSERT ON user
FOR EACH ROW
BEGIN
    IF NEW.role = 'instructor' THEN
        INSERT INTO Instructor (userID, instructorName)
        VALUES (NEW.userID, NEW.fullName);
    END IF;
END$$

DELIMITER ;