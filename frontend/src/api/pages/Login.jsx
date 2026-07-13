import api from "../../service/axiosconfig";
import { useEffect, useState, useRef } from "react";
import { token } from "../context/AuthContext";
import { list_lead } from "../endpoint/deashboard";

function Login() {
  const [users, setUsers] = useState([]);
  const [leads, setLeads] = useState([]);

  const inputEmail = useRef();
  const inputPassword = useRef();

  async function carregarLeads() {
    try {
      const data = await list_lead();
      setLeads(data);
    } catch (error) {
      console.error("Erro ao carregar leads:", error);
    }
  }
  async function loginUsers() {
    const userlogin = {
      email: inputEmail.current.value,
      senha: inputPassword.current.value,
    };
    await token(userlogin);
    await carregarLeads();
  }

  return (
    <>
      <div className="login">
        <form>
          <h1>Login User</h1>
          <input
            name="Email"
            type="email"
            placeholder="Email"
            ref={inputEmail}
          />
          <input
            name="password"
            type="password"
            placeholder="Senha"
            ref={inputPassword}
          />
          <button type="button" onClick={loginUsers}>
            Entrar
          </button>
        </form>
      </div>

      <div className="lead-container" style={{ marginTop: "20px" }}>
        <h1>Meus Leads</h1>
        <table border="1">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Número</th>
              <th>Status</th>
              <th>Intenção</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {leads.length > 0 ? (
              leads.map((lead) => (
                <tr key={lead.id}>
                  <td>{lead.nome}</td>
                  <td>{lead.numero}</td>
                  <td>{lead.Status}</td>
                  <td>{lead.intencao}</td>
                  <td>{lead.data}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">Nenhum lead encontrado ou faça login.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default Login;
