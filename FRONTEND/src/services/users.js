// src/services/users.js
import http from "./http";

export const createUser = async (userData) => {
  const response = await http.post("/auth/users", userData);
  return response.data;
};

export const getUsers = async () => {
  const response = await http.get("/auth/users");
  return response.data;
};
