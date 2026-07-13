import api from "../../service/axiosconfig";

export const register = async (dadosUser) => {
  try {
    const response = await api.post("/user/register", dadosUser);
    return response.data;
  } catch (erros) {
    console.error("Falha ao cadastrar Usuario:", erros);
    throw erros;
  }
};
export const login = async (dadosUser) => {
  try {
    const response = await api.post("/user/login", dadosUser);
    return response.data;
  } catch (erros) {
    console.error("Falha ao realizar o Usuario:", erros);
    throw erros;
  }
};
// intensao
