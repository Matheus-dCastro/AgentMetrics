import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response, // Se der tudo certo, apenas retorna a resposta
  async (error) => {
    const originalRequest = error.config;

    // Se o erro for 401 e a requisição ainda não foi tentada novamente
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Chama sua rota de refresh no backend
        const refreshToken = localStorage.getItem("refresh_token");
        const response = await api.post("/user/refresh", {
          refresh: refreshToken,
        });

        // Salva o novo access_token
        const newAccessToken = response.data.access_token;
        localStorage.setItem("access_token", newAccessToken);

        // Atualiza o header da requisição original e tenta de novo
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Se o refresh falhar (token expirou mesmo), desloga o usuário
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  },
);
export default api;
