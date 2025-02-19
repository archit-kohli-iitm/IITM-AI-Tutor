<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-warning">
      <div class="container-fluid d-flex justify-content-between">
        <div>
          <img src="../assets/image.png" alt="IITM Logo" class="logo me-2 w-5" width="50" height="50"/>
          <router-link to="/" class="btn btn-light border-dark ms-2">Home</router-link>
        </div>
        <span class="navbar-brand mb-0 h1 text-dark">AI Tutor Application</span>
        
        <router-link to="/signup" class="btn btn-light border-dark">Sign up</router-link>
      </div>
    </nav>
    
    <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light" style="margin-top: -50px;">
     
      <div class="card shadow-lg p-4 border border-dark" style="max-width: 500px; width: 100%;">
        
        <div class="card-body text-center">
        
          <h2 class="mb-3">Please log in</h2>
          
          <br>
          
          <form @submit.prevent="handleLogin" class="mb-3">
          
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2" style="width: 40%; text-align: left;">Email Address</label>
              <input v-model="email" type="email" class="form-control border border-dark" style="width: 60%;" required />
            </div>
          
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2" style="width: 40%">Password</label>
              <input v-model="password" type="password" class="form-control border border-dark" style="width: 60%;" required />
            </div>
          
            <br>
          
            <div class="d-flex justify-content-center gap-5">
              <router-link to="/home">
                <button type="submit" class="btn btn-warning border border-dark" style="width: 100px;">
                  Log in
                </button>
              </router-link>
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
      password: ''
    };
  },
  methods: {
    handleLogin() {
      alert(`Login successful for: ${this.email}`);
    },
    clearForm() {
      this.email = '';
      this.password = '';
    }
  }
};
</script>

<style scoped>
.form-label {
  text-align: left;
  margin-bottom: 8px;
}

input.form-control {
  width: 100%;
}
</style>
