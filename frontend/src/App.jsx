import { useEffect, useState } from "react";
import { fetchUsers } from "./api";

function App() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadUsers() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchUsers();
        if (Array.isArray(data)) {
          setUsers(data);
        } else if (data?.mensagem) {
          setError(data.mensagem);
          setUsers([]);
        } else {
          setUsers([]);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadUsers();
  }, []);

  const emptyMessage =
    !loading && !error && users.length === 0
      ? "Nenhum usuário encontrado."
      : null;

  return (
    <div className="app-container">
      <h1>Front-end AgentMetrics</h1>
      <p>Consumindo FastAPI com React + Axios</p>

      {loading && <p>Carregando usuários...</p>}
      {error && <p className="error">Erro: {error}</p>}
      {emptyMessage && <p>{emptyMessage}</p>}

      <ul>
        {users.map((user) => (
          <li key={user.id || user.email}>
            {user.name || user.nome || user.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
