// src/services/reimbursements.js
import http from "./http";

export const createReimbursement = async (data) => {
  return await http.post("/reimbursements/reimbursements", data);
};

export const getReimbursements = async () => {
  return await http.get("/reimbursements/reimbursements");
};

export const approveReimbursement = async (id) => {
  return await http.put(`/reimbursements/reimbursements/${id}/approve`);
};

export const rejectReimbursement = async (id, reason) => {
  return await http.put(`/reimbursements/reimbursements/${id}/reject`, {
    reason,
  });
};
