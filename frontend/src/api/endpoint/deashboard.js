import api from "../../service/axiosconfig";

export const list_lead = async () => {
  try {
    const response = await api.get("/user/list-leads");
    console.log(response);
    return response.data;
  } catch (erros) {
    console.error("Falha ao listar os leads", erros);
    throw erros;
  }
};
