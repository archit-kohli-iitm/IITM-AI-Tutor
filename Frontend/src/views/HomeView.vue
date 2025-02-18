<template>
  <main class="d-flex flex-column justify-content-center align-items-center vh-100 bg-white">
   
    <div class="mb-1">
      <img src="../assets/image.png" alt="IITM Logo" class="logo" width="200" height="200"/>
    </div>

   
    <div class="card text-center p-5 rounded-lg shadow-lg border border-dark bg-white mt-4">
      <h1 class="text-warning mb-4">Welcome to the AI Tutor</h1>
      <div class="d-flex flex-column align-items-center gap-3">
        <router-link to="/signup" class="btn btn-warning text-dark w-50 border border-dark">Signup</router-link>
        <router-link to="/login" class="btn btn-warning text-dark w-50 border border-dark">Login</router-link>
      </div>
    </div>
  </main>
</template>