<template>
    <div class="max-w-lg mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6">Cadastrar Reembolso</h2>
        <form @submit.prevent="submitForm">
            <div class="mb-4">
                <label for="description" class="block text-sm font-medium text-gray-700">Descrição</label>
                <input v-model="description" type="text" id="description"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    required />
            </div>
            <div class="mb-4">
                <label for="amount" class="block text-sm font-medium text-gray-700">Valor</label>
                <input v-model="amount" type="number" id="amount"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    required />
            </div>
            <div class="mb-4">
                <label for="date" class="block text-sm font-medium text-gray-700">Data</label>
                <input v-model="date" type="date" id="date"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    required />
            </div>
            <button type="submit"
                class="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md shadow hover:bg-blue-600">Cadastrar</button>
        </form>
        <p v-if="error" class="mt-4 text-red-500">{{ error }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { createReimbursement } from '../../services/reimbursements';

const description = ref('');
const amount = ref('');
const date = ref('');
const error = ref(null);
const router = useRouter();

const submitForm = async () => {
    try {
        await createReimbursement({ description: description.value, amount: amount.value, request_date: date.value });
        router.push('/employee/reimbursements');
    } catch (err) {
        error.value = 'Erro ao cadastrar reembolso. Por favor, tente novamente.';
    }
};
</script>
