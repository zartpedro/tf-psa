<template>
    <div class="max-w-4xl mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6">Gerar Relatórios</h2>
        <form @submit.prevent="generateReport" class="space-y-4">
            <div>
                <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
                <select v-model="status" id="status"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option value="">Todos</option>
                    <option value="pending">Pendente</option>
                    <option value="approved">Aprovado</option>
                    <option value="rejected">Rejeitado</option>
                </select>
            </div>
            <div>
                <label for="startDate" class="block text-sm font-medium text-gray-700">Data de Início</label>
                <input v-model="startDate" type="date" id="startDate"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
            </div>
            <div>
                <label for="endDate" class="block text-sm font-medium text-gray-700">Data de Fim</label>
                <input v-model="endDate" type="date" id="endDate"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
            </div>
            <button type="submit"
                class="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md shadow hover:bg-blue-600">Gerar
                Relatório</button>
        </form>
        <div v-if="report" class="mt-6">
            <h3 class="text-xl font-bold mb-4">Relatório</h3>
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Descrição</th>
                        <th scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Valor
                        </th>
                        <th scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data
                        </th>
                        <th scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="item in report" :key="item.id">
                        <td class="px-6 py-4 whitespace-nowrap">{{ item.description }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ item.amount }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ item.date }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ item.status }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { generateReport } from '../../services/reimbursements';

const status = ref('');
const startDate = ref('');
const endDate = ref('');
const report = ref(null);

const generateReport = async () => {
    const params = {
        status: status.value,
        startDate: startDate.value,
        endDate: endDate.value,
    };
    const response = await generateReport(params);
    report.value = response.data;
};
</script>
