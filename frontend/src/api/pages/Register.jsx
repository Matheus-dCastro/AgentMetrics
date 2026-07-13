import api from "../../service/axiosconfig";
import { register } from "../endpoint/auth";
import { useEffect, useState, useRef } from "react";

function Register() {
  const [users, setUsers] = useState([]);
  const inputName = useRef();
  const inputNumber = useRef();
  const inputEmail = useRef();
  const inputPassword = useRef();

  async function registerUsers() {
    const user = {
      name: inputName.current.value,
      numero: inputNumber.current.value,
      email: inputEmail.current.value,
      senha: inputPassword.current.value,
    };
    register(user);
  }

  return (
    <>
      <div className="register">
        <form>
          <h1>Register User</h1>
          <input name="name" type="text" ref={inputName} />
          <input name="Email" type="email" ref={inputEmail} />
          <input name="number" type="text" ref={inputNumber} />
          <input name="password" type="password" ref={inputPassword} />
          <button type="button" onClick={registerUsers}>
            Register
          </button>
        </form>
      </div>
    </>
  );
}

export default Register;
