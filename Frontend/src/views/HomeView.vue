<template>
<main class="d-flex flex-column justify-content-start align-items-center bg-white" style="padding-top: 5vh;">
  <div class="mb-1">
    <img src="../assets/image.png" alt="IITM Logo" class="logo" width="190" height="200"/>
  </div>

  <div class="card text-center p-5 rounded-lg shadow-lg border border-dark bg-white mt-4">
    <h2 class="text mb-3">Welcome to the AI Tutor</h2>
    <br>
    <div class="d-flex flex-column align-items-center gap-3">
      <router-link to="/signup" class="btn btn-warning text-dark w-50 border border-dark">Sign up</router-link>
      <router-link to="/login" class="btn btn-warning text-dark w-50 border border-dark">Log in</router-link>
    </div>
  </div>
</main>



</template>