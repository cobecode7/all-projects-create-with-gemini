import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || '/api';

class AdminService {
  // Users API
  async getUsers(page = 1, limit = 10) {
    const response = await axios.get(`${API_URL}/admin/users?page=${page}&limit=${limit}`);
    return response.data;
  }

  async getUserById(id) {
    const response = await axios.get(`${API_URL}/admin/users/${id}`);
    return response.data;
  }

  async createUser(userData) {
    const response = await axios.post(`${API_URL}/admin/users`, userData);
    return response.data;
  }

  async updateUser(id, userData) {
    const response = await axios.put(`${API_URL}/admin/users/${id}`, userData);
    return response.data;
  }

  async deleteUser(id) {
    const response = await axios.delete(`${API_URL}/admin/users/${id}`);
    return response.data;
  }

  async resetUserPassword(id, newPassword) {
    const response = await axios.post(`${API_URL}/admin/users/${id}/reset-password`, { newPassword });
    return response.data;
  }

  // Roles API
  async getRoles(page = 1, limit = 10) {
    const response = await axios.get(`${API_URL}/admin/roles?page=${page}&limit=${limit}`);
    return response.data;
  }

  async getRoleById(id) {
    const response = await axios.get(`${API_URL}/admin/roles/${id}`);
    return response.data;
  }

  async createRole(roleData) {
    const response = await axios.post(`${API_URL}/admin/roles`, roleData);
    return response.data;
  }

  async updateRole(id, roleData) {
    const response = await axios.put(`${API_URL}/admin/roles/${id}`, roleData);
    return response.data;
  }

  async deleteRole(id) {
    const response = await axios.delete(`${API_URL}/admin/roles/${id}`);
    return response.data;
  }

  // Permissions API
  async getPermissions(page = 1, limit = 10) {
    const response = await axios.get(`${API_URL}/admin/permissions?page=${page}&limit=${limit}`);
    return response.data;
  }

  async getPermissionById(id) {
    const response = await axios.get(`${API_URL}/admin/permissions/${id}`);
    return response.data;
  }

  async createPermission(permissionData) {
    const response = await axios.post(`${API_URL}/admin/permissions`, permissionData);
    return response.data;
  }

  async updatePermission(id, permissionData) {
    const response = await axios.put(`${API_URL}/admin/permissions/${id}`, permissionData);
    return response.data;
  }

  async deletePermission(id) {
    const response = await axios.delete(`${API_URL}/admin/permissions/${id}`);
    return response.data;
  }

  // Get permissions grouped by resource
  async getPermissionGroups() {
    const response = await axios.get(`${API_URL}/admin/permissions/groups`);
    return response.data;
  }

  // Dashboard API
  async getDashboardStats() {
    const response = await axios.get(`${API_URL}/admin/dashboard/stats`);
    return response.data;
  }
}

export default new AdminService();
