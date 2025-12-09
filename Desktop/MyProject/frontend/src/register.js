import React,{useState} from 'react';
import axios from 'axios';

function Register(){
    const [role, setRole] = useState('student');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [studentData, setStudentData] = useState({
        name: '',
        age: '',
        number: '',
        roll_number: '',
        class_name: '',
        address: '',
        guardian_name: '',
        guardian_contact: '',
    });

    const [teacherData, setTeacherData] = useState({
        name: '',
        number: '',
        subject: '',
        address: '',
        employee_id: '',
        salary: '',
        qualification: '',
    });

    const [message, setMessage] = useState('');

    const handleStudentChange = (e) => {
        setStudentData({...studentData, [e.target.name]: e.target.value});
    };
    const handleTeacherChange = (e) => {
        setTeacherData({...teacherData, [e.target.name]: e.target.value});
    };
    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = {email, password, role};

        if(role === 'student') payload.student_data = studentData;
        else payload.teacher_data = teacherData;

        try {
      const response = await axios.post("http://localhost:8000/api/users/register/", payload);
      setMessage("Registration successful!");
      console.log(response.data);
    } catch (error) {
      console.error(error);
      if (error.response) setMessage(error.response.data);
      else setMessage("Something went wrong!");
    }
  };

  return (
    <div>
      <h2>Register as {role}</h2>
      <form onSubmit={handleSubmit}>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <label>Role:</label>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="student">Student</option>
          <option value="teacher">Teacher</option>
        </select>

        {role === "student" &&
          Object.keys(studentData).map((key) => (
            <div key={key}>
              <label>{key.replace("_", " ").toUpperCase()}:</label>
              <input
                type="text"
                name={key}
                value={studentData[key]}
                onChange={handleStudentChange}
              />
            </div>
          ))}

        {role === "teacher" &&
          Object.keys(teacherData).map((key) => (
            <div key={key}>
              <label>{key.replace("_", " ").toUpperCase()}:</label>
              <input
                type="text"
                name={key}
                value={teacherData[key]}
                onChange={handleTeacherChange}
              />
            </div>
          ))}

        <button type="submit">Register</button>
      </form>
      {message && <p>{JSON.stringify(message)}</p>}
    </div>
  );
}

export default Register;


