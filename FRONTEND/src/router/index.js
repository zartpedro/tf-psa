import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Dashboard from "../views/Dashboard.vue";

import CreateReimbursement from "../views/Employee/CreateReimbursement.vue";
import ViewReimbursements from "../views/Employee/ViewReimbursements.vue";
import ApproveReimbursements from "../views/Manager/ApproveReimbursements.vue";
import GenerateReports from "../views/Manager/GenerateReports.vue";
import ReimbursementDetails from "../views/Manager/ReimbursementDetails.vue";
import Login from "../views/Login.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "LoginPage",
    component: Login,
  },
  {
    path: "/employee/create-reimbursement",
    name: "CreateReimbursement",
    component: CreateReimbursement,
  },
  {
    path: "/employee/reimbursements",
    name: "ViewReimbursements",
    component: ViewReimbursements,
  },
  {
    path: "/manager/approve-reimbursements",
    name: "ApproveReimbursements",
    component: ApproveReimbursements,
  },
  {
    path: "/manager/generate-reports",
    name: "GenerateReports",
    component: GenerateReports,
  },
  {
    path: "/manager/reimbursement-details/:id",
    name: "ReimbursementDetails",
    component: ReimbursementDetails,
  },

  {
    path: "/dashboard",
    name: "DashboardPage",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL),
  routes,
});

// Verifica a autenticação antes de cada navegação
router.beforeEach((to, from, next) => {
  // console.log();
  // to.name == "LoginPage"
  const isAuthenticated = !!localStorage.getItem("jwt");
  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !isAuthenticated
  ) {
    next({ name: "LoginPage" });
  } else {
    next();
  }
});

export default router;
