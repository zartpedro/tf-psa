<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow p-4 flex justify-center space-x-4" v-if="userStore.token">
      <router-link to="/employee/create-reimbursement" class="text-blue-500 hover:text-blue-700"
        v-if="userStore.isEmployee">Cadastrar
        Reembolso</router-link>
      <router-link to="/employee/reimbursements" class="text-blue-500 hover:text-blue-700"
        v-if="userStore.isEmployee">Meus Reembolsos</router-link>
      <router-link to="/manager/approve-reimbursements" class="text-blue-500 hover:text-blue-700"
        v-if="userStore.isManager">Aprovar
        Reembolsos</router-link>
      <router-link to="/manager/generate-reports" class="text-blue-500 hover:text-blue-700"
        v-if="userStore.isManager">Gerar
        Relatórios</router-link>
      <router-link to="/login" class="text-blue-500 hover:text-blue-700" @click="logout">Logout</router-link>
    </nav>
    <router-view class="p-4" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from "./stores/user.js"

const router = useRouter();
const userStore = useUserStore();

const logout = async () => {
  await userStore.logout();
  router.push('/login');
};
</script>
