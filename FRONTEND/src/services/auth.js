// src/services/auth.js
import http from "./http";

export const login = async (credentials) => {
  const response = await http.post("/auth/login", credentials);
  localStorage.setItem("jwt", response.data.token);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem("jwt");
};
