<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
        <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
            <h1 class="text-2xl font-bold mb-6 text-center">Login</h1>
            <form @submit.prevent="login" class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700">Usuário:</label>
                    <input v-model="username" type="text" id="username"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        required />
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700">Senha:</label>
                    <input v-model="password" type="password" id="password"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        required />
                </div>
                <button type="submit"
                    class="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md shadow hover:bg-blue-600">Login</button>
            </form>
            <p v-if="error" class="mt-4 text-red-500 text-center">{{ error }}</p>

            <div class="mt-8">
                <h2 class="text-xl font-bold mb-4 text-center">Registrar Novo Usuário</h2>
                <form @submit.prevent="register" class="space-y-4">
                    <div>
                        <label for="newUsername" class="block text-sm font-medium text-gray-700">Usuário:</label>
                        <input v-model="newUsername" type="text" id="newUsername"
                            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                            required />
                    </div>
                    <div>
                        <label for="newPassword" class="block text-sm font-medium text-gray-700">Senha:</label>
                        <input v-model="newPassword" type="password" id="newPassword"
                            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                            required />
                    </div>
                    <div>
                        <label for="role" class="block text-sm font-medium text-gray-700">Função:</label>
                        <select v-model="role" id="role"
                            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                            <option value="funcionario">Funcionário</option>
                            <option value="gerente">Gerente</option>
                        </select>
                    </div>
                    <button type="submit"
                        class="w-full py-2 px-4 bg-green-500 text-white font-semibold rounded-md shadow hover:bg-green-600">Registrar</button>
                </form>
                <p v-if="registerError" class="mt-4 text-red-500 text-center">{{ registerError }}</p>
                <p v-if="registerSuccess" class="mt-4 text-green-500 text-center">{{ registerSuccess }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// import { login as access } from '../services/auth';
import { useUserStore } from "../stores/user.js"
import { createUser } from '../services/users';

const username = ref('');
const password = ref('');
const error = ref(null);

const newUsername = ref('');
const newPassword = ref('');
const role = ref('employee');
const registerError = ref(null);
const registerSuccess = ref(null);

const router = useRouter();
const userStore = useUserStore();

const login = async () => {
    try {
        const response = await userStore.login({ username: username.value, password: password.value });

        // Redireciona com base no papel do usuário (exemplo básico)
        if (response.role === 'Gerente') {
            router.push('/manager/approve-reimbursements');
        } else {
            router.push('/employee/reimbursements');
        }
    } catch (err) {
        console.log(err);
        error.value = 'Login failed. Please check your credentials and try again.';
    }
};

const register = async () => {
    try {
        await createUser({ username: newUsername.value, password: newPassword.value, role: role.value });
        registerSuccess.value = 'User registered successfully. You can now login.';
    } catch (err) {
        registerError.value = 'Registration failed. Please try again.';
    }
};
</script>
