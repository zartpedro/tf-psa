// src/stores/user.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { login as loginService } from "../services/auth";

export const useUserStore = defineStore("user", () => {
  const user = ref(localStorage.getItem("user") || "");
  const role = ref(localStorage.getItem("role") || "");
  const token = ref(localStorage.getItem("jwt") || "");

  const isManager = computed(() => role.value === "Gerente");
  const isEmployee = computed(() => role.value === "Funcionario");

  const login = async (credentials) => {
    const response = await loginService(credentials);
    user.value = response.user;
    role.value = response.role;
    token.value = response.access_token;
    localStorage.setItem("jwt", response.access_token);
    localStorage.setItem("user", response.user);
    localStorage.setItem("role", response.role);
    return response;
  };

  const logout = () => {
    token.value = "";
    user.value = "";
    role.value = "";
    localStorage.removeItem("jwt");
    localStorage.removeItem("user");
    localStorage.removeItem("role");
  };

  const loadUserFromToken = async () => {
    if (token.value) {
      // Faça uma chamada para obter os detalhes do usuário com base no token
      // Exemplo:
      // const response = await getUserDetailsFromToken(token.value);
      // user.value = response;

      // Para este exemplo, vou configurar um usuário fictício
      user.value = {
        username: "exampleUser",
        role: "employee", // ou 'manager'
      };
    }
  };

  return {
    user,
    token,
    isManager,
    isEmployee,
    login,
    logout,
    loadUserFromToken,
  };
});
