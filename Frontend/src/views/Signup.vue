<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-warning">
        <div class="container-fluid d-flex justify-content-between">
          <div>
          <img src="../assets/image.png" alt="IITM Logo" class="logo me-2 w-5" width="50" height="50"/>
          <router-link to="/" class="btn btn-light border-dark ms-2">Home</router-link>
          </div>
          <span class="navbar-brand mb-0 h1 text-dark">AI Tutor Application</span>
        
          <router-link to="/login" class="btn btn-light border-dark">Log in</router-link>
        </div>
      </nav>
    
    <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light" style="margin-top: -30px;">
      
      <div class="card shadow-lg p-4 border border-dark" style="max-width: 500px; width: 100%;">
        
        <div class="card-body text-center">
          
          <h2 class="mb-3">Please sign up</h2>
          
          <br>
          
          <form @submit.prevent="handleSignup" class="mb-3">
          
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2" style="width: 40%; text-align: left;">Email Address</label>
              <input v-model="email" type="email" class="form-control border border-dark" style="width: 60%;" required />
            </div>
          
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2" style="width: 40%; text-align: left;">Name</label>
              <input v-model="name" type="text" class="form-control border border-dark" style="width: 60%;" required />
            </div>
          
            <div class="mb-3 d-flex justify-content-between align-items-center">
              <label class="form-label me-2" style="width: 40%; text-align: left;">Password</label>
              <input v-model="password" type="password" class="form-control border border-dark" style="width: 60%;" required />
            </div>
          
            <br>
          
            <div class="d-flex justify-content-center gap-5">
              <button type="submit" class="btn btn-warning w-25  border border-dark">Sign up</button>
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
