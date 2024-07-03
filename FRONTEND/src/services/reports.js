// src/services/reimbursements.js
import http from "./http";

export const generateReport = async (params) => {
  return await http.get("/reports/reports/total_by_period", { params });
};
