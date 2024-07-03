<template>
    <div class="max-w-4xl mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6">Meus Reembolsos</h2>
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
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status
                    </th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="reimbursement in reimbursements" :key="reimbursement.id">
                    <td class="px-6 py-4 whitespace-nowrap">{{ reimbursement.description }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ reimbursement.amount }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ reimbursement.date }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ reimbursement.status }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getReimbursements } from '../../services/reimbursements';

const reimbursements = ref([]);

onMounted(async () => {
    const response = await getReimbursements();
    reimbursements.value = response.data;
});
</script>
