<template>
    <div class="max-w-4xl mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6">Detalhes do Reembolso</h2>
        <div v-if="reimbursement">
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700">Descrição:</label>
                <p class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm">{{
                    reimbursement.description }}</p>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700">Valor:</label>
                <p class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm">{{ reimbursement.amount }}
                </p>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700">Data:</label>
                <p class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm">{{ reimbursement.request_date }}
                </p>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700">Status:</label>
                <p class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm">{{ reimbursement.status }}
                </p>
            </div>
            <div v-if="reimbursement.status === 'Pending'" class="mt-6 flex space-x-4">
                <button @click="approveReimbursement"
                    class="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-600">Aprovar</button>
                <button @click="showRejectModal = true"
                    class="px-4 py-2 bg-red-500 text-white rounded shadow hover:bg-red-600">Reprovar</button>
            </div>
        </div>
        <p v-else class="text-center text-gray-500">Carregando detalhes...</p>

        <div v-if="showRejectModal" class="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-75">
            <div class="bg-white p-6 rounded shadow-md w-full max-w-md">
                <h3 class="text-xl font-bold mb-4">Motivo da Recusa</h3>
                <textarea v-model="rejectionReason" class="w-full border border-gray-300 rounded-md p-2"
                    rows="4"></textarea>
                <div class="mt-4 flex justify-end space-x-4">
                    <button @click="rejectReimbursement"
                        class="px-4 py-2 bg-red-500 text-white rounded shadow hover:bg-red-600">Enviar</button>
                    <button @click="showRejectModal = false"
                        class="px-4 py-2 bg-gray-300 rounded shadow hover:bg-gray-400">Cancelar</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getReimbursements, approveReimbursement as aprove, rejectReimbursement as reject } from '../../services/reimbursements';

const route = useRoute();
const router = useRouter();
const reimbursement = ref(null);
const showRejectModal = ref(false);
const rejectionReason = ref('');

const fetchReimbursementDetails = async () => {
    const response = await getReimbursements();
    const id = parseInt(route.params.id);
    reimbursement.value = response.data.find(r => r.id === id);
};

const approveReimbursement = async () => {
    await aprove(reimbursement.value.id);
    router.push('/manager/approve-reimbursements');
};

const rejectReimbursement = async () => {
    if (rejectionReason.value.trim()) {
        await reject(reimbursement.value.id, rejectionReason.value);
        showRejectModal.value = false;
        router.push('/manager/approve-reimbursements');
    } else {
        alert('Por favor, forneça um motivo para a recusa.');
    }
};

onMounted(fetchReimbursementDetails);
</script>
