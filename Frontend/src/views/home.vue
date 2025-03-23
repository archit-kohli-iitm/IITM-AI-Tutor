<template>
  <div class="container-fluid bg-light vh-100 d-flex flex-column">
    <nav class="navbar navbar-light bg-warning px-3 w-100">
      <div class="mt-100">
        <img src="../assets/image.png" alt="IITM Logo" class="logo me-2" width="50" height="50"/>
        
      </div>
      <span class="navbar-brand mb-0 h1 text-dark">Welcome to the AI Tutor</span>
      <button class="btn btn-light border-dark" @click="logout">Logout</button>
    </nav>

    <div class="row flex-grow-1 p-3">
      <div class="col-12 d-flex flex-wrap justify-content-start">
        <router-link
          v-for="(details, subject) in chats"
          :key="subject"
          :to="{ path: '/course', query: { subject: subject } }"
          class="card-link"
          
        >
          <div class="card m-3 p-3" style="width: 20rem;">
            <div class="card-header bg-dark text-white text-center">
              <h5>{{ subject }}</h5>
              <small v-if="details.repeat" class="text-warning">REPEAT FULL COURSE</small>
              <small v-else class="text-light">NEW COURSE</small>
            </div>
            <div class="card-body">
              <ul class="list-unstyled">
                <li v-for="(score, week) in details.assignments" :key="week">
                  {{ week }} Assignment - {{ score }}
                </li>
              </ul>
              <p v-if="details.quiz">Quiz - {{ details.quiz }}</p>
              <p><strong>Allowed to take End Term Exam?</strong> {{ details.allowed ? 'Yes' : 'No' }}</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // Import axios

export default {
  data() {
    return {
      chats: {
        "PDSA": {
          repeat: false,
          assignments: {
            "Week 1": 80,
            "Week 2": 72,
            "Week 3": 100,
            "Week 4": 97,
            "Week 5": 100,
            "Week 6": 100,
            "Week 7": 100,
          },
          allowed: true,
        },
        "Software Engineering": {
          repeat: false,
          assignments: {
            "Week 1": 93,
            "Week 2": 100,
            "Week 3": 83,
            "Week 4": 56,
            "Week 5": 92,
            "Week 7": 80,
          },
          allowed: true,
        },
        "AI: Search Methods for Problem Solving": {
          repeat: false,
          assignments: {
            "Week 1": 90,
            "Week 2": 90,
            "Week 3": 85,
            "Week 4": 85,
            "Week 5": 100,
            "Week 6": 17,
            "Week 7": "Absent",
          },
          allowed: true,
        },
      },
    };
  },
  methods: {
    reloadPage() {
      window.location.reload();
    },
    logout() {
      localStorage.clear();
      this.$router.push({ name: "HOME" });
    },
    
  },
  mounted() {
    let user = localStorage.getItem("user-info");
    if (!user) {
      this.$router.push({ name: "Login" });
    }
  },
};
</script>


<style scoped>
.container-fluid {
  height: 100vh;
}
.card {
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: scale(1.05);
}
.card-header {
  font-size: 1.2rem;
  font-weight: bold;
}
.card-link {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}
</style>
