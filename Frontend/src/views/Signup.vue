<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-warning">
        <div class="container-fluid d-flex justify-content-between">
          <div>
          <img src="../assets/image.png" alt="IITM Logo" class="logo me-2 w-5" width="50" height="50"/>
          <router-link to="/" class="btn btn-light border-dark">HOME</router-link>
          </div>
          <router-link to="/login" class="btn btn-light border-dark">LOGIN</router-link>
        </div>
      </nav>
    
    
    <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
       
      <div class="card shadow-lg p-4 border border-dark" style="max-width: 400px; width: 100%;">
        <div class="card-body text-center">
          <h2 class="mb-4">Welcome to the Tutor</h2>
          
          <form @submit.prevent="handleSignup" class="mb-3">
            <div class="mb-3">
              <label class="form-label">Email Address</label>
              <input v-model="email" type="email" class="form-control border border-dark " required />
            </div>
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input v-model="name" type="text" class="form-control border border-dark" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control border border-dark" required />
            </div>
            <button type="submit" class="btn btn-warning w-100">Signup</button>
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
      name: '',
      password: ''
    };
  },
  methods: {
    handleSignup() {
      alert(`Signup successful for: ${this.name}`);
    }
  }
};
</script>

<style scoped>
</style>
