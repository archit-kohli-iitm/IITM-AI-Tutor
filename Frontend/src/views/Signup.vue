<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-warning">
        <div class="container-fluid d-flex justify-content-between">
          <div>
          <img src="../assets/image.png" alt="IITM Logo" class="logo me-2 w-5" width="50" height="50"/>
          <router-link to="/" class="btn btn-light border-dark">HOME</router-link>
          </div>
          <span class="navbar-brand mb-0 h1 text-dark">AI Tutor Application</span>
        
          <router-link to="/login" class="btn btn-light border-dark">LOGIN</router-link>
        </div>
      </nav>
    
    <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
      
      <div class="card shadow-lg p-5 border border-dark" style="max-width: 600px; width: 100%;">
        <div class="card-body text-center">
          <h2 class="mb-4">Please sign up</h2>
          
          <form @submit.prevent="handleSignup" class="mb-3">
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2">Email Address</label>
              <input v-model="email" type="email" class="form-control border border-dark w-50" required />
            </div>
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2">Name</label>
              <input v-model="name" type="text" class="form-control border border-dark w-50" required />
            </div>
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2">Password</label>
              <input v-model="password" type="password" class="form-control border border-dark w-50" required />
            </div>
            <div class="d-flex justify-content-center gap-2">
              <button type="submit" class="btn btn-warning w-25  border border-dark">Signup</button>
              <button type="button" class="btn btn-secondary w-25 border border-dark" @click="clearForm">Clear</button>
            </div>
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
    },
    clearForm() {
      this.email = '';
      this.name = '';
      this.password = '';
    }
  }
};
</script>

<style scoped>
</style>
