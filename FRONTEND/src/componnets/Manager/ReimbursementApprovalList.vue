<template>
    <div class="max-w-4xl mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6">Aprovar/Reprovar Reembolsos</h2>
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th scope="col"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição
                    </th>
                    <th scope="col"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Valor
                    </th>
                    <th scope="col"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                    <th scope="col"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações
                    </th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="reimbursement in reimbursements" :key="reimbursement.id">
                    <td class="px-6 py-4 whitespace-nowrap">{{ reimbursement.description }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ reimbursement.amount }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ reimbursement.date }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <button @click="approve(reimbursement.id)"
                            class="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-600">Aprovar</button>
                        <button @click="reject(reimbursement.id)"
                            class="px-4 py-2 bg-red-500 text-white rounded shadow hover:bg-red-600 ml-2">Reprovar</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getReimbursements, approveReimbursement, rejectReimbursement } from '../../services/reimbursements';

const reimbursements = ref([]);

onMounted(async () => {
    const response = await getReimbursements();
    reimbursements.value = response.data.filter(reimbursement => reimbursement.status === 'pending');
});

const approve = async (id) => {
    await approveReimbursement(id);
    reimbursements.value = reimbursements.value.filter(reimbursement => reimbursement.id !== id);
};

const reject = async (id) => {
    const reason = prompt('Por favor, informe o motivo da recusa:');
    if (reason) {
        await rejectReimbursement(id, reason);
        reimbursements.value = reimbursements.value.filter(reimbursement => reimbursement.id !== id);
    }
};
</script>
