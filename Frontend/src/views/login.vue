<template>
    <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-warning">
        <div class="container-fluid d-flex justify-content-between">
            <div>
            <img src="../assets/image.png" alt="IITM Logo" class="logo me-2 w-5" width="50" height="50"/>
          <router-link to="/" class="btn btn-light border-dark">Home</router-link>
         </div>
          <router-link to="/signup" class="btn btn-light border-dark">Signup</router-link>
        </div>
      </nav>
      
      <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
        <div class="card shadow-lg p-4 border border-dark" style="max-width: 400px; width: 100%; background-color: white;">
          <div class="card-body text-center">
            <h2 class="mb-4 text-warning">Welcome to the Tutor</h2>
            
            <form @submit.prevent="handleLogin" class="mb-3">
              <div class="mb-3">
                <label class="form-label">Email Address</label>
                <input v-model="email" type="email" class="form-control border border-dark" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input v-model="password" type="password" class="form-control border border-dark" required />
              </div>
              <button to="/home" type="submit" class="btn btn-warning w-100">Login</button>
              <router-link to="/home" class="btn btn-light">Home</router-link>
              
            </form>
          </div>
        </div>
      </div>
      
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      handleLogin() {
        alert(`Login successful for: ${this.email}`);
      }
    }
  };
  </script>
  
  <style scoped>
  </style>