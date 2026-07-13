import api from "../../service/axiosconfig";
import { login } from "../endpoint/auth";

export const token = async (userDados) => {
  const tokens = await login(userDados);
  localStorage.setItem("access_token", tokens.access_token);
  localStorage.setItem("refresh_token", tokens.refresh_token);

  return tokens;
};
